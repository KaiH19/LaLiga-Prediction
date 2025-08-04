import dash
from dash import dcc, html, Input, Output, State, ctx, MATCH, ALL
import pandas as pd
import numpy as np
import joblib

# Load model and define features
rf_model = joblib.load("artifacts/model_random_forest_rf.pkl")
feature_cols = ['Points', 'GoalsScored', 'GoalsConceded', 'GoalDifference', 'WinRate', 'AvgGoals']

# Load real dataset
data_df = pd.read_csv("artifacts/predictions.csv")
data_df = data_df.dropna(subset=feature_cols + ['Team'])

# Manually defined teams and logo filenames
teams = [
    {"name": "Barcelona", "logo": "FC-Barcelona.png"},
    {"name": "Real Madrid", "logo": "Real-Madrid.png"},
    {"name": "Atlético Madrid", "logo": "atltico-madrid.png"},
    {"name": "Real Sociedad", "logo": "real-sociedad.png"},
    {"name": "Villarreal", "logo": "villarreal_cf.png"},
    {"name": "Real Betis", "logo": "real_betis.png"},
    {"name": "Osasuna", "logo": "ca_osasuna.png"},
    {"name": "Athletic Club", "logo": "athletic_bilbao.png"},
    {"name": "Mallorca", "logo": "rcd_mallorca.png"},
    {"name": "Girona", "logo": "girona_fc.png"},
    {"name": "Rayo Vallecano", "logo": "rayo-vallecano.png"},
    {"name": "Sevilla", "logo": "sevilla_fc.png"},
    {"name": "Celta Vigo", "logo": "celta_vigo.png"},
    {"name": "Cádiz", "logo": "cadiz_cf.png"},
    {"name": "Getafe", "logo": "getafe_cf.png"},
    {"name": "Valencia", "logo": "valencia_cf.png"},
    {"name": "Almería", "logo": "UD-Almeria.png"},
    {"name": "Valladolid", "logo": "Vallodollid.png"},
    {"name": "Espanyol", "logo": "Espanyol.png"},
    {"name": "Elche", "logo": "Elche.png"}
]

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

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
                n_clicks=0
            )
            for team in teams
        ],
        style={"display": "flex", "flexWrap": "wrap", "justifyContent": "center", "gap": "10px"}
    ),
    html.Div(id="slider-container", style={"textAlign": "center", "marginBottom": "20px"}),
    html.Div(id="simulation-output", style={"textAlign": "center", "fontSize": "18px"})
])

def get_real_team_features(team_name, seed):
    team_data = data_df[data_df["Team"] == team_name]
    if team_data.empty:
        return None
    np.random.seed(seed)
    sample = team_data.sample(1, random_state=seed)
    return sample[feature_cols].iloc[0].to_dict()

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
                   marks={i: str(i) for i in range(1, 11)}, tooltip={"placement": "bottom"},
                   updatemode="drag"),
        html.Br(),
        html.Button("Simulate", id="simulate-btn"),
        html.Div(id="selected-team", style={"display": "none"}, children=team_selected)
    ])

@app.callback(
    Output("simulation-output", "children"),
    Input("simulate-btn", "n_clicks"),
    State("season-slider", "value"),
    State("selected-team", "children"),
    prevent_initial_call=True
)
def simulate_results(n_clicks, num_seasons, team_name):
    predictions = []
    for i in range(num_seasons):
        features = get_real_team_features(team_name, seed=i)
        if features is None:
            continue
        input_df = pd.DataFrame([features])[feature_cols]
        pred = rf_model.predict(input_df)[0]
        predictions.append(pred)

    win_count = sum(predictions)
    return html.Div([
        html.H2(f"{team_name} - Simulation Results for {num_seasons} Season(s)", style={"textAlign": "center"}),
        html.P(f"Predicted Wins: {win_count} out of {num_seasons}"),
        html.P(f"Season-by-Season: {' | '.join(str(p) for p in predictions)}"),
        html.P("Winner (1), Not Winner (0)")
    ])

if __name__ == "__main__":
    app.run(debug=True)
