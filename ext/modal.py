import discord, secrets
from utils.bot import Bonbons
from .enums import InputStyle
from typing import Union, List
import asyncio

__all__ = ('TextInput', 'Modal')

class TextInput:
    def __init__(self, payload: dict):
        self.type = payload['type']
        self.custom_id = payload['custom_id']
        self.style = payload['style']
        self.label = payload['label']
        self.min_length = payload.get('min_length')
        self.max_length = payload.get('max_length')
        self.required = payload.get('required')
        self.value = payload.get('value')
        self.placeholder = payload.get('placeholder')

class Modal:
    def __init__(self, title: str = 'Title', options: List[TextInput] = None):
        self.bot = Bonbons()
        self.title = title
        self.custom_id = secrets.token_urlsafe(16)
        self.payload = {
          'title': title,
          'custom_id': self.custom_id,
          'components': []
        }
        self.adapter = discord.webhook.async_.async_context.get()
        self.fields = []
        self.options = options



    def add_option(
        self,
        *,
        style: Union[int, InputStyle]=InputStyle.short,
        label: str=None,
        custom_id: int=secrets.token_urlsafe(16),
        min_length: int=None,
        max_length: int=None,
        required: bool=False,
        value: str=None,
        placeholder: str=None,
        ):

        """
        Adds a field to the modal.
        
        Parameters
        ----------

        style: InputStyle
            The style of the input.

        label: str
            The label of the input.

        min_length: int
            The minimum length of the input.

        max_length: int
            The maximum length of the input.

        required: bool
            Whether the input is required or not.

        value: str
            The value of the input.
        
        placeholder: str
            The placeholder of the input.
        """


        component = {
            'type': 4,
            'custom_id': custom_id,
            'style': style.value if hasattr(style, 'value') else 1,
            'label': label,
            'required': str(required),
        }

        if min_length:
            component['min_length'] = min_length

        if max_length:
            component['max_length'] = max_length

        if value:
            component['value'] = value

        if placeholder:
            component['placeholder'] = placeholder

        self.payload['components'].append({
            'type': 1,
            'components': [component]
        })

        self.fields.append(TextInput(component))

    async def send_modal(self, interaction: discord.Interaction):

        """
        Sends the modal.
        
        Parameters
        ----------
        
        interaction: discord.Interaction
            The interaction that triggered the modal.
        """


        interaction.response._responded = True

        await self.adapter.create_interaction_response(
            interaction_id = interaction.id,
            token = interaction.token,
            session = interaction._session,
            data = self.payload,
            type = 9
        )

    async def wait(self, timeout: int=180):

        """
        Waits for the modal to be sent.

        Parameters
        ----------

        timeout: int
            The timeout in seconds.
        """

        def interaction_check(interaction: discord.Interaction):
            return interaction.data.get('custom_id') == self.custom_id

        try:
            interaction = await self.bot.wait_for('interaction', check=interaction_check, timeout=timeout)
        except asyncio.TimeoutError:
            return None, []

        components = interaction.data['components']

        result = []
        for component in components:
            for field in self.fields:
                if component['components'][0]['custom_id'] == field.custom_id:
                    field.value = component['components'][0]['value']
                    result.append(field)

        return interaction, result
