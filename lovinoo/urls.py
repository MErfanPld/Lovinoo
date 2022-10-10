from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("config.urls", namespace="config")),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("profiles/", include("profiles.urls", namespace="profiles")),
    path("chat/", include("chat.urls", namespace="chat")),
    path("activity/", include("activity.urls", namespace="activity")),
    path("financial/", include("financial.urls", namespace="financial")),
]
if settings.DEBUG:
    # ADD ROOT MEDIA FILES
    urlpatterns = urlpatterns + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns = urlpatterns + static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )

    
