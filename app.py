from model_wrapper import WearDetectionModel
import configparser
from datastats import preprocessor
import socketio
import pandas as pd
import numpy as np
import pickle
from collections import Counter
import time
import paramiko
from flask_cors import CORS
from flask import Flask, request, render_template, jsonify


# Créez un client Socket.IO
sio = socketio.Client()
app = Flask(__name__)
CORS(app)


config_path = 'config.ini'
model = WearDetectionModel(config_path)
config = configparser.ConfigParser()
config.read(config_path)
PATH_DATA_TO_PREDICT = config.get('Paths', 'PATH_DATA_TO_PREDICT')


ssh_status = 1

max_buffer_size = 5000  # Nombre maximum de lignes avant la transformation

# Load the serialized data
path = "test_dir/replay.pkl"
with open(path, 'rb') as file:
    print("\t \t Loading processed data =========>>>>>>>>")
    df = pickle.load(file)
print(df.head())



@sio.event
def connect():
    print("connecté")
    sio.emit('data_request', {'key': 'value'})

@sio.event
def disconnect():
    print("Déconnecté du serveur")


def perform_prediction():
    print("permorming predictions")
    predictions = []
    signalt = []
    signalb = []

    max_buffer_size = 5000

    for i in range(0, 25000, max_buffer_size):
        data_chunk = df[i:i + max_buffer_size]
        print(len(data_chunk))
        for index, row in data_chunk.iterrows():
            b = row['acc_broche']
            t = row['acc_table']
            time.sleep(1 / 2000)
            signalt.append(t)
            signalb.append(b)


        signalt = pd.Series(signalt)
        signalb = pd.Series(signalb)
        to_predict = preprocessor.dataTransformer(signalb, signalt)
        predicted = model.predict(to_predict)
        print("predicted = ", predicted[0])
        predictions.append(predicted[0])
        print("prediction list = ", predictions)
        # Réinitialiser le tampon après la transformation
        signalt = []
        signalb = []

    occurrences = Counter(predictions)
    state = occurrences.most_common(1)[0][0]
    return state



# Route pour récupérer les prédictions
@app.route('/model', methods=['GET'])
def get_model():
    return jsonify({"model": type(model.model).__name__})

"""@app.route('/get_predictions', methods=['GET'])
def get_predictions():
    state = perform_prediction()
    print("the state is :", str(state))
    return jsonify({"state": str(state)})"""



@app.route('/sshserver', methods=['GET'])
def server_ssh():
    try:
        print("Connexion ssh")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname='100.111.209.119', username='badrt', password='badrT')

        #stdin, stdout, stderr = client.exec_command('python /home/badrt/dev_hat/get_data.py')
        client.exec_command('python /home/badrt/dev_hat/get_data.py')

        client.close()
        print("Connexion SSH fermée avec succès.")
        connected = False
        while not connected:
            try:
                # Tentez de vous connecter au serveur Socket.IO
                sio.connect('http://100.111.209.119:8765')
                connected = True
                print("Connexion réussie à Socket.IO")
            except Exception as e:
                print("Erreur lors de la connexion à Socket.IO : ", str(e))
                print("Réessayez dans quelques secondes...")
                time.sleep(2)  # Attendre 5 secondes avant de réessayer
        state = perform_prediction()
        print("the state is :", str(state))
        return jsonify({"state": str(state)})
        #return jsonify({"succès": "SSH connection ok"})
    except paramiko.ssh_exception.SSHException as e:
        print("SSH Exception:", str(e))
        return jsonify({"error": "SSH connection failed"})


@app.route('/offsshserver', methods=['GET'])
def off_server():
    print("Turning down the server")
    # Commande SSH pour obtenir le PID du processus
    command = "pgrep -f 'python /home/badrt/dev_hat/get_data.py'"

    # Établir une connexion SSH
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname="100.111.209.119", username="badrt", password="badrT")

    # Exécutez la commande sur le serveur distant
    stdin, stdout, stderr = client.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()
    print(f'get pid status {exit_status}')
    pid = stdout.read().strip()
    pid = int(pid.decode('utf-8'))
    print(f' pid status {pid}')
    stdin, stdout, stderr = client.exec_command(f"kill -9 {pid}")
    kill_status = stdout.channel.recv_exit_status()
    client.close()

    print(f'kill status {kill_status}')
    if kill_status == 0:
        return jsonify({'message': 'Succès'})
    else:
        return jsonify({'message': 'failed'})




""""@sio.event
def data(data):
    signalt = []
    signalb = []

    while True:
        # Recevoir des données du serveur (vous devrez adapter cette partie)
        # Si aucune donnée n'est reçue, la connexion est probablement fermée
        if not data:
            break
            # Effectuer des prédictions
            perform_predictions(signalb, signalt)"""

# Connectez-vous au serveur Socket.IO
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5005)  # Exécutez l'API Flask sur le port 5000
