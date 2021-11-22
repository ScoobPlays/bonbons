from disnake.ext.commands import Bot
from aiohttp import ClientSession
from typing import Union

applications = {
    "youtube": "755600276941176913",  # Youtube
    "youtubedev": "880218832743055411",  # Youtube Development
    "poker": "755827207812677713",  # Poker
    "betrayal": "773336526917861400",  # Betrayal
    "fishing": "814288819477020702",  # Fishing
    "chess": "832012774040141894",  # Chess
    "chessdev": "832012586023256104",  # Chess Development
    "lettertile": "879863686565621790",  # Lettertile
    "wordsnack": "879863976006127627",  # Wordsnack
    "doodlecrew": "878067389634314250",  # Doodlecrew
    "spellcast": "852509694341283871",  # Spellcast
    "checkers": "807655087643557919",  # Checkers
}


class Together(object):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def create_link(self, voice_channel: int, activity: Union[str, int]):
        try:
            if not isinstance(voice_channel, int):
                raise TypeError(
                    f"Voice channel must be an integer, not {type(voice_channel).__name__}"
                )

            headers = {
                "Authorization": f"Bot {self.bot.http.token}",
                "Content-Type": "application/json",
            }

            async with ClientSession() as session:

                if str(activity) in applications.keys():
                    activity = applications[activity]

                data = {
                    "max_age": 1800,
                    "max_uses": None,
                    "target_application_id": int(activity) or applications[str(activity)],
                    "target_type": 2,
                    "temporary": False,
                    "validate": None,
                }

                async with session.post(
                    f"https://discord.com/api/v8/channels/{voice_channel}/invites",
                    json=data,
                    headers=headers,
                ) as raw:
                    data = await raw.json()
                    return f'https://discord.gg/{data["code"]}'

        except Exception as e:
            print(e)

