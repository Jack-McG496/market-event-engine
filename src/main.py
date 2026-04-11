from datetime import datetime
from database.db import insert_event, insert_event_analysis
from llm_analysis.llm_event_analysis import analyze_event_with_llm


def run_pipeline():
    # 1️⃣ Create event (manual for V0)
    event = {
        "event_type": "EIA_CRUDE_INVENTORY",
        "event_time": datetime.utcnow(),
        "asset": "WTI",
        "forecast": -1.5,
        "actual": 3.2,
        "previous": -0.8,
        "surprise": 3.2 - (-1.5),
        "source": "manual_test"
    }

    # 2️⃣ Store event
    event_id = insert_event(event)
    print(f"Event stored with ID: {event_id}")

    # 3️⃣ Run LLM analysis
    analysis = analyze_event_with_llm(event)

    if not analysis:
        print("LLM analysis failed")
        return

    # 4️⃣ Store analysis
    analysis_record = {
        "event_id": event_id,
        "bias": analysis["bias"],
        "magnitude": analysis["magnitude"],
        "time_horizon": analysis["time_horizon"],
        "confidence": analysis["confidence"],
        "explanation": analysis["explanation"]
    }

    insert_event_analysis(analysis_record)

    print("Analysis stored successfully")
    print(analysis)


if __name__ == "__main__":
    run_pipeline()