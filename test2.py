import socketio
from flask import Flask, jsonify

# Crée une application Flask
app = Flask(__name__)

# Crée une instance de serveur Socket.IO
sio = socketio.Server(cors_allowed_origins="*")  # Configurez les origines autorisées selon vos besoins

# Attachez le serveur Socket.IO à l'application Flask
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

# Gestionnaire de route Flask normale
@app.route('/')
def index():
    return jsonify({'message': 'Succès'})

# Gestionnaire d'événement "connect" Socket.IO
@sio.event
def connect(sid, environ):
    print(f"Client connecté: {sid}")

# Gestionnaire d'événement "message" Socket.IO
@sio.event
def message(sid, data):
    print(f"Message reçu de {sid}: {data}")

    # Vous pouvez ajouter ici la logique pour répondre au client si nécessaire

# Gestionnaire d'événement "disconnect" Socket.IO
@sio.event
def disconnect(sid):
    print(f"Client déconnecté: {sid}")

if __name__ == '__main__':
    # Démarrez l'application Flask avec Socket.IO sur le port 5000
    app.run(host='0.0.0.0', port=5010)
