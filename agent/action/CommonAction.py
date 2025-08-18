import time

from maa.agent.agent_server import AgentServer
from maa.context import Context
from maa.custom_action import CustomAction

POINT1 = [371, 303]
POINT2 = [626, 164]
POINT3 = [755, 265]
POINT4 = [1015, 200]
POINT5 = [1155, 292]

REMOVE1 = [469, 185]
REMOVE2 = [518, 121]
REMOVE3 = [869, 189]
REMOVE4 = [914, 122]
REMOVE5 = [1259, 188]

points = [POINT1, POINT2, POINT3, POINT4, POINT5]
removes = [REMOVE1, REMOVE2, REMOVE3, REMOVE4, REMOVE5]


@AgentServer.custom_action("RemoveAllMember")
class RemoveAllMember(CustomAction):
    """
    移除小队所有人
    """

    def run(
            self,
            context: Context,
            argv: CustomAction.RunArg,
    ) -> CustomAction.RunResult:
        for (px, py), (rx, ry) in zip(points, removes):
            context.tasker.controller.post_click(px, py)
            time.sleep(0.5)

            context.tasker.controller.post_click(rx, ry)
            time.sleep(0.5)

        return CustomAction.RunResult(success=True)
