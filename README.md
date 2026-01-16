🧘 Real-Time Posture Corrector

An AI-powered application that helps maintain healthy posture. 
It uses MediaPipe Pose Estimation to track body landmarks in real-time and alerts the user if they slouch for a prolonged period.

🛠 Tech Stack

Language: Python
Libraries: OpenCV (cv2), MediaPipe (mediapipe)

✨ Key Features

Real-Time Detection: Instantly tracks key body landmarks (shoulders and ears) using the webcam.
Smart Slouch Detection: Calculates the horizontal alignment between the ear and shoulder to detect forward head posture.
Timer-Based Alerts: Triggers a visual "SIT UP STRAIGHT!" warning only after 3 seconds of continuous slouching to prevent false alarms.
Privacy First: All processing happens locally on your device; no video is recorded or sent to the cloud.

🚀 How to Run

Install Dependencies:
pip install opencv-python mediapipe

Run the App:

python posture_checker.py
Usage: Sit in front of the webcam.
The app will display "Good" or "Slouching" based on your position. Press q to quit.

👤 Author

Mehul Bharat Chavan
Student, DKTE's Textile & Engineering Institute
