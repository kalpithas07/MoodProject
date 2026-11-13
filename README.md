# 🌟 MindMate — MoodProject

**MindMate (MoodProject)** is a comprehensive wellness and emotional health web application built with **Streamlit**, **OpenCV**, and **DeepFace**. It combines AI-powered facial emotion recognition, daily mood logging, habit tracking, and relaxation mini-games into an intuitive, gamified dashboard.

---

## 🚀 Features

- **🎭 AI Facial Mood Detection**:
  - Live webcam and image-based facial emotion detection using DeepFace and OpenCV.
  - Emotion mapping to core mood states (Happy, Sad, Angry, Stressed, Neutral) with tailored wellness advice.

- **📊 Mood Tracking & Analytics**:
  - Log daily moods, notes, and emotional triggers.
  - Interactive charts and visual trends to monitor emotional wellbeing over time.

- **✅ Habit & Routine Tracker**:
  - Track essential wellness habits (hydration, sleep, movement, mindfulness, screen breaks, social connection).
  - Track streaks and completion history.

- **🎮 Relaxation & Zen Mini-Games**:
  - Interactive games including *Bubble Wrap, Memory Matrix, Cosmic Particles, Brick Breaker, Koi Pond, Glow Snake, Rhythm Harmony, Zen Sand Garden, Ambient Sound Mixer, Mandala Painter, Zen Piano*, and more.

- **🏆 Gamified Progress**:
  - Earn XP, complete daily quests, and level up your wellness journey.

---

## 🛠️ Tech Stack

- **Frontend & App Framework**: [Streamlit](https://streamlit.io/)
- **Computer Vision & AI**: [OpenCV](https://opencv.org/), [DeepFace](https://github.com/serengil/deepface), TensorFlow / Keras
- **Data & Visualization**: Pandas, NumPy, Matplotlib, Pillow
- **Language**: Python 3.10+

---

## 📦 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/kalpithas07/MoodProject.git
cd MoodProject
```

### 2. Set Up Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 📁 Project Structure

```plaintext
MoodProject/
│
├── app.py                 # Main Streamlit application and navigation
├── face_mood.py           # DeepFace & OpenCV emotion detection module
├── games.py               # Interactive wellness games and zen widgets
├── habits.csv             # Habit tracking data storage
├── mood_data.csv          # Mood logs data storage
├── user_progress.json     # Gamification progress (XP, quests)
├── requirements.txt       # Python dependencies
├── .gitignore             # Ignored files (venv, cache, etc.)
└── README.md              # Project documentation
```

---

## 👤 Author

- **GitHub**: [@kalpithas07](https://github.com/kalpithas07)
