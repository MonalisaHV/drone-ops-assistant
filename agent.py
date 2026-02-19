from datetime import datetime

def dates_overlap(start1, end1, start2, end2):
    return start1 <= end2 and end1 >= start2

def assign_mission(mission, pilots, drones, missions):
    results = []
    warnings = []

    # Dates
    mission_start = datetime.strptime(mission["start_date"], "%Y-%m-%d")
    mission_end = datetime.strptime(mission["end_date"], "%Y-%m-%d")

    for pilot in pilots:

        # Availability
        if pilot["status"] != "Available":
            continue

        # Skill
        if mission["required_skills"] not in pilot["skills"]:
            warnings.append(f"Skill mismatch: {pilot['pilot_id']}")
            continue

        # Certification
        if mission["required_certs"] not in pilot["certifications"]:
            warnings.append(f"Certification mismatch: {pilot['pilot_id']}")
            continue

        # Budget
        total_cost = pilot["daily_rate_inr"] * (
            (mission_end - mission_start).days + 1
        )

        if total_cost > mission["mission_budget"]:
            warnings.append(f"Budget overrun risk: {pilot['pilot_id']}")
            continue

        # Double booking check
        double_booked = False

        if pilot["current_assignment"] != "-":
            for m in missions:
                if m["project_id"] == pilot["current_assignment"]:

                    existing_start = datetime.strptime(m["start_date"], "%Y-%m-%d")
                    existing_end = datetime.strptime(m["end_date"], "%Y-%m-%d")

                    if dates_overlap(mission_start, mission_end, existing_start, existing_end):
                        warnings.append(f"Double booking risk: {pilot['pilot_id']}")
                        double_booked = True
                        break

        if double_booked:
            continue

        # Drone matching
        for drone in drones:

            if drone["status"] != "Available":
                continue

            if drone["location"] != mission["location"]:
                continue

            # Weather risk
            if mission["weather_forecast"] == "Rainy" and "IP43" not in drone["weather_resistance"]:
                warnings.append(f"Weather risk: {drone['drone_id']}")
                continue

            results.append({
                "pilot_id": pilot["pilot_id"],
                "pilot_name": pilot["name"],
                "drone_id": drone["drone_id"],
                "drone_model": drone["model"],
                "project_id": mission["project_id"],
                "estimated_cost": total_cost,
                "location": mission["location"],
            })

    # Urgent Reassignment
    if mission["priority"] in ["High", "Urgent"] and not results:
        warnings.append("⚠ Urgent mission — No available match found. Consider reassigning from lower priority project.")

    return results, warnings
