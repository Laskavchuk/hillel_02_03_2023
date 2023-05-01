from django.urls import path

from favorites.views import FavoriteView, FavoriteAddOrRemoveView

urlpatterns = [
    path('', FavoriteView.as_view(), name='favorites'),
    path('<uuid:pk>', FavoriteAddOrRemoveView.as_view(),
         name='add_or_remove_favorite'
         ),
]
