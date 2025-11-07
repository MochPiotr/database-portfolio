from django.contrib import admin

from .models import User, Lead, Agent, UserProfile, Category, Deal, Contact

admin.site.register(Category)
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Lead)
admin.site.register(Agent)
admin.site.register(Deal)
admin.site.register(Contact)
