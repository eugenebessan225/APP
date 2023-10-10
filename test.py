import socketio
sio = socketio.Client()



@sio.event
def connect():
    print("Connecté au serveur")

    sio.emit('data_request', {'key': 'value'})


@sio.on('data')
def handle_row_data(data):
    while True:
        print(data)

@sio.event
def disconnect():
    print("déconnecté au serveur")


sio.connect('http://100.111.209.119:8765')
