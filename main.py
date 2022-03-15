import asyncio
import random

from utils.bot import Bonbons

bot = Bonbons()

class TextGenerator:#  credit: swas.py
    def __init__(self, depth=1) -> None:
        self.map = {}
        self.depth = depth

    def train(self, text: str):
        s = ["__start__"] + text.split(" ")
        c = self.depth
        while c >= 1:
            for i, word in enumerate(s[:-c]):
                x = s[i+1:i+c+1]
                if word in self.map:
                    self.map[word].append(x)
                else:
                    self.map[word] = [x]
            c -= 1

    def generate_text(self, start = None):
        sentence = []
        if start and start in self.map:
            sentence.append(start)
        else:
            start = random.choice(self.map["start"])[0]
            sentence.append(start)

        while start in self.map and len(sentence) < 25:
            x = random.choice(self.map[start])
            sentence += x
            start = x[-1]

        return " ".join(sentence)

bot.text = TextGenerator(depth=3) 

@bot.listen("on_message")
async def on_message(message):
    bot.text.train(message.content)

@bot.command(name="gentext")
async def gentext(ctx, start: str = None):
    result = bot.text.generate_text(start)
    await ctx.send(result)

async def main():
    await bot.start()

asyncio.run(main())
