import dash
from dash import dcc, html, Input, Output, State
import pandas as pd
import numpy as np
import joblib
from tensorflow.keras.models import load_model

# Load models
log_model = joblib.load("artifacts/model_logistic.pkl")
rf_model = joblib.load("artifacts/model_random_forest_rf.h5")  # Should be .pkl ideally
mlp_model = load_model("artifacts/model_mlp.h5")

# Features used across all models
feature_cols = ['Points', 'GoalsScored', 'GoalsConceded', 'GoalDifference', 'WinRate', 'AvgGoals']

# Dash App
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("🏆 La Liga Winner Prediction"),

    html.Div([
        html.Label(f"{feature}:"),
        dcc.Input(id=feature, type='number', value=0, step=0.1)
        for feature in feature_cols
    ]),

    html.Br(),
    html.Button("Predict", id="predict-btn"),
    html.Br(), html.Br(),

    html.Div(id="prediction-output")
])

@app.callback(
    Output("prediction-output", "children"),
    Input("predict-btn", "n_clicks"),
    [State(f, 'value') for f in feature_cols]
)
def predict(n_clicks, *values):
    if not n_clicks:
        return ""

    input_array = np.array(values).reshape(1, -1)

    # Predictions
    log_pred = log_model.predict(input_array)[0]
    rf_pred = rf_model.predict(input_array)[0]
    mlp_pred = mlp_model.predict(input_array)
    mlp_pred_class = int(mlp_pred[0][0] > 0.5)  # Assuming binary sigmoid output

    return html.Div([
        html.H4(f"Logistic Regression Prediction: {log_pred}"),
        html.H4(f"Random Forest Prediction: {rf_pred}"),
        html.H4(f"MLP Prediction: {mlp_pred_class}")
    ])

if __name__ == "__main__":
    app.run_server(debug=True)
