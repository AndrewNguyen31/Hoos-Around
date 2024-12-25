"""
Core website URLs
"""
from django.urls import path

from .views import *

app_name = "core"
urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("onboarding", onboarding, name="onboarding"),
    path("checked_off/<int:pk>",checked_off,name = "checked_off"),
    path("revoke", revoke, name="revoke"),
    path("social/signup/", signup_redirect, name="signup_redirect"),
    path("account", AccountView.as_view(), name="account"),
    path("map", map_view, name="map"),
    path("leaderboard/", combined_leaderboard, name="combined_leaderboard"),

    path("place/create", create_place, name="create_place"),
    path("place/<int:pk>", PlaceView.as_view(), name="place"),
    path("qr/<int:pk>", qr, name="qr"),
    path("complete/<int:pk>", complete, name="complete"),
    path("place/<int:pk>/print", PrintPlace.as_view(), name="print"),
    path("shareTask/<int:pk>", shareTask,name = "shareTask"),
    path("refreshTasks", refresh_tasks, name="refreshTasks"),

    path("approvals", ApprovalQueue.as_view(), name="approvals"),
    path("approve/<int:pk>", Approve.as_view(), name="approve"),
]