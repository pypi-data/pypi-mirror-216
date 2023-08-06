from typing import Type
from flask import Blueprint, request
from xia_puller import Puller
from xia_agent import Agent
from xia_agent_flask import AgentFunctionApi, FlaskRequestParser


class PullerApi(AgentFunctionApi):
    @classmethod
    def get_puller_blueprint(
            cls,
            path_name: str,
            puller: Type[Puller],
            parser: Type[FlaskRequestParser],
            agent: Agent,
    ):
        """Get blueprint of a Data Puller

        Args:
            path_name: path name to be registered in application
            puller: AgentFunction class
            parser: Parse class for parsing flask's request
            agent (Agent): Agent object (contain agent configuration)

        """
        api = Blueprint(path_name, __name__)

        @api.route('/', methods=["GET", "POST"])
        def agent_function():
            if request.method == 'GET':
                return "Welcome to use X-I-A Puller"
            data_logs = parser.parse()
            if data_logs:
                return cls.get_response(puller.pull(data_logs, agent))
        return api
