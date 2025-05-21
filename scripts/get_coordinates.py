import cv2

def get_coordinates(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Coordinates: (x: {x}, y: {y})")
        coordinates.append((x, y))

image_path = "GreenCertificate.png"
image = cv2.imread(image_path)

if image is None:
    print("Error: Could not load image. Check the file path.")
    exit()

coordinates = []

# إعداد نافذة قابلة لتغيير الحجم
cv2.namedWindow("image", cv2.WINDOW_NORMAL)
cv2.resizeWindow("image", 800, 600)  # ضبط حجم النافذة (يمكنك تغيير 800x600)
cv2.setMouseCallback("image", get_coordinates)

while True:
    cv2.imshow("image", image)
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break

cv2.destroyAllWindows()
print("Saved Coordinates:", coordinates)