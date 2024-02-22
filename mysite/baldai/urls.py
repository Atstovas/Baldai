from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('vehicles/', views.vehicles, name="vehicles"),
    path("vehicles/<int:vehicle_id>", views.vehicle, name="vehicle"),
    path("orders/", views.OrderListView.as_view(), name="orders"),
    path("orders/<int:pk>", views.OrderDetailView.as_view(), name="order"),
    path('search/', views.search, name="search"),
    path('my_orders/', views.MyOrderListView.as_view(), name="my_orders"),
    path('register/', views.register, name='register'),
    path("profile/", views.profile, name="profile"),
    path("order/new", views.OrderCreateView.as_view(), name="order_new"),
    path("order/<int:pk>/update", views.OrderUpdateView.as_view(), name="order_update"),
    path("order/<int:pk>/delete", views.OrderDeleteView.as_view(), name="order_delete"),
    path("order/<int:order_pk>/newline", views.OrderLineCreateView.as_view(), name="orderline_new"),
    path("order/<int:order_pk>/line/<int:pk>/update", views.OrderLineUpdateView.as_view(), name="orderline_update"),
    path("order/<int:order_pk>/line/<int:pk>/delete", views.OrderLineDeleteView.as_view(), name="orderline_delete"),
]