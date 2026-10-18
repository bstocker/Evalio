"""Point d'entree WSGI (PythonAnywhere pointe sur ce fichier)."""

import os

from atelier import create_app

app = create_app()

if __name__ == "__main__":
    # utile en local uniquement ; ATELIER_HOST=0.0.0.0 pour l'ouvrir au
    # reseau de la salle, sans le debogueur interactif dans ce cas.
    host = os.environ.get("ATELIER_HOST", "127.0.0.1")
    app.run(host=host, port=5000, debug=host == "127.0.0.1")
