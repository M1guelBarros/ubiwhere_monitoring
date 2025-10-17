import os
import sys
import django
import pandas as pd

# 👇 garantir que o Django encontra o projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ubiwhere_monitoring.settings")
django.setup()

from roads.models import Road
from readings.models import Reading

CSV_PATH = os.path.join(BASE_DIR, "data", "traffic_speed.csv")

def main():
    df = pd.read_csv(CSV_PATH)

    required = {"Long_start", "Lat_start", "Long_end", "Lat_end", "Length", "Speed"}
    missing = required - set(df.columns)
    if missing:
        raise RuntimeError(f"CSV missing columns: {missing}")

    print(f"Importing {len(df)} rows from {CSV_PATH}...")

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
        f"✅ Done. roads created={created_roads}, reused={reused_roads}, "
        f"readings created={created_readings}"
    )

if __name__ == "__main__":
    main()
