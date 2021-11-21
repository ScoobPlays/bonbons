from aiohttp import ClientSession
from disnake import Client, AutoShardedClient, HTTPException
from disnake.ext.commands import Bot, AutoShardedBot, BotMissingPermissions
from disnake.http import Route
from typing import Union, Optional
from .errors import (
    InvalidChannelID,
    InvalidActivityChoice,
    InvalidCustomID,
    RangeExceeded,
)

applications = {
    "youtube": "755600276941176913", #Youtube 
    "youtubedev": "880218832743055411", #Youtube Development
    "poker": "755827207812677713", # Poker
    "betrayal": "773336526917861400", # Betrayal
    "fishing": "814288819477020702", # Fishing
    "chess": "832012774040141894", # Chess
    "chessdev": "832012586023256104", # Chess Development
    "lettertile": "879863686565621790", # Lettertile
    "wordsnack": "879863976006127627", # Wordsnack
    "doodlecrew": "878067389634314250", # Doodlecrew
    "spellcast": "852509694341283871", # Spellcast
    "checkers": "807655087643557919", # Checkers
}

class ActivityLink:
    def __init__(self, invite_code: str):
        self.raw_code = invite_code
        self.short_link = f"discord.gg/{invite_code}"

    def __repr__(self):
        return f"https://discord.gg/{self.raw_code}"

