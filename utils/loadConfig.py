# load_config.py

# === Known Inputs ===
USERS = 100
TARGET_TOTAL_RPS = 17.5  # ✅ NOT 175 — this is the actual RPS you want!
LAUNCH_API_COUNT = 3
MENU_API_PROBABILITY = 0.5  # Called 50% of the time

# === Derived
AVG_REQUESTS_PER_ITERATION = LAUNCH_API_COUNT + MENU_API_PROBABILITY  # 3 + 0.5 = 3.5
TARGET_RPS_PER_USER = TARGET_TOTAL_RPS / USERS  # 17.5 / 100 = 0.175