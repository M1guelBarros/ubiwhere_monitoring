import os
import sys
import django
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ubiwhere_monitoring.settings")
django.setup()

from roads.models import Road
from readings.models import Reading
from sensors.models import Sensor

SPEED_CSV = os.path.join(BASE_DIR, "data", "traffic_speed.csv")
SENSORS_CSV = os.path.join(BASE_DIR, "data", "sensors.csv")


def import_sensors():
    if not os.path.exists(SENSORS_CSV):
        print(f"  sensors.csv not found at {SENSORS_CSV}; skipping sensors import.")
        return

    df = pd.read_csv(SENSORS_CSV)

    required = {"id", "name", "uuid"}
    missing = required - set(df.columns)
    if missing:
        raise RuntimeError(f"sensors.csv missing columns: {missing}")

    created = 0
    reused_or_updated = 0

    for _, row in df.iterrows():
        uuid = str(row["uuid"]).strip()
        name = str(row["name"]).strip()

        sensor, was_created = Sensor.objects.get_or_create(
            uuid=uuid,
            defaults={"name": name},
        )
        if was_created:
            created += 1
        else:
            # keep name in sync if it changed
            if name and sensor.name != name:
                sensor.name = name
                sensor.save(update_fields=["name"])
            reused_or_updated += 1

    print(f" Sensors import: created={created}, reused/updated={reused_or_updated}")


def import_roads_and_readings():
    if not os.path.exists(SPEED_CSV):
        raise RuntimeError(f"traffic_speed.csv not found at {SPEED_CSV}")

    df = pd.read_csv(SPEED_CSV)

    required = {"Long_start", "Lat_start", "Long_end", "Lat_end", "Length", "Speed"}
    missing = required - set(df.columns)
    if missing:
        raise RuntimeError(f"traffic_speed.csv missing columns: {missing}")

    print(f"Importing {len(df)} rows from {SPEED_CSV}...")

    created_roads = 0
    reused_roads = 0
    created_readings = 0

    for _, row in df.iterrows():
        road, created = Road.objects.get_or_create(
            long_start=float(row["Long_start"]),
            lat_start=float(row["Lat_start"]),
            long_end=float(row["Long_end"]),
            lat_end=float(row["Lat_end"]),
            length=float(row["Length"]),
        )
        created_roads += int(created)
        reused_roads += int(not created)

        Reading.objects.create(road=road, speed=float(row["Speed"]))
        created_readings += 1

    print(
        f" Roads/Readings import: roads created={created_roads}, "
        f"reused={reused_roads}, readings created={created_readings}"
    )


def main():
    import_sensors()
    import_roads_and_readings()


if __name__ == "__main__":
    main()
