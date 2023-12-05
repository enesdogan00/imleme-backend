import requests
from pydantic import BaseModel

from app.mixins.general import BaseDocument


class NetGSM(BaseDocument):
    base_url: str = "https://api.netgsm.com.tr"
    usercode: str
    password: str
    msgheader: str

    class OneToN(BaseModel):
        msg: str
        phone: list[str]

    class NtoN(BaseModel):
        msg: str
        phone: str

    def post(self, url: str, data: str):
        headers = {"Content-Type": "application/xml", "Accept-Encoding": "identity"}
        return requests.post(self.base_url + url, data=data.encode(), headers=headers, timeout=10)

    async def send_1n_sms(self, data: OneToN) -> None:
        res = self.post(
            "/sms/send/xml",
            data=f"""<?xml version="1.0" encoding="UTF-8"?>
<mainbody>
    <header>
        <company dil="TR">Netgsm</company>
        <usercode>{self.usercode}</usercode>
        <password>{self.password}</password>
        <type>1:n</type>
        <msgheader>{self.msgheader}</msgheader>
    </header>
    <body>
        <msg>{data.msg}</msg>
        {"".join([f"<no>{phone}</no>" for phone in data.phone])}
    </body>
</mainbody>""",
        )
        return res.ok

    async def send_nn_sms(self, data: list[NtoN]) -> None:
        res = self.post(
            "/sms/send/xml",
            data=f"""<?xml version="1.0" encoding="UTF-8"?>
<mainbody>
    <header>
        <company dil="TR">Netgsm</company>
        <usercode>{self.usercode}</usercode>
        <password>{self.password}</password>
        <type>n:n</type>
        <msgheader>{self.msgheader}</msgheader>
    </header>
    <body>
    {"".join([f"<mp><msg>{row.msg}</msg><no>{row.phone}</no></mp>" for row in data])}
    </body>
</mainbody>""",
        )
        return res.ok
