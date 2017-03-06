from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$/?', views.index, name='index'),
    url(r'^subscribe_user_to_feed/', views.subscribe_user_to_feed, name='subscribe'),
    url(r'^unsubscribe_user_from_feed/', views.unsubscribe_user_from_feed, name='unsubscribe'),
    url(r'^add_article_to_feed/', views.add_article_to_feed, name='add_article_to_feed'),
    url(r'get_user_feeds/', views.get_user_feeds, name='get_user_feeds'),
    url(r'get_user_articles/', views.get_user_articles, name='get_user_articles'),

]