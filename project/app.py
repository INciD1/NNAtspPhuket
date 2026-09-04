from flask import Flask, jsonify, render_template
import random
import googlemaps
import os
from dotenv import load_dotenv

load_dotenv()  # loads variables from a local .env file, if present

app = Flask(__name__)

# Google Maps API Key -- read from the environment, never hardcoded here.
API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")
if not API_KEY:
    raise RuntimeError(
        "GOOGLE_MAPS_API_KEY is not set. Copy .env.example to .env and add your key."
    )
gmaps = googlemaps.Client(key=API_KEY)

# ฟังก์ชันตรวจสอบว่าเป็น Apartment หรือ Condo หรือที่อื่นๆ
def filter_apartments_and_condos(locations):
    keywords = ["apartment", "condo", "condominium", "Mansion", "Hotel", "House", "Office", "Residence", "gym", "Place",
                "Baan", "ban", "แมนชั่น", "School", "Central"]
    filtered = [
        loc for loc in locations
        if any(keyword in loc.lower() for keyword in keywords)
    ]
    return filtered

# ฟังก์ชันคำนวณระยะทางระหว่างสองจุด
def is_within_distance(lat1, lng1, lat2, lng2, max_distance_km=2):
    from geopy.distance import geodesic
    distance = geodesic((lat1, lng1), (lat2, lng2)).km
    return distance <= max_distance_km

# Get the current directory of this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to NLP.txt
NLP_FILE_PATH = os.path.join(BASE_DIR, "NLP.txt")

def load_locations(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines()]

# โหลดข้อมูลจาก NLP.txt
raw_locations = load_locations(NLP_FILE_PATH)

@app.route("/")
def index():
    # Pass the API key to the template server-side, so it's injected into
    # the page at render time instead of being hardcoded in the HTML source.
    return render_template("index.html", google_maps_api_key=API_KEY)

@app.route("/generate", methods=["GET"])
def generate_locations():
    """
    ค้นหาสถานที่ที่อยู่ในระยะ 1-2 กม. และสุ่ม 5 สถานที่
    """
    # พิกัดกลางในเมืองภูเก็ต
    city_center = {"lat": 7.8804, "lng": 98.3923}  # Patong Beach

    # Geocode สถานที่และกรองระยะทาง
    nearby_locations = []
    for loc in raw_locations:  # เปลี่ยนจาก `locations` เป็น `raw_locations`
        geocode_result = gmaps.geocode(f"{loc}, Phuket, Thailand")
        if geocode_result:
            lat = geocode_result[0]["geometry"]["location"]["lat"]
            lng = geocode_result[0]["geometry"]["location"]["lng"]
            if is_within_distance(city_center["lat"], city_center["lng"], lat, lng):
                nearby_locations.append({
                    "name": loc,
                    "lat": lat,
                    "lng": lng,
                })

    # สุ่ม 6 สถานที่
    sampled_locations = random.sample(nearby_locations, min(6, len(nearby_locations)))
    return jsonify(sampled_locations)

if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug_mode)
