from django.contrib import admin
from .models import Profile, Team, Membership, MemberRequest


class MembershipInLine(admin.TabularInline):
    model = Membership
    extra = 1


class ProfileAdmin(admin.ModelAdmin):
    inlines = [MembershipInLine,]


class TeamAdmin(admin.ModelAdmin):
    inlines = [MembershipInLine,]
    # exclude = ('members')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Team, TeamAdmin)

admin.site.register(MemberRequest)

