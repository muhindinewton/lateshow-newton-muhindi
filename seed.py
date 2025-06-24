#!/usr/bin/env python3

from app import app
from models import db, Episode, Guest, Appearance
import csv
import random

CSV_FILE_PATH = 'seed.csv' 

def seed_database():
    with app.app_context():
        print("Clearing existing data...")
        Appearance.query.delete()
        Episode.query.delete()
        Guest.query.delete()
        db.session.commit()
        print("Existing data cleared.")

        print("Seeding episodes and guests from CSV...")
        episodes_data = []
        guests_data = {} # Using a dict to avoid duplicate guests
        appearances_data = []

        with open(CSV_FILE_PATH, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row_num, row in enumerate(reader):
                try:
                    # Episode
                    episode_date = row['Show']
                    episode_number = row_num + 1 # Using row number as a unique episode number
                    
                    # Create episode if not already added (based on unique number/date)
                    episode = Episode.query.filter_by(date=episode_date, number=episode_number).first()
                    if not episode:
                        episode = Episode(date=episode_date, number=episode_number)
                        db.session.add(episode)
                        db.session.flush() # Flush to get the episode.id for relationships
                    episodes_data.append(episode)

                    # Guest
                    guest_name = row['Raw_Guest_List']
                    guest_occupation = row['GoogleKnowlege_Occupation']
                    
                    if guest_name not in guests_data:
                        guest = Guest(name=guest_name, occupation=guest_occupation)
                        db.session.add(guest)
                        db.session.flush() # Flush to get the guest.id for relationships
                        guests_data[guest_name] = guest
                    else:
                        guest = guests_data[guest_name]

                    # Appearance
                    appearance_rating = random.randint(1, 5) # Generate random rating
                    
                    appearance = Appearance(
                        rating=appearance_rating,
                        episode_id=episode.id,
                        guest_id=guest.id
                    )
                    appearances_data.append(appearance)
                    db.session.add(appearance)

                except (ValueError, KeyError) as e:
                    print(f"Skipping row {row_num + 2} due to error: {e} in row: {row}")
                except Exception as e:
                    print(f"An unexpected error occurred at row {row_num + 2}: {e} in row: {row}")

        db.session.commit()
        print(f"Seeding complete. Added {len(set(e.id for e in episodes_data))} episodes, {len(guests_data)} guests, and {len(appearances_data)} appearances.")

if __name__ == '__main__':
    seed_database()