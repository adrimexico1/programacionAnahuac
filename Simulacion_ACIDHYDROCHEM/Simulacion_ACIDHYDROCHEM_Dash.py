import dash
from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
from scipy.integrate import solve_ivp
import numpy as np
import plotly.graph_objects as go
import pandas as pd

# Aplicación Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "ACIDHYDROCHEM Simulator V0.1"

# Layout de la aplicación
app.layout = dbc.Container(
    [
        html.H1("ACIDHYDROCHEM Simulator V0.1", className="text-center my-4"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Razón Líquido/Sólido (kg):"),
                        dbc.Input(id="lsr", type="number", placeholder="Ejemplo: 10", value=10),
                        html.Label("Razón Sólido:"),
                        dbc.Input(id="rs", type="number", placeholder="Ejemplo: 5", value=5),
                        html.Label("Concentración Ácida:"),
                        dbc.Input(id="acid", type="number", placeholder="Ejemplo: 0.5", value=0.5),
                        html.Label("Tiempo de Residencia:"),
                        dbc.Input(id="residence", type="number", placeholder="Ejemplo: 10", value=10),
                        dbc.Button("Simular", id="simulate-btn", color="primary", className="mt-3 me-2"),
                        dbc.Button("Reiniciar", id="reset-btn", color="danger", className="mt-3"),
                        html.Div(id="output-message", className="mt-3"),
                    ],
                    width=4,
                ),
                dbc.Col(
                    [
                        dcc.Graph(id="simulation-graph"),
                        dbc.Row(
                            [
                                dbc.Button("Exportar CSV", id="export-csv-btn", color="success"),
                            ],
                            className="mt-3",
                        ),
                        dcc.Download(id="download-csv"),  # Agregar componente de descarga
                    ],
                    width=8,
                ),
            ]
        ),
    ],
    fluid=True,
)


# Callback para ejecutar la simulación o reiniciar
@app.callback(
    [
        Output("lsr", "value"),
        Output("rs", "value"),
        Output("acid", "value"),
        Output("residence", "value"),
        Output("simulation-graph", "figure"),
        Output("output-message", "children"),
    ],
    [Input("simulate-btn", "n_clicks"), Input("reset-btn", "n_clicks")],
    [
        State("lsr", "value"),
        State("rs", "value"),
        State("acid", "value"),
        State("residence", "value"),
    ],
)
def handle_simulation_or_reset(simulate_clicks, reset_clicks, lsr, rs, acid_concentration, residence_time):
    ctx = callback_context  # Determina qué botón fue presionado

    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger_id == "reset-btn":
        # Reiniciar valores y limpiar gráfica
        empty_fig = go.Figure()
        empty_fig.update_layout(
            title="Resultados de la Simulación",
            xaxis_title="Tiempo",
            yaxis_title="Concentraciones",
            template="plotly_white",
        )
        return [10, 5, 0.5, 10, empty_fig, ""]

    elif trigger_id == "simulate-btn":
        # Ejecutar simulación
        # Parámetros cinéticos y constantes
        kH0 = 7.709e8
        EH = 20301.9
        βH = 1
        R = 1.98
        kX0 = 2.6e8
        EX = 20312
        βX = 0.15
        T = 121.1 + 273.15
        ρa = 1.84

        # Cálculo del factor Φ
        RL = lsr * ρa
        Φ = RL / rs

        # Definir las ecuaciones diferenciales
        def acidH(t, u):
            du1 = -kH0 * acid_concentration**βH * np.exp(-(EH / (R * T))) * u[0] * Φ
            du2 = (
                kH0 * acid_concentration**βH * np.exp(-(EH / (R * T))) * u[0] * Φ
                - kX0 * acid_concentration**βX * np.exp(-(EX / (R * T))) * u[1] * Φ
            )
            du3 = (
                kH0 * acid_concentration**βH * np.exp(-(EH / (R * T))) * u[0]
                - kX0
                * acid_concentration**βX
                * np.exp(-(EX / (R * T)))
                * u[1]
                * 0.7
                * Φ
            )
            return [du1, du2, du3]

        # Condiciones iniciales
        u0 = [70, 0, 0]
        t_span = (0, residence_time)
        t_eval = np.linspace(0, residence_time, 100)

        # Resolver las ecuaciones diferenciales
        solution = solve_ivp(acidH, t_span, u0, method="RK45", t_eval=t_eval)

        # Crear el gráfico con Plotly
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=solution.t, y=solution.y[0], mode="lines", name="Hemicelulosa", line=dict(color="blue")
            )
        )
        fig.add_trace(
            go.Scatter(
                x=solution.t, y=solution.y[1], mode="lines", name="Xilosa", line=dict(color="green")
            )
        )
        fig.add_trace(
            go.Scatter(
                x=solution.t, y=solution.y[2], mode="lines", name="Furfural", line=dict(color="red")
            )
        )
        fig.update_layout(
            title="Resultados de la Simulación",
            xaxis_title="Tiempo",
            yaxis_title="Concentraciones",
            template="plotly_white",
        )

        return [lsr, rs, acid_concentration, residence_time, fig, "Simulación completada exitosamente."]


# Callback para exportar datos a CSV
@app.callback(
    Output("download-csv", "data"),
    Input("export-csv-btn", "n_clicks"),
    State("residence", "value"),
)
def export_to_csv(n_clicks, residence_time):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate

    # Crear datos simulados como ejemplo
    data = {
        "Tiempo": np.linspace(0, residence_time, 100),
        "Hemicelulosa": np.random.random(100),  # Simula datos
        "Xilosa": np.random.random(100),
        "Furfural": np.random.random(100),
    }
    df = pd.DataFrame(data)

    return dcc.send_data_frame(df.to_csv, "simulacion_resultados.csv")


# Ejecutar la aplicación
if __name__ == "__main__":
    app.run_server(debug=True)
