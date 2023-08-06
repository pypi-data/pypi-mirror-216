from django.utils.translation import gettext_lazy

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 2.7 or above to run this plugin!")




class PluginApp(PluginConfig):
    name = "pretix_net_mail"
    verbose_name = "NET Mail"

    class PretixPluginMeta:
        name = gettext_lazy("NES Mail")
        author = "NETWAYS GmbH"
        description = gettext_lazy("Custom Email Renderer for NETWAYS")
        visible = True
        restricted = False 
        version = 1.3
        category = "CUSTOMIZATION"
        

    def ready(self):
        from . import signals  # NOQA


default_app_config = "pretix_net_mail.PluginApp"
