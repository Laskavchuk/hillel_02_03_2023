from django.urls import path

from favorites.views import FavoriteView, FavoriteAddOrRemoveView, \
    AJAXAddOrRemoveFavorite

urlpatterns = [
    path('', FavoriteView.as_view(), name='favorites'),
    path('<uuid:pk>', FavoriteAddOrRemoveView.as_view(),
         name='add_or_remove_favorite'
         ),
    path('ajax/<uuid:pk>/', AJAXAddOrRemoveFavorite.as_view(),
         name='ajax_add_or_remove_favorite'
         ),
]
