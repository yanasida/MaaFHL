from maa.context import Context


def log(context: Context, msg: str, level: int = 0):
    """
    打印自定义 UI 日志。

    Args:
        context: MaaContext 对象
        msg: 日志内容
        level: 日志等级，默认 0（灰色）
            0 -> darkgray  运行信息
            1 -> orange  保留字段
            2 -> green  正常结束
            3 -> red  错误或者需手动提醒
    """
    # 日志等级对应颜色
    level_color_map = {
        0: "darkgray",
        1: "orange",
        2: "green",
        3: "red"
    }
    color = level_color_map.get(level, "darkgray")  # 默认灰色

    # 构造 focus 字符串
    focus_str = f"[color:{color}]{msg}[/color]"

    # 覆盖 pipeline 并运行 customUILog
    context.override_pipeline({
        "customUILog": {"focus": focus_str}
    })
    context.run_task("customUILog")
