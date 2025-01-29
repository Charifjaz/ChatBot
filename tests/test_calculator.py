# test_calculator.py
import sys
import os

# Ajoute le répertoire racine du projet au PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.calculator import add

def test_add():
    assert add(2, 3) == 5