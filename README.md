# Respiratory Public Health Decision Intelligence Agent

An AI-powered operational intelligence system that integrates live air quality data, geospatial resolution, and large language model reasoning to support respiratory public health advisory decisions.

Built as part of an ongoing exploration of agentic AI patterns for population health applications.

---

## Purpose

Most AI systems in public health are designed to answer questions on demand.

This system is designed differently. It monitors live environmental signals, reasons over emerging trends, and supports operational decisions — before conditions become critical.

The primary use case is respiratory health risk assessment using real-time Air Quality Index (AQI) and PM2.5 data, with AI-generated public health advisories constrained to reason only from explicitly available environmental data.

This project demonstrates a **Level 3 agentic AI pattern** — an agent with live external API access — built on top of prior agentic levels:

This project demonstrates a **Level 4-lite agentic AI pattern** — a signal-aware decision agent — built on top of prior agentic levels:

| Level | Pattern | Description |
|-------|---------|-------------|
| Level 1 | Reasoning-only agent | Public health advisory logic without external data |
| Level 2 | Knowledge-grounded agent | Agent augmented with domain/public health guidance |
| Level 3 | Live tool-use agent | Agent with real-time AQI API + geospatial resolution |
| Level 4 | Signal-aware decision agent | Agent interprets environmental trends (PM2.5 trajectory) and generates contextual public health recommendations ← *this build* |

---

## What This System Does

- This is a **Level 4 signal-aware decision agent** — it does not simply retrieve and report live data. It interprets environmental trends over time and generates contextual public health recommendations based on trajectory, not just threshold.
- **Monitors live AQI conditions** via real-time API integration
- **Resolves geospatial location** to provide jurisdiction-specific risk context
- **Analyzes PM2.5 trends** to distinguish current risk from emerging risk
- **Generates AI-powered public health advisories** using Azure OpenAI, constrained to available environmental data only
- **Flags early warning patterns** before AQI thresholds reach critical levels
- **Deploys as a live web application** via Streamlit for operational use

---

## Why This Matters for Public Health

Air quality events — wildfire smoke, industrial pollution episodes, seasonal PM2.5 spikes — require rapid, evidence-based public health communication. Current workflows often depend on manual monitoring, delayed reporting, and centralized analysis that cannot scale to real-time operational needs.

This system explores what it looks like when AI reasoning is tethered to live environmental signals, constrained by epidemiologic logic, and designed to support the kind of early warning that public health practitioners actually need.

The design principle throughout: **the AI reasons from what it knows, not what it assumes.**

---

## Architecture

### File Structure

```
respiratory-public-health-aqi-agent/
│
├── main_l3_script.py          # Code-driven API call version
├── main_l3_tool_call.py       # Tool-call version using function calling
├── app_streamlit.py           # Streamlit deployment interface
├── requirements.txt           # Dependencies
└── README.md
```

### Two Implementation Patterns

**Pattern 1 — Code-Driven (`main_l3_script.py`)**

Python directly calls the AQI API, retrieves live data, and sends structured results to the Azure OpenAI model for interpretation and advisory generation.

```
Python → AQI API → structured data → Azure OpenAI → public health advisory
```

Best for: controlled pipelines where data retrieval logic is explicit and auditable.

**Pattern 2 — Tool-Call (`main_l3_tool_call.py`)**

The Azure OpenAI model decides when to call the AQI tool based on the query context. The model orchestrates its own data retrieval.

```
Azure OpenAI → decides to call AQI tool → retrieves live data → reasons → advisory
```

Best for: exploratory or conversational interfaces where the agent manages its own context.

---

## Decision Intelligence Layer

The core design challenge in this system was not the API integration. It was building a **Level 4 signal-aware decision layer** — specifically, an agent that reasons over PM2.5 trajectory rather than just current AQI values. This is what separates a live data lookup from genuine decision intelligence:

- Distinguishing **current risk** (AQI threshold exceeded now) from **emerging risk** (PM2.5 trend pointing toward threshold)
- Constraining the AI to reason **only from explicitly available environmental data** — no hallucinated context
- Generating advisories that are **explainable and operationally useful** for public health practitioners
- Balancing **sensitivity** (catch early warning signals) with **specificity** (avoid alert fatigue)

These are epidemiologic design decisions, not just engineering decisions. They reflect the EpiOps principle: AI systems in public health require domain governance embedded at the reasoning layer, not just at the data layer.

---

## Technical Stack

| Component | Technology |
|-----------|-----------|
| AI Reasoning | Azure OpenAI (GPT-4 series) |
| Air Quality Data | IQAir / OpenWeatherMap AQI API |
| Geospatial Resolution | IP-based and query-based location resolution |
| Trend Analysis | PM2.5 time-series logic |
| Deployment | Streamlit Cloud |
| Language | Python 3.10+ |

---

## Getting Started

### Prerequisites

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file with the following:

```
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_DEPLOYMENT=your_deployment_name
AQI_API_KEY=your_aqi_api_key
```

### Run Locally

```bash
# Code-driven version
python main_l3_script.py

# Tool-call version
python main_l3_tool_call.py

# Streamlit app
streamlit run app_streamlit.py
```

---

## Intended Audience

This system is designed for exploration and feedback from:

- **Epidemiologists** evaluating AI-assisted environmental health surveillance
- **Environmental health professionals** assessing real-time advisory logic
- **Emergency preparedness teams** exploring early warning system design
- **Public health informatics practitioners** building operational AI workflows
- **Healthcare AI builders** interested in constrained, domain-governed reasoning systems

---

## Limitations and Honest Caveats

This is a research and exploration build, not a production public health system.

- AQI data accuracy depends on the coverage and calibration of the underlying monitoring network
- Geospatial resolution is approximate and may not reflect hyperlocal air quality variation
- AI-generated advisories should be reviewed by qualified public health professionals before operational use
- PM2.5 trend analysis uses simplified logic and has not been validated against clinical outcomes

---

## Connection to EpiOps

This project is part of a broader exploration of **EpiOps** — the operational framework for embedding epidemiologic governance into public health AI and data infrastructure.

The principle demonstrated here: AI reasoning in public health must be constrained by domain logic, tethered to real-world signals, and designed so that the system's outputs are trustworthy enough for a practitioner to act on.

More on the EpiOps framework: [Medium — Why Data Modernization in Public Health Matters](https://medium.com/@saikurmana/why-data-modernization-in-public-health-matters-and-how-to-actually-achieve-it-5973da876ca2)

---

## Author

**Sai Kurmana, MPH, MS, CPHIMS**
Healthcare Data & AI Executive | Public Health Scientist | Creator of EpiOps

[LinkedIn](https://www.linkedin.com/in/sai-kurmana/) | [GitHub](https://github.com/SaiKurmana) | [Medium/Substack](https://epiops.substack.com)

---

## Contributing

Feedback from public health practitioners, epidemiologists, and healthcare AI builders is actively welcomed. Open an issue or reach out directly via LinkedIn.

---

*Built as part of the BeSA Solutions Architect program — exploring agentic AI patterns for population health applications.*
