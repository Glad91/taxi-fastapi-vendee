# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Running the application
```bash
# Install dependencies
pip install -r requirements.txt

# Start the development server with auto-reload
uvicorn main:app --reload

# Start the server on a specific host/port
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Testing
- Use the `test_main.http` file for manual API testing with HTTP requests
- The FastAPI automatic documentation is available at `http://127.0.0.1:8000/docs` when running

## Architecture Overview

This is a FastAPI application that calculates taxi fares for Vendée, France based on official 2025 rates.

### Core Components

**CalculateurTarifsTaxi Class** (`main.py:8-79`)
- Contains all fare calculation logic with official Vendée 2025 rates
- Handles different tariff types (A, B, C, D) based on time and trip type
- Manages night/day rates, weekend/holiday rates, and round-trip vs one-way pricing

**API Endpoints** (`main.py:130-193`)
- `/verifier-sante` - Health check endpoint
- `/calculer-tarif` - POST endpoint for detailed fare calculation
- `/tarifs` - GET endpoint to retrieve current rates
- `/estimation-rapide` - GET endpoint for quick fare estimates

**Pydantic Models** (`main.py:83-116`)
- `CourseRequete`: Input validation for fare calculation requests
- `CourseReponse`: Structured response for detailed calculations
- `EstimationRapideReponse`: Response for quick estimates

### Key Business Logic

**Tariff System:**
- Tariff A: €1.08/km for round-trip day rides
- Tariff B: €1.62/km for round-trip night/weekend/holiday rides
- Tariff C: €2.16/km for one-way day rides
- Tariff D: €3.24/km for one-way night/weekend/holiday rides
- Base fare: €2.94
- Waiting time: €29.44/hour (€0.49/minute)
- Minimum fare: €8.00
- Night hours: 19:00-07:00

**Date/Time Logic:**
- Night rates apply from 19:00 to 07:00
- Sunday is considered a holiday (higher rates)
- Round-trip vs one-way affects the per-kilometer rate significantly

## File Structure

- `main.py` - Single file containing the entire application
- `requirements.txt` - Python dependencies (FastAPI, uvicorn, pydantic)
- `test_main.http` - HTTP test requests for manual testing