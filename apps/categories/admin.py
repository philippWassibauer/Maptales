from django.contrib import admin
from categories.models import Category, CategorizedItem

from categories.forms import CategoryModelForm

class CategoryAdmin(admin.ModelAdmin):
    form = CategoryModelForm
    search_fields = ['name']
    prepopulated_fields = {'slug' : ['name']}

admin.site.register(CategorizedItem)
admin.site.register(Category, CategoryAdmin)

