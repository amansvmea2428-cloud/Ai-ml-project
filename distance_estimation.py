def estimate_distance(box_height):

    if box_height > 300:
        return "Very Near", (0, 0, 255)

    elif box_height > 180:
        return "Near", (0, 165, 255)

    elif box_height > 100:
        return "Medium", (0, 255, 255)

    else:
        return "Far", (0, 255, 0)