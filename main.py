import time
import os
import datetime
import schedule
from pkg.ConfigLoader import config
from internal.trader.trader import Trader

ROOT = os.getcwd()
CONFIG_DIR = os.path.join(ROOT, 'config')
CONFIG_PATH = os.path.join(CONFIG_DIR, 'account.json')

def job():
    # 加載帳戶配置
    print(f"Main execute at {datetime.datetime.now()}")
    account_config = config(CONFIG_PATH).load_config()
    trader = Trader(account_config)
    trader.run()

if __name__ == '__main__':
    # 在每小時的 00, 15, 30, 45 分執行
    schedule.every().hour.at(":00").do(job)
    schedule.every().hour.at(":15").do(job)
    schedule.every().hour.at(":30").do(job)
    schedule.every().hour.at(":45").do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
