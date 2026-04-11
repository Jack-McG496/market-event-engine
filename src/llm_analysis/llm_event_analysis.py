import json
from openai import OpenAI

client = OpenAI()

def analyze_event_with_llm(event):
    prompt = build_prompt(event)

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # cheap + fast
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except:
        print("LLM output parsing failed:")
        print(content)
        return None

def build_prompt(event):
    return f"""
    You are an energy market analyst.

    Analyze the following event:

    Event Type: {event['event_type']}
    Forecast: {event['forecast']}
    Actual: {event['actual']}
    Surprise: {event['surprise']}

    Context:
    - This is a US crude oil inventory report
    - Positive surprise = inventory build (bearish)
    - Negative surprise = inventory draw (bullish)

    Return ONLY valid JSON:

    {{
    "bias": "bullish | bearish | neutral",
    "magnitude": "low | medium | high",
    "time_horizon": "intraday | short-term | medium-term",
    "confidence": 0.0-1.0,
    "explanation": "short explanation"
    }}
    """