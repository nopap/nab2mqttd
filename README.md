
# Nab2MQTTd 
Client module connecting to MQTT and trigerring Nabaztag actions based on MQTT messages.

Docs:
- How to implement a Nabaztag service: https://github.com/nabaztag2018/pynab/wiki/How-to-create-a-new-service
- Forum: https://www.tagtagtag.fr/forum/

### deployment
PAHO MQTT is required, run as root:
```
pip install paho-mqtt
```

Add nab2mqttd in the INSTALLED_APPS section of nabweb/settings.py


### MQTT with TLS and self signed cert
For now if you plan to use TLS the public key must be copied to the server in:
```
/opt/pynab/nab2mqttd/ca.crt
```

### installation
```
cd /opt/pynab
source /opt/pynab/venv/bin/activate
pip install paho-mqtt
git clone https://github.com/nopap/nab2mqttd.git
python manage.py makemigrations
python manage.py migrate
sudo cp nab2mqttd.service /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable nab2mqttd
sudo service nab2mqttd start
```

### Usage
Send to MQTT server on the specified topic the JSON commands as described in Pynab PROTOCOL documentation
https://github.com/nabaztag2018/pynab/blob/master/PROTOCOL.md

Examples:
- {"type":"sleep"}
- {"type":"wakeup"}
- {"type":"ears","left":10,"right":30} (should not be used here, as it repositions the ears instead of just moving them, normally for the rabbit pairing)
- {"type":"message", "body":[{"audio":["nabsurprised/2.mp3"]}]}
- {"type":"message", "body":[{"audio":["nabsurprised/2.mp3"]}], "expiration":"TAGEXPIRATION"}
- {"type":"command", "sequence":[{"audio":["nabsurprised/2.mp3"]}] }
- {"type":"command", "sequence":[{"choreography":"data:application/x-nabaztag-mtl-choreography;base64,ABQAAAARAAo="}] }

- {"type":"info", "info_id":"nab2mqtt", "animation": {"tempo":15,"colors":[{"left":"ff0000","center":"00ff00","right":"0000ff"},{"left":"00ff00","center":"0000ff","right":"ff0000"},{"left":"0000ff","center":"ff0000","right":"00ff00"}]}}

Tips:
- Use TAGEXPIRATION to set automatically an expiration on 1 minute for the command. Will automatically be computed based on internal Nabaztag time.
- To ensure *sleep* and *wakeup* commands are effective, you need to stop the *nabclockd* and *nabmastodond* service, otherwise commands will be overridden.
- type:info sends a new animation that the service will play regularly. send another or an empty one to change it or cancel it.

### Chroregraphies:
{"type":"command", "sequence":[{"audio":["nabsurprised/2.mp3"]}] }
{"type":"command", "sequence":[{"choreography":"data:application/x-nabaztag-mtl-choreography;base64,xxx"}] }

Build the bas base64 sequence using different libraries:
- Javascript: use and customize *command.ts* from this project: https://github.com/datagutt/pynab.js
- C#: https://github.com/nopap/choreography
