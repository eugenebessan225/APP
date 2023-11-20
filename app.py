from model_wrapper import WearDetectionModel
import configparser
from datastats import preprocessor
import socketio
import pandas as pd
import pickle
from collections import Counter
import time
import paramiko
from flask_cors import CORS
from flask import Flask, request, render_template, jsonify
import psycopg2
from psycopg2 import sql

# Créez un client Socket.IO
sio = socketio.Client()
app = Flask(__name__)
CORS(app)
#connection.init_app(app)


"""try:
    connector = psycopg2.connect(dbname="postgres",
                                     user="postgres",
                                     password="badrT", #badrt pour vm
                                     host="localhost",
                                     port="5432")

    print("Connexion à la db reussie")
except Exception as e:
    print("erreur de connexion", e)"""


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
    df = pickle.load(file)


#conn = connector.connection()


@sio.event
def connect():
    print("connecté")
    try:
        sio.emit('data_request', {'key': 'value'})
        print("data_request send")
    except Exception as e:
        print("erreur d'envoie socket", e)

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
        predictions.append(predicted[0])
        print("prediction list = ", predictions)
        # Réinitialiser le tampon après la transformation
        signalt = []
        signalb = []

    occurrences = Counter(predictions)
    state = occurrences.most_common(1)[0][0]
    return state


connected = False  # Variable de contrôle de la connexion Socket.IO
#connection = None
@app.route('/sshserver', methods=['GET'])
def server_ssh():

    global connected
    try:
        print("Connexion ssh")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname='100.111.209.119', username='badrt', password='badrT')

        command = 'python /home/badrt/dev_hat/get_data_socket.py'
        client.exec_command(command)
        print("socket status", connected)
        while not connected:
            print("Socket Not connected")
            try:
                # Tentez de vous connecter au serveur Socket.IO
                sio.connect('http://100.111.209.119:8765')
                connected = True
                print("Connexion réussie à Socket.IO")
            except Exception as e:
                print("Erreur lors de la connexion à Socket.IO : ", str(e))
                print("Réessayez dans quelques secondes...")
                time.sleep(2)  # Attendre 2 secondes avant de réessayer

        """cannal.basic_consume(queue='row_data',
                              auto_ack=True,
                              on_message_callback=perform_prediction)"""
        #state = perform_prediction()
        state=1
        print("the state is :", str(state))
        return jsonify({"state": str(state)})

    except paramiko.ssh_exception.SSHException as e:
        print("SSH Exception:", str(e))
        return jsonify({"error": "SSH connection failed"})


@app.route('/offsshserver', methods=['GET'])
def off_server():
    global connected

    print("Turning down the server")
    # Commande SSH pour obtenir le PID du processus
    command = "pgrep -f 'python /home/badrt/dev_hat/get_data_socket.py'"

    # Établir une connexion SSH
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname="100.111.209.119", username="badrt", password="badrT")

    # Arrêtez la connexion Socket.IO
    if connected:
        sio.emit('stop_data', {'key': 'value'})
        sio.disconnect()
        print("Disconnecting Socket")
        connected = False

    # Exécutez la commande sur le serveur distant
    stdin, stdout, stderr = client.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()
    print(f'get pid status {exit_status}')
    pid = stdout.read().strip()
    pid = int(pid.decode('utf-8'))
    print(f' pid status {pid}')
    time.sleep(2)
    stdin, stdout, stderr = client.exec_command(f"kill -9 {pid}")
    kill_status = stdout.channel.recv_exit_status()
    client.close()
    print("Connexion SSH fermée avec succès.")
    print(f'kill status {kill_status}')
    if kill_status == 0:
        return jsonify({'message': 'Succès'})
    else:
        return jsonify({'message': 'failed'})


@app.route('/', methods=['GET'])
def send():
    value = int(request.args.get('value', -1))
    print(f"Received value: {value}")

    # Créez un objet de curseur
    #cursor = connector.cursor()

    # Requête SQL pour insérer des valeurs génériques dans la table ml_table
    #insert_query = sql.SQL("""
            #INSERT INTO ml_table (predict_ID, ope_ID, time, predict_value, pred_eval, ope_eval, observation)
            #VALUES (
                #DEFAULT, -- predict_ID
                #DEFAULT, -- ope_ID
                #NOW(),   -- time
                #%s,      -- predict_value
                #%s,      -- pred_eval
                #%s,      -- ope_eval
                #%s       -- observation
            #);
        #)

    # Paramètres des valeurs constantes
    #values = (1, value, 1, 'Op ok')

    # Exécutez votre requête SQL pour insérer la valeur dans la base de données
    #cursor.execute(insert_query, values)

    # Validez la transaction et fermez le curseur
    #connector.commit()
    #cursor.close()

    return jsonify({'message': 'Succès'})


# Connectez-vous au serveur Socket.IO
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5005)  # Exécutez l'API Flask sur le port 5000
