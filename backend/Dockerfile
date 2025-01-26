# Utiliser une image Python minimale
FROM python:3.12-alpine

# Définir le répertoire de travail
WORKDIR /app

# Installer uniquement les dépendances nécessaires
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier les fichiers du backend
COPY . .

# Supprimer les fichiers temporaires pour réduire la taille de l'image
# RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Exposer le port Flask
EXPOSE 5000

# Lancer l'application
CMD ["python", "app.py"]
