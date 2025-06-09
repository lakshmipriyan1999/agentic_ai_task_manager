from google_calendar import find_next_available_slot

def test_next_available_slot_found():
    busy_slots = [
        {"start": "2025-06-02T09:00:00+05:30", "end": "2025-06-02T10:00:00+05:30"},
        {"start": "2025-06-02T10:30:00+05:30", "end": "2025-06-02T11:00:00+05:30"},
    ]
    duration = 30  # in minutes
    preferred_start = "2025-06-02T10:00:00+05:30"
    
    next_slot = find_next_available_slot(busy_slots, duration, preferred_start)
    
    # Expecting a free 30-minute window between 10:00 and 10:30
    assert next_slot == "2025-06-02T10:00:00+05:30"
