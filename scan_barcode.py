import cv2
from pyzbar.pyzbar import decode

# Load your barcode image file
# image = cv2.imread("images/shreya_code.jpeg")
image = cv2.imread("images/jit_code.jpeg")
# print("Image loaded:", image is not None)

if image is None:
    print("Error: Failed to load image.")
    exit()

# Try all 4 orientations (0, 90, 180, 270 degrees)
found = False
for angle in [0, 90, 180, 270]:
    if angle != 0:
        # Rotate image clockwise
        image_rotated = cv2.rotate(image, {
            90: cv2.ROTATE_90_CLOCKWISE,
            180: cv2.ROTATE_180,
            270: cv2.ROTATE_90_COUNTERCLOCKWISE
        }[angle])
    else:
        image_rotated = image.copy()

    gray = cv2.cvtColor(image_rotated, cv2.COLOR_BGR2GRAY)
    decoded_objects = decode(gray)

    if decoded_objects:
        found = True
        # print(f"Barcode detected at {angle}° rotation:")
        for obj in decoded_objects:
            barcode_data = obj.data.decode("utf-8")
            barcode_type = obj.type
            print(f"{barcode_type}: {barcode_data}")

            # Draw rectangle (optional)
            (x, y, w, h) = obj.rect
            cv2.rectangle(image_rotated, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(image_rotated, barcode_data, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Show result (optional)
        # cv2.imshow("Detected Barcode", image_rotated)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        break

if not found:
    print("No barcode detected in any orientation.")
