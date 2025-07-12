import json
from datetime import datetime, timedelta
from prettytable import PrettyTable

EVENTS_FILE = "events.json"

# Load events from file
def load_events():
    try:
        with open(EVENTS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Save events to file
def save_events(events):
    with open(EVENTS_FILE, "w") as f:
        json.dump(events, f, indent=4)

# Check for time conflicts
def has_conflict(events, new_event):
    new_start = datetime.fromisoformat(new_event["start"])
    new_end = datetime.fromisoformat(new_event["end"])
    for event in events:
        start = datetime.fromisoformat(event["start"])
        end = datetime.fromisoformat(event["end"])
        if (new_start < end and new_end > start):
            return True
    return False

# Add a new event
def add_event():
    title = input("Event Title: ")
    start = input("Start Time (YYYY-MM-DD HH:MM): ")
    end = input("End Time (YYYY-MM-DD HH:MM): ")

    new_event = {
        "title": title,
        "start": datetime.strptime(start, "%Y-%m-%d %H:%M").isoformat(),
        "end": datetime.strptime(end, "%Y-%m-%d %H:%M").isoformat()
    }

    events = load_events()
    if has_conflict(events, new_event):
        print("⚠️ Conflict detected! Event not added.")
    else:
        events.append(new_event)
        save_events(events)
        print("✅ Event added successfully.")

# View all events
def view_events():
    events = sorted(load_events(), key=lambda e: e["start"])
    table = PrettyTable(["Title", "Start", "End"])
    for event in events:
        table.add_row([event["title"], event["start"], event["end"]])
    print(table)

# Main menu
def main():
    while True:
        print("\n📅 Smart Calendar Scheduler")
        print("1. View Events")
        print("2. Add Event")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            view_events()
        elif choice == "2":
            add_event()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()

