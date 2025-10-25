from django.contrib import admin

from apps.edu.models import (AboutCompany, Blog, BlogCategory, Course,
                             CourseCategory, Instructor, Lecture, CompanySocialLink,
                             LectureContent, Section)


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
class AboutCompanyModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'email')
    inlines = SocialLinkInline,

    def has_add_permission(self, request):
        if AboutCompany.objects.count():
            return False
        return super().has_add_permission(request)


@admin.register(Blog)
class BlogModelAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(BlogCategory)
class BlogCategoryModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Instructor)
class InstructorModelAdmin(admin.ModelAdmin):
    pass


# def get_app_list(self, request, app_label=None):
#     """
#     Переопределяем метод для кастомной сортировки моделей
#     """
#     app_dict = self._build_app_dict(request, app_label)
#
#     model_order = [
#         'CourseCategory',
#         'Course',
#         'Lesson',
#         'Section',
#         'AboutCompany',
#         'BlogCategory',
#         'Blog'
#     ]
#
#     for app in app_dict.values():
#         app['models'].sort(
#             key=lambda x: (
#                 model_order.index(x['object_name'])
#                 if x['object_name'] in model_order
#                 else len(model_order)
#             )
#         )
#
#     return app_dict.values()


def get_app_list(self, request, app_label=None):
    """
    Return a sorted list of all the installed apps that have been
    registered in this site.
    """
    app_dict = self._build_app_dict(request, app_label)

    # Sort the apps alphabetically.
    app_list = sorted(app_dict.values(), key=lambda x: x["name"].lower())

    # Sort the models alphabetically within each app.
    for app in app_list:
        app["models"].sort(key=lambda x: x["name"])

    return app_list


admin.AdminSite.get_app_list = get_app_list
