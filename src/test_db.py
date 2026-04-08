from datetime import datetime
from database.db import insert_event, get_recent_events

event = {
    "event_type": "EIA_CRUDE_INVENTORY",
    "event_time": datetime.utcnow(),
    "asset": "WTI",
    "forecast": -1.5,
    "actual": 3.2,
    "previous": -0.8,
    "surprise": 4.7,
    "source": "manual_test"
}

event_id = insert_event(event)

print(f"Inserted event ID: {event_id}")

events = get_recent_events()

for e in events:
    print(e)