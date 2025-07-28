import dash
from dash import dcc, html, Input, Output, State, ctx
import random

# List of La Liga teams and logos
teams = [
    {"name": "Barcelona", "logo": "FC-Barcelona.png"},#
    {"name": "Real Madrid", "logo": "Real_Madrid.png"},#
    {"name": "Atlético Madrid", "logo": "atltico_madrid.png"},#
    {"name": "Real Sociedad", "logo": "real_sociedad.png"},#
    {"name": "Villarreal", "logo": "villarreal_cf.png"},#
    {"name": "Real Betis", "logo": "real_betis.png"},#
    {"name": "Osasuna", "logo": "ca_osasuna.png"},#
    {"name": "Athletic Club", "logo": "athletic_bilbao.png"},#
    {"name": "Mallorca", "logo": "rcd_mallorca.png"},#
    {"name": "Girona", "logo": "girona_fc.png"},#
    {"name": "Rayo Vallecano", "logo": "rayo_vallecano.png"},#
    {"name": "Sevilla", "logo": "sevilla_fc.png"},#
    {"name": "Celta Vigo", "logo": "celta_vigo.png"},#
    {"name": "Cádiz", "logo": "cadiz_cf.png"},#
    {"name": "Getafe", "logo": "getafe_cf.png"},#
    {"name": "Valencia", "logo": "valencia_cf.png"},#
    {"name": "Almería", "logo": "UD_Almería.png"},#
    {"name": "Valladolid", "logo": "Valladollid.png"},
    {"name": "Espanyol", "logo": "Espanyol.png"},
    {"name": "Elche", "logo": "Elche.png"}
]

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.Img(src=r"C:\Users\khint\OneDrive - belgiumcampus.ac.za\Documents\LaLiga Prediction\assets\LaLiga_logo.png", style={"height": "100px", "display": "block", "margin": "auto"}),
    
    html.H2("Select a Team", style={"textAlign": "center"}),

    html.Div(
        id="team-grid",
        children=[
            html.Div([
                html.Img(src=f"/assets/{team['logo']}", style={"height": "50px"}),
                html.Button(team["name"], id={'type': 'team-btn', 'index': team["name"]}, n_clicks=0)
            ], style={
                "display": "inline-block",
                "width": "120px",
                "margin": "10px",
                "textAlign": "center",
                "backgroundColor": "#1e1e1e",
                "borderRadius": "10px",
                "padding": "10px",
                "color": "white"
            })
            for team in teams
        ],
        style={"textAlign": "center", "marginBottom": "30px"}
    ),

    html.Div(id="slider-container", style={"textAlign": "center", "marginBottom": "20px"}),

    html.Div(id="simulation-output", style={"textAlign": "center", "fontSize": "18px"})
])

# Callback to show slider when team is selected
@app.callback(
    Output("slider-container", "children"),
    Input({'type': 'team-btn', 'index': dash.dependencies.ALL}, 'n_clicks'),
)
def show_slider(n_clicks_list):
    triggered_index = ctx.triggered_id
    if not triggered_index:
        return ""

    team_selected = triggered_index["index"]

    return html.Div([
        html.H3(f"{team_selected} selected"),
        html.Label("Seasons to simulate:"),
        dcc.Slider(id="season-slider", min=1, max=10, step=1, value=3,
                   marks={i: str(i) for i in range(1, 11)}, tooltip={"placement": "bottom"}),
        html.Br(),
        html.Button("Simulate", id="simulate-btn"),
        html.Div(id="selected-team", style={"display": "none"}, children=team_selected)
    ])

# Callback to simulate performance
@app.callback(
    Output("simulation-output", "children"),
    Input("simulate-btn", "n_clicks"),
    State("season-slider", "value"),
    State("selected-team", "children")
)
def simulate_season(n_clicks, num_seasons, team):
    if not n_clicks:
        return ""

    # Dummy simulation results (replace with real model later)
    finishes = [random.randint(1, 20) for _ in range(num_seasons)]
    avg_finish = sum(finishes) / num_seasons
    best = min(finishes)
    worst = max(finishes)

    return html.Div([
        html.H3(f"{team} Simulation Over {num_seasons} Season(s)"),
        html.P(f"Average League Finish: {avg_finish:.2f}"),
        html.P(f"Best Finish: {best}"),
        html.P(f"Worst Finish: {worst}"),
        html.P(f"Positions Each Season: {finishes}")
    ])
    
if __name__ == "__main__":
    app.run(debug=True)
