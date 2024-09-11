from test_plus.test import TestCase
from zanhu.articles.models import Article

class TestArticlesModelCase(TestCase):
    
    def setUp(self):
        self.user = self.make_user()
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
    
    def test__str__(self):
        self.assertEqual(self.article_published.__str__(), "第一篇文章")

    def test_object_instance(self):
        """判断实例对象是否为Article模型类"""
        assert isinstance(self.article_published, Article)
        assert isinstance(self.article_draft, Article)
        assert len(Article.objects.get_published()) == 1
        self.assertEqual(Article.objects.get_published().get(), self.article_published)

    def test_return_values(self):
        """测试返回类"""
        tags_dict = dict(Article.objects.counted_tags())
        assert "test1" in tags_dict
        assert tags_dict["test1"] == 1
        assert "test4" not in tags_dict
        assert len(Article.objects.get_drafts()) == 1
        self.assertEqual(Article.objects.get_drafts().get(), self.article_draft)

