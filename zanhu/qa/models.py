import uuid
from collections import Counter
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.db import models
from slugify import slugify
from taggit.managers import TaggableManager
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


class QuestionQuerySet(models.query.QuerySet):

    def get_answered(self):
        """获取已有被接受的回答的问题"""
        return self.filter(has_answer=True)

    def get_unanswered(self):
        """获取没有被接受的回答的问题"""
        return self.filter(has_answer=False)

    def get_draft(self):
        """获取草稿箱文章"""
        return self.filter(status="D")

    def get_counted_tags(self):
        """统计所有问题中每一个标签的数量"""
        tag_dict = {}
        query = self.all().exclude(status="D").annotate(tagged=models.Count("tags")).filter(tags__gt=0)
        for obj in query:
            for tag in obj.tags.names():
                if tag not in tag_dict:
                    tag_dict[tag] = 1
                else:
                    tag_dict[tag] += 1
        return tag_dict.items()

class Vote(models.Model):

    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name="qa_vote", verbose_name="用户")
    value = models.BooleanField(default=True, verbose_name="赞或者踩")

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="vote_on")
    object_id = models.CharField(max_length=255)
    vote = GenericForeignKey()

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "投票"
        verbose_name_plural = verbose_name
        unique_together = ("user", "content_type", "object_id")
        # SQL优化
        index_together = ("content_type", "object_id")


class Question(models.Model):

    STATUS = (("D", "Draft"), ("O", "Open"), ("C", "Close"))

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name="q_author", verbose_name="提问者")
    title = models.CharField(max_length=255, unique=True, verbose_name="标题")
    slug = models.CharField(max_length=255, verbose_name="（URL）别名")
    status = models.CharField(max_length=1, choices=STATUS, default="O", verbose_name="问题状态")
    content = MarkdownxField(verbose_name="问题的内容")
    tags = TaggableManager(help_text="多个标签使用英文逗号隔开(,)", verbose_name="问题的标签")
    has_answer = models.BooleanField(default=False, verbose_name="是否已经有被接受的答案")
    votes = GenericRelation(Vote, verbose_name="投票")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    objects = QuestionQuerySet.as_manager()

    class Meta:
        verbose_name = "问题"
        verbose_name_plural = verbose_name
        ordering = ("-created_at", )

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_upload=False, using=None, update_fields=None):
        self.slug = slugify(self.title)
        super(Question, self).save()

    def get_markdown(self):
        return markdownify(self.content)

    def total_votes(self):
        dic = Counter(self.votes.values_list("value", flat=True))
        return dic[True] - dic[False]

    def get_answers(self):
        return Answer.objects.filter(question=self)

    def count_answers(self):
        return self.get_answers().count()

    def get_upvoters(self):
        return [vote.user for vote in self.votes.filter(value=True)]

    def get_downvoters(self):
        return [vote.user for vote in self.votes.filter(value=False)]

    def get_accepted_answer(self):
        return Answer.objects.get(question=self, is_answer=True)

class Answer(models.Model):

    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name="a_author", verbose_name="回答者")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="回答对应的问题")
    content = MarkdownxField(verbose_name="回答的内容")
    is_answer = models.BooleanField(default=False, verbose_name="答案是否被接受")
    votes = GenericRelation(Vote, verbose_name="投票")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "回答"
        verbose_name_plural = verbose_name
        ordering = ("-is_answer", "-created_at", )

    def __str__(self):
        return self.content

    def get_markdown(self):
        return markdownify(self.content)

    def total_votes(self):
        dic = Counter(self.votes.values_list("value", flat=True))
        return dic[True] - dic[False]

    def get_downvoters(self):
        return [vote.user for vote in self.votes.filter(value=False)]

    def get_upvoters(self):
        return [vote.user for vote in self.votes.filter(value=True)]

    def get_accepted_answer(self):
        return Answer.objects.get(question=self, is_answer=True)

    def accept_answer(self):
        answer_set = Answer.objects.filter(question=self.question)
        answer_set.update(is_answer=False)

        self.is_answer = True
        self.save()

        self.question.has_answer = True
        self.question.save()
