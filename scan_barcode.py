import cv2
from pyzbar.pyzbar import decode
import numpy as np

# Initialize the webcam (try index 1 if 0 fails)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Cannot open webcam")
    exit()

# Function to preprocess frame for better blurry detection
def preprocess(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    sharpened = cv2.GaussianBlur(gray, (0, 0), 3)
    sharpened = cv2.addWeighted(gray, 1.5, sharpened, -0.5, 0)
    return sharpened

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    processed_frame = preprocess(frame)

    decoded_objects = decode(processed_frame)

    for obj in decoded_objects:
        try:
            points = obj.polygon

            if len(points) >= 4:
                pts = [(point.x, point.y) for point in points]
                barcode_data = obj.data.decode("utf-8")
                barcode_type = obj.type

                # Use green if decoded properly
                color = (0, 255, 0) if barcode_data else (0, 0, 255)

                # Draw barcode border
                for i in range(len(pts)):
                    cv2.line(frame, pts[i], pts[(i + 1) % len(pts)], color, 2)

                # Put barcode info text
                cv2.putText(
                    frame,
                    f"{barcode_type}: {barcode_data}",
                    (pts[0][0], pts[0][1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    color,
                    2,
                )
        except Exception as e:
            print("Decode error:", e)
            continue

    cv2.imshow("Universal Barcode Scanner", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
