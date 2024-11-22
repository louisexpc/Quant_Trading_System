from pymongo.mongo_client import MongoClient
from .ConfigLoader import config
from .discordconnector import DiscordConnector

class DatabaseConnector:
    _instance = None

    def __new__(cls, config_path=None):
        if cls._instance is None:
            cls._instance = super(DatabaseConnector, cls).__new__(cls)
        return cls._instance

    def __init__(self, config_path=None):
        # 避免重複初始化
        if not hasattr(self, '_initialized') or not self._initialized:
            self._initialized = True
            try:
                # 加載配置
                config_data = config(config_path).load_config()['mongo']['cloud']

                # 初始化 MongoDB 連接
                self.client = MongoClient(config_data['uri'])
                self.client.admin.command('ping')
                print("Successfully connected to MongoDB!")

                # 設置數據庫和集合
                self.collection = self.client[config_data['db']][config_data['collection']]

                # 連接discord
                self.discord = DiscordConnector()
            except Exception as e:
                print(f"Database: Error: Connection failed, {e}")
                self.client = None

    def get_cloud_connection(self):
        if self.client:
            return self.client
        else:
            print("Error: MongoDB connection is not available.")
            return None

    def store(self, data):
        try:
            # 使用顯式的 None 判斷來檢查 collection
            if self.collection is not None:
                self.collection.insert_one(data)
                print("Data stored successfully.")
                self.discord.send_message("Data stored successfully.")
            else:
                print("Error: Collection is not available.")
        except Exception as e:
            print(f"Error storing data: {e}")
            self.discord.send_message(f"Error storing data: {e}")

# if __name__ == "__main__":
#     # 初始化資料庫連接
#     CONFIG_PATH ="C:\\Users\\louislin\\OneDrive\\桌面\\data_analysis\\trading_system_v1\\config\\database.json"
#     db = DatabaseConnector(CONFIG_PATH)
#     cursor = db.collection.find({'symbol':"BTC/USDT"})  # 篩選年齡大於 20 的文件
#     for doc in cursor:
#         print(doc)


