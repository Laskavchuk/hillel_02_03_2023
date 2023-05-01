from django.urls import path

from favorites.views import FavoriteView, FavoriteAddOrRemoveView

urlpatterns = [
    path('favorites/', FavoriteView.as_view(), name='favorites'),
    path('favorites/<uuid:pk>/', FavoriteAddOrRemoveView.as_view(),
         name='add_or_remove_favorite'
         ),
]
