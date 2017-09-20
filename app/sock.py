from flask import Flask
from flask_socketio import SocketIO, send, emit
from solid_db import *
from sixer import *


PORT = 5200
app = Flask(__name__)
socketio = SocketIO(app)
db = SolidDB('data/db.json')


# Define status object
status = {}
status['message'] = 'Not Connected to Server'
status['is_connected'] = False


@socketio.on('connect')
def connected():
    # Client has connected to server.
    status['is_connected'] = True
    status['message'] = 'J7 Is Alive'
    emit('status', status)


@socketio.on('disconnect')
def connected():
    # Client has disconnected from server.
    status['is_connected'] = False
    status['message'] = 'Not Connected to J7'
    emit('status', status)


@socketio.on('updatePatient')
def updatePatient(patient):
    # Update the current patient model.
    patient = db.update(patient)
    emit('patient', patient)


@socketio.on('deletePatient')
def deletePatient(patient_id):
    # Update the current patient model.
    patient = db.delete(patient_id)


@socketio.on('createPatient')
def createPatient():
    # Client requests creation of new patient.
    patient = {}
    patient['hid'] = sixer()
    patient['gender'] = 'male'
    patient['age'] = 35
    patient['gcs'] = 15
    patient['notes'] = ''
    patient = db.insert('patient', patient)
    emit('patientCreated', patient)


@socketio.on('getPatients')
def getPatients():
    # List all available patients.
    patients = db.all('patients')
    emit('patients', patients)


@socketio.on('getPatient')
def getPatients(patient_id):
    # Find specifically requested patient.
    patient = db.find_by_id(patient_id)
    emit('patient', patient)


@socketio.on('startScan')
def startScan(patient_id):
    # Start scan for specified patient.
    # TODO
    pass


if __name__ == '__main__':
    print('Launching Socket Server on Port {}'.format(PORT))
    socketio.run(app, port=PORT, debug=False)
