from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import Book, CustomUser

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')

    list_filter = ('author', 'publication_year')

    search_fields = ('title', 'author')

# Register your models here.
admin.site.register(Book, BookAdmin)

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    
    fieldsets = UserAdmin.fieldsets + (
        (None, {
            "fields": (
                'profile_photo', 'date_of_birth'
            ),
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('profile_photo', 'date_of_birth'
            ),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
