import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import os
import io
import json
import random
from datetime import date, datetime, timedelta
from PIL import Image, ImageDraw, ImageOps

from face_mood import render_face_page
from games import (
    get_bubble_wrap_game,
    get_memory_matrix_game,
    get_cosmic_particles_game,
    get_brick_breaker_game,
    get_koi_pond_game,
    get_glow_snake_game,
    get_rhythm_harmony_game,
    get_zen_darts_game,
    get_zen_sand_garden,
    get_fireworks_zen,
    get_crystal_ball_oracle,
    get_mood_tarot_widget,
    get_ambient_sound_mixer,
    get_virtual_pet_widget,
    get_fortune_cookie_widget,
    get_spin_wheel_widget,
    get_mandala_painter,
    get_zen_piano,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="MindMate - Mental Wellness Companion",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# FILES & DATA
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "mood_data.csv")
HABIT_FILE = os.path.join(BASE_DIR, "habits.csv")
PROGRESS_FILE = os.path.join(BASE_DIR, "user_progress.json")
DATA_COLUMNS = ["Date", "Mood", "Journal", "Intensity"]


# ============================================================
# MOOD INFORMATION
# ============================================================

MOODS = {
    "Happy": {
        "emoji": "😊",
        "color": "#166534",
        "chart": "#22c55e",
        "score": 5,
        "description": "Keep the positive energy flowing!",
        "activity": "Balloon Pop"
    },
    "Sad": {
        "emoji": "😔",
        "color": "#1e40af",
        "chart": "#3b82f6",
        "score": 2,
        "description": "Take a gentle moment for yourself.",
        "activity": "Heart Catch"
    },
    "Angry": {
        "emoji": "😡",
        "color": "#991b1b",
        "chart": "#ef4444",
        "score": 1,
        "description": "Release the tension in a safe way.",
        "activity": "Stress Smash"
    },
    "Stressed": {
        "emoji": "😰",
        "color": "#5b21b6",
        "chart": "#8b5cf6",
        "score": 2,
        "description": "Slow down and give your mind some space.",
        "activity": "Calm Garden"
    },
    "Neutral": {
        "emoji": "😐",
        "color": "#334155",
        "chart": "#94a3b8",
        "score": 3,
        "description": "Relax and explore something peaceful.",
        "activity": "Music Lounge"
    }
}


# ---------- NEW MOODS (set 1) ----------
NEW_MOODS = {
    "Crying": {
        "emoji": "😢", "color": "#1e3a8a", "chart": "#60a5fa", "score": 1,
        "description": "It's okay to cry. Let it out, you're not alone.",
        "activity": "Heart Catch"
    },
    "Anxious": {
        "emoji": "😟", "color": "#7c2d12", "chart": "#fb923c", "score": 2,
        "description": "Ground yourself. One slow breath at a time.",
        "activity": "Sand Garden"
    },
    "Lonely": {
        "emoji": "🥺", "color": "#581c87", "chart": "#c084fc", "score": 2,
        "description": "You matter. Let's keep you company for a bit.",
        "activity": "Mochi Pet"
    },
    "Excited": {
        "emoji": "🤩", "color": "#854d0e", "chart": "#facc15", "score": 5,
        "description": "Ride that energy. Celebrate it!",
        "activity": "Fireworks"
    },
    "Tired": {
        "emoji": "😴", "color": "#374151", "chart": "#9ca3af", "score": 2,
        "description": "Your body is asking for rest. Go easy today.",
        "activity": "Ambient Sounds"
    },
    "Bored": {
        "emoji": "🥱", "color": "#0f766e", "chart": "#2dd4bf", "score": 3,
        "description": "Let's wake your mind up with something fun.",
        "activity": "Glow Snake"
    },
}
MOODS.update(NEW_MOODS)

# ---------- EXTRA MOODS: emoji, text color, chart color, score 1-5, description ----------
# NOTE: mood names must be ONE word (the CSV loader reads the first word).
_EXTRA_MOODS = {
    "Calm":         ("😌", "#0f766e", "#34d399", 4, "Stay in this peaceful space."),
    "Grateful":     ("🙏", "#166534", "#4ade80", 5, "Gratitude makes good days even better."),
    "Hopeful":      ("🌈", "#0369a1", "#38bdf8", 4, "Good things are on their way."),
    "Proud":        ("😎", "#854d0e", "#fbbf24", 5, "You earned this. Celebrate it!"),
    "Motivated":    ("💪", "#9a3412", "#fb923c", 5, "Use this drive while it's strong."),
    "Playful":      ("😜", "#be185d", "#f472b6", 5, "Time to have some fun!"),
    "Loved":        ("🥰", "#9d174d", "#f9a8d4", 5, "Feeling cared for is a beautiful thing."),
    "Overwhelmed":  ("🤯", "#6b21a8", "#a78bfa", 1, "Too much at once. One small step at a time."),
    "Confused":     ("😕", "#475569", "#94a3b8", 3, "It's okay not to have all the answers."),
    "Frustrated":   ("😤", "#b91c1c", "#f87171", 2, "Let the frustration out safely."),
    "Nervous":      ("😬", "#a16207", "#fcd34d", 2, "Nerves mean you care. Breathe through it."),
    "Scared":       ("😨", "#3730a3", "#818cf8", 1, "You're safe right now. Breathe slowly."),
    "Guilty":       ("😞", "#57534e", "#a8a29e", 2, "Be kind to yourself. Everyone makes mistakes."),
    "Jealous":      ("😒", "#14532d", "#86efac", 2, "Comparison steals joy. Focus on your own path."),
    "Heartbroken":  ("💔", "#881337", "#fb7185", 1, "Healing takes time. Be gentle with your heart."),
    "Numb":         ("😶", "#334155", "#cbd5e1", 2, "Feeling nothing is also a feeling. Go slow."),
    "Embarrassed":  ("😳", "#be123c", "#fda4af", 2, "This moment will pass. Nobody remembers it as much as you."),
    # ---- more moods ----
    "Relaxed":      ("🧘", "#0e7490", "#67e8f9", 4, "Soak in this easy, unhurried feeling."),
    "Peaceful":     ("🕊️", "#1d4ed8", "#93c5fd", 4, "A quiet mind is a gift. Enjoy it."),
    "Content":      ("🙂", "#15803d", "#86efac", 4, "Satisfied with where you are. That's beautiful."),
    "Joyful":       ("😄", "#a16207", "#fde047", 5, "Pure joy! Let it spill over."),
    "Inspired":     ("✨", "#7e22ce", "#d8b4fe", 5, "Ideas are flowing. Capture them!"),
    "Creative":     ("🎨", "#c2410c", "#fdba74", 4, "Make something, anything. Let it flow."),
    "Curious":      ("🧐", "#0369a1", "#7dd3fc", 4, "Curiosity is the start of every discovery."),
    "Confident":    ("🦁", "#b45309", "#fbbf24", 5, "You've got this. Own the moment."),
    "Energetic":    ("⚡", "#ca8a04", "#fde047", 5, "Full of energy! Put it to good use."),
    "Relieved":     ("😅", "#047857", "#6ee7b7", 4, "That weight is off your shoulders. Breathe out."),
    "Nostalgic":    ("🕰️", "#78350f", "#d6a77a", 3, "Memories are warm. Hold them gently."),
    "Restless":     ("🌀", "#9a3412", "#fdba74", 2, "Can't sit still? Give that energy somewhere to go."),
    "Irritated":    ("😠", "#b91c1c", "#fca5a5", 2, "Small things piling up. Take a breather."),
    "Disappointed": ("🙁", "#475569", "#94a3b8", 2, "Things didn't go as hoped. That's allowed to sting."),
    "Hurt":         ("🤕", "#9f1239", "#fda4af", 1, "Your feelings matter. Be gentle with yourself."),
    "Insecure":     ("🫤", "#6b7280", "#d1d5db", 2, "You are more than your doubts."),
    "Homesick":     ("🏠", "#92400e", "#fcd34d", 2, "Missing home shows how much love you carry."),
    "Exhausted":    ("😩", "#374151", "#9ca3af", 1, "You've been giving a lot. Time to refill."),
    "Hopeless":     ("🥀", "#3f3f46", "#a1a1aa", 1, "This feeling is heavy, but it is not permanent."),
    "Distracted":   ("🫠", "#0f766e", "#5eead4", 3, "Mind wandering? Gently bring it back."),
    "Silly":        ("🤪", "#be185d", "#f9a8d4", 5, "Laughter is great medicine. Be silly!"),
    "Shy":          ("🙈", "#7c3aed", "#c4b5fd", 3, "Quiet is okay. Take it at your own pace."),
    "Determined":   ("🔥", "#b91c1c", "#fb923c", 4, "Focus locked in. Keep going."),
    "Sleepy":       ("💤", "#1e3a8a", "#93c5fd", 3, "Your body wants rest. Wind down softly."),
}
for _name, (_emo, _col, _chart, _score, _desc) in _EXTRA_MOODS.items():
    MOODS[_name] = {
        "emoji": _emo, "color": _col, "chart": _chart,
        "score": _score, "description": _desc, "activity": ""
    }

