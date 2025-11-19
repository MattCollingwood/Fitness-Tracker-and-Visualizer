# Fitness Tracker & Visualizer

A Python dashboard for tracking, analyzing, and visualizing fitness data — designed to help you make sense of your workouts, trends, and performance over time.

---

## Table of Contents

- [About](#about)  
- [Features](#features)  
- [Data](#data)  
- [Getting Started](#getting-started)  
  - [Prerequisites](#prerequisites)  
  - [Installation](#installation)  
- [Usage](#usage)  
- [Project Structure](#project-structure)  
- [How It Works](#how-it-works)  
- [License](#license)  

---

## About

This project allows you to seamlessly track your workouts (running, swimming, gym, etc.) and visualize them through an interactive dashboard. By leveraging your exported fitness data (e.g., from a smartwatch or fitness app), the tool helps you dive into your training history, analyze trends, and understand your performance over time.

---

## Features

- Import workout data from CSV (or other supported formats)  
- Interactive dashboard built with **Dash** + **Plotly**  
- Trend line charts (distance, duration, heart rate, etc.)  
- Workout-level detail: filter by date, type, or metrics  
- Summary metrics: weekly, monthly, or yearly totals  
- Visualizations: scatter plots, histograms, pie charts  
- Export insights or charts to images or HTML (if implemented)

---

## Data

To use this project, you’ll need:

- Your fitness data exported as `.csv` files  
- (Optional) Processed summary data (aggregate workout metrics)  
- An understanding of the schema: what columns your data has (distance, time, heart rate, etc.)

> **Tip**: If you’re exporting from a watch/app, make sure your export includes at least date, distance (or workout volume), and time — those are key for most visualizations.

---

## Getting Started

### Prerequisites

- Python 3.8+  
- A working Python environment (virtualenv or conda recommended)  
- Your fitness data CSV files

### Installation

1. **Clone the repo**  
   ```bash
   git clone https://github.com/MattCollingwood/Fitness-Tracker-and-Visualizer.git  
   cd Fitness-Tracker-and-Visualizer


2. **Set up a virtual environment**
```
python3 -m venv venv  
source venv/bin/activate  # or `.\venv\Scripts\activate` on Windows  
```

3. **Install dependencies**
```
pip install -r requirements.txt
```

### Usage

1. Place your data files in the assets/ (or similar) folder.
2. Run the dashboard:
```
python app.py
```
3. Open your browser to http://127.0.0.1:8050/ (or the local address Dash gives you).
4. Use the UI to:
    -View trend charts
    -Filter workouts by date
    -Select and inspect specific workout details
    -Explore different visualizations of your fitness data

### Project Structure
```
Fitness-Tracker-and-Visualizer/
│
├── assets/                     # Folder for your raw/processed CSV data  
│   ├── workouts.csv  
│   └── summary.csv  
│
├── app.py                       # Main Dash app  
├── data_processing.py           # (optional) scripts to clean / transform data  
├── visualizations.py             # (optional) helper functions for charts  
├── requirements.txt              # Python dependencies  
└── README.md                     # This file  
```

### How It Works
1. **Data Loading**: The app reads CSV files, processes date columns, sets indexes.
2. **Data Aggregation (if applicable)**: Computes summary metrics such as weekly or monthly totals.
3. **Dash App Layout**: Uses dash_bootstrap_components for layout, with graphs and tables.
4. **Callbacks:**
    -For filtering by date or workout
    -For updating visualizations (e.g., line charts, pie charts)
    -For updating detail cards (e.g., workout duration, distance)
5. **Visualization**: Uses Plotly Express (or Plotly) to create interactive charts.

### License

This project is MIT Licensed — see the LICENSE
 file for more details.
