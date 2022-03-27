
from concurrent import futures
import logging
import json
import grpc
import meterreader_pb2
import meterreader_pb2_grpc
import os
from csv import reader

SITE_ROOT = os.path.dirname(__file__)


class MeterReader(meterreader_pb2_grpc.MeterReaderServicer):

    def ReadMeter(self, request, context):
        filtered_data = self.get_meter_data(start=request.start_time, end=request.end_time)
        return meterreader_pb2.MeterReaderResponse(meterresponse=json.dumps(filtered_data))

    def read_data_from_csv(self, **params):
        file = self.get_csv_path()
        data = []
        with open(file, 'r') as f:
            csv_reader = reader(f)
            data = [row for row in csv_reader]
        return data

    def get_csv_path(self):
        return os.path.join(os.path.dirname(SITE_ROOT), 'meterusage.1648204779.csv')

    def filter_meter_data(self, **params):
        data = self.read_data_from_csv(**params)
        start = params.get('start') or None
        end = params.get('end') or None
        filtered_data = []
        for row in data[1:]:
            if (start and end and start <= row[0] <= end) or (not start and not end) or (not start and end and row[0] <= end) or (start and not end and row[0] >= start):
               filtered_data.append({'time': row[0], 'meter_used': row[1]})
        return filtered_data

    def get_meter_data(self, **params):
        return self.filter_meter_data(**params)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    meterreader_pb2_grpc.add_MeterReaderServicer_to_server(MeterReader(), server)
    server.add_insecure_port('[::]:5005')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()