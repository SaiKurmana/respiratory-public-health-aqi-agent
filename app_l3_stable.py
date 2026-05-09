import streamlit as st
import requests
from openai import OpenAI


st.set_page_config(page_title="Respiratory Public Health AQI Agent", layout="centered")

st.title("Respiratory Public Health AQI Agent")
st.caption("Level 3: live AQI data + Foundry/Azure OpenAI decision support")


def get_coordinates(location_query: str):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": location_query,
        "format": "json",
        "limit": 1,
    }

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

    return (
        results[0]["lat"],
        results[0]["lon"],
        results[0]["display_name"],
    )


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

    st.subheader("Live AQI Summary")
    st.metric("AQI", data.get("aqi"))
    st.write("Monitoring station:", data.get("city", {}).get("name"))
    st.write("Dominant pollutant:", data.get("dominentpol"))
    st.write("Time:", data.get("time", {}).get("iso"))

    client = OpenAI(
        api_key=azure_key,
        base_url=azure_endpoint,
    )

    prompt = f"""
You are a respiratory public health decision intelligence assistant.

Use the live AQI data below to advise whether a public health advisory is warranted.

Thresholds:
- AQI >100: sensitive groups should limit outdoor exposure.
- AQI >150: general population may be affected and public advisory is warranted.

User-entered location:
{city}

Resolved location:
{display_name}

Live AQI data:
{aqi_data}

Return:
1. AQI summary
2. Risk interpretation
3. Advisory decision
4. Data limitations
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

    st.subheader("Agent Recommendation")
    st.write(response.choices[0].message.content)