
# Nab2MQTTd 
Client module connecting to MQTT and trigerring Nabaztag actions based on MQTT messages.

### deployment
PAHO MQTT is required, run as root:
```
pip install paho-mqtt
```

Add nab2mqttd in the INSTALLED_APPS section of nabweb/settings.py


### MQTT with TLS and self signed cert
For now if you plan to use TLS the public key must be copied to the server in:
```
/home/pi/pynab/nab2mqttd/ca.crt
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

Tips:
- Use TAGEXPIRATION to set automatically an expiration on 1 minute for the command. Will automatically be computed based on internal Nabaztag time.
- To ensure *sleep* and *wakeup* commands are effective, you need to stop the *nabclockd* and *nabmastodond* service, otherwise commands will be overridden.

### TODO
Manage chroregraphies:
{"type":"command", "sequence":[{"audio":["nabsurprised/2.mp3"]}] }
{"type":"command", "sequence":[{"choreography":"data:application/x-nabaztag-mtl-choreography;base64,xxx"}] }
