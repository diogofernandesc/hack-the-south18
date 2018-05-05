#TODO
#Django is not importable in this environment :(
#Mailbox system
##Mail model:
###(id)
###Voter ID
###To (true) or From (false) Voter
###Date/time
###Text
###Parent ID
from django.contrib import admin

from .models import Poll, Vote

class PollAdmin(admin.ModelAdmin):
    list_display=['id', 'title', 'question']
    list_filter=['approved']

admin.site.register(Poll, PollAdmin)