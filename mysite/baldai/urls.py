from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .views import CommentUpdateView, login_test_user

urlpatterns = [
    path("", views.index, name="index"),
    path('login_test_user/', login_test_user, name='login_test_user'),
    path('baldai/', views.baldai, name="baldai"),
    path("baldai/<int:baldas_id>", views.baldas, name="baldas"),
    path('products/', views.products, name="products"),
    path("products/<int:product_id>", views.product, name="product"),
    path("orders/", views.OrderListView.as_view(), name="orders"),
    path("orders/<int:pk>", views.OrderDetailView.as_view(), name="order"),
    path('search/', views.search, name="search"),
    path('my_orders/', views.MyOrderListView.as_view(), name="my_orders"),
    path('register/', views.register, name='register'),
    path("profile/", views.profile, name="profile"),
    path('accounts/logout/', include('allauth.urls')),
    path("order/new", views.OrderCreateView.as_view(), name="order_new"),
    path("order/<int:pk>/update", views.OrderUpdateView.as_view(), name="order_update"),
    path("order/<int:pk>/delete", views.OrderDeleteView.as_view(), name="order_delete"),
    path("order/<int:order_pk>/newline", views.OrderLineCreateView.as_view(), name="orderline_new"),
    path("order/<int:order_pk>/line/<int:pk>/update", views.OrderLineUpdateView.as_view(), name="orderline_update"),
    path("order/<int:order_pk>/line/<int:pk>/delete", views.OrderLineDeleteView.as_view(), name="orderline_delete"),
    path('order/<int:order_pk>/ordercomment/<int:pk>/update', CommentUpdateView.as_view(), name='ordercomment_update'),
    path('order/<int:order_pk>/comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
]
