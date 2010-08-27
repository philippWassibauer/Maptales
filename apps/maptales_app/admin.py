from models import TourCities
from django.contrib.gis import admin

admin.site.register(TourCities, admin.GeoModelAdmin)