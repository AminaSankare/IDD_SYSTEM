from django.contrib import admin
from . models import *

# register models
admin.site.register(Citizen)
admin.site.register(CitizenAddress)
admin.site.register(CitizenDocument)
admin.site.register(CitizenParent)
admin.site.register(DocumentApplication)
admin.site.register(Service)
