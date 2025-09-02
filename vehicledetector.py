import cv2
import datetime
import os

# Load Haar cascade for car detection (comes with OpenCV)
car_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_car.xml')

# Initialize counts
counts = {'cars': 0}

# Make logs directory to store counts
if not os.path.exists('logs'):
    os.makedirs('logs')

# Create log file with current date and time
log_filename = 'logs/count_log_' + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.txt'

# Start capturing video from webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to grayscale (required for Haar cascade)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect cars
    cars = car_cascade.detectMultiScale(gray, 1.2, 3)

    # Draw rectangles around detected cars
    for (x, y, w, h) in cars:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Update count (simple count of detected cars per frame)
    counts['cars'] = len(cars)

    # Display counts on the frame
    cv2.putText(frame, f"Cars Count: {counts['cars']}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Show the frame
    cv2.imshow('Vehicle Detection and Counting', frame)

    # Log counts into file with timestamp
    with open(log_filename, 'a') as f:
        f.write(f"{datetime.datetime.now()}: Cars Count: {counts['cars']}\n")

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
