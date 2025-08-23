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


@AgentServer.custom_action("ReceiveTyCheck")
class ReceiveTyCheck(CustomAction):
    """
    桃源居检查
    """

    def run(
            self,
            context: Context,
            argv: CustomAction.RunArg,
    ) -> CustomAction.RunResult:
        use_tong_bao = json.loads(argv.custom_action_param)["useTongBao"]

        start_time = LocalStorage.get(task='TyHomeAct', key="todayStartTime")
        if start_time is not None:
            if not is_same_day_with_offset(start_time):
                LocalStorage.remove_task("TyHomeAct")
        if start_time is None:
            LocalStorage.set("TyHomeAct", "todayStartTime", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        vitality1 = LocalStorage.get(task='TyHomeAct', key="HomeReceiveVitality1")
        vitality2 = LocalStorage.get(task='TyHomeAct', key="HomeReceiveVitality2")
        convert_pic = LocalStorage.get(task='TyHomeAct', key="convertPic")

        if convert_pic:
            context.override_pipeline(
                {"convertPicStart": {"enabled": False}}
            )

        res = is_tao_yuan_time()
        if vitality2 and vitality1:
            context.override_pipeline(
                {"enterReceiveVitality": {"enabled": False}}
            )
        # 11点前
        elif res == 0:
            print("当前时间不可领取体力")
            context.override_pipeline(
                {"enterReceiveVitality": {"enabled": False}}
            )
        # 11点到15点
        elif res == 1 and vitality1:
            context.override_pipeline(
                {"enterReceiveVitality": {"enabled": False}}
            )
        # 15点到17点
        elif res == 2 and (not use_tong_bao or vitality1):
            context.override_pipeline(
                {"enterReceiveVitality": {"enabled": False}}
            )
        elif res == 3 and not use_tong_bao and vitality2:
            context.override_pipeline(
                {"enterReceiveVitality": {"enabled": False}}
            )
        elif res == -1 and not use_tong_bao:
            context.override_pipeline(
                {"enterReceiveVitality": {"enabled": False}}
            )

        context.run_task("onHomePageCheckForEnterHome")

        return CustomAction.RunResult(success=True)


@AgentServer.custom_action("DisableNode")
class DisableNode(CustomAction):
    """
    将特定 node 设置为 disable 状态 。

    参数格式:
    {
        "node_name": "结点名称"
    }
    """

    def run(
            self,
            context: Context,
            argv: CustomAction.RunArg,
    ) -> CustomAction.RunResult:
        node_name = json.loads(argv.custom_action_param)["node_name"]

        context.override_pipeline({f"{node_name}": {"enabled": False}})

        return CustomAction.RunResult(success=True)


@AgentServer.custom_action("DailyStartCheck")
class DailyStartCheck(CustomAction):
    """
    日常检查
    """

    def run(
            self,
            context: Context,
            argv: CustomAction.RunArg,
    ) -> CustomAction.RunResult:
        # data = json.loads(argv.custom_action_param)
        #
        # cat_gift = data.get("catGift")
        # cat_fish = data.get("catFish")
        # send_gift = data.get("sendGift")
        # hide_and_seek = data.get("hideAndSeek")

        start_time = LocalStorage.get(task='DailyStart', key="todayStartTime")
        if start_time is not None:
            if not is_same_day_with_offset(start_time):
                LocalStorage.remove_task("DailyStart")
        if start_time is None:
            LocalStorage.set("DailyStart", "todayStartTime", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        local_cat_gift = LocalStorage.get(task='DailyStart', key="catGift")
        local_cat_fish = LocalStorage.get(task='DailyStart', key="catFish")
        local_send_gift = LocalStorage.get(task='DailyStart', key="sendGift")
        local_hide_and_seek = LocalStorage.get(task='DailyStart', key="hideAndSeek")
        local_seek_cats = LocalStorage.get(task='DailyStart', key="hideAndSeekClear")
        local_friends_gift = LocalStorage.get(task='DailyStart', key="friendsGift")
        local_world_speech = LocalStorage.get(task='DailyStart', key="worldSpeech")
        local_email = LocalStorage.get(task='DailyStart', key="email")
        local_cats_feed = LocalStorage.get(task='DailyStart', key="catsFeed")
        local_cats_petting = LocalStorage.get(task='DailyStart', key="catsPetting")

        if local_cat_gift and local_cat_fish and local_send_gift and local_hide_and_seek and local_seek_cats:
            context.override_pipeline(
                {"quickStartClick": {"enabled": False}}
            )
        else:
            if local_cat_gift:
                context.override_pipeline({"catGift": {"enabled": False}})
            if local_cat_fish:
                context.override_pipeline({"catFish": {"enabled": False}})
            if local_send_gift:
                context.override_pipeline({"sendGift": {"enabled": False}})
            if local_hide_and_seek and local_seek_cats:
                context.override_pipeline(
                    {"hideAndSeekClearSwipe": {"enabled": False}}
                )
            else:
                if local_hide_and_seek:
                    context.override_pipeline({"hideAndSeekReceive": {"enabled": False}})
                if local_seek_cats:
                    context.override_pipeline({"seekCatsGo": {"enabled": False}})
        if local_friends_gift:
            context.override_pipeline({"friendsGiftStart": {"enabled": False}})
        if local_world_speech:
            context.override_pipeline({"worldSpeechStart": {"enabled": False}})
        if local_email:
            context.override_pipeline({"emailStart": {"enabled": False}})
        if local_cats_feed and local_cats_petting:
            context.override_pipeline({"catsHomeStart": {"enabled": False}})
        else:
            if local_cats_feed:
                context.override_pipeline({"catsHomeFeed": {"enabled": False}})
            if local_cats_petting:
                context.override_pipeline({"catsHomePetting": {"enabled": False}})

        return CustomAction.RunResult(success=True)
