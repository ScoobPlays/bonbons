from disnake.ext.commands import Bot
from aiohttp import ClientSession
from typing import Union
from .constants import applications


class Together:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def create_activity(self, voice_channel: int, activity: Union[str, int]):
        try:
            if not isinstance(voice_channel, int):
                raise TypeError(
                    f"Voice channel must be an integer, not {type(voice_channel).__name__}"
                )

            headers = {
                "Authorization": f"Bot {self.bot.http.token}",
                "Content-Type": "application/json",
            }

            async with ClientSession(headers=headers) as session:

                if str(activity) in applications.keys():
                    activity = applications[activity]

                data = {
                    "max_age": 1800,
                    "max_uses": None,
                    "target_application_id": int(activity)
                    or applications[str(activity)],
                    "target_type": 2,
                    "temporary": False,
                    "validate": None,
                }

                async with session.post(
                    f"https://discord.com/api/v9/channels/{voice_channel}/invites",
                    json=data,
                ) as raw:
                    data = await raw.json()
                    print(data)
                    return f'https://discord.gg/{data["code"]}'

        except Exception as e:
            print(e)
