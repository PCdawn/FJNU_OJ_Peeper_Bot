import base64
import json

from botpy import BotAPI
from botpy.message import Message, GroupMessage

__interact_version__ = "v2.0.1"

_key_words = {
    "傻逼": "谢谢夸奖",
    "性别": "盲猜我的性别是武装直升机",
    "干嘛": "how",
    "谢谢": "qaq",
    "qaq": "qwq",
    "你是谁": "猜猜我是谁",
    "愚蠢": "yes，我只会关键词匹配",
    "丁真": "妈妈生的",
}


class RobotMessage:
    def __init__(self, api: BotAPI):
        self.api = api
        self.guild = False
        self.guild_message = None
        self.group_message = None
        self.content = ""
        self.msg_seq = 0

    def setup_guild_message(self, message: Message):
        self.guild = True
        self.guild_message = message
        self.content = message.content
        self.msg_seq = 0

    def setup_group_message(self, message: GroupMessage):
        self.guild = False
        self.group_message = message
        self.content = message.content
        self.msg_seq = 0

    def get_author(self):
        if self.guild:
            return self.guild_message.author.__dict__['id']
        else:
            return self.group_message.author.__dict__['member_openid']

    async def reply(self, content: str, img_path: str = None, img_url: str = None):
        self.msg_seq += 1
        if self.guild:  # 频道消息
            await self.api.post_message(channel_id=self.guild_message.channel_id, msg_id=self.guild_message.id,
                                        content=f"<@{self.guild_message.author.id}>{content}", file_image=img_path,
                                        image=img_url)
        else:  # 群消息
            if img_path is not None:
                with open(img_path, "rb") as img:
                    file_image = img.read()
                media = await self.api.post_group_file(
                    group_openid=self.group_message.group_openid,
                    file_type=1,
                    file_data=base64.b64encode(file_image).decode('UTF-8'),
                )
                await self.api.post_group_message(
                    group_openid=self.group_message.group_openid,
                    msg_type=7,
                    msg_id=self.group_message.id,
                    content=content,
                    media=media,
                    msg_seq=self.msg_seq
                )
            elif img_url is not None:
                media = await self.api.post_group_file(
                    group_openid=self.group_message.group_openid,
                    file_type=1,
                    url=img_url,
                )
                await self.api.post_group_message(
                    group_openid=self.group_message.group_openid,
                    msg_type=7,
                    msg_id=self.group_message.id,
                    content=content,
                    media=media,
                    msg_seq=self.msg_seq
                )
            else:
                await self.api.post_group_message(
                    group_openid=self.group_message.group_openid,
                    msg_type=0,
                    msg_id=self.group_message.id,
                    content=content,
                    msg_seq=self.msg_seq
                )


def match_key_words(content: str) -> str:
    for each in _key_words:
        if each in content:
            return _key_words[each]
    return "你干嘛"

