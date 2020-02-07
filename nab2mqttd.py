import sys
import datetime
#from asgiref.sync import sync_to_async
from asgiref.sync import async_to_sync
from nabcommon.nabservice import NabInfoService
import logging
import json
import paho.mqtt.client as mqtt

class Nab2MQTTd(NabInfoService):

    # on_connect callback
    def on_connect(self, client, userdata, flags, rc):
        from . import models
        logging.debug("Connected to MQTT with result code " + str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        config = models.Config.load()
        client.subscribe(config.topic)

    # on_message callback
    # samples:
    # {"type":"sleep"}
    # {"type":"wakeup"}
    # {"type":"message", "body":[{"audio":["nabsurprised/2.mp3"]}]}
    # {"type":"message", "body":[{"audio":["nabsurprised/2.mp3"]}], "expiration":"TAGEXPIRATION"}
    def on_message(self, client, userdata, msg):
          logging.debug(msg.payload)
          packet = str(msg.payload.decode("utf-8","ignore"))
          #state = json.loads(m_decode)
          #logging.debug(state)

          # replace TAGEXPIRATION string by properly formatted expiration datetime
          if "TAGEXPIRATION" in packet:
            now = datetime.datetime.now(datetime.timezone.utc)
            expiration = now + datetime.timedelta(minutes=1)
            packet = packet.replace("TAGEXPIRATION", expiration.isoformat())

          # add mandatory carriage return
          packet = packet + "\r\n"
          self.writer.write(packet.encode("utf8"))
          async_to_sync(self.writer.drain)()
            
    def __init__(self):
        super().__init__()
        from . import models

        config = models.Config.load()
        logging.debug("Config.server: " + str(config.server))
        #logging.debug("Config.clientid: " + str(config.clientid))
        #logging.debug("Config.username: " + str(config.username))
        #logging.debug("Config.password: " + str(config.password))
        #logging.debug("Config.port: " + str(config.port))
        #logging.debug("Config.tls: " + str(config.tls))
        #logging.debug("Config.tlsinsecure: " + str(config.tlsinsecure))
        logging.debug("Config.topic: " + str(config.topic))

        self.client = mqtt.Client(client_id = config.clientid)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        if config.username:
          self.client.username_pw_set(config.username, config.password)
        if config.tls == 'true':
          self.client.tls_set("/home/pi/pynab/nab2mqttd/ca.crt") # merdique... 
        if config.tlsinsecure == 'true':
          self.client.tls_insecure_set(True)
        self.client.connect(config.server, int(config.port), 60)
        self.client.loop_start()

    def get_config(self):
        from . import models
        
        config = models.Config.load()
        return (
            config.next_performance_date,
            config.next_performance_type,
            (
                config.server,
                config.clientid,
                config.username,
                config.password,
                config.port,
                config.tls,
                config.tlsinsecure,
                config.topic,
            ),
        )

    def update_next(self, next_date, next_args):
        #logging.debug("update_next")
        from . import models
        config = models.Config.load()
        config.next_performance_date = next_date
        config.next_performance_type = next_args
        config.save()

    async def fetch_info_data(self, config_t):
        #logging.debug("fetch_info_data")
        return None

 #   def next_info_update(self, config):
 #       logging.debug("next_info_update")
 #       if config is None:
 #           return None
 #       now = datetime.datetime.now(datetime.timezone.utc)
 #       next_loop = now + datetime.timedelta(seconds=30)
 #       return next_loop

    def get_animation(self, info_data):
        #logging.debug("get_animation")
        return None

    async def perform_additional(self, expiration, type, info_data, config_t):
        #logging.debug("perform_additional")
        #if (info_data is None):
        return

if __name__ == "__main__":
    Nab2MQTTd.main(sys.argv[1:])
