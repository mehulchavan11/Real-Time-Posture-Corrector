import cv2
import mediapipe as mp
import time

# --- Constants ---
# Threshold to detect slouching. Lower value means more sensitive.
# You might need to adjust this value based on your camera angle and distance.
SLOUCH_THRESHOLD = 0.15 

# Time in seconds to wait before triggering an alert after slouching is detected.
ALERT_DELAY_SECONDS = 3.0 

# --- Initialization ---
# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Initialize video capture from the default webcam
cap = cv2.VideoCapture(0)

# Variables for slouch detection logic
slouch_detected = False
slouch_start_time = 0
alert_active = False

print("Starting Posture Notifier. Press 'q' to quit.")

# --- Main Loop ---
while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Flip the image horizontally for a later selfie-view display
    image = cv2.flip(image, 1)
    
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False # <-- FIX #1
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Process the image and find pose landmarks
    results = pose.process(image_rgb)
    
    # Draw the pose annotation on the image.
    image.flags.writeable = True # <-- FIX #2
    image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

    # --- Posture Logic ---
    posture_status = "Unknown"
    
    if results.pose_landmarks:
        # Get coordinates of the left shoulder and left ear
        landmarks = results.pose_landmarks.landmark
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        left_ear = landmarks[mp_pose.PoseLandmark.LEFT_EAR]
        
        # We only need the X-coordinates to check for forward slouching
        # Check if landmarks are visible
        if left_shoulder.visibility > 0.5 and left_ear.visibility > 0.5:
            # Calculate the horizontal distance
            horizontal_distance = abs(left_ear.x - left_shoulder.x)

            # Check if the person is slouching
            if horizontal_distance > SLOUCH_THRESHOLD:
                posture_status = "Slouching"
                if not slouch_detected:
                    slouch_detected = True
                    slouch_start_time = time.time() # Start the timer
            else:
                posture_status = "Good"
                slouch_detected = False
                slouch_start_time = 0
                alert_active = False # Reset alert if posture is corrected
        else:
            posture_status = "Not fully visible"
            slouch_detected = False
            slouch_start_time = 0
            alert_active = False

        # --- Alert Logic ---
        # If slouching has been detected for long enough, activate the alert
        if slouch_detected and (time.time() - slouch_start_time > ALERT_DELAY_SECONDS):
            alert_active = True

        # Draw the pose annotation on the image.
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS)

    # --- Display Information on Screen ---
    # Display posture status
    cv2.putText(image, f"POSTURE: {posture_status}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Display the alert message if active
    if alert_active:
        cv2.putText(image, "SIT UP STRAIGHT!", (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    # Show the final image
    cv2.imshow('Posture Notifier', image)

    # Exit loop when 'q' is pressed
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# --- Cleanup ---
cap.release()
cv2.destroyAllWindows()