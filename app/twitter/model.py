import tweepy

from pydantic import  Field

from app.mixins.general import BaseDocument


class TwitterPost(BaseDocument):
    text: str = Field(title="Tweet İçeriği")
    sent: bool = Field(title="Gönderildi mi?", default=False)
    

class Twitter(BaseDocument):
    name: str|None = Field(title="İsim",default="")
    consumer_key: str = Field(title="Consumer Key")
    consumer_secret: str = Field(title="Consumer Secret")
    access_token: str = Field(title="Access Token")
    access_token_secret: str = Field(title="Access Token Secret")


    def send_post(self, text: str):
        client = tweepy.Client(consumer_key=self.consumer_key,
                               consumer_secret=self.consumer_secret,
                               access_token=self.access_token,
                               access_token_secret=self.access_token_secret)
        return client.create_tweet(text=text)
