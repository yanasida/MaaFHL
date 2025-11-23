import json

from maa.agent.agent_server import AgentServer
from maa.context import Context
from maa.custom_action import CustomAction

from common import *


@AgentServer.custom_action("TLQQGDCount")
class TLQQGDCount(CustomAction):
    """
    千奇诡道 计数器 默认为0，每次进入自增1
    {
        "countPlus": "1"
    }
    """

    def run(
            self,
            context: Context,
            argv: CustomAction.RunArg,
    ) -> CustomAction.RunResult:

        count = LocalStorage.get(task='TLAQQGD', key="TMAQQGDCount")
        if count is None:
            count = 1
            LocalStorage.set(task='TLAQQGD', key="TMAQQGDCount", value=count)
        else:
            count = count + 1
            LocalStorage.set(task='TLAQQGD', key="TMAQQGDCount", value=count)

        real_count = count % 4

        log(context, f"开始第{real_count}次战斗")

        if real_count == 1:
            context.run_task("QQGDBattlePreparation1")
        elif real_count == 2:
            context.run_task("QQGDGoCombat")
        elif real_count == 3:
            context.run_task("QQGDGoCombat")
        elif real_count == 0:
            context.run_task("QQGDBattlePreparation2")

        return CustomAction.RunResult(success=True)
