
import os
import numpy as np
import pandas as pd

from datetime import datetime, timedelta

# Reproducibility: same random data every run
np.random.seed(42)

# Project configuration
OUTPUT_DIR = "data/raw"
os.makedirs(OUTPUT_DIR, exist_ok=True)

NOW = datetime.now()

# ----------------------------------
# 1. GENERATE PRODUCTS
# ----------------------------------

manufacturers = [
    "MedPharma Ltd",
    "EuroHealth GmbH",
    "BioCare Industries",
    "GlobalMed Solutions",
    "PharmaNova"
]

categories = [
    "Antibiotic",
    "Analgesic",
    "Antiviral",
    "Cardiovascular",
    "Antidiabetic"
]

products = pd.DataFrame({
    "product_id": [f"P{i:03d}" for i in range(1, 51)],
    "product_name": [
        f"Medicine {i}" for i in range(1, 51)
    ],
    "manufacturer": np.random.choice(
        manufacturers, 50
    ),
    "category": np.random.choice(
        categories, 50
    )
})

# ----------------------------------
# 2. GENERATE BATCHES
# ----------------------------------

batches = []

for i in range(1, 201):
    product = products.sample(1).iloc[0]

    manufacture_date = NOW - timedelta(
        days=int(np.random.randint(30, 900))
    )

    expiry_date = manufacture_date + timedelta(
        days=int(np.random.randint(365, 1500))
    )

    batches.append({
        "batch_id": f"B{i:03d}",
        "product_id": product["product_id"],
        "manufacture_date": manufacture_date.date(),
        "expiry_date": expiry_date.date(),
        "quantity": int(np.random.randint(500, 10000))
    })

batches = pd.DataFrame(batches)

# ----------------------------------
# 3. GENERATE LOCATIONS
# ----------------------------------

countries = [
    "France", "Germany", "Belgium",
    "Spain", "Italy", "Netherlands",
    "Portugal", "Poland"
]

locations = pd.DataFrame({
    "location_id": [
        f"L{i:03d}" for i in range(1, 101)
    ],
    "location_name": [
        f"Pharmacy {i}" for i in range(1, 101)
    ],
    "country": np.random.choice(
        countries, 100
    ),
    "location_type": np.random.choice(
        ["Pharmacy", "Hospital", "Wholesaler"],
        100
    )
})

# ----------------------------------
# 4. GENERATE VERIFICATION EVENTS
# ----------------------------------

events = []

statuses = [
    "SUCCESS",
    "UNKNOWN_PRODUCT",
    "ALREADY_DECOMMISSIONED",
    "EXPIRED",
    "RECALLED"
]

probabilities = [0.88, 0.035, 0.025, 0.04, 0.02]

for i in range(1, 50001):

    product = products.sample(1).iloc[0]
    batch = batches[
        batches["product_id"] == product["product_id"]
    ].sample(1).iloc[0]

    location = locations.sample(1).iloc[0]

    timestamp = NOW - timedelta(
        days=int(np.random.randint(0, 365)),
        minutes=int(np.random.randint(0, 1440))
    )

    status = np.random.choice(
        statuses, p=probabilities
    )

    serial = f"SN{i:07d}"

    events.append({
        "event_id": f"E{i:07d}",
        "serial_number": serial,
        "product_id": product["product_id"],
        "batch_id": batch["batch_id"],
        "location_id": location["location_id"],
        "event_timestamp": timestamp,
        "verification_status": status,
        "response_reason": status
    })

events = pd.DataFrame(events)

# ----------------------------------
# 5. INTRODUCE CONTROLLED ANOMALIES
# ----------------------------------

# Repeated serial numbers
events.loc[100:109, "serial_number"] = (
    events.loc[99, "serial_number"]
)

# Missing location values: data-quality issue
events.loc[200:204, "location_id"] = np.nan

# Duplicate event records
events = pd.concat([
    events,
    events.iloc[300:305]
], ignore_index=True)

# ----------------------------------
# 6. EXPORT DATASETS
# ----------------------------------

datasets = {
    "products": products,
    "batches": batches,
    "locations": locations,
    "verification_events": events
}

for name, dataframe in datasets.items():
    path = f"{OUTPUT_DIR}/{name}.csv"

    dataframe.to_csv(path, index=False)

    print(
        f"{name}: {len(dataframe):,} records exported"
    )

print("\nSynthetic data generation completed.")