# name -> (icon, required XP, where to find it)
GAME_INFO = {
    "Infinite Bubble Wrap": ("🫧", 0, "Arcade → Pop & Tactile"),
    "Balloon Pop": ("🎈", 0, "Arcade → Pop & Tactile"),
    "Heart Catch": ("💙", 0, "Arcade → Pop & Tactile"),
    "Stress Smash": ("💥", 0, "Arcade → Pop & Tactile"),
    "Memory Matrix": ("🧠", 100, "Arcade → Focus & Arcade"),
    "Zen Brick Breaker": ("🧱", 300, "Arcade → Focus & Arcade"),
    "Glow Snake": ("🐍", 350, "Arcade → Focus & Arcade"),
    "Lotus Darts": ("🎯", 400, "Arcade → Focus & Arcade"),
    "Mandala Painter": ("🎨", 250, "Arcade → Art & Music"),
    "Zen Chime Piano": ("🎹", 500, "Arcade → Art & Music"),
    "Rhythm Harmony": ("🎵", 600, "Arcade → Art & Music"),
    "Zen Koi Pond": ("🌸", 150, "Arcade → Nature & Zen"),
    "Japanese Sand Garden": ("🪨", 200, "Arcade → Nature & Zen"),
    "Cosmic Particles": ("🌌", 1000, "Arcade → Nature & Zen"),
    "Midnight Fireworks": ("🎆", 1200, "Arcade → Nature & Zen"),
    "Cosmic Oracle": ("🔮", 700, "Arcade → Mystic Lounge"),
    "3-Card Tarot": ("🃏", 800, "Arcade → Mystic Lounge"),
    "Spin Wheel": ("🎡", 0, "Arcade → Mystic Lounge"),
    "Fortune Cookie": ("🥠", 0, "Arcade → Mystic Lounge"),
    "Mochi Pet": ("🐾", 0, "Dashboard"),
    "Ambient Sound Mixer": ("🎧", 0, "Ambient Sound Lounge"),
    "Guided Breathing": ("🌬️", 0, "Calm Toolkit"),
    "Grounding": ("🌳", 0, "Calm Toolkit → 5-4-3-2-1"),
    "Gratitude Journal": ("🙏", 0, "Calm Toolkit → Gratitude"),
    "Affirmations": ("💬", 0, "Calm Toolkit → Affirmations"),
    "Journal Writing": ("📔", 0, "Journal page"),
}

# Mood -> 6 recommended games / tools (every name must exist in GAME_INFO)
MOOD_GAMES = {
    "Happy":        ["Balloon Pop", "Midnight Fireworks", "Rhythm Harmony", "Spin Wheel", "Mochi Pet", "Gratitude Journal"],
    "Sad":          ["Heart Catch", "Zen Koi Pond", "Mochi Pet", "Ambient Sound Mixer", "Journal Writing", "Affirmations"],
    "Angry":        ["Stress Smash", "Infinite Bubble Wrap", "Zen Brick Breaker", "Guided Breathing", "Lotus Darts", "Journal Writing"],
    "Stressed":     ["Zen Koi Pond", "Japanese Sand Garden", "Guided Breathing", "Ambient Sound Mixer", "Mandala Painter", "Grounding"],
    "Neutral":      ["Memory Matrix", "Mandala Painter", "Cosmic Particles", "Fortune Cookie", "Glow Snake", "3-Card Tarot"],
    "Crying":       ["Heart Catch", "Zen Chime Piano", "Ambient Sound Mixer", "Mochi Pet", "Grounding", "Journal Writing"],
    "Anxious":      ["Japanese Sand Garden", "Mandala Painter", "Guided Breathing", "Grounding", "Infinite Bubble Wrap", "Ambient Sound Mixer"],
    "Lonely":       ["Mochi Pet", "Heart Catch", "Zen Chime Piano", "Fortune Cookie", "Cosmic Oracle", "Affirmations"],
    "Excited":      ["Midnight Fireworks", "Rhythm Harmony", "Zen Brick Breaker", "Balloon Pop", "Spin Wheel", "Cosmic Particles"],
    "Tired":        ["Ambient Sound Mixer", "Zen Koi Pond", "Heart Catch", "Guided Breathing", "Fortune Cookie", "Affirmations"],
    "Bored":        ["Glow Snake", "Memory Matrix", "Lotus Darts", "Spin Wheel", "Rhythm Harmony", "3-Card Tarot"],
    "Calm":         ["Mandala Painter", "Zen Chime Piano", "Zen Koi Pond", "Cosmic Particles", "Japanese Sand Garden", "Ambient Sound Mixer"],
    "Grateful":     ["Gratitude Journal", "Fortune Cookie", "Mochi Pet", "Zen Chime Piano", "Spin Wheel", "Journal Writing"],
    "Hopeful":      ["Fortune Cookie", "Spin Wheel", "Midnight Fireworks", "Cosmic Oracle", "Mandala Painter", "Affirmations"],
    "Proud":        ["Midnight Fireworks", "Rhythm Harmony", "Lotus Darts", "Spin Wheel", "Zen Brick Breaker", "Journal Writing"],
    "Motivated":    ["Zen Brick Breaker", "Lotus Darts", "Memory Matrix", "Glow Snake", "Rhythm Harmony", "Affirmations"],
    "Playful":      ["Balloon Pop", "Infinite Bubble Wrap", "Spin Wheel", "Rhythm Harmony", "Glow Snake", "Mochi Pet"],
    "Loved":        ["Heart Catch", "Mochi Pet", "Zen Chime Piano", "Fortune Cookie", "Gratitude Journal", "Midnight Fireworks"],
    "Overwhelmed":  ["Guided Breathing", "Zen Koi Pond", "Japanese Sand Garden", "Ambient Sound Mixer", "Grounding", "Journal Writing"],
    "Confused":     ["Memory Matrix", "Mandala Painter", "3-Card Tarot", "Cosmic Oracle", "Guided Breathing", "Journal Writing"],
    "Frustrated":   ["Stress Smash", "Infinite Bubble Wrap", "Zen Brick Breaker", "Lotus Darts", "Guided Breathing", "Glow Snake"],
    "Nervous":      ["Guided Breathing", "Infinite Bubble Wrap", "Japanese Sand Garden", "Zen Koi Pond", "Grounding", "Affirmations"],
    "Scared":       ["Grounding", "Guided Breathing", "Mochi Pet", "Ambient Sound Mixer", "Zen Koi Pond", "Affirmations"],
    "Guilty":       ["Japanese Sand Garden", "Heart Catch", "Guided Breathing", "Journal Writing", "Affirmations", "Ambient Sound Mixer"],
    "Jealous":      ["Mandala Painter", "Memory Matrix", "Guided Breathing", "Gratitude Journal", "Fortune Cookie", "Journal Writing"],
    "Heartbroken":  ["Heart Catch", "Zen Koi Pond", "Ambient Sound Mixer", "Mochi Pet", "Journal Writing", "Zen Chime Piano"],
    "Numb":         ["Infinite Bubble Wrap", "Glow Snake", "Cosmic Particles", "Ambient Sound Mixer", "Grounding", "Rhythm Harmony"],
    "Embarrassed":  ["Infinite Bubble Wrap", "Balloon Pop", "Mochi Pet", "Spin Wheel", "Affirmations", "Fortune Cookie"],
    "Relaxed":      ["Zen Koi Pond", "Ambient Sound Mixer", "Glow Snake", "Zen Chime Piano", "Cosmic Particles", "Gratitude Journal"],
    "Peaceful":     ["Japanese Sand Garden", "Zen Chime Piano", "Zen Koi Pond", "Ambient Sound Mixer", "Guided Breathing", "Cosmic Oracle"],
    "Content":      ["Fortune Cookie", "Mochi Pet", "Zen Chime Piano", "Gratitude Journal", "Zen Koi Pond", "Spin Wheel"],
    "Joyful":       ["Balloon Pop", "Midnight Fireworks", "Rhythm Harmony", "Spin Wheel", "Mochi Pet", "Zen Brick Breaker"],
    "Inspired":     ["Mandala Painter", "Zen Chime Piano", "Cosmic Particles", "Cosmic Oracle", "Journal Writing", "Rhythm Harmony"],
    "Creative":     ["Mandala Painter", "Zen Chime Piano", "Japanese Sand Garden", "Cosmic Particles", "Rhythm Harmony", "Journal Writing"],
    "Curious":      ["Cosmic Oracle", "3-Card Tarot", "Memory Matrix", "Cosmic Particles", "Fortune Cookie", "Glow Snake"],
    "Confident":    ["Lotus Darts", "Zen Brick Breaker", "Rhythm Harmony", "Midnight Fireworks", "Affirmations", "Spin Wheel"],
    "Energetic":    ["Zen Brick Breaker", "Rhythm Harmony", "Glow Snake", "Balloon Pop", "Lotus Darts", "Midnight Fireworks"],
    "Relieved":     ["Guided Breathing", "Zen Koi Pond", "Midnight Fireworks", "Fortune Cookie", "Ambient Sound Mixer", "Gratitude Journal"],
    "Nostalgic":    ["Zen Chime Piano", "Ambient Sound Mixer", "Journal Writing", "Fortune Cookie", "Mochi Pet", "Cosmic Oracle"],
    "Restless":     ["Glow Snake", "Infinite Bubble Wrap", "Guided Breathing", "Lotus Darts", "Japanese Sand Garden", "Grounding"],
    "Irritated":    ["Stress Smash", "Infinite Bubble Wrap", "Guided Breathing", "Zen Brick Breaker", "Ambient Sound Mixer", "Grounding"],
    "Disappointed": ["Heart Catch", "Zen Koi Pond", "Affirmations", "Journal Writing", "Fortune Cookie", "Mandala Painter"],
    "Hurt":         ["Heart Catch", "Mochi Pet", "Mandala Painter", "Affirmations", "Journal Writing", "Japanese Sand Garden"],
    "Insecure":     ["Affirmations", "Mochi Pet", "Mandala Painter", "Lotus Darts", "Fortune Cookie", "Guided Breathing"],
    "Homesick":     ["Mochi Pet", "Zen Chime Piano", "Ambient Sound Mixer", "Heart Catch", "Journal Writing", "Fortune Cookie"],
    "Exhausted":    ["Ambient Sound Mixer", "Guided Breathing", "Zen Chime Piano", "Japanese Sand Garden", "Gratitude Journal", "Mochi Pet"],
    "Hopeless":     ["Mochi Pet", "Ambient Sound Mixer", "Affirmations", "Grounding", "Fortune Cookie", "Zen Koi Pond"],
    "Distracted":   ["Memory Matrix", "Guided Breathing", "Grounding", "Lotus Darts", "Glow Snake", "Mandala Painter"],
    "Silly":        ["Balloon Pop", "Spin Wheel", "Infinite Bubble Wrap", "Glow Snake", "Rhythm Harmony", "Fortune Cookie"],
    "Shy":          ["Mochi Pet", "Zen Koi Pond", "Affirmations", "Zen Chime Piano", "Mandala Painter", "Fortune Cookie"],
    "Determined":   ["Lotus Darts", "Memory Matrix", "Affirmations", "Journal Writing", "Grounding", "Zen Brick Breaker"],
    "Sleepy":       ["Ambient Sound Mixer", "Cosmic Particles", "Guided Breathing", "Zen Koi Pond", "Journal Writing", "Fortune Cookie"],
}

