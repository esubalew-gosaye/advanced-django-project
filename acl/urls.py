from acl.views import *
from django.urls import path

app_name = "acl"
urlpatterns = [
    path("", home_page, name="home"),
    path("login/", login, name="login"),
    path("list_content/", content_listing_page, name="content-listing"),

    path("create_user/", user_creation_page, name="user-creation"),
    path("user_detail/<str:pk>/", user_detail_page, name="user-details"),
    path("user_update/<str:pk>/", user_update_page, name="user-updating"),

    path("create_group/", group_creation_page, name="group-creation"),
    path("group_detail/<str:pk>/", group_detail_page, name="group-details"),
    path("group_update/<str:pk>/", group_update_page, name="group-updating"),

    path("logout/", logout, name="user-logout")
]
