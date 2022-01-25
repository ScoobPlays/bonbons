from utils.bot import Bonbons

bot = Bonbons()

import random

@bot.listen()
async def on_message(msg):

    if msg.content.startswith("!!"):
        new_msg = msg.content.replace("!!", "").split()

        if new_msg[0].lower() not in ["sus", "pedo", "gay", "lesbian"]:
            return
            
        await msg.channel.send(f"{new_msg[1]} is {random.randint(1, 100)}% {new_msg[0]}")

bot.run()