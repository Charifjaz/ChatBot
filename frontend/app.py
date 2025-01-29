from dash import Dash, html, dcc, Input, Output, State
import requests
from datetime import datetime

app = Dash(__name__, assets_folder="assets", suppress_callback_exceptions=True)

# Initialiser chat_history avant de l'utiliser
chat_history = []


app.layout = html.Div([
    html.Div(className="main-container", children=[
        html.Header(className="header", children=[
            html.H1("Charif Is Listenning ! How Can I help you ?", className="title")
        ]),
        
        html.Div(className="chat-container", children=[
            html.Div(id="chat-history", className="chat-history"),
            
            html.Div(className="input-wrapper", children=[
                dcc.Textarea(
                    id="user-input",
                    className="input-field",
                    placeholder="Waiting for your Inouts !",
                    spellCheck=True
                ),
                html.Button(
                    html.Div(className="send-arrow"),
                    id="submit-button",
                    className="send-button",
                    n_clicks=0
                )
            ])
        ])
    ])
])

@app.callback(
    Output("chat-history", "children"),
    [Input("submit-button", "n_clicks")],
    [State("user-input", "value")]
)
def update_chat(n_clicks, user_input):
    global chat_history
    
    if n_clicks > 0 and user_input:
        try:
            response = requests.post(
                # "http://backend:5000/chat",
                "http://localhost:5000/chat",
                json={"message": user_input}
            )
            bot_response = response.json().get("response", "Erreur : Pas de réponse.")
        except Exception as e:
            bot_response = f"Erreur de connexion : {e}"

        # Message utilisateur
        user_message = html.Div(
            html.Div([
                html.P(user_input, className="message-text"),
                html.Span(datetime.now().strftime("%H:%M"), className="message-time")
            ]),
            className="message user"
        )
        
        # Message bot
        bot_message = html.Div(
            html.Div([
                html.P(bot_response, className="message-text"),
                html.Span(datetime.now().strftime("%H:%M"), className="message-time")
            ]),
            className="message bot"
        )

        chat_history.extend([user_message, bot_message])
    
    return chat_history

if __name__ == "__main__":
    app.run_server(debug=True)