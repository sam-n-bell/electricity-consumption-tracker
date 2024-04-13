from datetime import date

from sqlalchemy import select, true, false
from sqlalchemy.ext.asyncio import AsyncSession

from database.pg_models import EnergyStat


async def get_energy(
    db_session: AsyncSession,
    classification: str,
    end_date: date = None,
    start_date: date = None,
):
    stmt = select(EnergyStat)
    if classification == "surplus":
        stmt = stmt.where(EnergyStat.surplus == true())
    elif classification == "consumption":
        stmt = stmt.where(EnergyStat.surplus == false())

    if end_date:
        stmt = stmt.where(EnergyStat.use_date <= end_date)
    if start_date:
        stmt = stmt.where(EnergyStat.use_date >= start_date)
    results = (await db_session.scalars(stmt)).all()
    return results
