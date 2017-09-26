from gevent.wsgi import WSGIServer
from flask import Flask, request, jsonify, Response
from flask_restful import Resource, Api
from flask_cors import CORS
from sixer import sixer
from solid_db import *
from gazepoint import GazePoint
from generate_summaries import generate_summaries


'''RESTFUL API for Johnny Seven'''
PORT = 5100
app = Flask(__name__)
CORS(app)
api = Api(app)
db = SolidDB('data/db.json')
gazepoint = GazePoint()


class Patients(Resource):

    def get(self):
        # Index
        patients = db.all('patients')
        return patients

    def post(self):
        # Create
        patient = {}
        patient['hid'] = sixer()
        patient['gender'] = 'male'
        patient['age'] = 35
        patient['gcs'] = 15
        patient['notes'] = ''
        patient = db.insert('patient', patient)
        return patient


class Patient(Resource):

    def get(self, _id):
        # Index the resource
        data = db.find_by_id(_id)
        return data

    def put(self, _id):
        # Update existing resource
        data = request.json
        data = db.update(data)
        return data

    def delete(self, _id):
        # Delete resource
        db.delete(_id)
        return 200


class Scans(Resource):

    def get(self, patient_id):
        # Index
        scans = db.find_where('scans', 'patient_id', patient_id)
        return scans

    def put(self, _id):
        # Update!
        data = request.json
        data = db.update(data)
        return data

    def post(self, patient_id):
        # Create
        scan = {}
        scan['patient_id'] = patient_id
        scan['isComplete'] = False
        scan['notes'] = ''
        scan['gcs'] = 15
        scan = db.insert('scan', scan)
        return scan


class Scan(Resource):

    def get(self, _id):
        # Index
        data = db.find_by_id(_id)
        return data

    def put(self, _id):
        # Update!
        data = request.json
        data = db.update(data)
        return data

    def delete(self, _id):
        # Delete scan.
        scan = db.find_by_id(_id)
        patient = db.find_by_id(scan['patient_id'])
        db.delete(_id)
        return patient


class Commands(Resource):

    def post(self):
        # Initiate a scan.
        scan = request.json
        scan = gazepoint.collect(scan)
        scan['isComplete'] = True
        scan = db.update(scan)
        return scan

class Download(Resource):

    def get(self, patient_id):
        # Create download.
        file_url = generate_summaries(patient_id)
        return file_url



# ADD RESOURCE ROUTES.
api.add_resource(Patients, '/patients')
api.add_resource(Patient, '/patient/<string:_id>')
api.add_resource(Scans, '/patient/<string:patient_id>/scans')
api.add_resource(Scan, '/scan/<string:_id>')
api.add_resource(Commands, '/commands')
api.add_resource(Download, '/download/<string:patient_id>')


if __name__ == '__main__':
    # wsgi.server(eventlet.listen(('localhost', PORT)), app)
    # app.run(port=PORT, threaded=True)
    http_server = WSGIServer(('', PORT), app)
    http_server.serve_forever()
