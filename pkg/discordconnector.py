from discord import SyncWebhook

from pkg.ConfigLoader import config


class DiscordConnector(object):
    def __init__(self,config_path):
        try:
            self.url = config(config_path).load_config()['webhookURL']
        except Exception as e:
            print(f"Error: can't load config URL {e}")

    def send_message(self, message):
        webhook = SyncWebhook.from_url(self.url)
        webhook.send(message)