AirWrite – Virtual Whiteboard using Hand Gestures

AirWrite is a gesture-controlled virtual whiteboard that allows users to draw in the air using their hand gestures captured through a webcam. The system detects finger movements and converts them into drawing strokes on a digital canvas in real time.

This project demonstrates the integration of Computer Vision, Hand Gesture Recognition, and Human-Computer Interaction to create an intuitive and touchless drawing interface.

📌 Features

✋ Hand Gesture Recognition

🖊 Draw in Air using finger tracking

🎨 Multiple Drawing Colors

🧹 Erase / Clear Canvas Option

📷 Real-time Webcam Input

⚡ Low latency drawing experience

💻 Simple and lightweight implementation

🧠 Problem Statement

Traditional digital whiteboards require touchscreens, stylus pens, or physical input devices, which may not always be accessible.

AirWrite solves this problem by enabling users to draw on a virtual whiteboard using only hand gestures, making the interaction touchless, natural, and more interactive.

This approach can be useful in:

Smart classrooms

Online teaching

AR/VR interfaces

Interactive presentations

Touchless systems

🛠 Tech Stack

Programming Language

Python

Libraries Used

OpenCV – for real-time webcam processing

MediaPipe – for hand tracking and gesture detection

NumPy – for array and image operations

Tools

Webcam

Python environment (Anaconda / venv)

⚙️ How It Works

The webcam captures real-time video input.

MediaPipe detects hand landmarks (21 key points of the hand).

The system identifies specific finger positions.

When the index finger is raised, the system enters drawing mode.

The finger movement is tracked and drawn on the virtual canvas.

Different gestures trigger different actions like:

Drawing

Selecting color

Clearing the screen

🖥 Installation

Clone the repository:

git clone https://github.com/yourusername/airwrite-virtual-whiteboard.git
cd airwrite-virtual-whiteboard

Install dependencies:

pip install opencv-python mediapipe numpy

Run the program:

python main.py
🎮 Controls (Example Gestures)
Gesture	Action
Index finger up	Draw
Two fingers up	Selection mode
Hand over clear button	Clear canvas
Color section selection	Change color
📂 Project Structure
AirWrite-Virtual-Whiteboard
│
├── main.py
├── hand_tracking.py
├── utils.py
├── assets/
│   └── UI elements
└── README.md
🚀 Future Improvements

Add shape recognition (circle, square, line)

Add save drawing as image

Add AI handwriting recognition

Multi-hand interaction

Gesture-based UI controls

Web-based version using TensorFlow.js

📸 Demo

(Add screenshots or GIF here)

Example:

![Demo](demo.gif)
👨‍💻 Author

Anshul Pagar
B.Tech CSE Core
SRM Institute of Science and Technology

Skills:
Python • Computer Vision • OpenCV • AI • Software Development

📜 License

This project is licensed under the MIT License.
