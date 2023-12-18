from datetime import datetime
from tempfile import NamedTemporaryFile

from feedparser import parse
from openpyxl import Workbook
from pydantic import Field
from unidecode import unidecode

from app.medium.model import MediumPost
from app.folkd.model import FolkdPost
from app.general.functions import crop_text, html_2_text
from app.mixins.general import BaseDocument
from app.twitter.model import TwitterPost


class RSS(BaseDocument):
    active: bool = Field(title="Aktif", default=True)
    feed_url: str | None = Field(title="RSS URL", default="")

    async def feed_to_twitter(self):
        last_sent = (
            await TwitterPost.find(TwitterPost.website == self.feed_url)
            .sort("-date")
            .to_list(1)
        )
        last_sent = (
            last_sent[0] if last_sent else TwitterPost(date=datetime(2021, 1, 1))
        )
        news = []
        feed = parse(self.feed_url).entries
        for post in feed:
            post_date = (
                datetime(*post.published_parsed[:6])
                if hasattr(post, "published_parsed")
                else last_sent.date
            )
            if last_sent.date <= post_date:
                tag = f"#{unidecode(post.title).replace(' ','')}"
                if post.description:
                    desc = html_2_text(post.description)
                    desc = html_2_text(desc).replace("\n", " ")
                    desc = crop_text(desc, 280 - len(desc) - len(post.link) - len(tag) - 10)
                else:
                    desc = ""
                text = f"{post.title} {desc} {post.link} {tag}"
                news.append(
                    TwitterPost(text=text, website=self.feed_url, date=post_date, blogURL=post.link)
                )
        await TwitterPost.insert_many(
            news,
        )

    async def feed_to_folkd(self):
        last_sent = (
            await FolkdPost.find(FolkdPost.website == self.feed_url)
            .sort("-date")
            .to_list(1)
        )
        last_sent = (
            last_sent[0] if last_sent else FolkdPost(date=datetime(2021, 1, 1))
        )
        news = []
        feed = parse(self.feed_url).entries
        default_tags = FolkdPost.model_fields['tags'].default
        for post in feed:
            post_date = (
                datetime(*post.published_parsed[:6])
                if hasattr(post, "published_parsed")
                else last_sent.date
            )
            if last_sent.date <= post_date:
                tag = f"{unidecode(post.title).replace(' ','')}"
                if post.description:
                    desc = html_2_text(post.description)
                    desc = html_2_text(desc).replace("\n", " ")
                    desc = crop_text(desc, 300 - len(desc) - len(post.link) - len(tag))
                else:
                    desc = ""
                
                news.append(
                    FolkdPost(title=post.title, desc=desc, tags=[tag, *default_tags], website=self.feed_url, date=post_date, blogURL=post.link)
                )
        await FolkdPost.insert_many(
            news,
        )

    async def feed_to_medium(self):
        last_sent = (
            await MediumPost.find(MediumPost.website == self.feed_url)
            .sort("-date")
            .to_list(1)
        )
        last_sent = (
            last_sent[0] if last_sent else MediumPost(date=datetime(2021, 1, 1))
        )
        news = []
        feed = parse(self.feed_url).entries
        default_tags = MediumPost.model_fields['tags'].default
        for post in feed:
            post_date = (
                datetime(*post.published_parsed[:6])
                if hasattr(post, "published_parsed")
                else last_sent.date
            )
            if last_sent.date <= post_date:
                tag = f"{unidecode(post.title).replace(' ','')}"
                if post.description:
                    desc = html_2_text(post.description)
                    desc = html_2_text(desc).replace("\n", " ")
                    desc = crop_text(desc, 300 - len(desc) - len(post.link) - len(tag))
                else:
                    desc = ""
                
                news.append(
                    MediumPost(title=post.title, desc=desc, tags=[tag, *default_tags], website=self.feed_url, date=post_date, blogURL=post.link)
                )
        await MediumPost.insert_many(
            news,
        )

    async def excel_report(self):
        classes = [TwitterPost]
        wb = Workbook()
        ws = wb.active
        wb.remove(ws)
        for cls in classes:
            fields = {
                column.title: column.alias
                for column in cls.model_fields.values()
                if column.title
            }
            ws = wb.create_sheet(cls.__title__)
            ws.append(list(fields.keys()))
            now = datetime.now()
            start_time = datetime(month=now.month, year=now.year, day=1)
            end_time = datetime(
                month=now.month,
                year=now.year,
                day=now.day,
                hour=23,
                minute=59,
                second=59,
            )
            for item in await cls.find(
                cls.website == self.feed_url,
                cls.sentDate >= start_time,
                cls.sentDate <= end_time,
                cls.sent == True,
            ).to_list():
                ws.append([getattr(item, field) for field in fields.values()])
            tmp = NamedTemporaryFile(delete=False)
            wb.save(tmp.name)
            return tmp
