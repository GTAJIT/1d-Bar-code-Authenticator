import cv2
from pyzbar.pyzbar import decode

# Load your barcode image file
image = cv2.imread("images/jit_code.jpeg")  # <-- change filename if needed
print("Image loaded:", image is not None)

# Convert to grayscale to improve detection
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Decode barcodes
decoded_objects = decode(gray)

if decoded_objects:
    for obj in decoded_objects:
        barcode_data = obj.data.decode("utf-8")
        barcode_type = obj.type
        print(f"Detected {barcode_type}: {barcode_data}")

        # Draw rectangle around barcode
        (x, y, w, h) = obj.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(
            image,
            barcode_data,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
        )

    # Show result
    cv2.imshow("Barcode Scanner", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No barcode detected.")
