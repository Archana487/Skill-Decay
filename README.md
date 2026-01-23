# 🧠 Neural Nexus | Skill Decay Tracker

Neural Nexus is a cognitive intelligence interface designed to track, predict, and combat **skill decay**. Using mathematical models (Exponential & Linear), it helps you maintain proficiency in complex subjects by suggesting timely interventions.

---

## 🚀 Quick Start

### 1. Launch the Application
- Double-click the **`run.bat`** file in the root directory.
- A terminal will open to start the backend, and after 3 seconds, your dashboard will open automatically at **[http://localhost:5000](http://localhost:5000)**.

### 2. Establish a New Skill Node
- Click the **`ESTABLISH_SYNAPSE`** button in the top right.
- Enter the skill name (e.g., "Python Architecture").
- Provide your **Confidence Index** (0-100) and your **Performance Metric** (e.g., last test score or self-assessment).

---

## 📊 Dashboard Intelligence

### 🧬 Signal Strength (Proficiency %)
This bar represents your current estimated proficiency. It drains automatically over time based on the **Decay Model**.
- **Green (>80%)**: Stable. You have high retention.
- **Cyan (60-80%)**: Drift. You are starting to lose nuance.
- **Red (<60%)**: Critical. Your risk of failure is high.

### ⚠️ Skill Debt & Failure Probability
- **Skill Debt**: A numerical representation of how much "relearning" you owe the system to return to an optimal level.
- **Fail Prob**: The likelihood (0-100%) that you will fail a real-world task involving this skill *today*.

---

## ⚡ Reinforcement Protocols

### Log Practice
Click the **Flash Icon (⚡)** on any skill card to log a practice session.
- Choose your **Activity Vector** (Project, Tutorial, Quiz, or Mentoring).
- Gaining practice points resets the decay timer and grants **XP**.

### Accelerate Decay (Testing)
Click the **Hourglass Icon (⏳)** to simulate 30 days of time passing instantly. This is useful to see how different skills degrade and when the system triggers alerts.

---

## 🛠️ Advanced Operation

### Suggested Interventions
The system automatically generates a list of **Micro-Tasks** on each card. These are tailored to your current proficiency:
- **Maintenance Dose**: Small tasks for stable skills.
- **Recovery Protocol**: Aggressive tasks for skills in the "Critical" zone.

### Gamification
- **XP & Levels**: Every practice session increases your level.
- **Streaks**: Practice daily to maintain your learning momentum.

---

> [!NOTE]
> All data is stored locally in `skills.db`. If you need to reset the entire system, simply delete this file and restart the application.
