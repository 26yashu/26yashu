"""
config.py
=========
Single source of truth for every constant used by the SVG / README
generator scripts. Nothing else in this repo should hard-code a name,
color, or path — everything is pulled from here so the profile can be
re-skinned by editing one file.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------

ROOT_DIR: Path = Path(__file__).resolve().parent
ASSETS_DIR: Path = ROOT_DIR / "assets"
SCRIPTS_DIR: Path = ROOT_DIR / "scripts"
README_PATH: Path = ROOT_DIR / "README.md"

ASSETS_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------------------------------
# Personal information
# --------------------------------------------------------------------------

NAME: str = "Gandlaparthi Yaswanthi"
GITHUB_USERNAME: str = "26yashu"
ROLE: str = "AI/ML Engineer • Software Developer"
SUBTITLE: str = "AI/ML Engineer • Software Developer"
EDUCATION: str = "B.Tech, Computer Science & Engineering (Artificial Intelligence & Machine Learning)"
CGPA: str = "9.10 / 10.0"
LOCATION: str = "India"
CURRENT_FOCUS: str = "Building production-grade AI systems & full-stack apps"

AVATAR_URL: str = f"https://github.com/{GITHUB_USERNAME}.png?size=200"
PROFILE_URL: str = f"https://github.com/{GITHUB_USERNAME}"
LINKEDIN_URL: str = "https://www.linkedin.com/in/gandlaparthi-yaswanthi-91b16a2a3"
EMAIL: str = "gyaswanthi467@gmail.com"


# --------------------------------------------------------------------------
# Color palette — "Deep Dark / Neon Glass" theme
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class Palette:
    bg: str = "#0d1117"
    bg_alt: str = "#0a0d12"
    panel: str = "#111722"
    border: str = "#1f2937"
    text: str = "#e6edf3"
    text_dim: str = "#8b949e"
    cyan: str = "#39d0ff"
    green: str = "#3ddc84"
    orange: str = "#ff9f43"
    purple: str = "#b06bff"
    white: str = "#ffffff"


PALETTE = Palette()

# Ordered accent cycle used for gradients / per-row coloring
ACCENTS: list[str] = [PALETTE.cyan, PALETTE.green, PALETTE.purple, PALETTE.orange]


# --------------------------------------------------------------------------
# Typography
# --------------------------------------------------------------------------

FONT_MONO: str = "'JetBrains Mono','Fira Code','SFMono-Regular',Consolas,monospace"
FONT_SANS: str = "'Segoe UI','Inter',Helvetica,Arial,sans-serif"


# --------------------------------------------------------------------------
# Tech stack (used both for badges and the info card)
# --------------------------------------------------------------------------

TECH_STACK: dict[str, list[str]] = {
    "Programming Languages": ["Python", "SQL", "Java", "JavaScript"],
    "AI / Machine Learning": [
        "TensorFlow", "PyTorch", "Scikit--learn", "Deep%20Learning",
        "NLP", "OpenCV", "FAISS",
    ],
    "Frameworks": ["Flask", "Streamlit", "FastAPI", "React", "Node.js", "Express", "Vite"],
    "Databases": ["MySQL", "SQLite", "MongoDB"],
    "Developer Tools": ["Git", "GitHub", "VS%20Code", "Jupyter", "Google%20Colab", "Tableau", "Excel"],
}

# shields.io logo slugs (best-effort mapping; falls back to plain badge)
SHIELD_LOGOS: dict[str, str] = {
    "Python": "python", "SQL": "mysql", "Java": "openjdk", "JavaScript": "javascript",
    "TensorFlow": "tensorflow", "PyTorch": "pytorch", "Scikit--learn": "scikitlearn",
    "OpenCV": "opencv", "FAISS": "meta",
    "Flask": "flask", "Streamlit": "streamlit", "FastAPI": "fastapi", "React": "react",
    "Node.js": "nodedotjs", "Express": "express", "Vite": "vite",
    "MySQL": "mysql", "SQLite": "sqlite", "MongoDB": "mongodb",
    "Git": "git", "GitHub": "github", "VS%20Code": "visualstudiocode",
    "Jupyter": "jupyter", "Google%20Colab": "googlecolab", "Tableau": "tableau", "Excel": "microsoftexcel",
}

BADGE_COLORS = {
    "Programming Languages": "39d0ff",
    "AI / Machine Learning": "3ddc84",
    "Frameworks": "b06bff",
    "Databases": "ff9f43",
    "Developer Tools": "8b949e",
}


# --------------------------------------------------------------------------
# Projects
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class Project:
    name: str
    description: str
    tech: list[str]
    features: list[str]
    status: str = "Active"
    repo: str = ""
    demo: str = ""


PROJECTS: list[Project] = [
    Project(
        name="Eco-Vision",
        description="AI-powered leaf disease detection system with offline mobile inference.",
        tech=["TensorFlow", "MobileNetV2", "TensorFlow Lite", "Python", "OpenCV"],
        features=["Disease Detection", "Offline Mobile Deployment", "Image Processing", "Deep Learning"],
    ),
    Project(
        name="RAFT",
        description="Real-time AI dashboard forecasting financial crashes and flood events.",
        tech=["PyTorch", "LSTM", "FAISS", "REST APIs", "Streamlit"],
        features=["Real-Time Forecasting", "Similarity Search", "API Integration", "Predictive Analytics"],
    ),
    Project(
        name="NyayVandan",
        description="AI-powered legal research assistant for case analysis and outcome prediction.",
        tech=["Python", "Flask", "Machine Learning", "NLP"],
        features=["Legal Case Analysis", "Outcome Prediction", "Intelligent Search", "AI Dashboard"],
    ),
    Project(
        name="Sable AI",
        description="AI-powered emotional wellness chatbot with mood analytics.",
        tech=["React", "Vite", "Node.js", "Express", "MongoDB"],
        features=["Emotion Detection", "Mood Analytics", "Personalized Conversations", "Wellness Dashboard"],
    ),
    Project(
        name="Sakhi AI",
        description="AI-powered women safety platform with real-time voice SOS.",
        tech=["Next.js", "Twilio", "Mapbox", "Web Speech API"],
        features=["Voice SOS", "Live GPS Sharing", "Smart Safety Routes", "Emergency Notifications"],
    ),
    Project(
        name="SquadPlay",
        description="Modern multiplayer quiz application with real-time battles.",
        tech=["React", "Vite", "JavaScript"],
        features=["Quiz Battle", "Rapid Fire", "Leaderboards", "Multiplayer", "Offline Support"],
    ),
]

ACHIEVEMENTS: list[str] = [
    "CGPA 9.10 / 10.0 in B.Tech CSE (AI & ML)",
    "Built 6+ production-style AI/full-stack projects",
    "Active open-source contributor",
]

CURRENTLY_LEARNING: list[str] = ["LLM Agents", "System Design", "Cloud (AWS/GCP)", "MLOps"]

SOCIAL_LINKS: dict[str, str] = {
    "GitHub": PROFILE_URL,
    "LinkedIn": LINKEDIN_URL,
    "Email": f"mailto:{EMAIL}",
}


# --------------------------------------------------------------------------
# SVG canvas sizes
# --------------------------------------------------------------------------

HEADER_WIDTH, HEADER_HEIGHT = 900, 220
TERMINAL_WIDTH, TERMINAL_HEIGHT = 560, 620
INFO_CARD_WIDTH, INFO_CARD_HEIGHT = 560, 620
CONTRIB_WIDTH, CONTRIB_HEIGHT = 828, 128
CARD_WIDTH, CARD_HEIGHT = 420, 210

# Contribution grid
CONTRIB_COLS = 53
CONTRIB_ROWS = 7
CONTRIB_CELL = 11
CONTRIB_GAP = 3
