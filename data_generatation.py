# Mobile App Store - Sample Data Generator
# Generates the 6 tables from the case study (Users, Apps, Search, Click, Download, Revenue)
# Foreign keys stay consistent across tables (click points to a real search, etc.)

import csv
import random
from datetime import datetime, timedelta

# fixed seed so results are reproducible
random.seed(42)

# settings
N_USERS = 2000
N_APPS = 100
N_SEARCHES = 20000

START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2025, 6, 30)

COUNTRIES = ["Turkey", "Germany", "USA", "France", "Azerbaijan", "UK", "UAE", "Spain", "Italy", "Canada"]
DEVICES = ["Android", "iOS"]
CATEGORIES = ["Games", "Social", "Productivity", "Finance", "Education", "Entertainment", "Health", "Shopping"]

APP_NAMES = [
    "PixelDash", "ChatWave", "TaskFlow", "CoinTrack", "LearnHub", "StreamGo",
    "FitPulse", "ShopEase", "PhotoLab", "MapNow", "MusicBeat", "NewsBird",
    "FoodFast", "TravelPal", "NoteBoxx", "BudgetPro", "PlayZone", "SkyMail",
    "FocusTimer", "QuizMaster", "MoneyJar", "DriveSafe", "YogaMind", "BookBee",
    "VoiceNote", "CryptoWatch", "HomeFix", "PetCare", "WeatherNow", "JobSeek",
    "LangoLearn", "MeetUpp", "SnapEdit", "GameVerse", "CloudDrop", "FitRun",
    "ShopSmart", "ChefBook", "ZenBreath", "TrackIt", "PulseFit", "InkNote",
    "WavePlay", "BrightMind", "QuickCart", "TimeBox", "SafeVault", "SkyChat",
    "MindMap", "GoGreen", "CityGuide", "PixelPaint",
]

SEARCH_TERMS = [
    "free games", "budget app", "photo editor", "learn english", "music player",
    "fitness tracker", "chat app", "weather app", "note taking", "crypto tracker",
    "recipe app", "vpn", "language learning", "video editor", "meditation app",
    "job search", "task manager", "grocery list", "travel planner", "puzzle games",
]

OUTPUT_DIR = "/mnt/user-data/outputs"


# picks a random date between start and end
def random_date(start, end):
    day_diff = (end - start).days
    random_day = random.randint(0, day_diff)
    return start + timedelta(days=random_day)


# writes rows to a csv file using ; as separator
def write_csv(file_name, headers, rows):
    path = OUTPUT_DIR + "/" + file_name
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(headers)
        writer.writerows(rows)
    print(file_name, "written -", len(rows), "rows")


# 1) USERS table
users = []
for user_id in range(1, N_USERS + 1):
    username = "user" + str(user_id)
    country = random.choice(COUNTRIES)
    device = random.choice(DEVICES)
    signup_date = random_date(START_DATE, END_DATE)

    users.append([
        user_id,
        username,
        country,
        device,
        signup_date.strftime("%Y-%m-%d"),
    ])


# 2) APPS table
apps = []
for app_id in range(1, N_APPS + 1):
    # reuse names if we run out of unique ones
    base_name = APP_NAMES[(app_id - 1) % len(APP_NAMES)]
    app_name = base_name if app_id <= len(APP_NAMES) else base_name + str(app_id)
    developer_id = random.randint(1, 30)
    category = random.choice(CATEGORIES)
    release_date = random_date(START_DATE - timedelta(days=400), START_DATE)

    apps.append([
        app_id,
        app_name,
        developer_id,
        category,
        release_date.strftime("%Y-%m-%d"),
    ])


# 3) SEARCH table
searches = []
for search_id in range(1, N_SEARCHES + 1):
    user_id = random.randint(1, N_USERS)
    term = random.choice(SEARCH_TERMS)
    search_date = random_date(START_DATE, END_DATE)

    searches.append([
        search_id,
        user_id,
        term,
        search_date.strftime("%Y-%m-%d"),
    ])


# 4) CLICK table
# about 50% of searches turn into a click
clicks = []
click_id = 1

for row in searches:
    search_id = row[0]
    user_id = row[1]
    search_date_str = row[3]

    if random.random() < 0.5:
        app_id = random.randint(1, N_APPS)
        search_date = datetime.strptime(search_date_str, "%Y-%m-%d")
        click_date = search_date + timedelta(days=random.randint(0, 2))

        clicks.append([
            click_id,
            search_id,
            user_id,
            app_id,
            click_date.strftime("%Y-%m-%d"),
        ])
        click_id = click_id + 1


# 5) DOWNLOAD table
# about 40% of clicks turn into a download
downloads = []
download_id = 1

for row in clicks:
    user_id = row[2]
    app_id = row[3]
    click_date_str = row[4]

    if random.random() < 0.4:
        click_date = datetime.strptime(click_date_str, "%Y-%m-%d")
        download_date = click_date + timedelta(days=random.randint(0, 1))

        downloads.append([
            download_id,
            user_id,
            app_id,
            download_date.strftime("%Y-%m-%d"),
        ])
        download_id = download_id + 1


# 6) REVENUE table
# about 30% of downloads turn into a purchase
revenues = []
transaction_id = 1

for row in downloads:
    user_id = row[1]
    app_id = row[2]
    download_date_str = row[3]

    if random.random() < 0.3:
        download_date = datetime.strptime(download_date_str, "%Y-%m-%d")
        transaction_date = download_date + timedelta(days=random.randint(0, 5))
        amount = round(random.uniform(0.99, 49.99), 2)

        revenues.append([
            transaction_id,
            user_id,
            app_id,
            amount,
            transaction_date.strftime("%Y-%m-%d"),
        ])
        transaction_id = transaction_id + 1


# save all tables as csv
write_csv("users.csv", ["user_id", "username", "country", "device_type", "signup_date"], users)
write_csv("apps.csv", ["app_id", "app_name", "developer_id", "category", "release_date"], apps)
write_csv("search.csv", ["search_id", "user_id", "search_query", "search_date"], searches)
write_csv("click.csv", ["click_id", "search_id", "user_id", "app_id", "click_date"], clicks)
write_csv("download.csv", ["download_id", "user_id", "app_id", "download_date"], downloads)
write_csv("revenue.csv", ["transaction_id", "user_id", "app_id", "revenue_amount", "transaction_date"], revenues)

# print a short summary
print("")
print("Total users:", len(users))
print("Total apps:", len(apps))
print("Total searches:", len(searches))
print("Total clicks:", len(clicks))
print("Total downloads:", len(downloads))
print("Total revenue records:", len(revenues))
