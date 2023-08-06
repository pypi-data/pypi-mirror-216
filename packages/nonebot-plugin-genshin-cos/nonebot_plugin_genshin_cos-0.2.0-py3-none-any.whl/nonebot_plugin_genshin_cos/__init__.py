from nonebot.adapters.onebot.v11 import (
    Bot,
    Message,
    MessageEvent,
    MessageSegment,
    GroupMessageEvent
)
from nonebot.plugin import on_regex, on_command, require, PluginMetadata
from nonebot.params import RegexGroup, ArgPlainText, CommandArg
from nonebot.typing import T_State
from nonebot.log import logger
from nonebot import get_driver, get_bot
from nonebot.matcher import Matcher
from nonebot.exception import ActionFailed
from typing import Tuple, Any
from random import choice
from datetime import datetime
from .config import Config
from .utils import *
from .hoyospider import *
try:
    scheduler = require("nonebot_plugin_apscheduler").scheduler
except:
    scheduler = None
try:
    import ujson as json
except ModuleNotFoundError:
    import json
import asyncio
import re

__plugin_meta__ = PluginMetadata(
    name="米游社cos",
    description="获取原神coser图片",
    config=Config,
    usage="原神cos,CosPlus,下载cos",
    type="application",
    homepage="https://github.com/Cvandia/nonebot_plugin_genshin_cos",
    supported_adapters={"~onebot.v11"},
    extra={
        "unique_name": "genshin_cos",
        "example": "保存cos:保存cos图片至本地文件",
        "author": "divandia <106718176+Cvandia@users.noreply.github.com>",
        "version": "0.2.0",
    }
)
logo = """<g>
  /$$$$$$                                /$$       /$$                  /$$$$$$                     
 /$$__  $$                              | $$      |__/                 /$$__  $$                    
| $$  \__/  /$$$$$$  /$$$$$$$   /$$$$$$$| $$$$$$$  /$$ /$$$$$$$       | $$  \__/  /$$$$$$   /$$$$$$$
| $$ /$$$$ /$$__  $$| $$__  $$ /$$_____/| $$__  $$| $$| $$__  $$      | $$       /$$__  $$ /$$_____/
| $$|_  $$| $$$$$$$$| $$  \ $$|  $$$$$$ | $$  \ $$| $$| $$  \ $$      | $$      | $$  \ $$|  $$$$$$ 
| $$  \ $$| $$_____/| $$  | $$ \____  $$| $$  | $$| $$| $$  | $$      | $$    $$| $$  | $$ \____  $$
|  $$$$$$/|  $$$$$$$| $$  | $$ /$$$$$$$/| $$  | $$| $$| $$  | $$      |  $$$$$$/|  $$$$$$/ /$$$$$$$/
 \______/  \_______/|__/  |__/|_______/ |__/  |__/|__/|__/  |__/       \______/  \______/ |_______/ 
 </g>"""


logger.opt(colors=True).info(logo)

#用户cd数据
user_data = {}
CONFIG: Dict[str, Dict[str,str]] = {'原神':{},'崩坏3':{},'大别野':{},'星穹铁道':{}}
DRIVER = get_driver()
# 读取配置文件
config_path = Path("config/genshincos.json")
config_path.parent.mkdir(parents=True, exist_ok=True)
if config_path.exists():
    with open(config_path, "r", encoding="utf8") as f:
        CONFIG = json.load(f)
else:
    with open(config_path, "w", encoding="utf8") as f:
        json.dump(CONFIG, f, ensure_ascii=False, indent=4)

#事件响应器
download_cos = on_command('下载cos', aliases={'cos保存', '保存cos'}, block=False, priority=5, permission=SUPER_PERMISSION)
hot_cos = on_command('热门cos', aliases={'热门coser', '热门cos图'}, block=False, priority=5)
rank_cos = on_regex(r'^(日|月|周)榜cos[r]?[图]?(.+)?',priority=5, block=False, flags=re.I)
latest_cos = on_command('最新cos', aliases={'最新coser', '最新cos图'}, block=False, priority=5)
good_cos = on_command('精品cos', aliases={'精品coser', '精品cos图'}, block=False, priority=5)
turn_aps = on_regex(r'^(开启|关闭)每日推送(原神|崩坏3|星穹铁道|大别野)(\s)?(.+)?', block=False, priority=5, flags=re.I, permission=SUPER_PERMISSION)
show_aps = on_command('查看本群推送', aliases={'查看推送','查看订阅'}, block=False, priority=5)

@show_aps.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    send_msg = '本群订阅的推送有:\n'
    for game_type, dict in CONFIG.items():
        if game_type == "": continue
        for goup_id, time in dict.items():
            if str(event.group_id) == goup_id:
                send_msg += f"{game_type}的每日{time}推送\n"
    await show_aps.finish(send_msg)


