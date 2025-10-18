from django.contrib import admin

from main.models import CourseCategory, Course, AboutCompany, Blog, BlogCategory, LectureContent, Lecture
from main.models.contacts import CompanySocialLink


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


# class ModuleInline(admin.StackedInline):
#     model = Module


class LectureContentInline(admin.TabularInline):
    model = LectureContent


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    inlines = (LectureContentInline,)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'overview')
    # inlines = (LectureContentInline,)


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
