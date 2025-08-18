import sys

from maa.agent.agent_server import AgentServer
from maa.toolkit import Toolkit

from reco import *
from action import *


def main():
    Toolkit.init_option("./")

    AgentServer.start_up("5a73f0f8-297e-4d29-92d1-35167435ddfc")
    AgentServer.join()
    AgentServer.shut_down()


if __name__ == "__main__":
    main()
