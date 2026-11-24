
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Pharmaceutical Supply Chain Intelligence",
    page_icon="💊",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"


@st.cache_data
def load_data():
    events = pd.read_csv(DATA_DIR / "dashboard_events.csv")
    investigations = pd.read_csv(
        DATA_DIR / "dashboard_investigations.csv"
    )

    events["event_timestamp"] = pd.to_datetime(
        events["event_timestamp"],
        format="mixed",
        utc=True
    )

    return events, investigations


events, investigations = load_data()

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("Pharmaceutical Supply Chain Intelligence")
st.caption(
    "Verification analytics | Anomaly detection | "
    "Synthetic pharmaceutical supply chain data"
)

st.divider()

# --------------------------------------------------
# FILTERS
# --------------------------------------------------

st.sidebar.header("Dashboard Filters")

record_types = st.sidebar.multiselect(
    "Record type",
    options=events["record_type"].dropna().unique(),
    default=events["record_type"].dropna().unique()
)

filtered_events = events[
    events["record_type"].isin(record_types)
]

filtered_serials = filtered_events["serial_number"].unique()

filtered_investigations = investigations[
    investigations["serial_number"].isin(filtered_serials)
]

# --------------------------------------------------
# KEY PERFORMANCE INDICATORS
# --------------------------------------------------

total_events = len(filtered_events)

success_count = (
    filtered_events["verification_status"] == "SUCCESS"
).sum()

failure_count = total_events - success_count

flagged_count = filtered_investigations[
    filtered_investigations["combined_flag"] == True
].shape[0]

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Verifications", f"{total_events:,}")
col2.metric(
    "Successful Verifications",
    f"{success_count:,}"
)
col3.metric("Failed Verifications", f"{failure_count:,}")
col4.metric("Flagged Serial Numbers", f"{flagged_count:,}")

st.divider()

# --------------------------------------------------
# VERIFICATION OUTCOMES
# --------------------------------------------------

st.subheader("Verification Outcomes")

outcomes = (
    filtered_events["verification_status"]
    .value_counts()
    .reset_index()
)

outcomes.columns = ["Status", "Count"]

fig_outcomes = px.pie(
    outcomes,
    names="Status",
    values="Count",
    hole=0.55,
    title="Distribution of Verification Outcomes"
)

st.plotly_chart(fig_outcomes, use_container_width=True)

# --------------------------------------------------
# GEOGRAPHICAL ANALYSIS
# --------------------------------------------------

st.subheader("Geographical Activity")

country_activity = (
    filtered_events.groupby("country")
    .size()
    .reset_index(name="Verifications")
    .sort_values("Verifications", ascending=False)
)

fig_country = px.bar(
    country_activity,
    x="country",
    y="Verifications",
    title="Verification Events by Country",
    color="Verifications"
)

st.plotly_chart(fig_country, use_container_width=True)

# --------------------------------------------------
# RISK DISTRIBUTION
# --------------------------------------------------


st.subheader("Anomaly and Risk Monitoring")

# Count serial numbers in each risk category
risk_counts = (
    filtered_investigations["risk_level"]
    .value_counts()
    .reindex(["High", "Medium", "Low"], fill_value=0)
    .reset_index()
)

risk_counts.columns = ["Risk Level", "Serial Numbers"]

# Calculate percentage of total serial numbers
total_serials = risk_counts["Serial Numbers"].sum()

risk_counts["Percentage"] = (
    risk_counts["Serial Numbers"] / total_serials * 100
).round(2)

# Create horizontal bar chart
fig_risk = px.bar(
    risk_counts,
    x="Serial Numbers",
    y="Risk Level",
    orientation="h",
    color="Risk Level",
    text="Serial Numbers",
    hover_data={"Percentage": True},
    title="Serial Numbers by Risk Level",
    category_orders={
        "Risk Level": ["Low", "Medium", "High"]
    }
)

fig_risk.update_traces(
    textposition="outside",
    cliponaxis=False
)

fig_risk.update_layout(
    xaxis_title="Number of Serial Numbers (Log Scale)",
    yaxis_title="Risk Classification",
    xaxis_type="log",
    showlegend=False,
    height=400
)

st.plotly_chart(fig_risk, use_container_width=True)

# --------------------------------------------------
# INVESTIGATION TABLE
# --------------------------------------------------

st.subheader("Investigation Centre")

flagged_records = filtered_investigations[
    filtered_investigations["combined_flag"] == True
].copy()

if not flagged_records.empty:
    display_columns = [
        "serial_number",
        "scan_count",
        "distinct_countries",
        "failure_rate",
        "anomaly_score",
        "risk_level",
        "investigation_reason"
    ]

    st.dataframe(
        flagged_records[display_columns],
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No flagged serial numbers in the selected dataset.")

# --------------------------------------------------
# SERIAL NUMBER SEARCH
# --------------------------------------------------

st.subheader("Serial Number Investigation")

selected_serial = st.selectbox(
    "Select a serial number",
    options=filtered_events["serial_number"].dropna().unique()
)

serial_history = filtered_events[
    filtered_events["serial_number"] == selected_serial
].sort_values("event_timestamp")

st.dataframe(
    serial_history[
        [
            "event_timestamp",
            "country",
            "location_name",
            "verification_status"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

st.divider()

st.caption(
    "Educational prototype using synthetic data. "
    "Anomaly flags indicate patterns requiring investigation; "
    "they do not establish counterfeit products or fraud."
)
