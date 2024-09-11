from django.urls import path

from zanhu.articles import views


app_name = "articles"

urlpatterns = [
    path("", view=views.ArticlesListView.as_view(), name="list"),
    path("drafts/", view=views.DeaftListView.as_view(), name="drafts"),
    path("write-new-article/", view=views.ArticlesCreateView.as_view(), name="write_new"),
    path("<slug:slug>/", view=views.ArticlesDetailView.as_view(), name="article"),
    path("edit/<int:pk>/", view=views.ArticleEditView.as_view(), name="edit_article"),
]