@turn_aps.handle()
async def _(event: GroupMessageEvent, args: Tuple[Any, ...] = RegexGroup()):
    # 检查是否安装了apscheduler插件，并且是否开启了定时推送
    if scheduler == None:
        await turn_aps.finish("未安装apscheduler插件,无法使用此功能")
    mode = args[0] 
    game_type = args[1]
    time = args[3]
    group_id = str(event.group_id)
    MyConfig = CONFIG.copy()
    if mode == "开启":
        for name in MyConfig.keys():
            if name == game_type:
                if group_id in MyConfig[name].keys():
                    await turn_aps.finish("该群已开启,无需重复开启")
                elif not time:
                    await turn_aps.finish("请指定推送时间")
                else:
                    CONFIG[name][group_id] = time
                    try:
                        scheduler.add_job(aps_send, trigger="cron", hour=time.split(":")[0], minute=time.split(":")[1], id=f"{game_type}{group_id}")
                        logger.debug(f"已成功添加{group_id}的{game_type}定时推送")
                        scheduler.start()
                    except Exception as e:
                        logger.error(e)
    else:
        for name in MyConfig.keys():
            if name == game_type:
                if group_id in MyConfig[name].keys():
                    CONFIG[name].pop(group_id)
                    try:
                        scheduler.remove_job(f"{game_type}{group_id}")
                    except Exception as e:
                        logger.error(e)
                        continue
                else:
                    await turn_aps.finish("该群已关闭,无需重复关闭")
    with open(config_path, "w", encoding="utf8") as f:
        f.write(json.dumps(CONFIG, ensure_ascii=False, indent=4))
    await turn_aps.finish(f"已成功{mode}{group_id}的{game_type}定时推送")


@hot_cos.handle()
async def _(bot: Bot, matcher: Matcher, event: MessageEvent, arg: Message = CommandArg()):
    if not arg:
        await hot_cos.finish("请指定cos类型")
    args = arg.extract_plain_text().split()
    if args[0] in GENSHIN_NAME:
        send_type = Hot(ForumType.GenshinCos)
    elif args[0] in HONKAI3RD_NAME:
        send_type = Hot(ForumType.Honkai3rdPic)
    elif args[0] in DBY_NAME:
        send_type = Hot(ForumType.DBYCOS)
    elif args[0] in STAR_RAIL:
        send_type = Hot(ForumType.StarRailCos)
    else:
        await hot_cos.finish("暂不支持该类型")
    await send_images(bot,matcher,args,event,send_type)

@rank_cos.handle()
async def _(bot: Bot, matcher: Matcher, event: MessageEvent, group: Tuple[str, ...] = RegexGroup()):
    if not group[1]:
        await rank_cos.finish("请指定cos类型")
    args = group[1].split()
    if group[0] == "日":
        rank_type = RankType.Daily
    elif group[0] == "周":
        rank_type = RankType.Weekly
    elif group[0] == "月":
        rank_type = RankType.Monthly

    if args[0] in GENSHIN_NAME:
        send_type = Rank(ForumType.GenshinCos, rank_type)
    elif args[0] in HONKAI3RD_NAME:
        send_type = Rank(ForumType.Honkai3rdPic, rank_type)
    elif args[0] in DBY_NAME:
        send_type = Rank(ForumType.DBYCOS, rank_type)
    elif args[0] in STAR_RAIL:
        send_type = Rank(ForumType.StarRailCos, rank_type)
    else:
        await rank_cos.finish("暂不支持该类型")
    await send_images(bot,matcher,args,event,send_type)

@latest_cos.handle()
async def _(bot: Bot, matcher: Matcher, event: MessageEvent, arg: Message = CommandArg()):
    if not arg:
        await latest_cos.finish("请指定cos类型")
    args = arg.extract_plain_text().split()
    if args[0] in GENSHIN_NAME:
        send_type = Latest(ForumType.GenshinCos, LatestType.LatestComment)
    elif args[0] in HONKAI3RD_NAME:
        send_type = Latest(ForumType.Honkai3rdPic, LatestType.LatestComment)
    elif args[0] in DBY_NAME:
        send_type = Latest(ForumType.DBYCOS, LatestType.LatestComment)
    elif args[0] in STAR_RAIL:
        send_type = Latest(ForumType.StarRailCos, LatestType.LatestComment)
    else:
        await latest_cos.finish("暂不支持该类型")
    await send_images(bot,matcher,args,event,send_type)

@good_cos.handle()
async def _(bot: Bot, matcher: Matcher, event: MessageEvent, arg: Message = CommandArg()):
    if not arg:
        await good_cos.finish("请指定cos类型")
    args = arg.extract_plain_text().split()
    if args[0] in GENSHIN_NAME:
        await good_cos.finish("原神暂不支持精品cos")
    elif args[0] in HONKAI3RD_NAME:
        send_type = Good(ForumType.Honkai3rdPic)
    elif args[0] in DBY_NAME:
        send_type = Good(ForumType.DBYCOS)
    elif args[0] in STAR_RAIL:
        await good_cos.finish("星穹铁道暂不支持精品cos")
    else:
        await good_cos.finish("暂不支持该类型")
    await send_images(bot,matcher,args,event,send_type)


