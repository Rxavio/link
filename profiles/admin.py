from django.contrib import admin
from .models import Profile, Relationship, Table, Booking, Video, Contact
from django.contrib.auth.models import Group
# Register your models here.

# admin header and title modification
admin.site.site_header = "Admin DashBoard"
admin.site.site_title = "Remarkable"
admin.site.index_title = 'Remarkable'

class ProfileAdmin(admin.ModelAdmin):
    list_display=('user','first_name','last_name','slug','address','created','updated','nationalid','telephone','age')
    list_display_links = ('user', 'slug')
    list_filter = ('user',) 
    date_hierarchy = 'created'  
    search_fields=('age','first_name','last_name','address','slug',)
    

admin.site.register(Profile, ProfileAdmin)    


class RelationShipAdmin(admin.ModelAdmin):
    list_display=('sender','receiver','status','created','updated')
    list_display_links = ('sender', 'receiver','status',)
    list_filter = ('status',) 
    date_hierarchy = 'created'  
    search_fields=('status',)
    
    
admin.site.register(Relationship, RelationShipAdmin) 


class BookingAdmin(admin.ModelAdmin):
    list_display=('user','table','check_in','check_out')
    list_display_links = ('user','table','check_in','check_out', )
    list_filter = ('check_in',) 
    date_hierarchy = 'check_in'  
    # search_fields=('user',)
    
admin.site.register(Booking, BookingAdmin)


admin.site.register(Table)


class VideoAdmin(admin.ModelAdmin):
    list_display=('caption','video')
    list_display_links = ('caption','video', )
    list_filter = ('caption',) 
   
    
admin.site.register(Video, VideoAdmin)   




class ContactAdmin(admin.ModelAdmin):
    list_display=('subject','message','author','date_posted')
    list_filter = ('subject',) 
   
    
admin.site.register(Contact, ContactAdmin)    


