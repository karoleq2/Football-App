import os
import sqlite3
import pandas as pd

if not os.path.exists("instance"):
    os.makedirs("instance")
    print("Missing folder created 'instance'.")

print("Database creation and CSV file import started...")

db = sqlite3.connect("instance/database.db")

pd.read_csv("static/csv/appearances.csv").to_sql("appearances", db, if_exists="replace", index=False)
print("- Imported appearances")
pd.read_csv("static/csv/club_games.csv").to_sql("club_games", db, if_exists="replace", index=False)
print("- Imported club_games")
pd.read_csv("static/csv/clubs.csv").to_sql("clubs", db, if_exists="replace", index=False)
print("- Imported clubs")
pd.read_csv("static/csv/games.csv").to_sql("games", db, if_exists="replace", index=False)
print("- Imported games")
pd.read_csv("static/csv/national_teams.csv").to_sql("national_teams", db, if_exists="replace", index=False)
print("- Imported national_teams")
pd.read_csv("static/csv/players.csv").to_sql("players", db, if_exists="replace", index=False)
print("- Imported players")
pd.read_csv("static/csv/transfers.csv").to_sql("transfers", db, if_exists="replace", index=False)
print("- Imported transfers")

db.close()
print("Success! The database has been fully created.")