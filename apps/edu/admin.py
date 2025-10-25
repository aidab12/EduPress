from django.contrib import admin
from django.db.models.expressions import DatabaseDefault

from edu.models import (AboutCompany, Blog, BlogCategory, Course,
                             CourseCategory, Instructor, Lecture,
                             LectureContent, Section)
from edu.models.contacts import CompanySocialLink


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'overview')


class LectureContentInline(admin.StackedInline):
    model = LectureContent
    extra = 1


class LectureInline(admin.StackedInline):
    model = Lecture
    extra = 1

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    inlines = [LectureInline, LectureContentInline]


# _________________End________________

class SocialLinkInline(admin.TabularInline):
    model = CompanySocialLink
    extra = 1


@admin.register(AboutCompany)
class AboutCompanyAdmin(admin.ModelAdmin):
    list_display = ('title', 'email')
    inlines = SocialLinkInline,


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Instructor)
class InstuctorAdmin(admin.ModelAdmin):
    pass
