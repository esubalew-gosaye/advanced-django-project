from acl.views import *
from django.urls import path

app_name = "acl"
urlpatterns = [
    path("", home_page, name="home"),
    path("login/", login, name="login"),
    path("list_content/", content_listing_page, name="content-listing"),
    path("create_user/", user_creation_page, name="user-creation"),
    path("create_group/", group_creation_page, name="group-creation"),

    path("logout/", logout, name="user-logout")
]
