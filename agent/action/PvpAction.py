import json

from maa.agent.agent_server import AgentServer
from maa.context import Context
from maa.custom_action import CustomAction

from common import *


@AgentServer.custom_action("CombatResRecord")
class CombatResRecord(CustomAction):
    """
    todo 重新构建、支持九段以上的bp、减少等待时间
    记录pvp胜利、失败
    1:胜利
    2:失败
    参数格式：
    {
        "combatRes": "1/2/3/4",
    }
    """

    def run(
            self,
            context: Context,
            argv: CustomAction.RunArg,
    ) -> CustomAction.RunResult:
        combat_res = json.loads(argv.custom_action_param)["combatRes"]

        log(context, f"当前战斗结果: {combat_res}")

        # 总战斗次数
        total_combat = LocalStorage.get(task='pvpCombat', key="totalCombat")
        if total_combat is None:
            LocalStorage.set(task='pvpCombat', key="totalCombat", value=1)
        else:
            LocalStorage.set(task='pvpCombat', key="totalCombat", value=total_combat + 1)

        # 胜利次数
        if combat_res:
            total_win = LocalStorage.get(task='pvpCombat', key="totalWin")
            if total_win is None:
                LocalStorage.set(task='pvpCombat', key="totalWin", value=1)
            else:
                LocalStorage.set(task='pvpCombat', key="totalWin", value=total_win + 1)

        # 活跃度次数
        cur_start_lv = LocalStorage.get(task='pvpCombat', key="curStartLv")
        if cur_start_lv is not None:
            if (cur_start_lv > 6 and is_battle_time()) or cur_start_lv <= 6:
                total_r_combat = LocalStorage.get(task='pvpCombat', key="totalRCombat")
                if total_r_combat is None:
                    LocalStorage.set(task='pvpCombat', key="totalRCombat", value=1)
                else:
                    LocalStorage.set(task='pvpCombat', key="totalRCombat", value=total_r_combat + 1)
        return CustomAction.RunResult(success=True)
