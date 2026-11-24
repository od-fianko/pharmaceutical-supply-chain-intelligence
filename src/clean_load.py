
import os
import pandas as pd
from sqlalchemy import create_engine, text

# ==========================================
# PHARMACEUTICAL SUPPLY CHAIN INTELLIGENCE
# ETL: EXTRACT, TRANSFORM AND LOAD
# ==========================================

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"

os.makedirs(PROCESSED_DIR, exist_ok=True)

print("=" * 55)
print("PHARMACEUTICAL DATA ETL PIPELINE")
print("=" * 55)

# ------------------------------------------
# 1. EXTRACT
# ------------------------------------------

print("\n[1] EXTRACTING DATA...")

products = pd.read_csv(f"{RAW_DIR}/products.csv")
batches = pd.read_csv(f"{RAW_DIR}/batches.csv")
locations = pd.read_csv(f"{RAW_DIR}/locations.csv")
events = pd.read_csv(
    f"{RAW_DIR}/verification_events.csv"
)

print(f"Products: {len(products):,}")
print(f"Batches: {len(batches):,}")
print(f"Locations: {len(locations):,}")
print(f"Events: {len(events):,}")

# ------------------------------------------
# 2. TRANSFORM
# ------------------------------------------

print("\n[2] CLEANING AND TRANSFORMING DATA...")

# Remove duplicate event IDs
initial_events = len(events)

events = events.drop_duplicates(
    subset=["event_id"],
    keep="first"
).copy()

duplicates_removed = initial_events - len(events)

print(f"Duplicate events removed: {duplicates_removed}")

# Handle missing location IDs
missing_locations = events["location_id"].isna().sum()

print(f"Missing location values: {missing_locations}")

UNKNOWN_LOCATION_ID = "L999"

if missing_locations > 0:

    unknown_location = pd.DataFrame([{
        "location_id": UNKNOWN_LOCATION_ID,
        "location_name": "Unknown Location",
        "country": "Unknown",
        "location_type": "Unknown"
    }])

    # Add the unknown location only once
    if UNKNOWN_LOCATION_ID not in locations["location_id"].values:
        locations = pd.concat(
            [locations, unknown_location],
            ignore_index=True
        )

    events["location_id"] = events["location_id"].fillna(
        UNKNOWN_LOCATION_ID
    )

print("Missing locations handled.")

# Standardise date fields
batches["manufacture_date"] = pd.to_datetime(
    batches["manufacture_date"]
).dt.date

batches["expiry_date"] = pd.to_datetime(
    batches["expiry_date"]
).dt.date

events["event_timestamp"] = pd.to_datetime(
    events["event_timestamp"], utc=True
)

# Validate product relationships
valid_products = set(products["product_id"])

assert set(batches["product_id"]).issubset(valid_products)
assert set(events["product_id"]).issubset(valid_products)

# Validate batch relationships
valid_batches = set(
    zip(batches["batch_id"], batches["product_id"])
)

event_batches = set(
    zip(events["batch_id"], events["product_id"])
)

assert event_batches.issubset(valid_batches)

# Validate location relationships
valid_locations = set(locations["location_id"])

assert set(events["location_id"]).issubset(valid_locations)

# Validate event identifiers
assert events["event_id"].is_unique

print("Product relationships validated.")
print("Batch relationships validated.")
print("Location relationships validated.")
print("Event identifiers validated.")

# ------------------------------------------
# 3. EXPORT CLEANED DATA
# ------------------------------------------

print("\n[3] EXPORTING CLEANED DATA...")

datasets = {
    "products": products,
    "batches": batches,
    "locations": locations,
    "verification_events": events
}

for name, dataframe in datasets.items():

    output_path = f"{PROCESSED_DIR}/{name}.csv"

    dataframe.to_csv(output_path, index=False)

    print(
        f"{name}: {len(dataframe):,} cleaned records"
    )

# ------------------------------------------
# 4. LOAD INTO POSTGRESQL
# ------------------------------------------

print("\n[4] CONNECTING TO POSTGRESQL...")

# Uses your local PostgreSQL account and socket
DATABASE_URL = "postgresql+psycopg2:///pharma_intelligence"

engine = create_engine(DATABASE_URL)

try:

    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    print("PostgreSQL connection successful.")

    # Start a transaction so the load can be rolled back
    with engine.begin() as connection:

        connection.execute(text("""
            TRUNCATE TABLE
                verification_events,
                batches,
                locations,
                products
            RESTART IDENTITY CASCADE
        """))

        # Load parent tables before dependent tables
        for name in [
            "products",
            "batches",
            "locations",
            "verification_events"
        ]:

            datasets[name].to_sql(
                name,
                connection,
                if_exists="append",
                index=False,
                chunksize=5000,
                method="multi"
            )

            print(
                f"Loaded {len(datasets[name]):,} rows into {name}"
            )

    print("\nDATABASE LOAD COMPLETED SUCCESSFULLY.")

except Exception as error:

    print("\nETL PIPELINE FAILED.")
    print(f"Error: {error}")
    raise

finally:
    engine.dispose()

print("\n" + "=" * 55)
print("ETL PIPELINE FINISHED")
print("=" * 55)
