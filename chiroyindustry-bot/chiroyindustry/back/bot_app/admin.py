from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name',  'phone_number', 'lang_id', 'chat_id')
    # list_display_links = ('first_name')

admin.site.register(User, UserAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id',  'status', 'user_id', 'created_at','order_id','amount')

admin.site.register(Order, OrderAdmin)