# Hand-written tips for some moods. Moods without custom tips get tips auto-built from their games.
MOOD_TIPS = {
    "Crying": [
        "Let the tears come. Crying is a natural release, not a weakness.",
        "Drink some water and take slow breaths.",
        "Reach out to someone you trust, or write it in the Journal.",
    ],
    "Anxious": [
        "Try 5-4-3-2-1 Grounding in the Calm Toolkit.",
        "Do 4-7-8 breathing for two minutes.",
        "Rake the Sand Garden slowly and focus on each stroke.",
    ],
    "Lonely": [
        "Say hi to Mochi on the Dashboard 🐾",
        "Message one person, even just a 'how are you?'",
        "Play some soft notes on the Zen Chime Piano.",
    ],
    "Excited": [
        "Channel it: launch fireworks or play Rhythm Harmony!",
        "Write down what you're excited about in the Journal.",
        "Share the good news with someone.",
    ],
    "Tired": [
        "Put on gentle rain in the Ambient Sound Lounge.",
        "Take a 10-minute rest, no screens.",
        "Drink water and stretch lightly.",
    ],
    "Bored": [
        "Challenge your brain with Memory Matrix.",
        "Try Glow Snake or Lotus Darts for quick fun.",
        "Spin the wheel and see what you get!",
    ],
}
for _m, _g in MOOD_GAMES.items():
    MOOD_TIPS.setdefault(_m, [
        f"Try {_g[0]} ({GAME_INFO[_g[0]][2]}).",
        f"Then switch to {_g[1]} ({GAME_INFO[_g[1]][2]}) for a different feel.",
        f"When you're ready, try {_g[2]} ({GAME_INFO[_g[2]][2]}).",
    ])

# Heavier moods: show a gentle support note
HEAVY_MOODS = {"Crying", "Heartbroken", "Scared", "Overwhelmed", "Numb", "Guilty", "Hopeless", "Hurt", "Exhausted"}


def render_support_note(mood):
    """Gentle support message for heavier moods."""
    if mood in HEAVY_MOODS:
        st.info(
            "💙 If this feeling is heavy or lasts a long time, please talk to someone you trust. "
            "In India you can call Tele-MANAS at 14416 (free, 24/7). More help is in Support & Settings."
        )


QUOTES = [
    ("You don't have to control your thoughts. You just have to stop letting them control you.", "Dan Millman"),
    ("Feelings are just visitors. Let them come and go.", "Mooji"),
    ("Almost everything will work again if you unplug it for a few minutes, including you.", "Anne Lamott"),
    ("Small steps every day still add up to a long journey.", "MindMate"),
    ("It's okay to not be okay. It's not okay to stay that way alone.", "MindMate"),
    ("Be gentle with yourself. You're doing the best you can.", "MindMate"),
    ("Rest is not a reward. It is part of the process.", "MindMate"),
    ("You have survived 100% of your hardest days.", "MindMate"),
    ("Nothing is permanent, including this feeling.", "MindMate"),
    ("Progress, not perfection.", "MindMate"),
]

JOURNAL_PROMPTS = [
    "What is one thing that made you smile today?",
    "What is weighing on your mind right now?",
    "Write about someone you are grateful for.",
    "What would you tell your best friend if they felt like you do today?",
    "What is one small thing you can do to take care of yourself tomorrow?",
    "Describe your perfect calm moment in detail.",
    "What did you learn about yourself this week?",
    "What are you proud of, even if it's small?",
    "What do you need more of in your life right now?",
    "Write a letter to your future self.",
]

AFFIRMATIONS = [
    "I am allowed to take up space.",
    "I can handle what today brings, one step at a time.",
    "My feelings are valid, and they will pass.",
    "I am doing better than I think.",
    "I choose to be kind to myself today.",
    "I deserve rest and peace.",
    "Every breath helps me reset.",
    "I am growing, even when it's slow.",
]

HABITS = {
    "💧 Drank enough water": "water",
    "😴 Slept 7+ hours": "sleep",
    "🚶 Moved / exercised": "move",
    "🧘 Meditated or breathed": "calm",
    "📵 Limited screen time": "screen",
    "🤝 Connected with someone": "social",
}


# ============================================================
# DATA HELPERS & HTML SANITIZER
# ============================================================

def html(s):
    """Strip leading/trailing indentation so Markdown never treats HTML as an indented code block."""
    if not s:
        return ""
    return "\n".join(line.strip() for line in str(s).strip().splitlines() if line.strip())


def render_html(s):
    """Render HTML cleanly in Streamlit without code-block artifacts."""
    st.markdown(html(s), unsafe_allow_html=True)


def clean_mood(value):
    """'Sad 😔' -> 'Sad'. Returns None for unknown values."""
    if pd.isna(value):
        return None
    word = str(value).strip().split(" ")[0]
    return word if word in MOODS else None


def load_mood_data():
    """Load mood_data.csv into a clean, analysis-ready DataFrame."""
    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_csv(DATA_FILE)
        except Exception:
            df = pd.DataFrame(columns=DATA_COLUMNS)
    else:
        df = pd.DataFrame(columns=DATA_COLUMNS)

    for col in DATA_COLUMNS:
        if col not in df.columns:
            df[col] = np.nan

    df["Journal"] = df["Journal"].fillna("").astype(str)
    df["Mood"] = df["Mood"].apply(clean_mood)
    df = df.dropna(subset=["Mood"]).copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce", format="mixed")
    df = df.dropna(subset=["Date"]).copy()
    df["Score"] = df["Mood"].map(lambda m: MOODS[m]["score"])
    df["Day"] = df["Date"].dt.normalize()
    return df.sort_values("Date").reset_index(drop=True)


def save_entry(mood, journal="", intensity=None):
    """Append one entry to mood_data.csv."""
    row = {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Mood": f"{mood} {MOODS[mood]['emoji']}",
        "Journal": journal.strip(),
        "Intensity": intensity if intensity is not None else "",
    }

    if os.path.exists(DATA_FILE):
        try:
            raw = pd.read_csv(DATA_FILE)
        except Exception:
            raw = pd.DataFrame(columns=DATA_COLUMNS)
    else:
        raw = pd.DataFrame(columns=DATA_COLUMNS)

    for col in DATA_COLUMNS:
        if col not in raw.columns:
            raw[col] = ""

    raw = pd.concat([raw, pd.DataFrame([row])], ignore_index=True)
    raw = raw[DATA_COLUMNS]
    raw.to_csv(DATA_FILE, index=False, encoding="utf-8")


def compute_streak(df):
    """Consecutive days with at least one check-in, ending today or yesterday."""
    if df.empty:
        return 0
    days = set(df["Day"].dt.date)
    cursor = date.today()
    if cursor not in days:
        cursor -= timedelta(days=1)
    streak_count = 0
    while cursor in days:
        streak_count += 1
        cursor -= timedelta(days=1)
    return streak_count


def daily_average(df):
    if df.empty:
        return pd.Series(dtype=float)
    return df.groupby("Day")["Score"].mean()


def load_habits():
    h = pd.DataFrame(columns=["Date", "Habit", "Done"])
    if os.path.exists(HABIT_FILE):
        try:
            h = pd.read_csv(HABIT_FILE)
        except Exception:
            h = pd.DataFrame(columns=["Date", "Habit", "Done"])
    h["Date"] = pd.to_datetime(h["Date"], errors="coerce")
    h["Done"] = pd.to_numeric(h["Done"], errors="coerce").fillna(0).astype(int)
    return h.dropna(subset=["Date"]).reset_index(drop=True)


def save_habits_for_day(day, done_keys):
    h = load_habits()
    h = h[h["Date"].dt.date != day]
    new_rows = pd.DataFrame(
        [
            {"Date": pd.Timestamp(day), "Habit": key, "Done": int(key in done_keys)}
            for key in HABITS.values()
        ]
    )
    pd.concat([h, new_rows], ignore_index=True).to_csv(
        HABIT_FILE, index=False, encoding="utf-8"
    )


def greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "Good morning"
    if hour < 17:
        return "Good afternoon"
    return "Good evening"


# ============================================================
# PROGRESSION & UNLOCK SYSTEM
# ============================================================

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "xp": 120,
        "claimed_quests": [],
        "face_scans": 0,
    }


def save_progress(data):
    try:
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass


def get_user_xp():
    if "user_progress" not in st.session_state:
        st.session_state.user_progress = load_progress()
    return st.session_state.user_progress.get("xp", 120)


def add_xp(points, reason=""):
    if "user_progress" not in st.session_state:
        st.session_state.user_progress = load_progress()
    st.session_state.user_progress["xp"] = st.session_state.user_progress.get("xp", 0) + points
    save_progress(st.session_state.user_progress)
    st.toast(f"🎉 +{points} Wellness XP! {reason}", icon="✨")


def is_feature_unlocked(required_xp):
    if st.session_state.get("dev_unlock_all", False):
        return True
    return get_user_xp() >= required_xp


def get_level_info(xp):
    levels = [
        (0, "🌱 Zen Novice", "#94a3b8"),
        (100, "🌿 Mindful Seeker", "#38bdf8"),
        (250, "🌸 Harmony Explorer", "#a855f7"),
        (500, "🧘 Calm Master", "#ec4899"),
        (1000, "🌌 Cosmic Zen Guru", "#f59e0b"),
    ]
    cur_lvl = levels[0]
    next_xp = 100
    for threshold, title, color in levels:
        if xp >= threshold:
            cur_lvl = (threshold, title, color)
    idx = levels.index(cur_lvl)
    next_xp = levels[idx + 1][0] if idx + 1 < len(levels) else cur_lvl[0] + 500
    return cur_lvl[1], cur_lvl[2], next_xp


