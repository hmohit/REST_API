import csv
from feeder.models import UserInfo, Feed, Article


def load_data():
    with open('feeder/newsCorpora.csv', 'r') as csvfile:
        f = csv.reader(csvfile, delimiter='\t')
        
        for row in f:
            a_id, title, url, publisher, feedname = row[0], row[1], row[2], row[3], row[4]
            article = Article(article_id=a_id, title=title, url=url, publisher=publisher)
            article.save()
            feed, present = Feed.objects.get_or_create(feedname=feedname)
            feed.articles.add(article)

    usernames = ['Mohit', 'Matt', 'Sabrina', 'Sara', 'Priya', 'Confluent']
    
    for uname in usernames:
        user = UserInfo(username=uname)
        user.save()
