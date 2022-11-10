from django.urls import path, re_path
from .views import (
    ItemDeleteView,
    itemCreateView,
    itemUpdateView,
    ItemDetailView,
    ItemListView,
    upvote,
    comment,
    ItemBuyView,
    flag
)

app_name = "item_management"
urlpatterns = [
    path('', ItemListView.as_view(), name='item-list'),
    re_path(r'^(?P<search>\w+)$', ItemListView.as_view(), name='item-list'),
    path('<int:id>/', ItemDetailView.as_view(), name='item-detail'),
    path('create/', itemCreateView, name='item-create'),
    path('<int:id>/update/', itemUpdateView, name='item-update'),
    path('<int:id>/delete/', ItemDeleteView.as_view(), name='item-delete'),
    path('<int:id>/upvote/', upvote, name='upvote'),
    path('<int:id>/comment/', comment, name='comment'),
    path('<int:id>/buy/', ItemBuyView.as_view(), name='buy'),
    path('<int:id>/flag/', flag, name='flag')
]
