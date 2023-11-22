from termcolor import colored
import random
import winsound
import time

class SmartWasteBin:
    def __init__(self, bin_id, house_number, street_name):
        self.bin_id = bin_id
        self.location = f"House {house_number}, {street_name}"
        self.fill_level = 0  
        self.is_full = False
        self.recycled = 0 
        self.wasted = 0  
        self.recycling_in_progress = False
        self.garbage_type = "plastic", "wires", "general","glass" 

    def update_fill_level(self):
        # Simulate a fill level update (0-100%)
        self.fill_level = random.randint(0, 100)
        if self.fill_level >= 90:
            self.is_full = True
            winsound.Beep(1000, 1000)  
            send_street_message(self.location, f"Bin {self.bin_id} is full and needs to be emptied.")
        else:
            self.is_full = False

    def start_recycling(self):
        self.recycling_in_progress = True
        time.sleep(2)  # Simulate a 2-second delay
        send_company_message(f"Initiating recycling process for {self.bin_id}. Recycling the waste into usable plastic, wires, and other...")
        recycle_steps = ["Sorting", "Cleaning", "Melting", "Reforming"]
        for step in recycle_steps:
            send_company_message(f"Recycling process for {self.bin_id}: {step}")
            time.sleep(2)  # Simulate a 2-second delay for each step
        
        # Determine the type of garbage recycled
        recycled_type = "plastic", "wires", "general","glass"
        
        self.recycled += 1
        self.fill_level = 0
        self.is_full = False
        self.recycling_in_progress = False
        # Change garbage type to the determined recycled type
        self.garbage_type = recycled_type
        
        # Display the recycling message
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
    print(colored(message, "red"))

def send_street_message(location, message):
    print(colored(f"{location}: {message}", "green"))

def send_company_message(message):
    print(colored(f"Company: {message}", "blue"))

def send_truck_to_bin(bin_id):
    send_company_message(f"Sending a truck to pick up garbage from {bin_id}.")
    time.sleep(5)  # Simulate a 5-second delay for the truck to arrive
    send_company_message(f"Truck has arrived at {bin_id}.")
    time.sleep(5)  # Simulate a 5-second delay for the truck to complete the pickup
    send_company_message(f"Truck departed with the garbage from {bin_id}.")

def display_header():
    print("\n\n\n\n\n\t" + "*" * 60)
    print("\t " + "*" * 58)
    print("\t  " + "*" * 56)
    print(colored("\n\t\t\t OPTIMIZING WASTE MANAGEMENT WITH AI SYSTEM", "blue"))
    print("\n\t  " + "*" * 56)
    print("\t " + "*" * 58)
    print("\t" + "*" * 60)

def display_status(bin):
    fill_level = bin.fill_level
    recycled = bin.recycled
    wasted = bin.wasted
    garbage_type = bin.garbage_type

    status = f"Bin ID: {bin.bin_id}\nLocation: {bin.location}\nFill Level: {fill_level}%\nRecycled: {recycled} items\nWasted: {wasted} items\nGarbage Type: {garbage_type}"

    return status


def login():
    # A simple login function
    valid_username = "AhmedDubai"
    valid_password = "Ahmed123"

    while True:
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        if username == valid_username and password == valid_password:
            return True
        else:
            print("Invalid username or password. Try again.")

def main():
    if not login():
        print("Authentication failed. Exiting.")
        return

    street_A = Street("Street A")
    street_A.add_houses(7)

    street_B = Street("Street B")
    street_B.add_houses(7)

    street_C = Street("Street C")
    street_C.add_houses(7)

    streets = [street_A, street_B, street_C]

    fill_threshold = 90  # Set the fill level threshold for sending an alert

    display_header()

    while True:
        print("\nChoose a street to check (1 - Street A, 2 - Street B, 3 - Street C, q - Quit):")
        choice = input()

        if choice == 'q':
            break
        elif choice == '1':
            street = street_A
        elif choice == '2':
            street = street_B
        elif choice == '3':
            street = street_C
        else:
            print("Invalid choice. Please enter 1, 2, 3, or q to quit.")
            continue

        print(colored(f"\nStatus for {street.name}:", "blue"))

        for house in street.houses:
            house.bin.update_fill_level()
            status = house.bin.get_bin_status()

            if status['fill_level'] >= fill_threshold:
                send_alert(status)
                send_truck_to_bin(house.bin.bin_id)
                if not status['recycling_in_progress']:
                    house.bin.start_recycling()

            print(colored(display_status(house.bin), "white"))
            print("-" * 40)

if __name__ == "__main__":
    main()          

