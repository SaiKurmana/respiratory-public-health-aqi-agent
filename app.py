import streamlit as st
import requests
from openai import OpenAI


st.set_page_config(page_title="Respiratory Public Health AQI Agent", layout="centered")
st.info(
    "Enter any city, county, or region in the USA to test live air quality monitoring and AI-assisted respiratory public health guidance."
)
st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(
            to bottom right,
            #f8fbff,
            #eef4ff,
            #e6f0ff
        );
        color: #111827;
    }

    h1, h2, h3, h4, h5, h6, p, label, div {
        color: #111827 !important;
    }

    .stTextInput input {
        background-color: white;
        color: #111827;
        border-radius: 10px;
        border: 1px solid #cbd5e1;
    }

    .stButton button {
        background-color: #2563eb;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }

    .stButton button:hover {
        background-color: #1d4ed8;
        color: white;
    }

    section[data-testid="stSidebar"] {
        background-color: #f1f5f9;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🌎 Respiratory Public Health AQI Agent")
st.caption(
    "Explore live air quality intelligence with real-time AQI monitoring, PM2.5 trend detection, and AI-powered public health recommendations."
)


def get_coordinates(location_query: str):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": location_query, "format": "json", "limit": 1}

    response = requests.get(
        url,
        params=params,
        headers={"User-Agent": "respiratory-public-health-aqi-agent"},
        timeout=20,
    )
    response.raise_for_status()

    results = response.json()
    if not results:
        return None

    return results[0]["lat"], results[0]["lon"], results[0]["display_name"]


def analyze_pm25_trend(aqi_data):
    pm25_forecast = (
        aqi_data.get("data", {})
        .get("forecast", {})
        .get("daily", {})
        .get("pm25", [])
    )

    recent = pm25_forecast[:3]

    if len(recent) < 3:
        return "Trend unavailable", recent

    values = [day.get("avg") for day in recent]

    if any(v is None for v in values):
        return "Trend unavailable", recent

    if values[2] > values[1] > values[0]:
        trend = "Rising PM2.5 trend — early warning signal"
    elif values[2] < values[1] < values[0]:
        trend = "Falling PM2.5 trend — improving conditions"
    else:
        trend = "Stable or mixed PM2.5 trend"

    return trend, recent


city = st.text_input("Enter city, state, or location", value="Jackson, Mississippi")

if st.button("Check AQI and Advisory"):
    waqi_token = st.secrets["WAQI_TOKEN"]
    azure_endpoint = st.secrets["AZURE_OPENAI_ENDPOINT"]
    azure_key = st.secrets["AZURE_OPENAI_KEY"]
    deployment = st.secrets["AZURE_OPENAI_DEPLOYMENT"]

    with st.spinner("Resolving location..."):
        coords = get_coordinates(city)

    if coords is None:
        st.error("Location not found. Try adding state/country, for example: Madison, Mississippi, USA")
        st.stop()

    lat, lon, display_name = coords

    st.subheader("Resolved Location")
    st.write(display_name)

    with st.spinner("Getting live AQI data..."):
        aqi_url = f"https://api.waqi.info/feed/geo:{lat};{lon}/"
        aqi_response = requests.get(
            aqi_url,
            params={"token": waqi_token},
            timeout=20,
        )
        aqi_response.raise_for_status()
        aqi_data = aqi_response.json()

    if aqi_data.get("status") != "ok":
        st.error(f"AQI API error: {aqi_data.get('data')}")
        st.stop()

    data = aqi_data["data"]

    st.subheader("🌎 Live AQI Summary")
    st.metric("AQI", data.get("aqi"))

    aqi = data.get("aqi", 0)

    if aqi <= 50:
        st.success("🟢 Good air quality")
    elif aqi <= 100:
        st.warning("🟡 Moderate air quality")
    elif aqi <= 150:
        st.warning("🟠 Unhealthy for sensitive groups")
    else:
        st.error("🔴 Unhealthy air quality")

    st.write("Monitoring station:", data.get("city", {}).get("name"))
    st.write("Dominant pollutant:", data.get("dominentpol"))
    st.write("Time:", data.get("time", {}).get("iso"))

    trend_label, recent_pm25 = analyze_pm25_trend(aqi_data)

    pm25_summary = "\n".join(
        [f"{d.get('day')}: avg {d.get('avg')}" for d in recent_pm25]
    )

    st.subheader("📈 PM2.5 Trend Signal")
    st.write(trend_label)

    if recent_pm25:
        st.table(recent_pm25)

    client = OpenAI(
        api_key=azure_key,
        base_url=azure_endpoint,
    )

    prompt = f"""
You are a respiratory public health decision intelligence assistant.

You MUST ONLY use the PM2.5 values explicitly provided below.
Do NOT infer, extrapolate, or reference any additional days or values beyond what is shown.

Thresholds:
- AQI >100: sensitive groups should limit outdoor exposure.
- AQI >150: general population may be affected and public advisory is warranted.
- PM2.5 >35 µg/m³: may impact sensitive groups.

User-entered location:
{city}

Resolved location:
{display_name}

PM2.5 trend signal:
{trend_label}

Recent PM2.5 forecast values (ONLY use these):
{pm25_summary}

Live AQI data (current snapshot):
AQI: {data.get("aqi")}
Dominant pollutant: {data.get("dominentpol")}
Time: {data.get("time", {}).get("iso")}

STRICT RULES:
- Do NOT mention any dates or values not explicitly listed above.
- Do NOT extend the forecast beyond the provided rows.
- Base all PM2.5 trend reasoning ONLY on the provided PM2.5 values.
- If the current AQI is low but PM2.5 trend is rising, distinguish current risk from early warning risk.

Return:
1. AQI summary
2. PM2.5 trend interpretation
3. Risk interpretation
4. Advisory decision
5. Data limitations
"""

    with st.spinner("Generating public health recommendation..."):
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {
                    "role": "system",
                    "content": "You are a public health decision intelligence assistant.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

    st.subheader("🧠 Agent Recommendation")
    st.write(response.choices[0].message.content)
    
    st.markdown("---")
st.caption(
    "Built by Sai Kurmana • Live AQI via WAQI • Azure OpenAI decision intelligence"
)