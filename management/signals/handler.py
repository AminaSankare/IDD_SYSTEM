from management.models import Citizen, CitizenAddress, CitizenParent
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


@receiver(post_save, sender=Citizen)
def create_citizen(sender, **kwargs):
    if kwargs['created']:
        citizen = kwargs['instance']
        CitizenAddress.objects.create(
            citizen=citizen, province="", state="", city="", street="")
        CitizenParent.objects.create(
            citizen=citizen, parent="Father", first_name="", last_name="", professionalism="")
        CitizenParent.objects.create(
            citizen=citizen, parent="Mother", first_name="", last_name="", professionalism="")
