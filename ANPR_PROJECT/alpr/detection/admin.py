from django.contrib import admin
from .models import Images,Contact
# Register your models here.
@admin.register(Images)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id','photo','date']


admin.site.register(Contact)
