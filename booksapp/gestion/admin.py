from django.contrib import admin
from .models import Book, Author, Genre, Language, BookInstance, Member, Review

#admin.site.register(Book)
#admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Language)
#admin.site.register(BookInstance)

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name','first_name',)

class MemberAdmin(admin.ModelAdmin):
    list_display = ('last_name','first_name','phone_num','memberID',)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')

class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book','main_class','status','borrower','due_back','loan_date',)
    list_filter = ('status','main_class','due_back')

    fieldsets = (
        (None, {
            'fields': ('book','imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id','book','pub_date','user_name','comment','rating',)

admin.site.register(Author,AuthorAdmin)
admin.site.register(Book,BookAdmin)
admin.site.register(BookInstance,BookInstanceAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Review,ReviewAdmin)