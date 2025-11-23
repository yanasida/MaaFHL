import json
from datetime import datetime

from maa.agent.agent_server import AgentServer
from maa.context import Context
from maa.custom_recognition import CustomRecognition

from common import *

# 符信 段位 武魂
roi_data = [[129, 667, 86, 44], [1030, 298, 38, 67], [1137, 357, 74, 58]]

# 段位数字
number_map = {
    "一": 1,
    "二": 2,
    "三": 3,
    "四": 4,
    "儿": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9
}


def init_count_data(context, img) -> int:
    result = context.run_recognition(
        "readPvpData",
        img,
        pipeline_override={
            "readPvpData": {
                "roi": roi_data[0]
            }
        },
    )

    try:
        data = int(result.best_result.text)
    except Exception:
        data = -1
    return data


def init_soul_data(context, img) -> int:
    result = context.run_recognition(
        "readPvpData",
        img,
        pipeline_override={
            "readPvpData": {
                "roi": roi_data[2]
            }
        },
    )

    try:
        data = int(result.best_result.text)
    except Exception:
        data = -1
    return data


def init_lv_data(context, img) -> int:
    result = context.run_recognition(
        "readPvpData",
        img,
        pipeline_override={
            "readPvpData": {
                "roi": roi_data[1]
            }
        },
    )

    try:
        datastr = str(result.best_result.text)
        data = number_map.get(datastr)
    except Exception:
        data = -1
    return data


def should_exit_battle(count, pvp_type, lv, total_win, total_r_combat):
    """判断是否需要退出金戈演武"""

    if lv == -1:
        print("当前段位不支持自动金戈")
        return True
    if pvp_type == 1 and (count == -1 or count == 0):
        print("清符已完成，退出金戈演武")
        return True
    if pvp_type == 2 and total_win >= 1:
        print("首胜已完成，退出金戈演武")
        return True
    if pvp_type == 3 and total_r_combat >= 3:
        print("3场活跃度已完成，退出金戈演武")
        return True
    if pvp_type != 2 and lv > 6 and not is_battle_time():
        print("七段及以上非金戈时间仅支持首胜")
        return True
    return False


def handle_combat(context, soul, lv, count, pvp_type):
    """根据段位和时间状态决定执行任务"""

    print(f"段位{lv}, 枕戈符信{count}, 骁武魂{soul}")

    total_win = LocalStorage.get(task='pvpCombat', key="totalWin")
    if total_win is None:
        total_win = 0
    total_r_combat = LocalStorage.get(task='pvpCombat', key="totalRCombat")
    if total_r_combat is None:
        total_r_combat = 0
    total_combat = LocalStorage.get(task='pvpCombat', key="totalCombat")
    if total_combat is None:
        total_combat = 0

    # 任务完成、九段以上、七段上不在时间内只支持首胜
    if should_exit_battle(count, pvp_type, lv, total_win, total_r_combat):
        LocalStorage.set(task='pvpCombat', key="todayEndSoul", value=soul)
        LocalStorage.set(task='pvpCombat', key="todayEndtLv", value=lv)
        LocalStorage.set(task='pvpCombat', key="todayEndCount", value=count)
        return "backToPvpFlag"

    print(f"开始金戈, 第{total_combat + 1}次, 胜场{total_win}次, 活跃度次数{total_r_combat}")

    # 段位 6 及以下直接打
    if lv <= 6:
        return "startCombat"

    # 段位7-9需要判断时间
    return "startCombat" if is_battle_time() else "startCombatOutTime"


@AgentServer.custom_recognition("checkPvpVersionTime")
class CheckPvpVersionTimeRecongition(CustomRecognition):
    """

       参数格式：
       {
           "type": 1/2/3, 清符、首胜、3场活跃度
       }
       """

    def analyze(
            self,
            context: Context,
            argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        try:
            pvp_type = json.loads(argv.custom_recognition_param)["type"]
        except Exception:
            pvp_type = 2

        img = argv.image
        soul = init_soul_data(context, img)
        lv = init_lv_data(context, img)
        count = init_count_data(context, img)

        # 仅保留当天pvp数据
        start_time = LocalStorage.get(task='pvpCombat', key="todayStartTime")

        if not is_same_day_with_today(start_time):
            LocalStorage.remove_task("pvpCombat")
            LocalStorage.set(task='pvpCombat', key="todayStartTime", value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            LocalStorage.set(task='pvpCombat', key="todayStartSoul", value=soul)
            LocalStorage.set(task='pvpCombat', key="todayStartLv", value=lv)
            LocalStorage.set(task='pvpCombat', key="todayStartCount", value=count)

        LocalStorage.set(task='pvpCombat', key="curStartLv", value=lv)

        next_task = handle_combat(context, soul, lv, count, pvp_type)
        context.run_task(next_task)

        return CustomRecognition.AnalyzeResult(
            box=[0, 0, 0, 0],
            detail="1"
        )


@AgentServer.custom_recognition("useSoulOrNot")
class UseSoulOrNot(CustomRecognition):
    """

    参数格式：
    {
        "use": "true/false",
    }
    """

    def analyze(
            self,
            context: Context,
            argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:

        use = json.loads(argv.custom_recognition_param)["use"]

        result = context.run_recognition(
            "useSoul",
            argv.image

        )
        try:
            score = result.best_result.score
        except Exception:
            score = -1

        if score == -1:
            context.run_task("afterPvpConfirm")
        else:
            if use:
                print("使用骁武魂")
                context.run_task("useSoul")
            else:
                print("不使用骁武魂")
                context.run_task("notUseSoul")

        return CustomRecognition.AnalyzeResult(
            box=[0, 0, 0, 0],
            detail="1"
        )
