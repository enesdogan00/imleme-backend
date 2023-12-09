from beanie import PydanticObjectId
from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.general.exceptions import NoRecordException
from app.rss.model import RSS

router = APIRouter()


@router.get("/{feed_id}")
async def get_monthly_report(feed_id: PydanticObjectId) -> FileResponse:
    feed = await RSS.get(feed_id)
    if not feed:
        raise NoRecordException
    file = await feed.excel_report()
    return FileResponse(
        file.name,
        filename="report.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
