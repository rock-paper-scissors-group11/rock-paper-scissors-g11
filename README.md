# ✋ HandPlay — Rock Paper Scissors

**A desktop Rock Paper Scissors game powered by computer vision and hand gesture recognition.**

HandPlay is an interactive game that uses Python, OpenCV, and MediaPipe to recognize hand gestures through a webcam. Players can interact with the game using hand gestures or mouse controls, making gameplay more accessible and engaging.

The project demonstrates how computer vision and real-time hand tracking can be used to create an interactive gaming experience.

## 📌 Table of Contents

- [About the Project](#-about-the-project)
- [Objectives](#-objectives)
- [Features](#-features)
- [Technologies Used](#-technologies-used)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [How to Run](#-how-to-run)
- [How to Play](#-how-to-play)
- [Hand Gesture Controls](#-hand-gesture-controls)
- [Project Structure](#-project-structure)
- [Running Tests](#-running-tests)
- [Browser Version](#-browser-version)
- [Known Limitations](#-known-limitations)
- [Team Members](#-team-members)
- [Future Improvements](#-future-improvements)
- [License](#-license)

## 🎮 About the Project

HandPlay is a computer-based Rock Paper Scissors game developed as a team project.

Instead of relying only on traditional controls, the game uses a webcam to detect hand landmarks and recognize the player's gestures. The computer selects its own move, and the game determines the result using the standard Rock Paper Scissors rules.

The project combines game logic, hand tracking, gesture classification, score management, and a graphical interface in a desktop application.

## 🎯 Objectives

- Develop an interactive Rock Paper Scissors game using Python.
- Apply computer vision to detect and track hand movements.
- Recognize Rock, Paper, and Scissors hand gestures.
- Allow players to interact with game menus and controls.
- Practice teamwork, programming, debugging, and software testing.

## ✨ Features

- **Hand Gesture Recognition:** Detect hand landmarks using MediaPipe and OpenCV.
- **Real-Time Webcam Tracking:** Track the player's hand through a connected camera.
- **Interactive Game Interface:** Navigate game screens using hand gestures or mouse clicks.
- **Dwell-to-Click Interaction:** Select a button by keeping the hand cursor over it for approximately one second.
- **Three-Second Countdown:** Prepare for each round before making a move.
- **Player vs. Computer:** Play against a computer-controlled opponent.
- **Automatic Scoring:** Record round results and determine the match winner.
- **Game History:** View recorded moves and results.
- **Settings:** Access available sound and volume controls.
- **Pause and Resume:** Use the available game controls to pause or continue a match.
- **Browser Version:** Run the separate browser interface using the provided local server script.
- **Automated Tests:** Test important game rules, gesture recognition, scoring, and interface behavior.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.11 | Main programming language |
| OpenCV | Webcam input, image processing, and desktop window display |
| MediaPipe | Hand landmark detection |
| NumPy | Image and numerical processing |
| Pillow | Image-processing support |
| pytest | Automated testing |
| HTML, CSS, JavaScript | Separate browser version |

## 💻 Requirements

Before installing HandPlay, make sure you have:

- Python 3.11 installed.
- A webcam for hand gesture controls.
- A working internet connection to install the required Python packages.
- Git installed if you want to clone the repository.

The Python dependencies are listed in `requirements.txt`.

## 📥 Installation

### Step 1: Clone the repository

Open a terminal or command prompt and run:

```bash
git clone https://github.com/rock-paper-scissors-group11/rock-paper-scissors-g11.git
```

### Step 2: Enter the project folder

```bash
cd rock-paper-scissors-g11
```

### Step 3: Create a virtual environment (recommended)

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

### Step 4: Install dependencies

```bash
python -m pip install -r requirements.txt
```

## ▶️ How to Run

### Desktop game

From the project root, run:

```bash
python main.py
```

The game opens in a desktop window. If the webcam is available, the game can use it for hand tracking.

**Keyboard shortcuts:**

- `Q` — Quit the game.
- `F` — Toggle fullscreen mode.

### Browser version

HandPlay also includes a separate browser version.

Start its local server from the project root:

```bash
python start_web.py
```

Then follow the local address displayed in your terminal to open the browser version.

The browser version is separate from the desktop game.

## 🕹️ How to Play

1. Start the desktop game using `python main.py`.
2. Select **Start Game** to enter the game menu.
3. Start a match using the available controls.
4. Wait for the three-second countdown.
5. Show a Rock, Paper, or Scissors gesture during the capture phase, or select a move button.
6. Wait for the game to recognize your move and reveal the result.
7. Continue playing until either the player or computer wins three rounds.
8. Start another match when the current match ends.

A draw is recorded but does not increase either player's score.

## ✋ Hand Gesture Controls

HandPlay recognizes the following gestures:

| Move | Gesture |
|---|---|
| Rock | No recognized fingers extended |
| Paper | Three or four recognized fingers extended |
| Scissors | Index and middle fingers extended, with ring finger and pinky folded |

### Hand cursor interaction

1. Position your hand where the webcam can see it clearly.
2. Use your index fingertip to move the on-screen hand cursor.
3. Keep the cursor over a button for approximately one second to select it.
4. You can also use mouse clicks and the available move buttons.

**Tip:** Use good lighting and keep your hand within the webcam's view to improve gesture recognition.

## 📁 Project Structure

```text
rock-paper-scissors-g11/
│
├── assets/                  # Project assets
├── src/                     # Core game modules
├── main.py                  # Desktop game entry point
├── play_game.py             # Main game interface and loop
├── requirements.txt         # Python dependencies
├── pytest.ini               # Test configuration
│
├── test_click_ui.py         # UI interaction tests
├── test_game_flow.py        # Game flow tests
├── test_gestures.py         # Gesture recognition tests
├── test_hand_tracker.py     # Hand tracking tests
├── test_rules.py            # Game rules tests
├── test_score.py            # Scoring tests
├── test_stabilizer.py       # Gesture stabilization tests
├── test_window_scaling.py   # Window scaling tests
│
├── architecture.md          # Architecture documentation
├── state-diagram.md         # Game state diagram
├── gesture-guide.md         # Gesture-related documentation file
│
├── index.html               # Browser version
├── app.js                   # Browser application logic
├── styles.css               # Browser styles
├── start_web.py             # Browser version launcher
│
└── README.md                # Project documentation
```

This tree highlights the main files; the repository may contain additional files and subfolders.

## 🧪 Running Tests

HandPlay includes automated tests for important parts of the application.

Run the test suite from the project root:

```bash
python -m pytest
```
The tests cover areas such as:

- Game rules and round outcomes.
- Score management.
- Gesture classification and stabilization.
- Hand tracking.
- Game flow and user interface interactions.
- Window scaling.

Review the test output to see which tests pass or fail in your environment.

## 📚 Documentation

Additional project documentation is available in the repository:

- [Architecture](architecture.md)
- [Game State Diagram](state-diagram.md)

## ⚠️ Known Limitations

- Hand gesture recognition can be affected by poor lighting, hand position, distance, and visibility.
- A working webcam is required for hand gesture controls.
- When multiple hands are detected, the application selects the hand with the largest normalized bounding box as its primary hand.
- Desktop sound support depends on the operating system; the current implementation's sound controls use Windows-specific functionality.
- The browser version is a separate implementation from the desktop game.

## 👥 Team Members

This project was developed collaboratively by Group 11.

Add each team member's name and actual contribution below:

- **[Team Member 1]** — [ KHORN MI ]
- **[Team Member 2]** — [ YA DAVID ]
- **[Team Member 3]** — [ KOY SOKYI]

## 🚀 Future Improvements

Potential improvements for future versions include:

- Improve gesture recognition in different lighting conditions.
- Improve hand cursor accuracy and button selection responsiveness.
- Add more customization options.
- Expand automated testing.
- Improve compatibility across operating systems.

These are possible future improvements, not claims about existing features.



