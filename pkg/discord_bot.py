import discord
import os
import ccxt
import pytz
import json
import asyncio
from dotenv import load_dotenv
from datetime import datetime, timedelta
load_dotenv("..\\.env")
class MyBot(discord.Client):
    
    def __init__(self, **options) :
        #初始化必備權限
        intents = discord.Intents.default()
        intents.message_content = True
         # 將設定好的 intents 傳入父類別
        super().__init__(intents=intents,**options)

        #初始化cctx
        self.binance = ccxt.binance()
        self.trade_pair = ["BTC/USDT","ETH/USDT"]

        #初始化參數
        self.period = 2 #unit: mins
        
    
    async def on_ready(self):
        print(f"Logged on as {self.user}!")
        # server ready and then get channel
        if os.getenv("CHANNEL_ID")!=None:
            print(f"channel id: {os.getenv('CHANNEL_ID')}")
            self.channel = self.get_channel(int(os.getenv("CHANNEL_ID")))
            if self.channel ==None:
                print("error: NoneType")
        else:
            print("Error: Couldn't find channel ID")
        self.loop.create_task(self.automatic_price_task())
    
    async def on_message(self,message):
        print(f"Message from {message.author}: {message.content}")

        if message.author == self.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('hello')

        # 查詢即時幣價
        if message.content.startswith("$search"):
            await self.price_search(self.channel)

        '''
        if message.content.startswith("<@698385089612087317>"):    
            await message.channel.send(f'<@698385089612087317> 是個噁心蘿莉控')

        if message.content.startswith("<@698385089612087317> 是蘿莉控嗎"):
            await message.channel.send(f'是的 <@698385089612087317> 真的超噁心')
        '''
    
    async def automatic_price_task(self):
        await self.wait_until_ready()
        while not self.is_closed():
            await self.price_search(self.channel)
            await asyncio.sleep(self.period * 60)


    async def price_search(self,channel):
        for pair in self.trade_pair:
            info = self.binance.fetch_ticker(pair)
            date = datetime.strptime(info['datetime'],'%Y-%m-%dT%H:%M:%S.%fZ')
            datetime_8_time = date + timedelta(hours=8)
            await channel.send(f'Pair: {pair}\ntime: {datetime_8_time} , Price: {info["close"]}')
            



    '''
    Extension: Error log: 錯誤訊息的紀錄: https://discordpy.readthedocs.io/en/stable/logging.html
    '''
if __name__=='__main__':
    token = os.getenv("TOKEN")
    client = MyBot()
    client.run(token=token)

