from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models import Count
from opengraphio import OpenGraphIO
from django.conf import settings

class Claim(models.Model):
    claim_key = models.CharField(max_length=32, unique=True)
    email_address = models.CharField(max_length=200)
    email_sent = models.BooleanField(default=False)

    def __str__(self):
        return "%s (%s)" % (self.email_address, self.claim_key)

class Item(models.Model):
    class ItemType(models.IntegerChoices):
        SINGLE = (1, "Single")
        MULTI = (2, "Multiple")

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    link = models.CharField(max_length=1000, blank=True)
    price = models.CharField(max_length=20, blank=True)
    item_type = models.SmallIntegerField(choices=ItemType.choices, default=ItemType.SINGLE)
    want_count = models.IntegerField(default=1)
    claims = models.ManyToManyField(Claim, symmetrical=False, blank=True)
    og_meta = models.BooleanField(default=False)
    og_title = models.CharField(max_length=500, blank=True)
    og_description = models.TextField(blank=True)
    og_image = models.CharField(max_length=500, blank=True)

    def __str__(self):
        #claim_count = Count("claims")
        #claim_count = 1
        return "%s" % self.name

@receiver(pre_save, sender=Item)
def opengraph_meta(sender, instance, *args, **kwargs):
    if instance.link == "":
        return

    opengraph = OpenGraphIO({ 'app_id': settings.OPENGRAPH_KEY })
    if "amazon" in instance.link:
        opengraph = OpenGraphIO({ 'app_id': settings.OPENGRAPH_KEY, 'use_proxy': 'true', 'cache_ok': 'false' })

    og_data = opengraph.get_site_info(instance.link)

    if og_data and (og_data.get("error", False) == False):
        instance.og_meta = True
        instance.og_title = og_data['hybridGraph']['title']
        instance.og_description = og_data['hybridGraph']['description']
        instance.og_image = og_data['hybridGraph']['image']