def render_game_tab(title, icon, required_xp, description, game_html, height=640, game_key="game"):
    """Render unlocked playable game component or a sleek locked card with live progress and unlock triggers."""
    xp = get_user_xp()
    unlocked = is_feature_unlocked(required_xp)

    if unlocked:
        render_html(
            f"""
            <div class="activity-box" style="border-left: 5px solid #38bdf8;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h2 style="margin:0; font-size:22px;">{icon} {title}</h2>
                    <span style="background:rgba(34,197,94,0.15); color:#15803d; border:1px solid #22c55e; padding:4px 12px; border-radius:20px; font-size:12px; font-weight:800;">
                        ✨ UNLOCKED
                    </span>
                </div>
                <p style="margin:8px 0 0; color:#64748b;">{description}</p>
            </div>
            """
        )
        components.html(game_html, height=height, scrolling=False)
    else:
        pct = min(100, int((xp / required_xp) * 100)) if required_xp > 0 else 100
        needed = max(0, required_xp - xp)
        render_html(
            f"""
            <div style="background:linear-gradient(135deg, #0f172a, #1e1b4b); border:2px dashed #818cf8; border-radius:24px; padding:35px 25px; text-align:center; color:white; margin:15px 0;">
                <div style="font-size:55px; margin-bottom:8px;">🔒</div>
                <h2 style="color:white; margin:0 0 6px; font-size:24px;">{icon} {title} is Locked</h2>
                <p style="color:#cbd5e1; font-size:14px; max-width:520px; margin:0 auto 18px;">
                    {description}<br>
                    <b style="color:#fde047;">Requires {required_xp} XP</b> to unlock (You need <b>{needed}</b> more XP).
                </p>
                <div style="max-width:400px; margin:0 auto 10px; background:rgba(255,255,255,0.1); border-radius:12px; height:14px; overflow:hidden; border:1px solid rgba(255,255,255,0.15);">
                    <div style="width:{pct}%; height:100%; background:linear-gradient(90deg, #38bdf8, #818cf8); transition:width 0.4s;"></div>
                </div>
                <div style="font-size:13px; color:#94a3b8; font-weight:700;">Progress: {xp} / {required_xp} XP ({pct}%)</div>
            </div>
            """
        )
        c_act1, c_act2, c_act3 = st.columns(3)
        with c_act1:
            if st.button(f"✨ Boost +30 XP for {title}", key=f"boost_{game_key}", use_container_width=True):
                add_xp(30, f"Unlocking {title}")
                st.rerun()
        with c_act2:
            if st.button("📸 Claim Face Scan Quest (+30 XP)", key=f"face_go_{game_key}", use_container_width=True):
                add_xp(30, "Face Mood Scan Quest")
                st.rerun()
        with c_act3:
            if st.button(f"🔓 Unlock {title} Instantly", key=f"instant_{game_key}", use_container_width=True):
                add_xp(needed, f"Unlocked {title}!")
                st.rerun()


def render_recommended_games(mood):
    """Show games/tools recommended for the current mood, 3 per row, using native Streamlit cards."""
    names = MOOD_GAMES.get(mood, [])
    if not names:
        return
    st.markdown(f"#### 🎮 Recommended for your {MOODS[mood]['emoji']} {mood.lower()} mood")
    for start in range(0, len(names), 3):
        row_names = names[start:start + 3]
        cols = st.columns(3)
        for col, name in zip(cols, row_names):
            icon, req, where = GAME_INFO[name]
            unlocked = is_feature_unlocked(req)
            with col:
                with st.container(border=True):
                    st.markdown(f"## {icon}")
                    st.markdown(f"**{name}**")
                    st.caption(f"📍 {where}")
                    if unlocked:
                        st.success("✨ Unlocked")
                    else:
                        st.warning(f"🔒 {req} XP needed")


# ============================================================
# SESSION STATE & GLOBAL VARIABLES
# ============================================================

if "current_mood" not in st.session_state:
    st.session_state.current_mood = "Happy"

mood_data = load_mood_data()
global_streak = compute_streak(mood_data)


# ============================================================
# CUSTOM CSS
# ============================================================

