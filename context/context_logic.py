def interpret_scene(objects):
    if not objects:
        return "Empty or natural scene"

    cars = objects.get("car", 0)
    buses = objects.get("bus", 0)
    trains = objects.get("train", 0)
    persons = objects.get("person", 0)
    dogs = objects.get("dog", 0)
    chairs = objects.get("chair", 0)
    tables = objects.get("diningtable", 0)
    bottles = objects.get("bottle", 0)

    total_vehicles = cars + buses + trains

    # =========================
    # 🔥 HIGH PRIORITY RULES
    # =========================

    # Person + dog (VERY IMPORTANT)
    if persons >= 1 and dogs >= 1:
        return "Person walking a dog"

    # Dining activity
    if tables >= 1 and persons >= 1:
        return "People dining or sitting at a table"

    if bottles >= 2 and persons >= 1:
        return "People eating or drinking"

    # =========================
    # FEATURE EXTRACTION
    # =========================

    if total_vehicles >= 6:
        traffic_level = "heavy"
    elif total_vehicles >= 3:
        traffic_level = "moderate"
    elif total_vehicles >= 1:
        traffic_level = "light"
    else:
        traffic_level = "none"

    if persons >= 5:
        human_level = "crowd"
    elif persons >= 2:
        human_level = "group"
    elif persons == 1:
        human_level = "single"
    else:
        human_level = "none"

    # =========================
    # GENERAL SCENE LOGIC (YOUR ORIGINAL)
    # =========================

    # 🚗 Traffic
    if traffic_level == "heavy":
        return f"Heavy traffic with {cars} cars and public transport"

    if traffic_level == "moderate":
        return "Moderate traffic on road"

    if traffic_level == "light" and human_level != "none":
        return "Pedestrians interacting with vehicles"

    # 🚆 Transport
    if trains >= 1:
        return "Railway transport scene"

    if buses >= 1:
        return "Public transport in operation"

    # 👥 Human
    if human_level == "crowd":
        return "Crowded public area"

    if human_level == "group":
        return "Group of people interacting"

    if human_level == "single":
        return "Single person in scene"

    # 🏠 Indoor
    if chairs >= 2:
        return "Indoor environment with furniture"

    # 🌿 Nature fallback (IMPORTANT — keep this)
    if total_vehicles == 0 and persons == 0:
        return "Natural or empty environment"

    return "Mixed activity scene"