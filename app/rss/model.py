from datetime import datetime
from random import randint
from beanie import Indexed
from requests import get
import tweepy

from pydantic import  Field
from feedparser import parse
from app.mixins.general import BaseDocument
from app.twitter.model import TwitterPost


class RSS(BaseDocument):
    active: bool = Field(title="Aktif",default=True)
    feed_url: str|None = Field(title="RSS URL",default="")

    async def feed_to_twitter(self):
        last_sent = await TwitterPost.find(TwitterPost.website == self.feed_url).sort("-date").to_list(1)
        last_sent = last_sent[0] if last_sent else TwitterPost(date=datetime(2021,1,1))
        news = []
        feed = parse(self.feed_url).entries
        for post in feed:
            post_date = datetime(*post.published_parsed[:6])
            if last_sent.date < post_date:
                news.append(TwitterPost(text=f"{post.title} {post.link}", website=self.feed_url, date=post_date))
        await TwitterPost.insert_many(news,)
        