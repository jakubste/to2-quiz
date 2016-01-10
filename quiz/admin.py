from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe


class MyUserAdmin(UserAdmin):
    def is_egzaminer(self, user):
        if user.is_staff and user.groups.filter(name='Egzaminatorzy').exists():
            return True
        return False

    is_egzaminer.boolean = True
    is_egzaminer.short_description = 'Egzaminer'

    def mark_egzaminer(self, user):
        return mark_safe(
            '<a href="' +
            reverse('accounts:mark_as_egzaminer', args=(user.pk,)) +
            '"><button type="button">Egzaminer</button></a>'
        )

    mark_egzaminer.short_description = 'Mark as egzaminer'

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_egzaminer',
        'mark_egzaminer',
        'is_superuser'
    )


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
