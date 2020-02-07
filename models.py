from django.db import models
from nabcommon import singleton_model


# ici on defini le modele de donnes pour la config


class Config(singleton_model.SingletonModel):

    server = models.TextField(null=True)
    clientid = models.TextField(null=True)
    username = models.TextField(null=True)
    password = models.TextField(null=True)
    port = models.TextField(null=True)
    tls = models.TextField(null=True)
    tlsinsecure = models.TextField(null=True)
    topic = models.TextField(null=True)

    # necessaire pour declencher via le site web
    next_performance_date = models.DateTimeField(null=True)
    next_performance_type = models.TextField(null=True)

    class Meta:
        app_label = "nab2mqttd"
