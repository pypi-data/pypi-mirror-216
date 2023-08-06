import json
import logging
from typing import Type
from flask import Blueprint, request
from xia_pusher import Pusher
from xia_agent import Agent
from xia_agent_flask import AgentFunctionApi, FlaskRequestParser


class PusherApi(AgentFunctionApi):
    @classmethod
    def get_pusher_blueprint(
            cls,
            path_name: str,
            pusher: Type[Pusher],
            parser: Type[FlaskRequestParser],
            agent: Agent,
    ):
        """Get blueprint of a Data Puller

        Args:
            path_name: path name to be registered in application
            pusher: AgentFunction class for pusher
            parser: Parse class for parsing flask's request
            agent (Agent): Agent object (contain agent configuration)

        """
        api = Blueprint(path_name, __name__)

        @api.route('/', methods=["GET", "POST"])
        def agent_function():
            if request.method == 'GET':
                return "Welcome to use X-I-A Pusher"
            data_logs = parser.parse()
            for data_log in data_logs:
                result, status_code = cls.get_response(pusher.push(data_log, agent))
                return result, status_code
        return api
