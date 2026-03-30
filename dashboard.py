import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Real-Time Anomaly Dashboard", layout="wide")

st.title("Real-Time Financial Anomaly Detection Dashboard")

# Read data
try:
    df = pd.read_csv("anomalies_live.csv")
except FileNotFoundError:
    df = pd.DataFrame(columns=["timestamp", "anomaly_score", "reason"])


# Metrics
col1, col2, col3 = st.columns(3)

col1.metric("Total Anomalies", len(df))
col2.metric("System Status", "LIVE")
col3.metric("Last Updated", datetime.now().strftime("%H:%M:%S"))


if not df.empty:
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Chart
    st.subheader("📈 Anomalies Over Time")
    ts = df.set_index("timestamp").resample("1min").count()
    st.line_chart(ts)

    # Table
    st.subheader("📋 Latest Anomalies")
    st.dataframe(
        df.sort_values("timestamp", ascending=False).head(20),
        use_container_width=True
    )

    # Distribution
    st.subheader("📊 Anomaly Score Distribution")
    st.bar_chart(df["anomaly_score"])

else:
    st.warning("No anomaly data found yet. Run streaming script.")