render_html(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
        radial-gradient(
            circle at top left,
            rgba(219, 234, 254, 0.7),
            transparent 32%
        ),
        linear-gradient(
            135deg,
            #f8fbff,
            #eef6ff
        );
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #172554 0%,
            #1e293b 100%
        );
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] * {
        color: #0f172a !important;
    }

    .main-title {
        font-size: 38px;
        font-weight: 800;
        color: #172554;
        margin-bottom: 4px;
    }

    .subtitle {
        color: #64748b;
        font-size: 16px;
        margin-bottom: 22px;
    }

    .kpi {
        background: white;
        border-radius: 20px;
        padding: 22px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 8px 25px rgba(15, 23, 42, 0.07);
        min-height: 105px;
    }

    .kpi-label {
        color: #64748b;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 6px;
    }

    .kpi-value {
        color: #172554;
        font-size: 24px;
        font-weight: 800;
    }

    .mood-card {
        background: linear-gradient(
            135deg,
            #172033,
            #273449,
            #334155
        );
        border-radius: 24px;
        padding: 30px;
        text-align: center;
        color: white;
        border: 1px solid #475569;
        box-shadow: 0 15px 40px rgba(15, 23, 42, 0.20);
    }

    .mood-card h2 {
        color: white !important;
        font-size: 28px;
        font-weight: 800;
        margin: 8px 0;
    }

    .mood-card p {
        color: #e2e8f0 !important;
        font-size: 16px;
        margin: 0;
    }

    .big-mood {
        font-size: 65px;
        line-height: 1;
    }

    .activity-box {
        background: white;
        border-radius: 22px;
        padding: 24px;
        border: 1px solid #dbeafe;
        box-shadow: 0 8px 25px rgba(15, 23, 42, 0.07);
        margin-bottom: 18px;
    }

    .activity-box h2 {
        color: #172554;
        margin-bottom: 8px;
    }

    .activity-box p {
        color: #64748b;
    }

    .footer {
        text-align: center;
        padding: 35px 0 10px;
        color: #94a3b8;
        font-size: 13px;
    }

    .stButton > button {
        border-radius: 12px;
        font-weight: 700;
        min-height: 45px;
    }

    .quote-card {
        background: linear-gradient(135deg, #4338ca, #6d28d9);
        border-radius: 22px;
        padding: 26px;
        color: white;
        box-shadow: 0 12px 30px rgba(67, 56, 202, 0.25);
    }

    .insight {
        background: white;
        border-left: 5px solid #6366f1;
        border-radius: 12px;
        padding: 12px 18px;
        margin-bottom: 8px;
        color: #1e293b;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
    }
    </style>
    """
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    render_html(
        """
        <div style="text-align:center; padding:15px 0 10px;">
            <div style="font-size:50px;">🧠</div>
            <h1 style="color:white; margin:0; font-size:26px;">MindMate</h1>
            <p style="color:#cbd5e1; font-size:13px;">
                Your mental wellness & arcade companion
            </p>
        </div>
        """
    )

    # XP & Level Display
    xp = get_user_xp()
    lvl_title, lvl_color, next_xp = get_level_info(xp)
    pct_lvl = min(100, int((xp / next_xp) * 100)) if next_xp > 0 else 100
    render_html(
        f"""
        <div style="background:rgba(255,255,255,0.08); border-radius:16px; padding:12px 16px; margin-bottom:12px; border:1px solid rgba(255,255,255,0.12);">
            <div style="display:flex; justify-content:space-between; align-items:center; font-size:13px; font-weight:700;">
                <span style="color:{lvl_color};">{lvl_title}</span>
                <span style="color:#fde047;">✨ {xp} XP</span>
            </div>
            <div style="background:rgba(255,255,255,0.15); border-radius:8px; height:6px; margin-top:8px; overflow:hidden;">
                <div style="width:{pct_lvl}%; height:100%; background:linear-gradient(90deg, #38bdf8, {lvl_color});"></div>
            </div>
            <div style="font-size:11px; color:#94a3b8; text-align:right; margin-top:4px;">{xp}/{next_xp} XP to Next Rank</div>
        </div>
        """
    )

    dev_unlocked = st.toggle("🔓 Unlock All Features (Sandbox)", value=st.session_state.get("dev_unlock_all", False), key="sidebar_dev_toggle")
    st.session_state.dev_unlock_all = dev_unlocked

    st.markdown("---")

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "💭 Mood Analysis",
            "📸 Face Mood Scan",
            "🎮 MindMate Arcade & Games",
            "🎧 Ambient Sound Lounge",
            "🧘 Calm Toolkit",
            "🏆 Achievements & XP",
            "📊 Analytics",
            "📔 Journal",
            "✅ Habits",
            "🆘 Support & Settings"
        ]
    )

    st.markdown("---")

    st.markdown("### 💙 Current Mood")

    selected_mood = st.selectbox(
        "How are you feeling?",
        list(MOODS.keys()),
        index=list(MOODS.keys()).index(st.session_state.current_mood),
        format_func=lambda m: f"{MOODS[m]['emoji']} {m}"
    )

    st.session_state.current_mood = selected_mood

    st.markdown("---")

    render_html(
        f"""
        <div style="text-align:center;">
            <div style="font-size:28px;">🔥 {global_streak}</div>
            <div style="font-size:13px; color:#cbd5e1;">
                day check-in streak
            </div>
        </div>
        """
    )


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    mood = st.session_state.current_mood
    info = MOODS[mood]

    render_html(f'<div class="main-title">{greeting()} 💙</div>')
    render_html('<div class="subtitle">Welcome to your personal MindMate wellness space & arcade.</div>')

    # ---- KPI row ----
    week_ago = pd.Timestamp(date.today() - timedelta(days=6))
    last7 = mood_data[mood_data["Day"] >= week_ago]
    avg7 = f"{last7['Score'].mean():.1f} / 5" if not last7.empty else "—"
    today_count = int((mood_data["Day"].dt.date == date.today()).sum())

    col1, col2, col3, col4 = st.columns(4)

    kpis = [
        (col1, "Current Mood", f"{info['emoji']} {mood}"),
        (col2, "Check-in Streak", f"🔥 {global_streak} day{'s' if global_streak != 1 else ''}"),
        (col3, "7-Day Mood Score", f"💚 {avg7}"),
        (col4, "Wellness Level", f"{lvl_title}"),
    ]

    for col, label, value in kpis:
        with col:
            render_html(
                f"""
                <div class="kpi">
                    <div class="kpi-label">{label}</div>
                    <div class="kpi-value" style="font-size:20px;">
                        {value}
                    </div>
                </div>
                """
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- Row with Mood Card & Virtual Pet Mochi ----
    left_m, right_m = st.columns([3, 2])

    with left_m:
        render_html(
            f"""
            <div class="mood-card">
                <div class="big-mood">{info["emoji"]}</div>
                <h2>{mood}</h2>
                <p>{info["description"]}</p>
            </div>
            """
        )

    with right_m:
        # Virtual Pet Widget
        render_html(get_virtual_pet_widget(mood))

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- Support note (heavy moods) + Recommended games for this mood ----
    render_support_note(mood)
    render_recommended_games(mood)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- Quick Check-in & Fortune Cookie ----
    c_check, c_fortune = st.columns([3, 2])

    with c_check:
        st.markdown("#### ⚡ Quick Check-in")
        intensity = st.slider(
            f"How strongly are you feeling {mood.lower()}?",
            1, 5, 3,
            key="dash_intensity"
        )
        note = st.text_input(
            "Optional note",
            placeholder="What's behind this feeling?",
            key="dash_note"
        )
        if st.button("📌 Log this mood (+30 XP)", use_container_width=True, key="dash_log"):
            save_entry(mood, note, intensity)
            add_xp(30, "Mood Check-in")
            st.toast(f"Logged {info['emoji']} {mood}. Thanks for checking in!", icon="💙")
            st.rerun()

        if today_count:
            st.caption(f"You've checked in {today_count}x today.")

    with c_fortune:
        st.markdown("#### 🥠 Daily Fortune Cookie")
        components.html(get_fortune_cookie_widget(), height=230)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- Daily Spin Wheel ----
    with st.expander("🎡 Daily Positivity Spin Wheel (Click to open)", expanded=False):
        components.html(get_spin_wheel_widget(), height=490)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- Quote of the day + 7 day trend ----
    q_col, t_col = st.columns([2, 3])

    with q_col:
        quote, author = QUOTES[date.today().toordinal() % len(QUOTES)]
        render_html(
            f"""
            <div class="quote-card">
                <div style="font-size:13px; font-weight:700; opacity:.8;">
                    ✨ QUOTE OF THE DAY
                </div>
                <div style="font-size:18px; font-weight:600; margin:10px 0;">
                    “{quote}”
                </div>
                <div style="font-size:13px; opacity:.85;">— {author}</div>
            </div>
            """
        )

    with t_col:
        st.markdown("#### 📈 Your Last 7 Days")
        daily = daily_average(last7)
        if daily.empty:
            st.info("Log a few moods and your weekly trend will appear here.")
        else:
            idx = pd.date_range(week_ago, periods=7)
            trend = daily.reindex(idx)
            trend.index = [d.strftime("%a %d") for d in idx]
            st.line_chart(trend, height=200)


# ============================================================
# MOOD ANALYSIS
# ============================================================

elif page == "💭 Mood Analysis":

    render_html('<div class="main-title">Mood Analysis 💭</div>')
    render_html('<div class="subtitle">Deep emotional insights and science-backed recommendations.</div>')

    mood = st.selectbox(
        "How are you feeling right now?",
        list(MOODS.keys()),
        index=list(MOODS.keys()).index(st.session_state.current_mood),
        format_func=lambda m: f"{MOODS[m]['emoji']} {m}",
        key="analysis_mood_select"
    )

    st.session_state.current_mood = mood
    info = MOODS[mood]

    render_html(
        f"""
        <div class="mood-card">
            <div class="big-mood">{info["emoji"]}</div>
            <h2>{mood}</h2>
            <p>{info["description"]}</p>
        </div>
        """
    )

    st.markdown("<br>", unsafe_allow_html=True)
    render_support_note(mood)
    st.markdown("### 🌱 Small things you can do right now")

    suggestions = {
        "Happy": [
            "Share your positive energy with someone.",
            "Listen to your favourite song in Ambient Sound Lounge.",
            "Write down something you are grateful for."
        ],
        "Sad": [
            "Talk to someone you trust.",
            "Pop bubbles in the Arcade or try Heart Catch.",
            "Write down what you are feeling in the Journal."
        ],
        "Angry": [
            "Take slow deep breaths in Calm Toolkit.",
            "Play Stress Smash in the Arcade to safely release tension.",
            "Step away from screens for 5 minutes."
        ],
        "Stressed": [
            "Try Guided Box Breathing in Calm Toolkit.",
            "Watch swimming fish in Zen Koi Pond.",
            "Listen to gentle rain in Ambient Sound Lounge."
        ],
        "Neutral": [
            "Try something creative in Cosmic Zen Particles.",
            "Play Mood Memory Matrix card matching.",
            "Spend some quiet time reflecting."
        ]
    }

    tips = suggestions.get(mood) or MOOD_TIPS.get(mood, [info["description"]])
    for suggestion in tips:
        st.info("🌿 " + suggestion)

    st.markdown("<br>", unsafe_allow_html=True)
    render_recommended_games(mood)


# ============================================================
# FACE MOOD SCAN & REAL-TIME ANALYSIS
# ============================================================

elif page == "📸 Face Mood Scan":

    render_face_page(MOODS, save_entry, render_html, add_xp=add_xp)


# ============================================================
# MINDMATE ARCADE & WELLNESS GAMES
# ============================================================

elif page == "🎮 MindMate Arcade & Games":

    render_html('<div class="main-title">MindMate Games & Arcade 🎮</div>')
    render_html('<div class="subtitle">17+ interactive games, stress-relief toys, art therapy & visual sandboxes. Earn XP to unlock higher tiers!</div>')

    # Mood-based recommendation at the top of the Arcade
    render_recommended_games(st.session_state.current_mood)
    st.markdown("<br>", unsafe_allow_html=True)

    cat_tabs = st.tabs([
        "🫧 Pop & Tactile (0 XP)",
        "🧠 Focus & Arcade (100-400 XP)",
        "🎨 Art & Music Sanctuary (250-600 XP)",
        "🌿 Nature & Zen Sandboxes (150-1200 XP)",
        "🔮 Mystic & Guidance Lounge (0-800 XP)"
    ])

    # Shared Mini-Game HTML Snippets
    balloon_game = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    * { box-sizing: border-box; }
    body { margin: 0; overflow: hidden; background: linear-gradient(135deg, #dbeafe, #eff6ff, #fdf2f8); }
    #game { height: 620px; position: relative; overflow: hidden; border-radius: 25px; }
    #score { position: absolute; top: 20px; left: 20px; z-index: 100; background: rgba(255,255,255,0.95); color: #172554; padding: 12px 20px; border-radius: 30px; font-size: 18px; font-weight: bold; }
    .balloon { position: absolute; border-radius: 50% 50% 48% 48%; cursor: pointer; animation: floatUp linear forwards; }
    @keyframes floatUp { from { transform: translateY(0); } to { transform: translateY(-800px); } }
    </style>
    </head>
    <body>
    <div id="game"><div id="score">🎈 Popped: <span id="count">0</span></div></div>
    <script>
    const game = document.getElementById("game");
    const count = document.getElementById("count");
    let score = 0;
    const colors = ["#ff6b81","#ff9f43","#ffd32a","#1dd1a1","#54a0ff","#5f27cd","#ff6bcb"];
    function createBalloon() {
        const b = document.createElement("div");
        b.className = "balloon";
        b.style.background = colors[Math.floor(Math.random() * colors.length)];
        const size = 50 + Math.random() * 30;
        b.style.width = size + "px";
        b.style.height = size * 1.25 + "px";
        b.style.left = Math.random() * 90 + "%";
        b.style.bottom = "-20px";
        const dur = 6 + Math.random() * 4;
        b.style.animationDuration = dur + "s";
        b.onclick = () => { score++; count.textContent = score; b.remove(); };
        game.appendChild(b);
        setTimeout(() => { if (b.parentNode) b.remove(); }, dur * 1000);
    }
    setInterval(createBalloon, 800);
    </script>
    </body>
    </html>
    """

    heart_game = """
    <!DOCTYPE html>
    <html>
    <style>
    body { margin: 0; overflow: hidden; background: linear-gradient(135deg, #dbeafe, #fdf4ff); }
    #game { height: 620px; position: relative; overflow: hidden; border-radius: 25px; }
    #score { position: absolute; top: 20px; left: 20px; background: white; padding: 12px 20px; border-radius: 25px; font-weight: bold; }
    .heart { position: absolute; font-size: 48px; cursor: pointer; user-select: none; animation: fall linear forwards; }
    @keyframes fall { from { transform: translateY(-80px); } to { transform: translateY(700px); } }
    </style>
    <div id="game"><div id="score">💙 Hearts: <span id="count">0</span></div></div>
    <script>
    const game = document.getElementById("game");
    const count = document.getElementById("count");
    let score = 0;
    const hearts = ["💙","💗","💜","💖","💛"];
    function createHeart() {
        const h = document.createElement("div");
        h.className = "heart";
        h.innerHTML = hearts[Math.floor(Math.random() * hearts.length)];
        h.style.left = Math.random() * 90 + "%";
        const dur = 5 + Math.random() * 3;
        h.style.animationDuration = dur + "s";
        h.onclick = () => { score++; count.textContent = score; h.remove(); };
        game.appendChild(h);
        setTimeout(() => { if (h.parentNode) h.remove(); }, dur * 1000);
    }
    setInterval(createHeart, 800);
    </script>
    </html>
    """

    smash_game = """
    <!DOCTYPE html>
    <html>
    <style>
    body { margin: 0; overflow: hidden; background: linear-gradient(135deg, #fee2e2, #fff1f2); }
    #game { height: 620px; position: relative; overflow: hidden; border-radius: 25px; }
    #score { position: absolute; top: 20px; left: 20px; background: white; padding: 12px 20px; border-radius: 25px; font-weight: bold; }
    .object { position: absolute; font-size: 60px; cursor: pointer; user-select: none; }
    </style>
    <div id="game"><div id="score">💥 Smashed: <span id="count">0</span></div></div>
    <script>
    const game = document.getElementById("game");
    const count = document.getElementById("count");
    let score = 0;
    const objects = ["💢","🟥","🎯","💥","🪨","📦"];
    function createObject() {
        const obj = document.createElement("div");
        obj.className = "object";
        obj.innerHTML = objects[Math.floor(Math.random() * objects.length)];
        obj.style.left = Math.random() * 88 + "%";
        obj.style.top = 15 + Math.random() * 70 + "%";
        obj.onclick = () => { score++; count.textContent = score; obj.remove(); };
        game.appendChild(obj);
        setTimeout(() => { if (obj.parentNode) obj.remove(); }, 3500);
    }
    setInterval(createObject, 900);
    </script>
    </html>
    """

    # --- CATEGORY 1: POP & TACTILE ---
    with cat_tabs[0]:
        t1, t2, t3, t4 = st.tabs(["🫧 Infinite Bubble Wrap", "🎈 Balloon Pop", "💙 Heart Catch", "💥 Stress Smash"])
        with t1:
            render_game_tab(
                "Infinite ASMR Bubble Wrap Popper", "🫧", 0,
                "Click, pop, and drag shiny 3D bubbles with Web Audio synth pops and combo multipliers.",
                get_bubble_wrap_game(), height=690, game_key="pop_bubble"
            )
        with t2:
            render_game_tab(
                "Floating Balloon Pop", "🎈", 0,
                "Pop floating colorful balloons and release uplifting positive energy.",
                balloon_game, height=640, game_key="pop_balloon"
            )
        with t3:
            render_game_tab(
                "Heart Catch", "💙", 0,
                "Catch falling warm hearts and collect soothing feelings.",
                heart_game, height=640, game_key="pop_heart"
            )
        with t4:
            render_game_tab(
                "Stress Smash", "💥", 0,
                "Click and smash stress obstacles to release tension instantly.",
                smash_game, height=640, game_key="pop_smash"
            )

    # --- CATEGORY 2: FOCUS & ARCADE ---
    with cat_tabs[1]:
        f1, f2, f3, f4 = st.tabs(["🧠 Memory Matrix (100 XP)", "🧱 Zen Brick Breaker (300 XP)", "🐍 Zen Glow Snake (350 XP)", "🎯 Lotus Target Darts (400 XP)"])
        with f1:
            render_game_tab(
                "Mood Memory Matrix", "🧠", 100,
                "Flip and match pairs of 3D mood cards. Sharpens focus, memory, and calm concentration.",
                get_memory_matrix_game(), height=690, game_key="focus_memory"
            )
        with f2:
            render_game_tab(
                "Endless Zen Brick Breaker", "🧱", 300,
                "Bounce glowing balls, smash bricks with harmonic chimes, and enjoy auto-cascade respawns!",
                get_brick_breaker_game(), height=640, game_key="focus_brick"
            )
        with f3:
            render_game_tab(
                "Zen Glow Snake", "🐍", 350,
                "Endless screen-wrapping glowing neon snake. Eat joy orbs with zero game-over stress!",
                get_glow_snake_game(), height=640, game_key="focus_snake"
            )
        with f4:
            render_game_tab(
                "Zen Lotus Target Darts", "🎯", 400,
                "Aim and throw glowing darts at the serene floating Lotus blossom target with bell sound effects.",
                get_zen_darts_game(), height=640, game_key="focus_darts"
            )

    # --- CATEGORY 3: ART & MUSIC SANCTUARY ---
    with cat_tabs[2]:
        a1, a2, a3 = st.tabs(["🎨 Mandala Painter (250 XP)", "🎹 Zen Chime Piano (500 XP)", "🎵 Rhythm Harmony (600 XP)"])
        with a1:
            render_game_tab(
                "Zen Kaleidoscope Mandala Painter", "🎨", 250,
                "Draw 8-fold symmetrical glowing sacred geometry with rainbow neon brushes. Deeply satisfying art therapy.",
                get_mandala_painter(), height=640, game_key="art_mandala"
            )
        with a2:
            render_game_tab(
                "Zen Mood Chime Piano", "🎹", 500,
                "Resonant harmonic bell chime piano. Tuned in pentatonic harmony so everything you play sounds magical.",
                get_zen_piano(), height=540, game_key="art_piano"
            )
        with a3:
            render_game_tab(
                "Rhythm Harmony Notes", "🎵", 600,
                "4-lane falling note musical rhythm catcher. Tap D-F-J-K to create melodic ambient chords.",
                get_rhythm_harmony_game(), height=640, game_key="art_rhythm"
            )

    # --- CATEGORY 4: NATURE & ZEN SANDBOXES ---
    with cat_tabs[3]:
        n1, n2, n3, n4 = st.tabs(["🌸 Zen Koi Pond (150 XP)", "🪨 Japanese Sand Garden (200 XP)", "🌌 Cosmic Particles (1000 XP)", "🎆 Midnight Fireworks (1200 XP)"])
        with n1:
            render_game_tab(
                "Zen Koi Ripple Pond", "🌸", 150,
                "Touch or click anywhere to generate water ripples and feed graceful swimming Koi fish.",
                get_koi_pond_game(), height=640, game_key="nat_koi"
            )
        with n2:
            render_game_tab(
                "Japanese Zen Sand Garden", "🪨", 200,
                "Rake soothing sand ripples, place smooth river stones & sakura blossom petals.",
                get_zen_sand_garden(), height=640, game_key="nat_sand"
            )
        with n3:
            render_game_tab(
                "Cosmic Zen Particles", "🌌", 1000,
                "Interactive galaxy particle sandbox. Move your cursor to create cosmic gravity swirls and burst neon shockwaves.",
                get_cosmic_particles_game(), height=640, game_key="nat_cosmic"
            )
        with n4:
            render_game_tab(
                "Midnight Zen Fireworks", "🎆", 1200,
                "Click the starry midnight sky to launch sparkling celebration bursts with synth echoes.",
                get_fireworks_zen(), height=640, game_key="nat_fireworks"
            )

    # --- CATEGORY 5: MYSTIC & GUIDANCE LOUNGE ---
    with cat_tabs[4]:
        m1, m2, m3, m4 = st.tabs(["🔮 Cosmic Oracle (700 XP)", "🃏 3-Card Tarot (800 XP)", "🎡 Daily Spin Wheel (0 XP)", "🥠 Fortune Cookie (0 XP)"])
        with m1:
            render_game_tab(
                "Mystic Cosmic Oracle", "🔮", 700,
                "Gaze into the glowing 3D crystal sphere and receive cosmic guidance for peace and clarity.",
                get_crystal_ball_oracle(), height=560, game_key="mys_oracle"
            )
        with m2:
            render_game_tab(
                "Mystic Mind & Soul Tarot", "🃏", 800,
                "Flip 3 sacred tarot cards to unveil spiritual wisdom for your Mind, Heart, and Spirit.",
                get_mood_tarot_widget(), height=640, game_key="mys_tarot"
            )
        with m3:
            render_game_tab(
                "Daily Positivity Spin Wheel", "🎡", 0,
                "Spin the glowing positivity wheel for your daily wellness boost and XP rewards!",
                get_spin_wheel_widget(), height=540, game_key="mys_wheel"
            )
        with m4:
            render_game_tab(
                "Golden Fortune Cookie", "🥠", 0,
                "Crack open today's crispy golden cookie for inspirational guidance.",
                get_fortune_cookie_widget(), height=320, game_key="mys_cookie"
            )


# ============================================================
# AMBIENT SOUND LOUNGE
# ============================================================

elif page == "🎧 Ambient Sound Lounge":

    render_html('<div class="main-title">Ambient Sound Lounge 🎧</div>')
    render_html('<div class="subtitle">Multi-track environmental sound generator. Mix Rain, Campfire, Waves, and Lo-Fi chords.</div>')

    components.html(get_ambient_sound_mixer(), height=420)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🎵 Peaceful Melodies")
    music_choice = st.selectbox(
        "Select a background soundtrack",
        [
            "Kho Gaye Hum Kahan — Anuv Jain",
            "Soft Instrumental Piano",
            "Lo-fi Cozy Bedroom Chill",
            "Rain & Acoustic Guitar",
            "Deep Sleep Meditation 432Hz"
        ]
    )
    st.success(f"🎵 Selected: {music_choice}. Enjoy with your favorite headphones!")


# ============================================================
# ACHIEVEMENTS & LEVEL PROGRESSION
# ============================================================

elif page == "🏆 Achievements & XP":

    render_html('<div class="main-title">Wellness Achievements & XP 🏆</div>')
    render_html('<div class="subtitle">Level up your mind, complete daily quests, unlock games, and earn achievement badges!</div>')

    xp = get_user_xp()
    lvl_title, lvl_color, next_xp = get_level_info(xp)

    c1, c2, c3 = st.columns(3)
    c1.metric("Current Wellness Rank", lvl_title)
    c2.metric("Total Experience", f"✨ {xp} XP")
    c3.metric("Next Level Target", f"{next_xp} XP")

    progress = min(1.0, max(0.0, xp / next_xp)) if next_xp > 0 else 1.0
    st.progress(progress)
    st.caption(f"Progress to next wellness rank: {xp} / {next_xp} XP ({int(progress * 100)}%)")

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- Daily Quests Board ----
    st.markdown("### 📋 Daily Wellness Quests")
    q_col1, q_col2, q_col3 = st.columns(3)

    with q_col1:
        render_html(
            """
            <div style="background:white; border-radius:18px; padding:18px; border:1px solid #e2e8f0; margin-bottom:12px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-weight:700; color:#1e293b;">📸 Scan Face Mood</div>
                        <div style="font-size:12px; color:#64748b;">Read live facial expressions</div>
                    </div>
                    <span style="font-weight:800; color:#3b82f6;">+30 XP</span>
                </div>
            </div>
            """
        )
        if st.button("✨ Claim +30 XP (Face Scan)", key="q_face", use_container_width=True):
            add_xp(30, "Face Scan Quest")
            st.rerun()

        render_html(
            """
            <div style="background:white; border-radius:18px; padding:18px; border:1px solid #e2e8f0; margin-bottom:12px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-weight:700; color:#1e293b;">🫧 Pop 30 Bubbles</div>
                        <div style="font-size:12px; color:#64748b;">Relieve tension in Popper</div>
                    </div>
                    <span style="font-weight:800; color:#3b82f6;">+25 XP</span>
                </div>
            </div>
            """
        )
        if st.button("✨ Claim +25 XP (Bubble Popper)", key="q_bubble", use_container_width=True):
            add_xp(25, "Bubble Popper Quest")
            st.rerun()

    with q_col2:
        render_html(
            """
            <div style="background:white; border-radius:18px; padding:18px; border:1px solid #e2e8f0; margin-bottom:12px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-weight:700; color:#1e293b;">🎨 Draw a Zen Mandala</div>
                        <div style="font-size:12px; color:#64748b;">Calming sacred geometry</div>
                    </div>
                    <span style="font-weight:800; color:#3b82f6;">+25 XP</span>
                </div>
            </div>
            """
        )
        if st.button("✨ Claim +25 XP (Mandala)", key="q_mandala", use_container_width=True):
            add_xp(25, "Mandala Quest")
            st.rerun()

        render_html(
            """
            <div style="background:white; border-radius:18px; padding:18px; border:1px solid #e2e8f0; margin-bottom:12px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-weight:700; color:#1e293b;">🥠 Crack Fortune Cookie</div>
                        <div style="font-size:12px; color:#64748b;">Open today's gold fortune</div>
                    </div>
                    <span style="font-weight:800; color:#3b82f6;">+15 XP</span>
                </div>
            </div>
            """
        )
        if st.button("✨ Claim +15 XP (Fortune Cookie)", key="q_cookie", use_container_width=True):
            add_xp(15, "Fortune Cookie Quest")
            st.rerun()

    with q_col3:
        render_html(
            """
            <div style="background:white; border-radius:18px; padding:18px; border:1px solid #e2e8f0; margin-bottom:12px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-weight:700; color:#1e293b;">🎯 Shoot Lotus Target</div>
                        <div style="font-size:12px; color:#64748b;">Hit a bullseye in Zen Darts</div>
                    </div>
                    <span style="font-weight:800; color:#3b82f6;">+25 XP</span>
                </div>
            </div>
            """
        )
        if st.button("✨ Claim +25 XP (Zen Darts)", key="q_darts", use_container_width=True):
            add_xp(25, "Zen Darts Quest")
            st.rerun()

        render_html(
            """
            <div style="background:white; border-radius:18px; padding:18px; border:1px solid #e2e8f0; margin-bottom:12px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-weight:700; color:#1e293b;">🪨 Rake Sand Garden</div>
                        <div style="font-size:12px; color:#64748b;">Draw peaceful grooves</div>
                    </div>
                    <span style="font-weight:800; color:#3b82f6;">+20 XP</span>
                </div>
            </div>
            """
        )
        if st.button("✨ Claim +20 XP (Sand Garden)", key="q_sand", use_container_width=True):
            add_xp(20, "Sand Garden Quest")
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🏅 Achievement Badges")

    badges = [
        ("🌱 Zen Novice", "Begin your wellness journey", True, "🌱", 0),
        ("📸 Face Scan Pioneer", "Scan mood with live camera", st.session_state.get("face_scanned", False) or xp >= 50, "🌟", 50),
        ("🫧 Master Popper", "Pop 30+ bubbles in Arcade", xp >= 60, "🫧", 60),
        ("🧠 Memory Maestro", "Unlock Mood Memory Matrix", xp >= 100, "🧠", 100),
        ("🌸 Koi Whisperer", "Unlock & feed the Zen Koi Fish", xp >= 150, "🌸", 150),
        ("🪨 Sand Master", "Rake Japanese Zen Sand Garden", xp >= 200, "🪨", 200),
        ("🎨 Mandala Artist", "Unlock Zen Kaleidoscope Painter", xp >= 250, "🎨", 250),
        ("🧱 Brick Smasher", "Reach 300 XP & play Brick Breaker", xp >= 300, "🧱", 300),
        ("🐍 Glow Snake Champion", "Unlock Zen Glow Snake", xp >= 350, "🐍", 350),
        ("🎯 Lotus Archer", "Unlock Zen Target Darts", xp >= 400, "🎯", 400),
        ("🎹 Chime Virtuoso", "Reach Calm Master (500 XP)", xp >= 500, "🎹", 500),
        ("🎵 Harmony Master", "Play Rhythm Harmony Notes", xp >= 600, "🎵", 600),
        ("🔮 Mystic Oracle", "Unlock Cosmic Crystal Ball", xp >= 700, "🔮", 700),
        ("🃏 Tarot Sage", "Unlock 3-Card Mystic Tarot", xp >= 800, "🃏", 800),
        ("🌌 Cosmic Zen Guru", "Reach 1000 XP Galaxy Tier", xp >= 1000, "🌌", 1000),
        ("🎆 Starlight Celebrator", "Unlock Midnight Fireworks", xp >= 1200, "🎆", 1200),
    ]

    b_cols = st.columns(4)
    for i, (title, desc, unlocked, icon, req) in enumerate(badges):
        with b_cols[i % 4]:
            opacity = "1" if unlocked else "0.45"
            badge_bg = "linear-gradient(135deg,#1e1b4b,#312e81)" if unlocked else "#1e293b"
            status_text = "✅ UNLOCKED" if unlocked else f"🔒 Needs {req} XP"
            status_color = "#4ade80" if unlocked else "#fde047"
            render_html(
                f"""
                <div style="background:{badge_bg}; border-radius:20px; padding:18px; color:white;
                            border:1px solid rgba(255,255,255,0.15); margin-bottom:15px; opacity:{opacity}; min-height:165px; display:flex; flex-direction:column; justify-content:space-between;">
                    <div>
                        <div style="font-size:36px;">{icon}</div>
                        <div style="font-weight:700; font-size:15px; margin:6px 0 2px;">{title}</div>
                        <div style="font-size:12px; color:#cbd5e1; margin-bottom:8px;">{desc}</div>
                    </div>
                    <div>
                        <span style="font-size:11px; font-weight:800; background:rgba(255,255,255,0.15); color:{status_color}; padding:3px 8px; border-radius:10px;">
                            {status_text}
                        </span>
                    </div>
                </div>
                """
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- Level Roadmap Section ----
    st.markdown("### 🗺️ Full Feature Unlock Roadmap")
    roadmap = [
        ("🌱 Level 1: Zen Novice (0 XP)", "🫧 Bubble Popper, 🎈 Balloon Pop, 💙 Heart Catch, 💥 Stress Smash, 🥠 Fortune Cookie, 🐾 Mochi Pet, 🎧 Sound Lounge"),
        ("🌿 Level 2: Mindful Seeker (100 - 200 XP)", "🧠 Mood Memory Matrix (100 XP), 🌸 Zen Koi Pond (150 XP), 🪨 Japanese Zen Sand Garden (200 XP)"),
        ("🌸 Level 3: Harmony Explorer (250 - 400 XP)", "🎨 Zen Mandala Painter (250 XP), 🧱 Zen Brick Breaker (300 XP), 🐍 Zen Glow Snake (350 XP), 🎯 Lotus Target Darts (400 XP)"),
        ("🧘 Level 4: Calm Master (500 - 800 XP)", "🎹 Zen Chime Piano (500 XP), 🎵 Rhythm Harmony (600 XP), 🔮 Mystic Oracle (700 XP), 🃏 3-Card Tarot (800 XP)"),
        ("🌌 Level 5: Cosmic Zen Guru (1000+ XP)", "🌌 Cosmic Zen Particles (1000 XP), 🎆 Midnight Zen Fireworks (1200 XP), Master Zen Badges"),
    ]

    for title, rewards in roadmap:
        render_html(
            f"""
            <div class="insight" style="padding:16px 20px; margin-bottom:10px;">
                <div style="font-weight:800; color:#172554; font-size:15px;">{title}</div>
                <div style="font-size:13px; color:#475569; margin-top:4px;">✨ Unlocks: <b>{rewards}</b></div>
            </div>
            """
        )



# ============================================================
# CALM TOOLKIT
# ============================================================

elif page == "🧘 Calm Toolkit":

    render_html('<div class="main-title">Calm Toolkit 🧘</div>')
    render_html('<div class="subtitle">Quick, science-backed tools to reset in a couple of minutes.</div>')

    tab_breath, tab_ground, tab_grat, tab_aff = st.tabs(
        [
            "🌬️ Guided Breathing",
            "🌳 5-4-3-2-1 Grounding",
            "🙏 Gratitude",
            "💬 Affirmations"
        ]
    )

    with tab_breath:
        patterns = {
            "Box breathing (4-4-4-4)": (4, 4, 4, 4),
            "Relaxing 4-7-8": (4, 7, 8, 0),
            "Calm 5-5": (5, 0, 5, 0),
        }
        choice = st.selectbox("Choose a pattern", list(patterns.keys()))
        inhale, hold1, exhale, hold2 = patterns[choice]

        breathing_html = f"""
        <div style="display:flex; flex-direction:column; align-items:center;
                    justify-content:center; height:400px; font-family:Arial;
                    background:linear-gradient(135deg,#dbeafe,#eff6ff,#ede9fe);
                    border-radius:24px;">
            <div id="circle" style="width:130px; height:130px; border-radius:50%;
                 background:radial-gradient(circle at 30% 30%,#a5b4fc,#6366f1);
                 box-shadow:0 0 45px rgba(99,102,241,.45);
                 transition:transform 1s ease-in-out;"></div>
            <div id="label" style="margin-top:35px; font-size:26px;
                 font-weight:700; color:#172554;">Press start</div>
            <div id="count" style="font-size:18px; color:#475569; margin-top:6px;"></div>
            <button id="btn" style="margin-top:20px; padding:10px 28px;
                 border:none; border-radius:30px; background:#172554;
                 color:white; font-size:16px; font-weight:700; cursor:pointer;">
                ▶ Start
            </button>
        </div>
        <script>
        const phases = [
            ["Breathe in 🌬️", {inhale}, 1.8],
            ["Hold", {hold1}, 1.8],
            ["Breathe out 😌", {exhale}, 1.0],
            ["Hold", {hold2}, 1.0]
        ].filter(p => p[1] > 0);
        const circle = document.getElementById("circle");
        const label = document.getElementById("label");
        const count = document.getElementById("count");
        const btn = document.getElementById("btn");
        let running = false, timer = null, idx = 0, left = 0;

        function setPhase() {{
            const [name, secs, scale] = phases[idx];
            label.textContent = name;
            left = secs;
            count.textContent = left + "s";
            circle.style.transitionDuration = secs + "s";
            circle.style.transform = "scale(" + scale + ")";
        }}
        function tick() {{
            left -= 1;
            if (left <= 0) {{
                idx = (idx + 1) % phases.length;
                setPhase();
            }} else {{
                count.textContent = left + "s";
            }}
        }}
        btn.onclick = () => {{
            if (running) {{
                clearInterval(timer); running = false;
                btn.textContent = "▶ Start"; label.textContent = "Paused";
                circle.style.transform = "scale(1)";
            }} else {{
                running = true; idx = 0; btn.textContent = "⏸ Stop";
                setPhase(); timer = setInterval(tick, 1000);
            }}
        }};
        </script>
        """
        components.html(breathing_html, height=420)

    with tab_ground:
        st.markdown("Use your 5 senses to anchor yourself in the present:")
        steps = [
            ("👀 5 things you can SEE", 5),
            ("✋ 4 things you can TOUCH", 4),
            ("👂 3 things you can HEAR", 3),
            ("👃 2 things you can SMELL", 2),
            ("👅 1 thing you can TASTE", 1),
        ]
        total_done = 0
        total_items = sum(n for _, n in steps)
        for title, n in steps:
            with st.expander(title, expanded=False):
                for i in range(n):
                    if st.checkbox(f"#{i + 1}", key=f"ground_{title}_{i}"):
                        total_done += 1
        st.progress(total_done / total_items)
        if total_done == total_items:
            st.success("🌿 Wonderful! You are fully grounded and present.")
            st.balloons()

    with tab_grat:
        st.markdown("Name three things you're grateful for today:")
        g1 = st.text_input("1.", key="g1")
        g2 = st.text_input("2.", key="g2")
        g3 = st.text_input("3.", key="g3")
        if st.button("💾 Save to Journal (+25 XP)", key="save_gratitude"):
            items = [g for g in (g1, g2, g3) if g.strip()]
            if items:
                save_entry(st.session_state.current_mood, "Gratitude: " + "; ".join(items))
                add_xp(25, "Gratitude Exercise")
                st.success("🙏 Saved to journal!")

    with tab_aff:
        if "affirmation" not in st.session_state:
            st.session_state.affirmation = random.choice(AFFIRMATIONS)
        render_html(
            f"""
            <div class="quote-card" style="text-align:center; padding:45px 25px;">
                <div style="font-size:24px; font-weight:700;">
                    {st.session_state.affirmation}
                </div>
            </div>
            """
        )
        if st.button("🔄 Give me another"):
            st.session_state.affirmation = random.choice(AFFIRMATIONS)
            st.rerun()


# ============================================================
# ANALYTICS
# ============================================================

elif page == "📊 Analytics":

    render_html('<div class="main-title">Mood Analytics 📊</div>')
    render_html('<div class="subtitle">Explore patterns, emotional trends, and check-in history.</div>')

    if mood_data.empty:
        st.info("📊 No mood history recorded yet. Log a mood to get started.")
    else:
        range_choice = st.radio(
            "Time range",
            ["Last 7 days", "Last 30 days", "Last 90 days", "All time"],
            horizontal=True,
            index=3
        )
        days_map = {"Last 7 days": 7, "Last 30 days": 30, "Last 90 days": 90}
        if range_choice == "All time":
            df = mood_data.copy()
        else:
            cutoff = pd.Timestamp(date.today() - timedelta(days=days_map[range_choice] - 1))
            df = mood_data[mood_data["Day"] >= cutoff].copy()

        if df.empty:
            st.info("No entries in this time range yet.")
            st.stop()

        top_mood = df["Mood"].value_counts().idxmax()
        daily = daily_average(df)

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Entries", len(df))
        k2.metric("Days tracked", df["Day"].nunique())
        k3.metric("Average mood score", f"{df['Score'].mean():.2f} / 5")
        k4.metric("Most common", f"{MOODS[top_mood]['emoji']} {top_mood}")

        st.markdown("#### Mood distribution")
        counts = df["Mood"].value_counts()
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.bar(
            [f"{MOODS[m]['emoji']} {m}" for m in counts.index],
            counts.values,
            color=[MOODS[m]["chart"] for m in counts.index],
        )
        plt.xticks(rotation=45, ha="right")
        ax.set_ylabel("Entries")
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", alpha=0.2)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)


# ============================================================
# JOURNAL
# ============================================================

elif page == "📔 Journal":

    render_html('<div class="main-title">My Journal 📔</div>')
    render_html('<div class="subtitle">Your private sanctuary to reflect and express yourself freely.</div>')

    mood = st.session_state.current_mood

    def _save_journal():
        text = st.session_state.get("journal_text", "")
        if text.strip():
            save_entry(
                st.session_state.current_mood,
                text,
                st.session_state.get("journal_intensity", 3)
            )
            add_xp(40, "Journal Entry")
            st.session_state.journal_text = ""
            st.session_state.journal_flash = "ok"
        else:
            st.session_state.journal_flash = "empty"

    tab_write, tab_hist = st.tabs(["✍️ Write", "📚 Past entries"])

    with tab_write:
        render_html(
            f"""
            <div class="activity-box">
                <h2>{MOODS[mood]["emoji"]} Today's mood: {mood}</h2>
                <p>Write freely. Everything is saved securely on your device.</p>
            </div>
            """
        )
        flash = st.session_state.pop("journal_flash", None)
        if flash == "ok":
            st.success("💙 Saved to journal (+40 XP)!")
        elif flash == "empty":
            st.warning("Please write something before saving.")

        if "journal_prompt" not in st.session_state:
            st.session_state.journal_prompt = random.choice(JOURNAL_PROMPTS)

        p1, p2 = st.columns([5, 1])
        p1.info("💡 Prompt: " + st.session_state.journal_prompt)
        if p2.button("🎲 New prompt"):
            st.session_state.journal_prompt = random.choice(JOURNAL_PROMPTS)
            st.rerun()

        st.text_area(
            "Write your thoughts...",
            height=240,
            key="journal_text",
            placeholder="How was your day? What are you grateful for?"
        )
        st.button("💾 Save Journal Entry (+40 XP)", use_container_width=True, on_click=_save_journal)

    with tab_hist:
        entries = mood_data[mood_data["Journal"].str.strip() != ""].copy()
        if entries.empty:
            st.info("No journal entries yet. Your entries will appear here.")
        else:
            for _, row in entries.sort_values("Date", ascending=False).head(20).iterrows():
                m = MOODS.get(row["Mood"], MOODS["Neutral"])
                stamp_str = row['Date'].strftime('%d %b %Y, %H:%M') if hasattr(row['Date'], 'hour') else str(row['Date'])
                render_html(
                    f"""
                    <div class="activity-box" style="border-left:6px solid {m['chart']}; padding:16px 20px;">
                        <div style="font-size:13px; color:#64748b; font-weight:600;">
                            {stamp_str} &nbsp;·&nbsp; {m['emoji']} {row['Mood']}
                        </div>
                        <div style="margin-top:6px; color:#0f172a; white-space:pre-wrap;">{row['Journal']}</div>
                    </div>
                    """
                )


# ============================================================
# HABITS
# ============================================================

elif page == "✅ Habits":

    render_html('<div class="main-title">Daily Habits ✅</div>')
    render_html('<div class="subtitle">Small routines that quietly shape how you feel.</div>')

    habits_df = load_habits()
    today = date.today()
    today_rows = habits_df[habits_df["Date"].dt.date == today]
    done_today = set(today_rows[today_rows["Done"] == 1]["Habit"])

    st.markdown(f"### Today · {today.strftime('%A, %d %B')}")

    checked = set()
    cols = st.columns(2)
    for i, (label, key) in enumerate(HABITS.items()):
        with cols[i % 2]:
            if st.checkbox(label, value=key in done_today, key=f"habit_{key}"):
                checked.add(key)

    st.progress(len(checked) / len(HABITS))
    st.caption(f"{len(checked)} of {len(HABITS)} habits completed today")

    if st.button("💾 Save Today's Habits (+20 XP)", use_container_width=True):
        save_habits_for_day(today, checked)
        add_xp(20, "Daily Habits Saved")
        st.success("Habits saved! 🌱")


# ============================================================
# SUPPORT & SETTINGS
# ============================================================

elif page == "🆘 Support & Settings":

    render_html('<div class="main-title">Support & Settings 🆘</div>')
    render_html('<div class="subtitle">Help when you need it, and control over your own data.</div>')

    st.markdown("### 💙 If you need someone to talk to")
    render_html(
        """
        <div class="activity-box">
            <p><b>🇮🇳 India</b></p>
            <p>📞 <b>Tele-MANAS</b>: 14416 or 1-800-891-4416 (free, 24/7, many languages)</p>
            <p>📞 <b>iCall</b>: 9152987821 (Mon to Sat, counselling)</p>
            <p>🚨 <b>Emergency</b>: 112</p>
            <p>🌍 Outside India: <a href="https://findahelpline.com" target="_blank">findahelpline.com</a></p>
        </div>
        """
    )


# ============================================================
# FOOTER
# ============================================================

render_html(
    """
    <div class="footer">
        🧠 MindMate • Your mental wellness & entertainment companion
    </div>
    """
)
