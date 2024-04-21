###########################################################
#                                                         #
#   Sample data generation script                         #
#   Usage:                                                #
#     1. Install Faker library: pip3 install Faker geopy  #
#     2. Run the script: python3 generate_data.py         #
#                                                         #
###########################################################

from faker import Faker
from geopy.distance import geodesic
import json, sys


#   Function to generate taxpayer data
def generate_taxpayer_data(num_taxpayers):
    fake = Faker()
    Faker.seed(0)
    
    taxpayers = []

    for _ in range(1000):
        geolocation = fake.local_latlng(country_code="MX")
        taxpayer = {
            "id": fake.uuid4(),
            "name": fake.name(),
            "location": {
            "latitude":float(geolocation[0]),
            "longitude":float(geolocation[1])
            },
            "age" : fake.random_int(18, 90),
            "accepted_offers" : fake.random_int(0, 100),
            "canceled_offers" : fake.random_int(0, 100),
            "average_reply_time" : fake.random_int(1, 3600),
        }
        taxpayers.append(taxpayer)
    return taxpayers

# Writing to taxpayers.json
def read_taxpayers_file():
    try:
        with open("taxpayers.json", "r") as outfile:
            taxpayers_data = json.load(outfile)
        return taxpayers_data
    except FileNotFoundError:
        print("ERROR: File 'taxpayers.json' not found.")
        sys.exit()
if __name__ == "__main__":
    taxpayers_data = read_taxpayers_file()
    if taxpayers_data:
        print("Successfully loaded taxpayers data.")

#   Function to calculate taxpayer scores
def calculate_scores(taxpayers, fixat_office_location):
    for taxpayer in taxpayers:
        #   Calculate distance between taxpayer and Fixat's office location
        taxpayer_location = (taxpayer["location"]["latitude"], taxpayer["location"]["longitude"])
        distance_to_fixat = geodesic(fixat_office_location, taxpayer_location).kilometers
        taxpayer["distance_to_office"] = int(round(distance_to_fixat))
        #   Calculate score for each taxpayer
        age_score = taxpayer["age"] / 90 * 10
        distance_score = (1 - taxpayer["distance_to_office"] / 100) * 10
        accepted_offers_score = taxpayer["accepted_offers"] / 100 * 30
        canceled_offers_score = (1 - taxpayer["canceled_offers"] / 100) * 30
        reply_time_score = (1 - taxpayer["average_reply_time"] / 3600 / 24) * 20
        
        total_score = (age_score + distance_score) * 0.2 + (accepted_offers_score + canceled_offers_score + reply_time_score) * 0.8
        taxpayer["score"] = int(round(total_score))
    return taxpayers

#   Function to select top 10 taxpayers
def select_top_taxpayers(taxpayers):
    sorted_taxpayers = sorted(taxpayers, key=lambda x: x["score"], reverse=True)
    return sorted_taxpayers[:10]

if __name__ == "__main__":
    # Request the latitude and length to the user
    latitude = float(input("Latitude: "))
    longitude = float(input("Longitude: "))
    
    fixat_office_location = (latitude, longitude)
    # Read data from taxpayers taxpayers.json
    taxpayers_data = read_taxpayers_file()
    # Calculate taxpayers scores
    taxpayers_with_scores = calculate_scores(taxpayers_data, fixat_office_location)
    # Select the 10 best taxpayers
    top_10_taxpayers = select_top_taxpayers(taxpayers_with_scores)
    # Show the console result in JSON format
    print(json.dumps(top_10_taxpayers, indent=4))