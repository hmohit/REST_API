from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from django.forms.models import model_to_dict
from feeder.models import UserInfo, Feed, Article


# Create your views here.


def index(request):
    return HttpResponse(
        "Hello!!! Try the following API: /subscribe_user_to_feed, "
        "/unsubscribe_user_from_feed, /add_article_to_feed, /get_user_feeds, "
        "/get_user_articles")


def subscribe_user_to_feed(request):
    """subscribes a user to a feed

    @input: username
    @input: feedname
    """

    username = request.GET.get('username', None)
    feedname = request.GET.get('feedname', None)

    if not username:
        return HttpResponse('No username entered')

    if not feedname:
        return HttpResponse('No feedname entered')

    try:
        user = UserInfo.objects.get(username=username)
    except Exception as e:
        return HttpResponse('Invalid username')

    try:
        feed = Feed.objects.get(feedname=feedname)
    except Exception as e:
        return HttpResponse('Invalid feedname')

    user.feeds.add(feed)
    return HttpResponse('Success!')


def unsubscribe_user_from_feed(request):
    """unsubscribes a user from a feed

    @input: username
    @input: feedname
    """

    username = request.GET.get('username', None)
    feedname = request.GET.get('feedname', None)

    if not username:
        return HttpResponse('No username entered')

    if not feedname:
        return HttpResponse('No feedname entered')

    try:
        user = UserInfo.objects.get(username=username)
    except Exception as e:
        return HttpResponse('Invalid username')

    try:
        feed = Feed.objects.get(feedname=feedname)
    except Exception as e:
        return HttpResponse('Invalid feedname')

    user.feeds.remove(feed)
    return HttpResponse('Success!')


def add_article_to_feed(request):
    """subscribes a user to a feed

    @input: article_id
    @input: feedname
    """

    article_id = request.GET.get('article_id', None)
    feedname = request.GET.get('feedname', None)

    if not article_id:
        return HttpResponse('No Article Id entered')

    if not article_id.isdigit():
        return HttpResponse('Article Id shoud be numeric')

    if not feedname:
        return HttpResponse('No feedname entered')

    try:
        feed = Feed.objects.get(feedname=feedname)
    except Exception as e:
        return HttpResponse('Invalid feedname')
    try:
        article = Article.objects.get(article_id=int(article_id))
    except Exception as e:
        return HttpResponse('Article does not exist')

    feed.articles.add(article)
    return HttpResponse('Success!')


def get_user_feeds(request):
    """subscribes a user to a feed

    @input: username
    """

    username = request.GET.get('username', None)

    if not username:
        return HttpResponse('No username entered')

    try:
        user = UserInfo.objects.get(username=username)
    except Exception as e:
        return HttpResponse('Invalid username')

    feednames = user.feeds.filter().values_list('feedname', flat=True)
    return HttpResponse(',  '.join(feednames))


def get_user_articles(request):
    """subscribes a user to a feed

    @input: username
    """

    username = request.GET.get('username', None)

    if not username:
        return HttpResponse('No username entered')

    try:
        user = UserInfo.objects.get(username=username)
    except Exception as e:
        return HttpResponse('Invalid username')

    # add to dict to avoid duplicates
    all_articles = {}
    for f in user.feeds.all():
        for a in f.articles.all():
            all_articles[a.article_id] = model_to_dict(a)

    return JsonResponse(all_articles)