@download_cos.got('game_type', prompt='你想下载哪种类型的,有原神和大别野,崩坏3')
async def got_type(game_type: str = ArgPlainText()):
    if game_type in GENSHIN_NAME:
        hot = Hot(ForumType.GenshinCos)
    elif game_type in DBY_NAME:
        hot = Hot(ForumType.DBYCOS)
    elif game_type in HONKAI3RD_NAME:
        hot = Hot(ForumType.Honkai3rdPic)
    elif game_type in STAR_RAIL:
        hot = Hot(ForumType.StarRailCos)
    image_urls = await hot.async_get_urls()
    if not image_urls:
        await download_cos.finish(f'没有找到{game_type}的cos图片')
    else:
        await download_cos.send(f'正在下载{game_type}的cos图片')
        try:
            await download_from_urls(image_urls, SAVE_PATH / f'{game_type}cos')
            await download_cos.finish(f'已成功保存{len(image_urls)}张{game_type}的cos图片')
        except WriteError as e:
            await download_cos.finish(f'保存{game_type}的cos图片失败,原因:{e}')

###########################################################################################

#定时任务
async def aps_send():
    logger.debug("正在发送定时推送")
    bot: Bot = get_bot()
    for game_type, dict in CONFIG.items():
        if game_type == "":
            continue
        for group_id, time in dict.items():
            if not (datetime.now().hour == int(time.split(":")[0]) and datetime.now().minute == int(time.split(":")[1])):
                continue
            try:
                group_id = int(group_id)
                if game_type in GENSHIN_NAME:
                    send_type = Rank(ForumType.GenshinCos, RankType.Daily)
                elif game_type in DBY_NAME:
                    send_type = Rank(ForumType.DBYCOS, RankType.Daily)
                elif game_type in HONKAI3RD_NAME:
                    send_type = Rank(ForumType.Honkai3rdPic, RankType.Daily)
                elif game_type in STAR_RAIL:
                    send_type = Rank(ForumType.StarRailCos, RankType.Daily)
                else:
                    continue
                image_list = await send_type.async_get_urls(page_size=5)
                name_list = await send_type.async_get_name(page_size=5)
                rank_text = '\n'.join([f"{i+1}.{name_list[i]}" for i in range(len(name_list))])
                msg_list = [f"✅米游社{game_type}cos每日榜单✅"]
                msg_list.append(rank_text)
                msg_list.append([MessageSegment.image(img) for img in image_list])
                msg_list = msglist2forward('米游社cos', '2854196306', msg_list)
                await bot.call_api("send_group_forward_msg", group_id=group_id, messages=msg_list)
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(e)


async def send_images(bot:Bot, matcher: Matcher, args: list, event: MessageEvent, send_type: HoyoBasicSpider):
    '''
    发送图片

    params:
        bot: 当前bot
        matcher: 事件响应器
        args: 命令参数(0:类型 1:数量)
        event: 消息事件类型
        send_type: 爬虫类型
    '''
    global user_data
    out_cd, deletime, user_data = check_cd(event.user_id, user_data)
    if out_cd:
        if len(args)<2:
            await matcher.send("获取图片中…请稍等")
            try:
                image_list = await send_type.async_get_urls()
                await matcher.send(MessageSegment.image(choice(image_list)))
            except ActionFailed:
                await matcher.finish("账户风控了,发送不了图片", at_sender=True)
        else:
            num = int(re.sub(r"[x|*|X]", "", args[1]))
            num = num if num <= MAX else MAX
            msg_list = [f'✅找到最新的一些{args[0]}图如下:✅']
            image_list = await send_type.async_get_urls()
            if num > len(image_list):
                await matcher.finish(f"最多只能获取{len(image_list)}张图片", at_sender=True)
            for i in range(num):
                msg_list.append(MessageSegment.image(image_list[i]))
            await send_forward_msg(bot, event, "米游社cos", bot.self_id, msg_list)
    else:
        await matcher.finish(f"cd冷却中,还剩{deletime}秒", at_sender=True)

@DRIVER.on_startup
@DRIVER.on_bot_connect
async def start_aps():
    try:
        if scheduler == None:
            logger.error("未安装apscheduler插件,无法使用此功能")
        with open(config_path, "r", encoding="utf8") as f:
            CONFIG = json.load(f)
        for game_type, dict in CONFIG.items():
            if game_type == "":
                continue
            for group_id, time in dict.items():
                if time == "":
                    continue
                try:
                    scheduler.add_job(aps_send, trigger="cron", hour=time.split(":")[0], minute=time.split(":")[1], id=f"{game_type}{group_id}")
                    logger.debug(f"已成功添加{group_id}的{game_type}定时推送")
                    scheduler.start()
                except Exception as e:
                    logger.error(e)
                    continue
    except Exception as e:
        logger.error(e)
        pass