from django.contrib import admin
from .models import Genre, Language, Author, Book, BookInstance

# Register your models here.


class BookInline(admin.StackedInline):
    model = Book
    extra = 1


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('display_full_name', 'date_of_birth', 'date_of_death')
    inlines = [BookInline]


class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 1


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None,
         {'fields': ('book', 'imprint', 'id')}
         ),
        ('Available',
         {'fields': ('status', 'due_back', 'borrower')}
         ),

    )


admin.site.register(Genre)
admin.site.register(Language)
