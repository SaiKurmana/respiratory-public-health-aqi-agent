# Respiratory Public Health Agent — Level 3 Local Build

## Purpose

This project demonstrates a Level 3 agentic AI pattern for a respiratory public health use case.

Level 3 adds live tool use to the prior agent levels:

- Level 1: reasoning-only public health agent
- Level 2: knowledge-grounded agent
- Level 3: agent with live external API access

This build uses live AQI data to support public health advisory decisions.

---

## Files

### `main_l3_script.py`

Code-driven API call version.

In this version, Python directly calls the AQI API first, retrieves live data, and then sends that data to the Foundry model for interpretation.

Pattern:

```text
Python code → AQI API → Foundry model → decision output