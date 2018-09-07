from django.contrib import admin
from nightstand_dashboard.models import Book, Chapter, Reader, ChapterComment


admin.site.register(Book)
admin.site.register(Chapter)
admin.site.register(Reader)
admin.site.register(ChapterComment)

