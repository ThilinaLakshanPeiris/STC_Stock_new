from django.contrib import admin

from stc.models import depot, document, master_data, movement, region, region_auth, user_details, user_level

# Register your models here.

# admin.site.register(users)
admin.site.register(user_level)
admin.site.register(region)
admin.site.register(depot)
admin.site.register(region_auth)
admin.site.register(user_details)
admin.site.register(document)
admin.site.register(master_data)
admin.site.register(movement)