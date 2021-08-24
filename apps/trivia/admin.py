from django.contrib import admin
from .models import Category, Level, Option, Question


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )
    list_display_links = ('id', 'name',)


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )
    list_display_links = ('id', 'name', )
    verbose_name_plural = 'levels'


class OptionInline(admin.StackedInline):
    model = Option
    can_delete = False
    verbose_name_plural = 'options'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'description', 'category', 'level',)
    list_display_links = ('content',)
    readonly_fields = ('created', 'modified',)
    inlines = (OptionInline, )
