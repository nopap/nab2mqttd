from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse, QueryDict
from django.utils.translation import ugettext as _
from .models import Config
from .nab2mqttd import Nab2MQTTd
from django.utils import translation
import datetime


class SettingsView(TemplateView):
    template_name = "nab2mqttd/settings.html"

    def get_context_data(self, **kwargs):
        # on charge les donnees depuis la base de données
        context = super().get_context_data(**kwargs)
        context["config"] = Config.load()
        return context

    def post(self, request, *args, **kwargs):
        # quand on reçoit une nouvelle config (via interface)
        config = Config.load()
        if "server" in request.POST:
            config.server = request.POST["server"]
        if "clientid" in request.POST:
            config.clientid = request.POST["clientid"]
        if "username" in request.POST:
            config.username = request.POST["username"]
        if "password" in request.POST:
            config.password = request.POST["password"]
        if "port" in request.POST:
            config.port = request.POST["port"]
        if "tls" in request.POST:
            config.tls = request.POST["tls"]
        if "tlsinsecure" in request.POST:
            config.tlsinsecure = request.POST["tlsinsecure"]
        if "topic" in request.POST:
            config.topic = request.POST["topic"]
        config.save()
        Nab2MQTTd.signal_daemon()
        context = self.get_context_data(**kwargs)
        return render(request, SettingsView.template_name, context=context)

    def put(self, request, *args, **kwargs):
        # quand on clique sur le bouton de l'intervaface pour jouer tout de suite
        # restart the MQTT daemon 
        Nab2MQTTd.signal_daemon()
        return JsonResponse({"status": "ok"})
