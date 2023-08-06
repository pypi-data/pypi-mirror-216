import base64
import json
from typing import List
from flask import request, jsonify
from xia_logger import DataLog, HttpLogger, JsonLogger


class FlaskRequestParser:
    """Parse Flask received request to Data log"""
    @classmethod
    def parse(cls) -> List[DataLog]:
        """Parse contents to DataLog object

        Args:
           There is no args. All is hold in Flask's request's context

        Returns:
            DataLog object list
        """


class GcpLogParser(FlaskRequestParser):
    @classmethod
    def parse(cls) -> List[DataLog]:
        envelope = request.get_json()
        if not envelope:
            raise ValueError("no Pub/Sub message received")
        if not isinstance(envelope, dict) or 'message' not in envelope:
            raise ValueError("invalid Pub/Sub message format")
        db_content = json.loads(base64.b64decode(envelope['message']['data']).decode())["jsonPayload"]
        data_log = DataLog.from_db(_engine=JsonLogger, **db_content)
        return [data_log]


class PubsubLogParser(FlaskRequestParser):
    @classmethod
    def parse(cls) -> List[DataLog]:
        envelope = request.get_json()
        if not envelope:
            raise ValueError("no Pub/Sub message received")
        if not isinstance(envelope, dict) or 'message' not in envelope:
            raise ValueError("invalid Pub/Sub message format")
        db_content = envelope['message'].get('attributes', {})
        db_content["data_content"] = base64.b64decode(envelope['message'].get('data', b""))
        data_log = DataLog.from_db(_engine=HttpLogger, **db_content)
        return [data_log]


class AgentFunctionApi:
    """"""
    @classmethod
    def get_response(cls, rest_response):
        if isinstance(rest_response, tuple):
            return jsonify(rest_response[0]), rest_response[1]
        else:
            return jsonify(rest_response), 200
