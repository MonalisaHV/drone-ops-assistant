import streamlit as st
import pandas as pd
from sheets_service import (
    get_pilots,
    get_drones,
    get_missions,
    update_pilot_status,
    update_drone_status,
)
from matching import match_pilot_drone
from agent import assign_mission

st.title("🚁 Drone Operations AI Agent")

# ---------------- LOAD DATA ----------------
if st.button("Load Data from Google Sheets"):
    st.session_state.pilots = get_pilots()
    st.session_state.drones = get_drones()
    st.session_state.missions = get_missions()

# ---------------- MAIN APP ----------------
if (
    "pilots" in st.session_state
    and "drones" in st.session_state
    and "missions" in st.session_state
):

    pilots = st.session_state.pilots
    drones = st.session_state.drones
    missions = st.session_state.missions

    pilots_df = pd.DataFrame(pilots)
    drones_df = pd.DataFrame(drones)
    missions_df = pd.DataFrame(missions)

    # ---------------- SHOW DATA ----------------
    st.subheader("Pilots Data")
    st.dataframe(pilots_df)

    st.subheader("Drone Data")
    st.dataframe(drones_df)

    st.subheader("Missions Data")
    st.dataframe(missions_df)

    # ---------------- FILTER ----------------
    st.subheader("🔎 Filter Available Pilots")

    location_filter = st.selectbox(
        "Select Location", pilots_df["location"].unique()
    )

    status_filter = st.selectbox(
        "Select Status", pilots_df["status"].unique()
    )

    filtered = pilots_df[
        (pilots_df["location"] == location_filter)
        & (pilots_df["status"] == status_filter)
    ]

    st.dataframe(filtered)

    # ---------------- COST ----------------
    st.subheader("💰 Calculate Pilot Cost")

    selected_pilot = st.selectbox(
        "Select Pilot", pilots_df["pilot_id"]
    )

    mission_days = st.number_input(
        "Enter Mission Duration (Days)", min_value=1
    )

    selected_row = pilots_df[pilots_df["pilot_id"] == selected_pilot]

    if not selected_row.empty:
        daily_rate = int(selected_row.iloc[0]["daily_rate_inr"])
        total_cost = daily_rate * mission_days
        st.success(f"Total Cost: ₹{total_cost}")

    # ---------------- SMART MATCH ----------------
    st.header("🤖 Smart Matching System")

    selected_location = st.selectbox(
        "Select Location for Matching",
        pilots_df["location"].unique(),
    )

    if st.button("Find Best Matches"):
        matches = match_pilot_drone(pilots, drones, selected_location)
        st.write(matches)

    # ---------------- MISSION ENGINE ----------------
    st.header("🚀 Mission Assignment Engine")

    selected_project = st.selectbox(
        "Select Project",
        missions_df["project_id"]
    )

    selected_mission_row = missions_df[
        missions_df["project_id"] == selected_project
    ].iloc[0]

    # Convert row to dictionary (VERY IMPORTANT FIX)
    selected_mission = selected_mission_row.to_dict()

    if st.button("Run AI Assignment"):

        results, warnings = assign_mission(
            selected_mission,
            pilots,
            drones,
            missions,
        )

        st.subheader("✅ Possible Assignments")
        st.write(results)

        st.subheader("⚠ Risk Warnings")
        st.write(warnings)

        # ---------------- AUTO UPDATE STATUS ----------------
        if results:
            best = results[0]

            update_pilot_status(best["pilot_id"], "Assigned")
            update_drone_status(best["drone_id"], "Assigned")

            st.success("✅ Status updated in Google Sheets!")

    # ---------------- SIMPLE CHAT ----------------
    st.header("💬 Drone Ops Assistant")

    user_query = st.text_input("Ask something...")

    if user_query:
        if "available pilots" in user_query.lower():
            available = pilots_df[pilots_df["status"] == "Available"]
            st.write(available)

        elif "available drones" in user_query.lower():
            available = drones_df[drones_df["status"] == "Available"]
            st.write(available)

        else:
            st.write(
                "I can help with pilots, drones, missions and assignments."
            )
