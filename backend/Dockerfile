# Utiliser une image Python minimale
FROM python:3.12-slim

# Définir le répertoire de travail
WORKDIR /app
# COPY ./backend /app


# Installer uniquement les dépendances nécessaires
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# Copier les fichiers du backend
# COPY . .

# Supprimer les fichiers temporaires pour réduire la taille de l'image
# RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Créer et se déplacer dans le répertoire /app

# Copier tous les fichiers du backend dans /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

# COPY requirements.txt .



# Exposer le port Fldask
EXPOSE 5000

# Lancer l'application
CMD ["python", "app.py"]
