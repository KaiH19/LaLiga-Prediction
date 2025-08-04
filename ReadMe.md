# La Liga Winner Prediction System

## Overview
This project predicts La Liga season winners using machine learning and historical data from the past 10 years. By engineering rich, season-level features like Elo ratings, squad market value, and win rates, it trains multiple models to forecast the top-performing teams. The results are deployed as an interactive Dash web app hosted on Render, enabling users to simulate seasons and visualize projected outcomes.

## Team Member
Kai Hinterholzer

## Features
- **Historical Data Processing**: Cleaned and combined datasets from FBref, Understat, and Kaggle.
- **Feature Engineering**: Created derived features like Elo ratings, goal differentials, and win percentages.
- **Model Training**: Trained and compared MLP (Multilayer Perceptron) and Random Forest classifiers.
- **Season Simulation**: Simulated final league standings from user input via Dash.
- **Web Deployment**: Hosted app on [Render](https://render.com) for real-time interaction.
- **Data Visualization**: Included performance charts and confidence metrics to support predictions.

## Technologies Used
- **Languages & Libraries**: Python, Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn, XGBoost
- **ML Models**: MLPClassifier, Random Forest, Logistic Regression
- **App Framework**: Plotly Dash
- **Deployment**: Render.com
- **Data Sources**: FBref, Understat, Kaggle

## Prerequisites
Ensure you have the following installed:
- Python 3.9+
- pip or conda
- Git

