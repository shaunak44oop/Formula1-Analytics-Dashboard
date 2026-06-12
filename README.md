# F1 Analytics Dashboard

A Python-based desktop application for visualizing Formula 1 race data. This tool allows users to generate professional-grade race pace boxplots, qualifying gaps, telemetry comparisons, and spatial track dominance maps using the [FastF1](https://docs.fastf1.dev/) API.

## Why I Built This
As a diehard supporter of Lewis Hamilton and the motorsport Formula 1, I began to blog about different grands prix, their results and the strategy behind the whole moving circus. However, I wanted to add a more analytical, objective and intellectually profound element to my page, and this project was the perfect fit for it. My Analytics Dashboard helps me understand the raw pace of different drivers, where they lacked in braking before the corner or accelerating through the apex. It assists me in providing a much better review of the race itself for my page.

## Tech Stack
- **Python**: Core logic and automation.
- **Tkinter**: Custom GUI for interactive user experience.
- **FastF1**: Telemetry data processing and API integration.
- **Matplotlib**: High-fidelity chart rendering.

## Features
- **Automated Data Processing**: Fetches official session data dynamically.
- **Custom GUI**: Built-in threading for responsive UI while data processes.
- **Professional Reporting**: Differentiates team data with unique line styles and hues.

## Setup Instructions
1. Clone the repository: `git clone [YOUR_REPO_URL]`
2. Create a virtual environment: `python -m venv venv`
3. Activate: `.\venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Launch the app: `python gui.py`
