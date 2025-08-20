import json
import time

from maa.agent.agent_server import AgentServer
from maa.context import Context
from maa.custom_action import CustomAction
from datetime import datetime

from agent.common import *

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


@AgentServer.custom_action("LoggerAndRecorder")
class LoggerAndRecorder(CustomAction):
    """
    日志和记录
    msg:打印日志
    logTask:taskID
    logKey：key
    logValue：value
    """

    def run(
            self,
            context: Context,
            argv: CustomAction.RunArg,
    ) -> CustomAction.RunResult:

        data = json.loads(argv.custom_action_param)

        msg = data.get("msg")
        log_task = data.get("logTask")
        log_key = data.get("logKey")
        log_value = data.get("logValue")

        if msg is not None:
            print(msg)
        if log_task is not None and log_key is not None and log_value is not None:
            LocalStorage.set(log_task, log_key, log_value)

        return CustomAction.RunResult(success=True)


@AgentServer.custom_action("ReceiveVitalityCheck")
class ReceiveVitalityCheck(CustomAction):
    """
    桃源居体力检查
    """

    def run(
            self,
            context: Context,
            argv: CustomAction.RunArg,
    ) -> CustomAction.RunResult:
        use_tong_bao = json.loads(argv.custom_action_param)["useTongBao"]

        if not is_same_day_with_offset(datetime.now().strftime("%Y-%m-%d %H:%M:%S")):
            LocalStorage.remove_task("HomeReceiveVitality")

        vitality1 = LocalStorage.get(task='HomeReceiveVitality', key="HomeReceiveVitality1")
        vitality2 = LocalStorage.get(task='HomeReceiveVitality', key="HomeReceiveVitality2")

        res = is_tao_yuan_time()
        # 11点前
        if res == 0:
            return CustomAction.RunResult(success=True)
        # 11点到15点
        elif res == 1:
            if vitality1 is None:
                context.run_task("onHomePageCheckForEnterHome")
        # 15点到17点
        elif res == 2:
            if use_tong_bao and vitality1 is None:
                context.run_task("onHomePageCheckForEnterHome")
        # 17点到22点,领取第二次，是否使用通宝补领第一次
        elif res == 3:
            if vitality2 is not None and not use_tong_bao:
                return CustomAction.RunResult(success=True)
            if not use_tong_bao:
                context.override_pipeline(
                    {"enterReceiveVitalityOutTime": {"enabled": False},
                     "receiveVitalityOutTime1": {"enabled": False}}
                )
            else:
                context.override_pipeline(
                    {"enterReceiveVitalityOutTime": {"enabled": False}}
                )
            context.run_task("onHomePageCheckForEnterHome")
        # 使用通宝补领第一、二次
        elif use_tong_bao and (vitality1 is None or vitality2 is None):
            context.run_task("onHomePageCheckForEnterHome")

        return CustomAction.RunResult(success=True)
