from django.contrib import admin

# Register your models here.
from .models import DanePomiarowe, Stacja, Jednostka, RodzajPomiaru

admin.site.register(DanePomiarowe)
admin.site.register(Stacja)
admin.site.register(Jednostka)
admin.site.register(RodzajPomiaru)