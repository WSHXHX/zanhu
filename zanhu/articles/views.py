from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django_comments.signals import comment_was_posted

from zanhu.articles.models import Article
from zanhu.articles.forms import ArticleForms
from zanhu.helpers import AuthorRequireMixin
from zanhu.notifications.views import notification_handler


class ArticlesListView(LoginRequiredMixin, ListView):
    model = Article
    paginate = 10
    context_object_name = "articles"
    template_name = "articles/article_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["popular_tags"] = Article.objects.counted_tags()
        return context

    def get_queryset(self):
        return Article.objects.get_published()


class DeaftListView(ArticlesListView):

    def get_queryset(self):
        return Article.objects.filter(user=self.request.user).get_drafts()


class ArticlesCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForms
    template_name = "articles/article_create.html"
    message = "文章创建成功！！！"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ArticlesCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse_lazy("articles:list")

class ArticlesDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = "articles/article_detail.html"


class ArticleEditView(LoginRequiredMixin, AuthorRequireMixin, UpdateView):
    model = Article
    form_class = ArticleForms
    template_name = "articles/article_update.html"
    message = "文章编辑成功！！！"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ArticleEditView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse_lazy("articles:article", kwargs={"slug": self.get_object().slug})

def notify_comment(**kwargs):
    """文章有评论时通知作者"""
    actor = kwargs['request'].user
    receiver = kwargs['comment'].content_object.user
    obj = kwargs['comment'].content_object
    notification_handler(actor, receiver, 'C', obj)


comment_was_posted.connect(receiver=notify_comment)  # 使用django_comments的信号机制

