from django.urls import path, include
from . import views

urlpatterns = [
    path("",views.index, name="home"),
    path("about/",views.about, name="about"),
    path("contact/",views.contact, name="contact"), 
    path("search/",views.search, name="search"),
    path("signup",views.handleSignup, name="handleSignup"),
    path("login",views.handleLogin, name="handleLogin"),
    path("logout",views.handleLogout, name="handleLogout"),
    path("products/<int:myid>",views.productView, name="productview"),
    path("checkout/",views.checkout, name="checkout"),
    path("handlerequest/",views.handlerequest, name="HandleRequest"),
    path("tracker/",views.tracker, name="tracker"),
    path("products/<int:myid>",views.productView, name="productview"),
    path("cart/",views.cart, name="cart"),
    path("update_item/",views.updateItem, name="update_item"),







    path('men/', views.men, name="men"),
    path('women/', views.women, name="women"),
    path('footwear/', views.footwear, name="footwear"),
    path('furniture/', views.furniture, name="furniture"),
    path('homeDecor/', views.homeDecor, name="homeDecor"),
    path('accessories/', views.accessories, name="accessories"),
] 
