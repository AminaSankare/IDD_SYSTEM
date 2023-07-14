from django.contrib import admin
from . models import *

# register models
admin.sites.register(Citizen)
admin.sites.register(CitizenAddress)
admin.sites.register(CitizenDocument)
admin.sites.register(CitizenParents)
admin.sites.register(DocumentApplication)
