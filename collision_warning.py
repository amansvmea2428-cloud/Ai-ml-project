def get_collision_warning(distance):

    if distance == "Very Near":
        return "DANGER", (0, 0, 255)

    elif distance == "Near":
        return "WARNING", (0, 165, 255)

    elif distance == "Medium":
        return "CAUTION", (0, 255, 255)

    else:
        return "SAFE", (0, 255, 0)