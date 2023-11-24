import logging.handlers
import os
import traceback

import requests
from khl import Bot, Cert, Message
from utils.open_json import open_json

if os.path.exists("./notification.log"):
    os.remove("./notification.log")

logger = logging.getLogger('khl')
logging.basicConfig(level='INFO')

handler = logging.handlers.RotatingFileHandler(
    filename='notification.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)

# 初始化机器人
# 打开config.json
config = open_json('./config/config.json')
bot = Bot(token=config['token'])  # 默认采用 websocket
"""main bot"""
if not config['using_ws']:  # webhook
    # 当配置文件中'using_ws'键值为false时，代表不使用websocket
    # 此时采用webhook方式初始化机器人
    print(f"[BOT] using webhook at port {config['webhook_port']}")
    bot = Bot(cert=Cert(token=config['token'],
                        verify_token=config['verify_token'],
                        encrypt_key=config['encrypt_token']),
              port=config['webhook_port'])

@bot.command(name='new')
async def new(msg: Message):
    try:
        newest = requests.get("https://gp.zkitefly.eu.org/https://github.com/burningtnt/HMCL-Snapshot-Update/raw/master/datas/snapshot.json")
        await msg.reply(f"""最新的版本为：{newest.json()['version']}
下载链接：[{newest.json()['jar']}]({newest.json()['jar']})
GitHub Commit：[https://github.com/huanghongxun/HMCL/commit/{newest.json()['version'][8:]}](https://github.com/huanghongxun/HMCL/commit/{newest.json()['version'][8:]})""")
    except:
        logging.error(traceback.format_exc())
        await msg.reply(f"获取最新版本失败，以下是详细错误信息\n```\n{traceback.format_exc()}\n```")
bot.run()
