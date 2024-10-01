from django.urls import path

from .views import NewsListView, NewsDeleteView, post_news, like, get_thread, post_comment, update_interactions

app_name = "news"

urlpatterns = [
    path("", view=NewsListView.as_view(), name="list"),
    path("post-news/", view=post_news, name="post_news"),
    path("like/", view=like, name="like_post"),
    path("get-thread/", view=get_thread, name="get_thread"),
    path("post-comment/", view=post_comment, name="post_comment"),
    path("delete/<str:pk>", view=NewsDeleteView.as_view(), name="delete_news"),
    path('update-interactions/', view=update_interactions, name='update_interactions'),
]
