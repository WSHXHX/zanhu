import tempfile
from PIL import Image

from django.test import Client
from django.test import override_settings
from django.urls import reverse
from test_plus.test import TestCase

from zanhu.articles.models import Article
from zanhu.articles.views import (
    ArticlesListView,
    DeaftListView,
    ArticlesCreateView,
    ArticlesDetailView,
    ArticleEditView
)


class TestArticlesCase(TestCase):

    def setUp(self):
        self.test_image = self.get_temp_img()
        self.user = self.make_user()

        self.client = Client()
        self.client.login(username="testuser", password="password")

        self.article_published = Article.objects.create(
            title="第一篇文章",
            user=self.user,
            status="P",
            content="第一篇文章的内容",
        )
        self.article_published.tags.add("test1", "test2", "test3")

        self.article_draft = Article.objects.create(
            title="第二篇文章",
            user=self.user,
            content="第二篇文章的内容",
        )
        self.article_draft.tags.add("test1", "test4", "test5")

    @staticmethod
    def get_temp_img():
        size = (200, 200)
        color = (255, 0, 0, 0)
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            image = Image.new("RGB", size, color)
            image.save(f, "PNG")
        return open(f.name, mode="rb")

    def tearDowm(self):
        self.test_image.close()

    def test_index_articles(self):
        """访问列表页"""
        response = self.get(reverse("articles:list"))
        assert response.status_code == 200
        assert self.article_published in response.context["articles"]
        assert self.article_draft not in response.context["articles"]

    def test_error_404(self):
        """访问不存在的文章"""
        response = self.get(reverse("articles:article", kwargs={"slug": "yi-pian-bu-cun-zai-de-wen-zhang"}))
        assert response.status_code == 404

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_create_article(self):
        response = self.client.post(
            reverse("articles:write_new"),
            {
                "title": "第三篇测试文章",
                "content": "第三篇测试文章的内容",
                "image": self.test_image,
                "status": "P",
                "edited": "False",
                "tags": "test1",
            }
        )
        assert response.status_code == 200

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_draft_article(self):
        response = self.client.post(
            reverse("articles:write_new"),
            {
                "title": "第四篇测试文章",
                "content": "第四篇测试文章的内容",
                "image": self.test_image,
                "status": "D",
                "edited": "False",
                "tags": "test1",
            }
        )
        assert response.status_code == 200
