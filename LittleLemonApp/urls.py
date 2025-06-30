from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path("menu/", views.MenuView.as_view()),
    path("menu/<int:pk>/", views.SingleMenuView.as_view()),
    path("category/", views.CategoryView.as_view()),
    path("category/<int:pk>/", views.SingleCategoryView.as_view()),
    path("booking/", views.BookingView.as_view()),
    path("booking/<int:pk>/", views.SingleBookingView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
