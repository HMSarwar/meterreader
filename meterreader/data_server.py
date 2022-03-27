import os

from flask import Flask, render_template, jsonify
from flask_restful import Api, Resource, reqparse

import grpc
from datetime import datetime
from meterreader_pb2 import MeterReaderRequest
from meterreader_pb2_grpc import MeterReaderStub
import json


app = Flask(__name__)
api = Api(app)

host = os.getenv("METERREADER_HOST", "localhost")
port = os.getenv("METERREADER_PORT", "5005")
channel = grpc.insecure_channel("{}:{}".format(host, port), options=(('grpc.enable_http_proxy', 0),))

client = MeterReaderStub(channel)


@app.route("/")
def render_homepage():

    return render_template(
        "home.html"
    )


class GetMeterDataAPI(Resource):

    def get(self):

        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('start_time', type=str, required=True)
        self.reqparse.add_argument('end_time', type=str, required=True)
        args = self.reqparse.parse_args()
        start_time = args.get('start_time')
        end_time = args.get('end_time')
        try:
            start_time = start_time.replace('T', ' ') + (':00' if start_time else '')
            end_time = end_time.replace('T', ' ') + (':00' if end_time else '')
            print(start_time, end_time)
        except Exception as e:
            return {'error': 'Start/End Time error'}
        request = MeterReaderRequest(start_time=str(start_time), end_time=str(end_time))
        try:
            response = client.ReadMeter(request)
            response = json.loads(response.meterresponse)
        except Exception as e:
            response = '[]'
        return response



@app.route("/")
def render_meter_data():
    return render_template(
        "home.html"
    )

api.add_resource(GetMeterDataAPI, '/get_meter_data/', endpoint='get_meter_data')



if __name__ == '__main__':
    app.run(host='127.0.0.1',port=4455,debug=True)
