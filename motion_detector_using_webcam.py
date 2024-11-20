import cv2
import winsound
import serial
import time
from datetime import datetime

# Initialize serial communication with Arduino
arduino = serial.Serial('COM5', 9600)  # Adjust COM port as needed
time.sleep(2)  # Wait for the connection to be established

# Open a log file in append mode
log_file = open("motion_log.txt", "a")

webcam = cv2.VideoCapture(0)

try:
    while True:
        _, im1 = webcam.read()
        _, im2 = webcam.read()
        diff = cv2.absdiff(im1, im2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for c in contours:
            if cv2.contourArea(c) < 5000:
                continue

            # Motion detected: beep, send signal to Arduino, and log event
            winsound.Beep(500, 100)
            arduino.write(b'1')  # Send '1' to Arduino to blink the LED

            # Log the timestamp of motion detection
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"Motion detected at: {timestamp}\n")
            print(f"Motion detected at: {timestamp}")  # For debugging

        cv2.imshow("Security Camera", gray)
        if cv2.waitKey(10) == 27:  # Exit on pressing 'Esc'
            break

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Release resources and close files
    webcam.release()
    cv2.destroyAllWindows()
    arduino.close()
    log_file.close()
