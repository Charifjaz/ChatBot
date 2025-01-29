from dash import Dash, html, dcc, Input, Output, State, clientside_callback, no_update
import dash
import requests
from datetime import datetime

app = Dash(__name__, assets_folder="assets", suppress_callback_exceptions=True)

app.layout = html.Div([
    html.Div(className="main-container", children=[
        html.Header(className="header", children=[
            html.H1("Charif Is Listening!", className="title")
        ]),
        
        html.Div(className="chat-container", children=[
            html.Div(id="chat-history", className="chat-history"),
            
            html.Div(className="input-wrapper", children=[
                dcc.Textarea(
                    id="user-input",
                    className="input-field",
                    placeholder="Écrivez votre message...",
                    spellCheck=True,
                    style={'whiteSpace': 'pre-wrap'},
                    persistence=True,
                ),
                html.Button(
                    html.Div(className="send-arrow"),
                    id="submit-button",
                    className="send-button",
                    n_clicks=0
                ),
                dcc.Store(id='event-trigger', data=0)
            ])
        ])
    ])
])

# Callback client-side pour gérer Entrée
clientside_callback(
    """
    function(n_blur, event) {
        const ctx = dash_clientside.callback_context;
        if (ctx.triggered[0].prop_id === "user-input.n_blur") {
            if (event && event.key === "Enter" && !event.shiftKey) {
                event.preventDefault();
                return Date.now();
            }
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output('event-trigger', 'data'),
    [Input('user-input', 'n_blur')],
    [State('user-input', 'n_blur_timestamp')],
    prevent_initial_call=True
)

# Callback principal
@app.callback(
    [Output("chat-history", "children"),
     Output("user-input", "value")],
    [Input("submit-button", "n_clicks"),
     Input("event-trigger", "data")],
    [State("user-input", "value"),
     State("chat-history", "children")]
)
def update_chat(n_clicks, trigger, user_input, existing_messages):
    ctx = dash.ctx

    if not ctx.triggered or not user_input or not user_input.strip():
        return existing_messages or [], no_update

    try:
        response = requests.post("http://backend:5000/chat", json={"message": user_input})
        bot_response = response.json().get("response", "Erreur : Pas de réponse.")
    except Exception as e:
        bot_response = f"Erreur de connexion : {str(e)}"

    new_messages = [
        html.Div([
            html.P(user_input, className="message-text"),
            html.Span(datetime.now().strftime("%H:%M"), className="message-time")
        ], className="message user"),
        html.Div([
            html.P(bot_response, className="message-text"),
            html.Span(datetime.now().strftime("%H:%M"), className="message-time")
        ], className="message bot")
    ]

    return (existing_messages or []) + new_messages, ""

if __name__ == "__main__":
    app.run_server(debug=True)