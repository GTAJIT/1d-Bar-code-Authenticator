import cv2
from pyzbar.pyzbar import decode

# Start webcam capture (0 = default camera)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Cannot access the webcam.")
    exit()

print("Press 'q' to quit.")

try:
    while True:
        success, frame = cap.read()
        if not success:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        decoded_objects = decode(gray)

        for obj in decoded_objects:
            barcode_data = obj.data.decode("utf-8")
            barcode_type = obj.type
            print(f"Detected {barcode_type}: {barcode_data}")

            (x, y, w, h) = obj.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, barcode_data, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow("Live Barcode Scanner", frame)

        key = cv2.waitKey(1)
        if key == ord("q") or key == 27:  # q or Esc
            break

except KeyboardInterrupt:
    print("Interrupted by user.")

finally:
    cap.release()
    cv2.destroyAllWindows()

