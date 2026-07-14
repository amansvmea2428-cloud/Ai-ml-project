import cv2
from ultralytics import YOLO
from road_monitor.distance_estimation import estimate_distance
from road_monitor.collision_warning import get_collision_warning
from alerts.alarm import play_alarm

# -----------------------------
# Load YOLOv8 Model
# -----------------------------
model = YOLO("yolov8n.pt")

# -----------------------------
# Open Dashcam Video
# -----------------------------
cap = cv2.VideoCapture("data/pexel2.mp4")

# -----------------------------
# Hazard Categories
# -----------------------------

vehicle_objects = [
    "car",
    "truck",
    "bus",
    "motorcycle",
    "bicycle"
]

human_objects = [
    "person"
]

animal_objects = [
    "dog",
    "cat",
    "bird",
    "horse",
    "sheep",
    "cow",
    "elephant",
    "bear",
    "zebra",
    "giraffe"
]

road_hazards = (
    vehicle_objects +
    human_objects +
    animal_objects
)

alarm_played = False
# -----------------------------
# Process Video
# -----------------------------
while cap.isOpened():

    ret, frame = cap.read()

    if not ret:
        break

    # Resize for faster processing
    frame = cv2.resize(frame, (960, 540))

    # Run YOLO
    results = model(frame, verbose=False)
    danger_detected = False

    for result in results:

        for box in result.boxes:

            cls = int(box.cls[0])
            class_name = model.names[cls]
            confidence = float(box.conf[0])

            # Ignore objects that are not hazards
            if class_name not in road_hazards:
                continue

            # Ignore weak detections
            if confidence < 0.50:
                continue

            # Bounding Box
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            box_height = y2 - y1
            distance, distance_color = estimate_distance(box_height)
            status, status_color = get_collision_warning(distance)
            if status == "DANGER":
                danger_detected = True

            # Determine Hazard Type
            if class_name in vehicle_objects:
                hazard_type = "Vehicle"
                status_color = (0, 255, 0)      # Green

            elif class_name in human_objects:
                hazard_type = "Human"
                status_color = (0, 255, 255)    # Yellow

            elif class_name in animal_objects:
                hazard_type = "Animal"
                status_color = (0, 0, 255)      # Red

            # Draw Bounding Box
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                status_color,
                2
            )

            # Display Label
            label = (
    f"{class_name} | "
    f"{distance} | "
    f"{status}"
)
            cv2.putText(
                frame,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                status_color,
                2
            )
            if danger_detected:
                cv2.putText(
        frame,
        "!!! COLLISION WARNING !!!",
        (180, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (0, 0, 255),
        3
    )

    if not alarm_played:
        play_alarm()
        alarm_played = True
    else:
        alarm_played = False

    # Optional alarm
    # play_alarm()

    cv2.imshow("DriveGuardian AI - Road Hazard Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# -----------------------------
# Cleanup
# -----------------------------
cap.release()
cv2.destroyAllWindows()