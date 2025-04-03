import requests
import re
import os
import json

# GitHub API setup
username = "ahmed-ishtiak-nihal"
token = os.getenv("GITHUB_TOKEN")
headers = {"Authorization": f"token {token}"}

# Fetch contribution data from GitHub API
query = """
query {
  user(login: "%s") {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
          }
        }
      }
    }
  }
}
""" % username

response = requests.post(
    "https://api.github.com/graphql",
    json={"query": query},
    headers=headers
)
data = response.json()

# Calculate current streak
weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
streak = 0
today = None
from datetime import datetime, timedelta

for week in reversed(weeks):
    for day in reversed(week["contributionDays"]):
        date = datetime.strptime(day["date"], "%Y-%m-%d")
        if today is None:
            today = date
        if date > today:
            continue
        if day["contributionCount"] > 0:
            streak += 1
        else:
            break
    if day["contributionCount"] == 0:
        break

# Define goal, progress, and achievement
goal = 30
progress = int((streak / goal) * 100)
if streak >= 20:
    achievement = "Gold Streak: 20 Days"
    rank = "Galactic Champion"
elif streak >= 10:
    achievement = "Silver Streak: 10 Days"
    rank = "Stellar Guardian"
elif streak >= 5:
    achievement = "Bronze Streak: 5 Days"
    rank = "Cosmic Defender"
else:
    achievement = "No Streak Yet"
    rank = "Space Cadet"

# Generate streak.json for the progress bar
streak_data = {"progress": streak}
with open("streak.json", "w") as f:
    json.dump(streak_data, f)

# Update README
with open("README.md", "r") as file:
    content = file.read()

# Replace the streak badge
new_streak_badge = f"https://img.shields.io/badge/Streak-{streak}%2F{goal}-7C4DFF?style=for-the-badge&logo=fire"
content = re.sub(r'https://img.shields.io/badge/Streak-\d+%2F\d+-7C4DFF\?style=for-the-badge&logo=fire', new_streak_badge, content)

# Replace the achievement badge
new_achievement_badge = f"https://img.shields.io/badge/{achievement.replace(' ', '%20')}-7C4DFF?style=for-the-badge&logo=trophy"
content = re.sub(r'https://img.shields.io/badge/[^-]*-7C4DFF\?style=for-the-badge&logo=trophy', new_achievement_badge, content)

# Replace the Galactic Rank badge
new_rank_badge = f"https://img.shields.io/badge/Galactic%20Rank-{rank.replace(' ', '%20')}-7C4DFF?style=for-the-badge&logo=rocket"
content = re.sub(r'https://img.shields.io/badge/Galactic%20Rank-[^-]*-7C4DFF\?style=for-the-badge&logo=rocket', new_rank_badge, content)

# Replace the text
new_text = f"**🌟 Current Streak: {streak} Days | Goal: {goal} Days 🌟**"
content = re.sub(r'\*\*🌟 Current Streak: \d+ Days \| Goal: \d+ Days 🌟\*\*', new_text, content)

with open("README.md", "w") as file:
    file.write(content)
