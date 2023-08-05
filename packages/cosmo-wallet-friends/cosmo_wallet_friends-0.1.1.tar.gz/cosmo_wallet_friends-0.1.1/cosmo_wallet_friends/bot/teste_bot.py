import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

        if message.content == '!regras':
            await message.channel.send('pong')
        
        if message.content == '!carteira':
            await message.author.send('10 mil reais')

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run('MTEyMjU2MTY2OTIxMDU4NzE1Nw.GC4i81.ZpuOw8AUQDfYvhuVhW8khUAUjsIYuIKWN7IaX0')