class Together:
    def __init__(
        self,
        client: Union[Client, Bot, AutoShardedClient, AutoShardedBot],
        *,
        debug: Optional[bool] = False,
    ):
        if isinstance(client, (Client, AutoShardedClient, Bot, AutoShardedBot)):
            self.client = client
        else:
            raise ValueError("The client/bot object parameter is not valid.")

        if isinstance(debug, bool):
            self.debug = debug
        else:
            self.debug = False
            print(
                "\033[93m"
                + "[WARN] (together) Debug parameter did not receive a bool object. "
                "Reverting to Debug = False." + "\033[0m"
            )

    async def create_link(
        self,
        voice_channel_id: Union[int, str],
        option: Union[int, str],
        *,
        max_age: Optional[int] = 0,
        max_uses: Optional[int] = 0,
    ) -> ActivityLink:

        if not isinstance(voice_channel_id, (str, int)):
            raise TypeError(
                f"'voiceChannelID' argument MUST be of type string or integer, "
                f'not a "{type(voice_channel_id).__name__}" type.'
            )
        if not isinstance(option, (str, int)):
            raise TypeError(
                f"'option' argument MUST be of type string or integer, not a \"{type(option).__name__}\" type."
            )

        if not 0 <= max_age <= 604800:
            raise RangeExceeded(
                f"max_age parameter value should be an integer between 0 and 604800"
            )
        if not 0 <= max_uses <= 100:
            raise RangeExceeded(
                f"max_uses parameter value should be an integer between 0 and 100"
            )

        if option and (
            str(option).lower().replace(" ", "") in applications.keys()
        ):

            data = {
                "max_age": max_age,
                "max_uses": max_uses,
                "target_application_id": applications[
                    str(option).lower().replace(" ", "")
                ],
                "target_type": 2,
                "temporary": False,
                "validate": None,
            }

            try:
                result = await self.client.http.request(
                    Route("POST", f"/channels/{voice_channel_id}/invites"), json=data
                )
            except HTTPException as e:
                if self.debug:
                    async with ClientSession() as session:
                        async with session.post(
                            f"https://discord.com/api/v8/channels/{voice_channel_id}/invites",
                            json=data,
                            headers={
                                "Authorization": f"Bot {self.client.http.token}",
                                "Content-Type": "application/json",
                            },
                        ) as resp:
                            result = await resp.json()
                    print(
                        "\033[95m"
                        + "\033[1m"
                        + "[DEBUG] (together) Response Output:\n"
                        + "\033[0m"
                        + str(result)
                    )

                if e.code == 10003 or "channel_id: snowflake value" in e.text:
                    raise InvalidChannelID("Voice Channel ID is invalid.")
                elif e.code == 50013:
                    raise BotMissingPermissions(["CREATE_INSTANT_INVITE"])
                elif e.code == 130000:
                    raise ConnectionError(
                        "API resource is currently overloaded. Try again a little later."
                    )
                else:
                    raise ConnectionError(
                        f"[status: {e.status}] (code: {e.code}): An unknown error occurred while retrieving "
                        f"data from discord API."
                    )

            if self.debug:
                print(
                    "\033[95m"
                    + "\033[1m"
                    + "[DEBUG] (together) Response Output:\n"
                    + "\033[0m"
                    + str(result)
                )

            return ActivityLink(result["code"])

        elif (
            option
            and (str(option).replace(" ", "") not in applications.keys())
            and str(option).replace(" ", "").isnumeric()
        ):
            data = {
                "max_age": max_age,
                "max_uses": max_uses,
                "target_application_id": str(option).replace(" ", ""),
                "target_type": 2,
                "temporary": False,
                "validate": None,
            }

            try:
                result = await self.client.http.request(
                    Route("POST", f"/channels/{voice_channel_id}/invites"), json=data
                )
            except HTTPException as e:
                if self.debug:
                    async with ClientSession() as session:
                        async with session.post(
                            f"https://discord.com/api/v8/channels/{voice_channel_id}/invites",
                            json=data,
                            headers={
                                "Authorization": f"Bot {self.client.http.token}",
                                "Content-Type": "application/json",
                            },
                        ) as resp:
                            result = await resp.json()
                    print(
                        "\033[95m"
                        + "\033[1m"
                        + "[DEBUG] (together) Response Output:\n"
                        + "\033[0m"
                        + str(result)
                    )

                if e.code == 10003 or "channel_id: snowflake value" in e.text:
                    raise InvalidChannelID("Voice Channel ID is invalid.")
                elif "target_application_id" in e.text:
                    raise InvalidCustomID(
                        str(option).replace(" ", "")
                        + " is an invalid custom application ID."
                    )
                elif e.code == 50013:
                    raise BotMissingPermissions(["CREATE_INSTANT_INVITE"])
                elif e.code == 130000:
                    raise ConnectionError(
                        "API resource is currently overloaded. Try again a little later."
                    )
                else:
                    raise ConnectionError(
                        f"[status: {e.status}] (code: {e.code}): An unknown error occurred while retrieving data from "
                        f"discord API."
                    )

            if self.debug:
                print(
                    "\033[95m"
                    + "\033[1m"
                    + "[DEBUG] (together) Response Output:\n"
                    + "\033[0m"
                    + str(result)
                )

            return ActivityLink(result["code"])

        else:
            raise InvalidActivityChoice(
                'Invalid activity option chosen. You may only choose between ("{}") or '
                "input a custom application ID.".format(
                    '", "'.join(applications.keys())
                )
            )

    async def create_activity(
        self,
        voice_channel_id: Union[int, str],
        option: Union[int, str],
        *,
        max_age: Optional[int] = 0,
        max_uses: Optional[int] = 0,
    ) -> ActivityLink:

        if not isinstance(voice_channel_id, (str, int)):
            raise TypeError(
                f"'voiceChannelID' argument MUST be of type string or integer, "
                f'not a "{type(voice_channel_id).__name__}" type.'
            )
        if not isinstance(option, (str, int)):
            raise TypeError(
                f"'option' argument MUST be of type string or integer, not a \"{type(option).__name__}\" type."
            )

        if not 0 <= max_age <= 604800:
            raise RangeExceeded(
                f"max_age parameter value should be an integer between 0 and 604800"
            )
        if not 0 <= max_uses <= 100:
            raise RangeExceeded(
                f"max_uses parameter value should be an integer between 0 and 100"
            )

        if option and (
            str(option).lower().replace(" ", "") in applications.keys()
        ):

            data = {
                "max_age": max_age,
                "max_uses": max_uses,
                "target_application_id": applications[
                    str(option).lower().replace(" ", "")
                ],
                "target_type": 2,
                "temporary": False,
                "validate": None,
            }

            try:
                result = await self.client.http.request(
                    Route("POST", f"/channels/{voice_channel_id}/invites"), json=data
                )
            except HTTPException as e:
                if self.debug:
                    async with ClientSession() as session:
                        async with session.post(
                            f"https://discord.com/api/v8/channels/{voice_channel_id}/invites",
                            json=data,
                            headers={
                                "Authorization": f"Bot {self.client.http.token}",
                                "Content-Type": "application/json",
                            },
                        ) as resp:
                            result = await resp.json()
                    print(
                        "\033[95m"
                        + "\033[1m"
                        + "[DEBUG] (together) Response Output:\n"
                        + "\033[0m"
                        + str(result)
                    )

                if e.code == 10003 or "channel_id: snowflake value" in e.text:
                    raise InvalidChannelID("Voice Channel ID is invalid.")
                elif e.code == 50013:
                    raise BotMissingPermissions(["CREATE_INSTANT_INVITE"])
                elif e.code == 130000:
                    raise ConnectionError(
                        "API resource is currently overloaded. Try again a little later."
                    )
                else:
                    raise ConnectionError(
                        f"[status: {e.status}] (code: {e.code}): An unknown error occurred while retrieving "
                        f"data from discord API."
                    )

            if self.debug:
                print(
                    "\033[95m"
                    + "\033[1m"
                    + "[DEBUG] (together) Response Output:\n"
                    + "\033[0m"
                    + str(result)
                )

            return ActivityLink(result["code"])

        elif (
            option
            and (str(option).replace(" ", "") not in applications.keys())
            and str(option).replace(" ", "").isnumeric()
        ):
            data = {
                "max_age": max_age,
                "max_uses": max_uses,
                "target_application_id": str(option).replace(" ", ""),
                "target_type": 2,
                "temporary": False,
                "validate": None,
            }

            try:
                result = await self.client.http.request(
                    Route("POST", f"/channels/{voice_channel_id}/invites"), json=data
                )
            except HTTPException as e:
                if self.debug:
                    async with ClientSession() as session:
                        async with session.post(
                            f"https://discord.com/api/v8/channels/{voice_channel_id}/invites",
                            json=data,
                            headers={
                                "Authorization": f"Bot {self.client.http.token}",
                                "Content-Type": "application/json",
                            },
                        ) as resp:
                            result = await resp.json()
                    print(
                        "\033[95m"
                        + "\033[1m"
                        + "[DEBUG] (together) Response Output:\n"
                        + "\033[0m"
                        + str(result)
                    )

                if e.code == 10003 or "channel_id: snowflake value" in e.text:
                    raise InvalidChannelID("Voice Channel ID is invalid.")
                elif "target_application_id" in e.text:
                    raise InvalidCustomID(
                        str(option).replace(" ", "")
                        + " is an invalid custom application ID."
                    )
                elif e.code == 50013:
                    raise BotMissingPermissions(["CREATE_INSTANT_INVITE"])
                elif e.code == 130000:
                    raise ConnectionError(
                        "API resource is currently overloaded. Try again a little later."
                    )
                else:
                    raise ConnectionError(
                        f"[status: {e.status}] (code: {e.code}): An unknown error occurred while retrieving data from "
                        f"discord API."
                    )

            if self.debug:
                print(
                    "\033[95m"
                    + "\033[1m"
                    + "[DEBUG] (together) Response Output:\n"
                    + "\033[0m"
                    + str(result)
                )

            return ActivityLink(result["code"])

        else:
            raise InvalidActivityChoice(
                'Invalid activity option chosen. You may only choose between ("{}") or '
                "input a custom application ID.".format(
                    '", "'.join(applications.keys())
                )
            )