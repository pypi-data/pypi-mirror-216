from pretix.base.email import TemplateBasedMailRenderer
from django.template.loader import get_template

class NESMailRenderer(TemplateBasedMailRenderer):
    verbose_name = "NES Training"
    identifier = "NES"
    thumbnail_filename = "pretix_net_mail/NETthumb.png"
    template_name = "pretix_net_mail/NES.html"

class STACKCONFMailRenderer(TemplateBasedMailRenderer):
    verbose_name = "stackconf"
    identifier = "stackconf"
    thumbnail_filename = "pretix_net_mail/STACKCONFthumb.png"
    template_name = "pretix_net_mail/STACKCONF.html"

class OSMCMailRenderer(TemplateBasedMailRenderer):
    verbose_name = "OSMC"
    identifier = "osmc"
    thumbnail_filename = "pretix_net_mail/OSMCthumb.png"
    template_name = "pretix_net_mail/OSMC.html"

class ICINGAMailRenderer(TemplateBasedMailRenderer):
    verbose_name = "Icinga"
    identifier = "icinga"
    thumbnail_filename = "pretix_net_mail/ICINGAthumb.png"
    template_name = "pretix_net_mail/ICINGA.html"

class DOSTMailRenderer(TemplateBasedMailRenderer):
    verbose_name = "DOST"
    identifier = "dost"
    thumbnail_filename = "pretix_net_mail/DOSTthumb.png"
    template_name = "pretix_net_mail/DOST.html"

