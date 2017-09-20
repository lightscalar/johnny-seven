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


@socketio.on('createScan')
def createScan(patient_id):
    # Create a new scan.
    print('Creating New Scan')
    scan = {}
    scan['patient_id'] = patient_id
    scan['complete'] = False
    scan['notes'] = ''
    scan['gcs'] = 15
    scan = db.insert('scan', scan)
    emit('scan', scan)


@socketio.on('getScans')
def getScans(patient_id):
    # List all available scans.
    scans = db.find_where('scans', 'patient_id', patient_id)
    emit('scans', scans)


@socketio.on('getScan')
def getScan(scan_id):
    # Find specifically requested scan.
    scan = db.find_by_id(scan_id)
    emit('scan', scan)


@socketio.on('deleteScan')
def deleteScan(scan_id):
    # Delete the specified scan.
    doc = db.find_by_id(scan_id)
    patient = db.find_by_id(doc.patient_id)
    scan = db.delete(scan_id)
    emit('patient', patient)



@socketio.on('startScan')
def startScan(scan):
    # Start scan for specified patient.
    scan = db.update(scan)
    scan_data = engine.scan()


if __name__ == '__main__':
    print('Launching Socket Server on Port {}'.format(PORT))
    socketio.run(app, port=PORT, debug=False)
