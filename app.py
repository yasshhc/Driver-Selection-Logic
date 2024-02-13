from flask import Flask, request, render_template
import numpy as np

app = Flask(__name__)

# Define your drivers here
drivers = {
    'D01': {'location': (45.494587566299614, -73.58057120870089), 'rating': 4.5},
    'D02': {'location': (45.49641847822808, -73.57646380997149), 'rating': 4.2},
    'D03': {'location': (45.493832821918396, -73.575127908443), 'rating': 4.0},
    'D04': {'location': (45.4938467987581, -73.57926521541557), 'rating': 4.8},
    'D05': {'location': (45.49658619237504, -73.58204668203088), 'rating': 3.8},
    'D06': {'location': (45.49803969407978, -73.57752056782698), 'rating': 4.9},
    'D07': {'location': (45.495866415654284, -73.57308417842265), 'rating': 4.1},
    'D08': {'location': (45.498081621456194, -73.57095072374281), 'rating': 4.3},
    'D09': {'location': (45.483070740952044, -73.62822689589451), 'rating': 4.6},
    'D10': {'location': (45.531230267914964, -73.59781037755069), 'rating': 3.9},
}

# Haversine formula to calculate the distance
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1_rad, lon1_rad, lat2_rad, lon2_rad = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = np.sin(dlat / 2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = R * c
    return distance

# Calculate scores for each driver based on the pickup location
def calculate_scores(pickup_location):
    driver_scores = {}
    for driver_id, info in drivers.items():
        distance = haversine(pickup_location[0], pickup_location[1], info['location'][0], info['location'][1])
        proximity_score = 10 / distance
        rating_score = (info['rating'] - 4.0) * 20 if info['rating'] > 4.0 else 0
        total_score = proximity_score + rating_score
        driver_scores[driver_id] = total_score
    return sorted(driver_scores.items(), key=lambda x: x[1], reverse=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit-location', methods=['POST'])
def submit_location():
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    pickup_location = (float(latitude), float(longitude))
    sorted_drivers = calculate_scores(pickup_location)
    return '<br>'.join([f"Driver {driver[0]}: {driver[1]:.2f}" for driver in sorted_drivers])

if __name__ == '__main__':
    app.run(debug=True)
