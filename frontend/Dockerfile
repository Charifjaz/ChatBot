# Utiliser l'image officielle Python
FROM python:3.12-alpine

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers nécessaires dans le conteneur
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Exposer le port 8050 pour Dash
EXPOSE 8050

# Commande pour lancer le frontend Dash
CMD ["python", "app.py"]