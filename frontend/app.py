from dash import Dash, html, dcc, Input, Output, State
import requests

# Créer l'application Dash
app = Dash(__name__)

# Structure de la page
app.layout = html.Div([
    html.H1("Chatbot GPT avec Dash", style={"textAlign": "center"}),

    dcc.Textarea(
        id="user-input",
        placeholder="Écrivez votre message ici...",
        style={"width": "100%", "height": "100px"}
    ),
    html.Button("Envoyer", id="submit-button", n_clicks=0),

    html.Div(id="chat-history", children=[], style={
        "marginTop": "20px",
        "padding": "10px",
        "border": "1px solid #ccc",
        "borderRadius": "5px",
        "height": "300px",
        "overflowY": "scroll",
        "backgroundColor": "#f9f9f9"
    })
])

# Historique des messages
chat_history = []

# Callback pour gérer l'envoi et l'affichage des messages
@app.callback(
    Output("chat-history", "children"),
    [Input("submit-button", "n_clicks")],
    [State("user-input", "value")]
)
def update_chat(n_clicks, user_input):
    global chat_history

    if n_clicks > 0 and user_input:
        # Envoyer le message à l'API Flask (backend)
        try:
            response = requests.post(
                "http://0.0.0.0:5000/chat",  # URL de ton backend Flask
                # "http://127.0.0.1:5000/chat",  # URL de ton backend Flask
                #"http://localhost:5000/chat",
                json={"message": user_input}
            )
            bot_response = response.json().get("response", "Erreur : Pas de réponse.")
        except Exception as e:
            bot_response = f"Erreur de connexion : {e}"

        # Ajouter le message utilisateur et la réponse du bot à l'historique
        chat_history.append(html.Div([
            html.P(f"👤 Utilisateur : {user_input}", style={"color": "blue"}),
            html.P(f"🤖 Bot : {bot_response}", style={"color": "green"})
        ]))

    # Réinitialiser le champ d'entrée
    return chat_history

# Lancer le serveur Dash
if __name__ == "__main__":
    app.run_server(debug=True)