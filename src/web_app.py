import dash
from dash import dcc, html, Input, Output, State, ctx, MATCH, ALL
import random
import numpy as np
import pandas as pd
import joblib

# Load Random Forest model
rf_model = joblib.load("artifacts/model_random_forest_rf.pkl")

# Feature columns (same order used in training)
feature_cols = ['Points', 'GoalsScored', 'GoalsConceded', 'GoalDifference', 'WinRate', 'AvgGoals']

# La Liga team list with image names (you must add these images to assets/)
teams = [
    {"name": "Barcelona", "logo": "FC-Barcelona.png"},#
    {"name": "Real Madrid", "logo": "Real-Madrid.png"},#
    {"name": "Atlético Madrid", "logo": "atltico-madrid.png"},#
    {"name": "Real Sociedad", "logo": "real-sociedad.png"},#
    {"name": "Villarreal", "logo": "villarreal_cf.png"},#
    {"name": "Real Betis", "logo": "real_betis.png"},#
    {"name": "Osasuna", "logo": "ca_osasuna.png"},#
    {"name": "Athletic Club", "logo": "athletic_bilbao.png"},#
    {"name": "Mallorca", "logo": "rcd_mallorca.png"},#
    {"name": "Girona", "logo": "girona_fc.png"},#
    {"name": "Rayo Vallecano", "logo": "rayo-vallecano.png"},#
    {"name": "Sevilla", "logo": "sevilla_fc.png"},#
    {"name": "Celta Vigo", "logo": "celta_vigo.png"},#
    {"name": "Cádiz", "logo": "cadiz_cf.png"},#
    {"name": "Getafe", "logo": "getafe_cf.png"},#
    {"name": "Valencia", "logo": "valencia_cf.png"},#
    {"name": "Almería", "logo": "UD-Almeria.png"},#
    {"name": "Valladolid", "logo": "Vallodollid.png"},
    {"name": "Espanyol", "logo": "Espanyol.png"},
    {"name": "Elche", "logo": "Elche.png"}
]

# Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# Layout
app.layout = html.Div([
    html.Img(src="/assets/LaLiga_logo.png", style={"height": "100px", "display": "block", "margin": "auto"}),
    
    html.H2("Select a Team", style={"textAlign": "center"}),

    html.Div(
        children=[
            html.Div(
                id={'type': 'team-card', 'index': team["name"]},
                className="team-card",
                children=[
                    html.Img(src=f"/assets/{team['logo']}", style={"height": "60px", "marginBottom": "10px"}),
                    html.Div(team["name"])
                ],
                n_clicks=0,
                style={
                    "cursor": "pointer",
                    "width": "120px",
                    "height": "120px",
                    "margin": "10px",
                    "textAlign": "center",
                    "backgroundColor": "#1e1e1e",
                    "borderRadius": "10px",
                    "padding": "10px",
                    "color": "white",
                    "display": "flex",
                    "flexDirection": "column",
                    "justifyContent": "center",
                    "alignItems": "center",
                    "transition": "transform 0.2s"
                }
            )
            for team in teams
        ],
        style={
            "display": "flex",
            "flexWrap": "wrap",
            "justifyContent": "center",
            "gap": "10px"
        }
    ),

    html.Div(id="slider-container", style={"textAlign": "center", "marginBottom": "20px"}),
    html.Div(id="simulation-output", style={"textAlign": "center", "fontSize": "18px"})
]),

# Dummy feature generator — to be replaced with real features later
def generate_team_features(team_name, seed):
    np.random.seed(seed)
    return {
        "Points": np.random.randint(30, 100),
        "GoalsScored": np.random.randint(30, 90),
        "GoalsConceded": np.random.randint(20, 80),
        "GoalDifference": np.random.randint(-30, 60),
        "WinRate": np.random.randint(0, 100),
        "AvgGoals": np.random.randint(0, 5)
    }

# Show slider when team is selected
@app.callback(
    Output("slider-container", "children"),
    Input({'type': 'team-card', 'index': ALL}, 'n_clicks')
)
def show_slider(n_clicks_list):
    triggered = ctx.triggered_id
    if not triggered:
        return ""
    team_selected = triggered["index"]

    return html.Div([
        html.H3(f"{team_selected} selected"),
        html.Label("Seasons to simulate:"),
        dcc.Slider(id="season-slider", min=1, max=10, step=1, value=3,
                   marks={i: str(i) for i in range(1, 11)}, tooltip={"placement": "bottom"}),
        html.Br(),
        html.Button("Simulate", id="simulate-btn"),
        html.Div(id="selected-team", style={"display": "none"}, children=team_selected)
    ])

# Run simulation using Random Forest
@app.callback(
    Output("simulation-output", "children"),
    Input("simulate-btn", "n_clicks"),
    State("season-slider", "value"),
    State("selected-team", "children")
)
def simulate_with_rf(n_clicks, num_seasons, team_name):
    if not n_clicks:
        return ""

    predictions = []

    for i in range(num_seasons):
        features = generate_team_features(team_name, i)
        input_df = pd.DataFrame([features])[feature_cols]
        pred = rf_model.predict(input_df)[0]  # 1 = Win, 0 = Not Win
        predictions.append(pred)

    win_count = sum(predictions)
    return html.Div([
        html.H3(f"{team_name} - Simulation Results for {num_seasons} Season(s)"),
        html.P(f"Predicted Wins: {win_count} out of {num_seasons}"),
        html.P(f"Season-by-Season: {' | '.join(str(p) for p in predictions)}"),
        html.P("Winner (1), Not Winner (0)")
    ])

if __name__ == "__main__":
    app.run(debug=True)
