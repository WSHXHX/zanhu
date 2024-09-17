from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.views.generic import RedirectView

from zanhu.users.models import User


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "users/user_detail.html"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user.username)
        context["moments_num"] = user.publisher.filter(reply=False).count()  # 'publisher'为News表中的related_name
        context["article_num"] = user.author.filter(status='P').count()  # 只算已发表的文章
        context["comment_num"] = user.publisher.filter(reply=True).count() + user.comment_comments.all().count()  # 文章+动态的评论数
        context["question_num"] = user.q_author.all().count()
        context["answer_num"] = user.a_author.all().count()

        # 互动数 = 动态点赞数 + 问答点赞数 + 评论数 + 私信用户数(都有发送或接收到私信)
        tmp = set()
        # 我发送私信给了多少不同的用户
        sent_num = user.sent_messages.all()
        for i in sent_num:
            tmp.add(i.recipient.username)
        # 我接收的所有私信来自多少不同的用户
        received_num = user.received_messages.all()
        for r in received_num:
            tmp.add(r.sender.username)

        context["interaction_num"] = user.liked_news.all().count() + user.qa_vote.all().count() + context["comment_num"] + len(tmp)
        return context


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["nickname", "job_title", "introduction", "picture", "location", "personal_url", "weibo", "zhihu", "github", "linkedin"]
    template_name = "users/user_form.html"
    success_message = _("Information successfully updated")

    def get_success_url(self) -> str:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user.get_absolute_url()

    def get_object(self, queryset: QuerySet | None=None) -> User:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user

class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})
