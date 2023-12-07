from datetime import datetime

from pydantic import  Field
from feedparser import parse
from unidecode import unidecode
from app.general.functions import crop_text, html_2_text
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
            post_date = datetime(*post.published_parsed[:6]) if hasattr(post, 'published_parsed')  else last_sent.date
            if last_sent.date <= post_date:
                if post.description:
                    desc = html_2_text(post.description)
                    desc = html_2_text(desc).replace("\n"," ")
                    desc = crop_text(desc, 160)
                else:
                    desc = ""
                text = f"{post.title} {desc} {post.link} #{unidecode(post.title).replace(' ','')}"
                news.append(TwitterPost(text=text, website=self.feed_url, date=post_date))
        await TwitterPost.insert_many(news,)
        