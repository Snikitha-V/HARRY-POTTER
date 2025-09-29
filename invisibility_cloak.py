import cv2
import time
import numpy as np

cap = cv2.VideoCapture(0)

print("Initializing camera...")
time.sleep(2)
print("Press 'b' to capture background, 'q' to quit.")

background = None

# Morphological kernels
open_kernel = np.ones((5, 5), np.uint8)
close_kernel = np.ones((3, 3), np.uint8)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (800, 800))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Detect low saturation & brightness (black areas)
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 40])  # Increased brightness threshold for better detection

    mask = cv2.inRange(hsv, lower_black, upper_black)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, open_kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, close_kernel)

    if background is not None:
        # Use HSV background for consistency
        background_hsv = cv2.cvtColor(background, cv2.COLOR_BGR2HSV)

        # Apply mask to background and current frame
        cloak = cv2.bitwise_and(background, background, mask=mask)
        visible = cv2.bitwise_and(frame, frame, mask=cv2.bitwise_not(mask))
        output = cv2.add(cloak, visible)
    else:
        output = frame

    cv2.imshow("Black Invisibility Cloak", output)

    key = cv2.waitKey(1)
    if key == ord('b'):
        background = frame.copy()
        print("✅ Background captured!")
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
