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