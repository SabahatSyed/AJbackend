from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import time

app = Flask(__name__)
CORS(app)
all_bins_data = []

class SmartWasteBin:
    def __init__(self, bin_id, house_number, street_name):
        self.bin_id = bin_id
        self.location = f"House {house_number}, {street_name}"
        self.fill_level = 0  
        self.is_full = False
        self.recycled = 0 
        self.wasted = 0  
        self.recycling_in_progress = False
        self.garbage_type = "plastic", "wires", "general", "glass" 

    def update_fill_level(self):
        self.fill_level = 0
        if self.fill_level >= 90:
            self.is_full = True
            send_street_message(self.location, f"Bin {self.bin_id} is full and needs to be emptied.")
        else:
            self.is_full = False

    def start_recycling(self):
        self.recycling_in_progress = True
        time.sleep(2)
        send_company_message(f"Initiating recycling process for {self.bin_id}. Recycling the waste into usable plastic, wires, and other...")
        recycle_steps = ["Sorting", "Cleaning", "Melting", "Reforming"]
        for step in recycle_steps:
            send_company_message(f"Recycling process for {self.bin_id}: {step}")
            time.sleep(2)
        
        recycled_type = "plastic", "wires", "general", "glass"
        
        self.recycled += 1
        self.fill_level = 0
        self.is_full = False
        self.recycling_in_progress = False
        self.garbage_type = recycled_type
        
        send_company_message(f"Waste from {self.bin_id} has been recycled into {recycled_type}.")

    def get_bin_status(self):
        return {
            "bin_id": self.bin_id,
            "location": self.location,
            "fill_level": self.fill_level,
            "recycled": self.recycled,
            "wasted": self.wasted,
            "recycling_in_progress": self.recycling_in_progress,
            "garbage_type": self.garbage_type
        }

class House:
    def __init__(self, house_number, street_name):
        self.house_number = house_number
        self.street_name = street_name
        self.bin = SmartWasteBin(f"Bin{house_number}", house_number, street_name)

class Street:
    def __init__(self, name):
        self.name = name
        self.houses = []

    def add_houses(self, num_houses):
        for i in range(1, num_houses + 1):
            self.add_house(House(i, self.name))

    def add_house(self, house):
        self.houses.append(house)

def send_alert(bin_status):
    message = f"ALERT: Bin {bin_status['bin_id']} at {bin_status['location']} is almost full (Fill Level: {bin_status['fill_level']}%, Type: {bin_status['garbage_type']})"
    print(message)  # Adjust as needed for your logging or alert system

def send_street_message(location, message):
    print(f"{location}: {message}")  # Adjust as needed for your logging or messaging system

def send_company_message(message):
    print(f"Company: {message}")  # Adjust as needed for your logging or messaging system

def send_truck_to_bin(bin_id):
    send_company_message(f"Sending a truck to pick up garbage from {bin_id}.")
    time.sleep(5)
    send_company_message(f"Truck has arrived at {bin_id}.")
    time.sleep(5)
    send_company_message(f"Truck departed with the garbage from {bin_id}.")

def display_header():
    print("\n\n\n\n\n\t" + "*" * 60)
    print("\t " + "*" * 58)
    print("\t  " + "*" * 56)
    print("\t\t\t OPTIMIZING WASTE MANAGEMENT WITH AI SYSTEM")
    print("\t  " + "*" * 56)
    print("\t " + "*" * 58)
    print("\t" + "*" * 60)

def display_status(bin):
    fill_level = bin.fill_level
    recycled = bin.recycled
    wasted = bin.wasted
    garbage_type = bin.garbage_type

    status = f"Bin ID: {bin.bin_id}\nLocation: {bin.location}\nFill Level: {fill_level}%\nRecycled: {recycled} items\nWasted: {wasted} items\nGarbage Type: {garbage_type}"

    return status

# Dummy array of streets and houses
street_A = Street("Street A")
street_A.add_houses(7)

street_B = Street("Street B")
street_B.add_houses(7)

street_C = Street("Street C")
street_C.add_houses(7)

streets = [street_A, street_B, street_C]

fill_threshold = 90

@app.route('/api/bin/status/<bin_id>/<street_id>/', methods=['GET'])
def get_bin_status(bin_id,street_id):
    bin_obj = find_bin_by_id(bin_id,street_id)
    if bin_obj is not None:
        status = bin_obj.get_bin_status()
        return jsonify(status)
    else:
        return jsonify({"error": "Bin not found"}), 404

@app.route('/api/bin/recycle/<bin_id>/<street_id>', methods=['POST'])
def start_recycling(bin_id, street_id):
    bin_obj = find_bin_by_id(bin_id, street_id)
    if bin_obj is not None:
        if not bin_obj.recycling_in_progress:
            bin_obj.start_recycling()

            # Update status for all bins after recycling within the existing global list
            for bin_data in all_bins_data:
                if bin_data['bin_id'] == bin_id and bin_data['location'].endswith(street_id):
                    bin_data['fill_level'] = 0  # Set fill level to 0
                    bin_data['recycled'] += 1  # Increment recycled count

            return jsonify({
                "message": f"Recycling process initiated for {bin_id}",
                "all_bins_data": all_bins_data
            }), 200
        else:
            return jsonify({"error": f"Recycling process already in progress for {bin_id}"}), 400
    else:
        return jsonify({"error": "Bin not found"}), 404

@app.route('/api/bins', methods=['GET'])
def get_all_bins():
    global all_bins_data
    fill_levels_sequence = [0, 32, 45, 75, 85, 95]
    print("sdj")
    # Check if data already exists
    if not all_bins_data:
        # Initialize the global list when first hit
        for street in streets:
            for house in street.houses:
                house.bin.update_fill_level()  # Simulate updating fill levels

                # If fill level is 0, set it to the first value in the sequence
                if house.bin.fill_level == 0:
                    house.bin.fill_level = fill_levels_sequence[0]

                all_bins_data.append(house.bin.get_bin_status())
    else:
        for bin_data in all_bins_data:
            # If fill level is 0, set it to the first value in the sequence
            if bin_data['fill_level'] == 0:
                bin_data['fill_level'] = fill_levels_sequence[1]
            elif bin_data['fill_level'] == 32:
                bin_data['fill_level'] = fill_levels_sequence[2]
            elif bin_data['fill_level'] == 45:
                bin_data['fill_level'] = fill_levels_sequence[3]
            elif bin_data['fill_level'] == 75:
                bin_data['fill_level'] = fill_levels_sequence[4]
            elif bin_data['fill_level'] == 85:
                bin_data['fill_level'] = fill_levels_sequence[5]

    return jsonify(all_bins_data)

def find_bin_by_id(bin_id,street_id):
    for street in streets:
        for house in street.houses:
            if house.bin.bin_id == bin_id and street_id in house.bin.location:
                return house.bin
    return None


if __name__ == "__main__":
    app.run(debug=True)