def match_pilot_drone(pilots, drones, location):
    matches = []

    for pilot in pilots:
        if pilot["status"] != "Available":
            continue
        if pilot["location"] != location:
            continue

        for drone in drones:
            if drone["status"] != "Available":
                continue
            if drone["location"] != location:
                continue

            matches.append({
                "pilot_id": pilot["pilot_id"],
                "pilot_name": pilot["name"],
                "drone_id": drone["drone_id"],
                "drone_model": drone["model"],
                "location": location
            })

    return matches
