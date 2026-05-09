import requests
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# 🔴 Your Foundry setup
PROJECT_ENDPOINT = "https://saikurmana-1817-resource.services.ai.azure.com/api/projects/saikurmana-1817"
MODEL = "gpt-4.1-mini-1"

# 🔴 PUT YOUR NEW TOKEN HERE
WAQI_TOKEN = "947a7a28b2e04aed22c4b57c8ab933f5376a06bf"


# 🔧 Simple AQI API call (tool)
def get_aqi(city):
    url = f"https://api.waqi.info/feed/{city}/"
    params = {"token": WAQI_TOKEN}

    response = requests.get(url, params=params)
    return response.json()


# 🔥 Call the tool
aqi_data = get_aqi("jackson")

# 🔧 Connect to Foundry
project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)

client = project.get_openai_client()

# 🧠 Agent prompt (Level 3 behavior)
prompt = f"""
You are a respiratory public health agent.

You must:
1. Use LIVE AQI data
2. Apply CDC-style thresholds
3. Make a decision

Thresholds:
- AQI >100: sensitive groups advisory
- AQI >150: public advisory

Live AQI data:
{aqi_data}

Output:
1. AQI summary
2. Risk level
3. Advisory decision
"""

response = client.responses.create(
    model=MODEL,
    input=prompt,
)

print(response.output_text)