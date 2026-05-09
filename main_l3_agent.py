import json
from typing import Any, cast

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import PromptAgentDefinition

PROJECT_ENDPOINT = "https://saikurmana-1817-resource.services.ai.azure.com/api/projects/saikurmana-1817"
MODEL = "gpt-4.1-mini-1"
OPENAPI_CONNECTION_NAME = "waqi-api-connection"

with open("aqi_openapi_v2.json", "r", encoding="utf-8") as f:
    aqi_openapi_spec = cast(dict[str, Any], json.load(f))

project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)

openai = project.get_openai_client()

connection = project.connections.get(OPENAPI_CONNECTION_NAME)
connection_id = connection.id

aqi_tool = {
    "type": "openapi",
    "openapi": {
        "name": "waqi_aqi_tool",
        "description": "Get current live AQI data by city using the World Air Quality Index API.",
        "spec": aqi_openapi_spec,
        "auth": {
            "type": "project_connection",
            "security_scheme": {
                "project_connection_id": connection_id
            }
        }
    }
}

agent = project.agents.create_version(
    agent_name="respiratory-public-health-agent-l3-openapi",
    definition=PromptAgentDefinition(
        model=MODEL,
        instructions="""
You are a Level 3 respiratory public health agent.

When the user asks about current air quality or AQI:
- Use the AQI OpenAPI tool.
- Do not invent live AQI values.
- After receiving live AQI data, compare it to these thresholds:
  - AQI >100: sensitive groups should limit outdoor exposure.
  - AQI >150: general population may be affected and public advisory is warranted.

Respond with:
1. Live AQI result
2. Interpretation
3. Advisory decision
4. Data limitations
""",
        tools=[aqi_tool],
    ),
)

response = openai.responses.create(
    input="What is the current AQI in Jackson, Mississippi, and should a public advisory be issued?",
    extra_body={
        "agent_reference": {
            "name": agent.name,
            "type": "agent_reference"
        }
    },
)

print(response.output_text)