# Multi-AI-Agent Fitness Assistant

An intelligent, multi-agent fitness companion built with Python, Streamlit, Gemini AI API, and Docker.

## Project Overview

This project features a system of specialized AI agents that work together via an orchestrator to provide personalized fitness assessment, workout planning, nutrition advice, and motivation. The system is designed for scalable web access through a Streamlit interface, containerized with Docker.

## Features

- Fitness Assessment Agent: Evaluates user’s fitness baseline and goals
- Nutrition Agent: Generates tailored meal plans and dietary advice
- Exercise Agent: Designs customized workout routines based on goals and fitness level
- Motivation Agent: Delivers context-aware motivational messages and reminders
- Orchestrator: Coordinates the agents, manages context, and ensures coherent responses using the Gemini AI API
- Streamlit UI: User-friendly web app for interacting with the system
- Docker Deployment: Containerized application for easy deployment and scalability

## Tech Stack

- Programming: Python
- AI / LLM: Gemini AI API
- Web Interface: Streamlit
- API / Backend: Python modules, agents and orchestrator logic
- Containerization: Docker
- Data Handling: Pandas, NumPy

## How It Works

1. The user enters fitness information and goals via the Streamlit app
2. The Orchestrator sends context to the appropriate agents (assessment to nutrition, exercise to motivation)
3. Each agent uses the Gemini AI API to generate insights, recommendations, or motivational messages
4. The Orchestrator collates agent outputs and delivers a final response to the user via the UI
5. The application runs within a Docker container for portability and scalability

## Getting Started

### Prerequisites

- Docker installed on your machine
- Valid Gemini AI API key stored in a `.env` file
- Python 3.x environment (if running without Docker)

### Setup

1. Clone the repository

git clone https://github.com/minnu1102/Fitness-assistent.git

cd Fitness-assistent


2. Create a `.env` file in the root directory with your API key



GEMINI_API_KEY=your_api_key_here


3. Build and run via Docker



docker build -t multi-ai-fitness .
docker run --env-file .env -p 8501:8501 multi-ai-fitness


4. Open your browser and navigate to `http://localhost:8501` for the UI

## Project Structure

- .env
- app.py: Main entry point
- orchestrator_agent.py
- assessment_agent.py
- exercise_agent.py
- nutrition_agent.py
- motivation_agent.py
- streamlit_app.py: UI definition
- requirements.txt
- Dockerfile

## Impact and Usage

- Demonstrates multi-agent AI architecture leveraging LLM workflows
- Provides personalized fitness advice accessible through a web interface
- Structured for scalability and production readiness using Docker
- Showcases full-stack AI engineering capabilities including models, APIs, UI, and deployment

## Contribution

Contributions are welcome. Features like workout logging, analytics dashboards, progress tracking, or UI improvements are encouraged. Please fork the repository and create a pull request.

## License and Acknowledgements

This project is open-source and free to use and modify. Thanks to the Gemini AI API and the open-source Python community tools.

## Contact

For questions or feedback, reach out via GitHub Issues or email at `poorna.trishitha@gmail.com
