from typing import NoReturn

from nonebot.exception import FinishedException
from nonebot_plugin_alconna.uniseg import UniMessage
from nonebot_plugin_alconna import Alconna, on_alconna, Args, CommandMeta

from .config import config
from .draw import ServerType, draw

try:
    from nonebot.adapters.onebot.v11 import GroupMessageEvent as OB11GroupMessageEvent
except ImportError:
    OB11GroupMessageEvent = None


async def finish_with_query(ip: str, svr_type: ServerType) -> NoReturn:
    try:
        ret = await draw(ip, svr_type)
    except Exception:
        msg = UniMessage("出现未知错误，请检查后台输出")
    else:
        msg = UniMessage.image(raw=ret)
    await msg.send(reply_to=config.reply_target)
    raise FinishedException


matcher = on_alconna(Alconna(
    "motd",
    Args["server_type", ServerType, "auto" if config.enable_auto_detect else "je"],
    Args["address", str],
    meta=CommandMeta(compact=True)
))

@matcher.handle()
async def _(server_type: ServerType, address: str):
    await finish_with_query(address, server_type)