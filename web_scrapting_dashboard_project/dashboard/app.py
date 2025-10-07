import streamlit as st 
import pandas as pd 
import altair as alt 
import os
st.write("Current working directory:", os.getcwd())


@st.cache_data
def load_data():
    df = pd.read_csv("../data/events.csv")
    df.columns = df.columns.str.strip().str.lower()

    if "year" not in df.columns:
        if "date" in df.columns:
            df["year"] = pd.to_datetime(df["date"], errors="coerce").dt.year
        else:
            st.error("❌ 'year' column missing and no date to extract it from.")
            st.stop()

    return df

events = load_data()

st.set_page_config(page_title="MLB Historical Events", layout="wide")
st.sidebar.title("Filters")

years = sorted(events['year'].dropna().unique())
selected_year = st.sidebar.selectbox("Select Year", years)

event_types = events['event'].dropna().unique()
selected_event = st.sidebar.selectbox("Select Event Type", event_types)

st.title("⚾ MLB Historical Events Dashboard")
st.markdown("Explore events year by year from the Baseball Almanac.")

# 📊 Events Per Year
st.subheader("1️⃣ Total Events Per Year")
events_per_year = events.groupby('year').size().reset_index(name='event_count')

chart1 = alt.Chart(events_per_year).mark_bar().encode(
    x='year:O',
    y='event_count:Q',
    tooltip=['year', 'event_count']
).properties(width=700, height=400)

st.altair_chart(chart1)

# 📋 Filtered Events
st.subheader(f"2️⃣ Events in {selected_year} - Type: {selected_event}")
filtered = events[
    (events['year'] == selected_year) & (events['event'] == selected_event)
]

if not filtered.empty:
    st.dataframe(filtered)
else:
    st.info("No events found for the selected filters.")

st.markdown("----")
st.markdown("Created for Capstone Project")
