"""Defines URL patterns for web_journals"""

from django.urls import path

from . import views

app_name = "web_journals"

urlpatterns = [
    # Home page
    path("", views.index, name="index"),
    # personal home page
    path("home/", views.home, name="home"),
    # Topics page
    path("topics/", views.topics, name="topics"),
    # Detailed page for single topic
    path("topics/<int:topic_id>/", views.topic, name="topic"),
    # Add a new topic
    path("new_topic/", views.new_topic, name="new_topic"),
    # Page to add a new entry for an associated topic
    path("new_entry/<int:topic_id>/", views.new_entry, name="new_entry"),
    # Page to edit current entries
    path("edit_entry/<int:entry_id>/", views.edit_entry, name="edit_entry"),

    path("delete_entry/<int:entry_id>", views.delete_entry, name="delete_entry"),

    path("delete_topic/<int:topic_id>", views.delete_topic, name="delete_topic"),

    path("edit_topic/<int:topic_id>/", views.edit_topic, name="edit_topic"),

]
