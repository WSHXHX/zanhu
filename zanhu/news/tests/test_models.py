from test_plus.test import TestCase
from zanhu.news.models import News

class TestNewsModelCase(TestCase):

    def setUp(self):
        self.user = self.make_user("user01")
        self.other_user = self.make_user("user02")
        self.first_news = News.objects.create(
            user=self.user,
            content="第一条动态"
        )
        self.second_news = News.objects.create(
            user=self.user,
            content="第二条动态"
        )
        self.third_news = News.objects.create(
            user=self.other_user,
            content="第一条评论",
            parent = self.first_news,
            reply = True
        )

    def test_switch_like(self):
        start_likers = self.first_news.count_likers()
        start_likers_list = self.first_news.get_likers()
        if self.user in start_likers_list:
            self.first_news.switch_like(self.user)
            assert self.first_news.count_likers() == (start_likers - 1)
            assert self.user not in self.first_news.get_likers()
            self.first_news.switch_like(self.user)
            assert self.first_news.count_likers() == start_likers
            assert self.user in self.first_news.get_likers()
        else:
            self.first_news.switch_like(self.user)
            assert self.first_news.count_likers() == (start_likers + 1)
            assert self.user in self.first_news.get_likers()
            self.first_news.switch_like(self.user)
            assert self.first_news.count_likers() == start_likers
            assert self.user not in self.first_news.get_likers()

    def test_reply_this(self):
        parent = self.third_news.get_parent()
        start_thread = self.first_news.comment_count()
        assert parent is self.first_news
        self.first_news.reply_this(self.other_user, "第二条评论")
        assert self.first_news.comment_count() == (start_thread + 1)
        assert self.third_news in self.first_news.get_thread()

    def test__str__(self):
        self.assertEqual(self.first_news.__str__(), "第一条动态")
