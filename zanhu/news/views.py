from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DeleteView
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.urls import reverse_lazy

from zanhu.news.models import News
from zanhu.helpers import AuthorRequireMixin, ajax_required


class NewsListView(LoginRequiredMixin, ListView):
    model = News
    paginate_by = 20
    template_name = "news/news_list.html"

    def get_queryset(self):
        return News.objects.filter(reply=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["views"] = 100
        return context


class NewsDeleteView(LoginRequiredMixin, AuthorRequireMixin, DeleteView):
    model = News
    template_name = "news/news_confirm_delete.html"
    success_url = reverse_lazy("news:list")


@login_required
@ajax_required
@require_http_methods(["POST"])
def post_news(request):
    post = request.POST["post"].strip()
    if post:
        posted = News.objects.create(user=request.user, content=post)
        html = render_to_string("news/news_single.html", {"news": posted, "request":request})
        return HttpResponse(html)
    else:
        return HttpResponseBadRequest("内容不能为空")


@login_required
@ajax_required
@require_http_methods(["POST"])
def like(request):
    news_id = request.POST["news"]
    news = News.objects.get(pk=news_id)
    news.switch_like(request.user)
    return JsonResponse({"likes": news.count_likers()})


@login_required
@ajax_required
@require_http_methods(["GET"])
def get_thread(request):
    news_id = request.GET["news"]
    news = News.objects.get(pk=news_id)
    news_html = render_to_string("news/news_single.html", {"news": news, "request": request})
    thread_html = render_to_string("news/news_thread.html", {"thread": news.get_thread(), "request": request})
    return JsonResponse({
        "uuid": news_id,
        "news": news_html,
        "thread": thread_html,
    })


@login_required
@ajax_required
@require_http_methods(["POST"])
def post_comment(request):
    post = request.POST["reply"].strip()
    parent_id = request.POST["parent"]
    parent = News.objects.get(pk=parent_id)
    if post:
        parent.reply_this(request.user, post)
        return JsonResponse({"comments": parent.comment_count(), "newsId": parent.get_parent().uuid_id})
    else:
        return HttpResponseBadRequest("评论不能为空")
