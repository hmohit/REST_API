import json
from django.test import TestCase
from django.test.client import RequestFactory
from django.forms.models import model_to_dict
from feeder.models import UserInfo
from feeder.models import Feed
from feeder.models import Article
from feeder.views import subscribe_user_to_feed
from feeder.views import unsubscribe_user_from_feed
from feeder.views import add_article_to_feed
from feeder.views import get_user_feeds
from feeder.views import get_user_articles


# Create your tests here.


class SimpleTest(TestCase):
    """docstring for ClassName"""

    def setUp(self):
        UserInfo.objects.create(username='Mohit')

    def testCase1(self):
        self.assertEqual(UserInfo.objects.filter(username='Mohit').exists(),
                         True)


class SubscribeUserTest(TestCase):
    def setUp(self):
        self.user = UserInfo(username='Mohit')
        self.user.save()
        self.feed = Feed(feedname='Yoga')
        self.feed.save()
        self.factory = RequestFactory()

    def test_add_user(self):
        """
        Tests subscribing a user to a feed
        """
        request = self.factory.get(
            '/feeder/subscribe_user_to_feed/?username=Mohit&feedname=Yoga')
        response = subscribe_user_to_feed(request)
        self.assertEqual(response.content, 'Success!')

        request = self.factory.get('/feeder/get_user_feeds/?username=Mohit')
        response = get_user_feeds(request)
        self.assertEqual(response.content, 'Yoga')

    def test_subscibe_multiple(self):
        """
        Tests when use subscribes multiple times to same feed
        """
        request = self.factory.get(
            '/feeder/subscribe_user_to_feed/?username=Mohit&feedname=Yoga')
        response = subscribe_user_to_feed(request)
        response = subscribe_user_to_feed(request)
        request = self.factory.get('/feeder/get_user_feeds/?username=Mohit')
        response = get_user_feeds(request)
        self.assertEqual(response.content, 'Yoga')

    def test_no_feedname(self):
        """
        Tests if feedname doesn't exist
        """
        request = self.factory.get(
            '/feeder/subscribe_user_to_feed/?username=Mohit')
        response = subscribe_user_to_feed(request)
        self.assertEqual(response.content, 'No feedname entered')

    def test_no_username(self):
        """
        test when username doesnt exist
        """
        request = self.factory.get(
            '/feeder/subscribe_user_to_feed/?username=Mona&feedname=b')
        response = subscribe_user_to_feed(request)
        self.assertEqual(response.content, 'Invalid username')


class UnSubscribeUserTest(TestCase):
    def setUp(self):
        self.u1 = user1 = UserInfo(username='Mohit')
        user1.save()
        self.u2 = user2 = UserInfo(username='Foo')
        user2.save()
        self.f1 = feed1 = Feed(feedname='Yoga')
        feed1.save()
        self.f2 = feed2 = Feed(feedname='Climbing')
        feed2.save()
        user1.feeds.add(feed1)
        user1.feeds.add(feed2)
        user2.feeds.add(feed2)
        self.factory = RequestFactory()

    def test_unsubscribe(self):
        """
        Test basic unsubscription
        """
        request = self.factory.get(
            '/feeder/unsubscribe_user_from_feed/?username=Mohit&feedname'
            '=Climbing')
        response = unsubscribe_user_from_feed(request)
        self.assertEqual(response.content, 'Success!')

        request = self.factory.get('/feeder/get_user_feeds/?username=Mohit')
        response = get_user_feeds(request)
        self.assertEqual(response.content, 'Yoga')

        request = self.factory.get('/feeder/get_user_feeds/?username=Foo')
        response = get_user_feeds(request)
        self.assertEqual(response.content, 'Climbing')

    def test_no_username(self):
        """
        test when username doesnt exist
        """
        request = self.factory.get(
            '/feeder/unsubscribe_user_to_feed/?username=Mona&feedname=b')
        response = subscribe_user_to_feed(request)
        self.assertEqual(response.content, 'Invalid username')


class ArticleTest(TestCase):
    def setUp(self):
        self.unames = ['Mohit', 'Foo', 'Bar']
        self.fnames = ['Yoga', 'Climbing', 'Coding']
        self.user = []
        self.feed = []
        self.factory = RequestFactory()
        for uname in self.unames:
            user = UserInfo(username=uname)
            user.save()
            self.user.append(user)

        for i, fname in enumerate(self.fnames):
            feed = Feed(feedname=fname)
            feed.save()
            self.feed.append(feed)
            self.user[i].feeds.add(feed)

        a1 = Article(article_id=1, title='the one', url='www.one.com',
                     publisher='My Publication1')
        a1.save()
        a2 = Article(article_id=2, title='the two', url='www.two.com',
                     publisher='My Publication2')
        a2.save()
        self.feed_map = (a1, a2)

    def test_add_article(self):
        """
        Test add article to feed
        """
        feed_map = self.feed_map
        for i, a in enumerate(feed_map):
            request = self.factory.get(
                '/feeder/add_article_to_feed/?article_id='
                + str(a.article_id) + '&feedname=' + self.fnames[i])
            response = add_article_to_feed(request)
            self.assertEqual(response.content, 'Success!')

            request = self.factory.get(
                '/feeder/get_user_articles/?username=' + self.unames[i])
            response = get_user_articles(request)
            d = {str(a.article_id): model_to_dict(a)}
            self.assertEqual(json.loads(response.content),
                             {str(a.article_id): model_to_dict(a)})

    def test_no_duplicates(self):
        """
        Test if there are no duplicates if article is present
        in multiple feeds
        """
        # add to 1st feed
        u, a = self.user[0], self.feed_map[0]
        # add the second feed to user
        u.feeds.add(self.feed[1])

        request = self.factory.get('/feeder/add_article_to_feed/?article_id='
                                   + str(a.article_id) + '&feedname=' +
                                   self.fnames[0])
        response = add_article_to_feed(request)
        self.assertEqual(response.content, 'Success!')

        # add to second feed
        request = self.factory.get('/feeder/add_article_to_feed/?article_id='
                                   + str(a.article_id) + '&feedname=' +
                                   self.fnames[1])
        response = add_article_to_feed(request)
        self.assertEqual(response.content, 'Success!')

        request = self.factory.get(
            '/feeder/get_user_articles/?username=' + self.unames[0])
        response = get_user_articles(request)
        d = {str(a.article_id): model_to_dict(a)}
        self.assertEqual(json.loads(response.content),
                         {str(a.article_id): model_to_dict(a)})
