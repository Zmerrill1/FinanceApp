from django.conf import settings
from django.contrib import admin
from django.urls import include, path

if settings.DEBUG:
    import debug_toolbar

urlpatterns = [
    path("", include("budget.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
