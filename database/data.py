from datetime import date

from sqlalchemy import extract, false, func, select, true
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


async def get_aggregate_energy(
    db_session: AsyncSession,
    group_date_by: str,
    end_date: date = None,
    start_date: date = None,
):
    group_date_by = group_date_by.upper()
    stmt = select(
        extract(group_date_by, EnergyStat.use_date),
        EnergyStat.surplus,
        func.sum(EnergyStat.kwh),
    )
    if end_date:
        stmt = stmt.where(EnergyStat.use_date <= end_date)
    if start_date:
        stmt = stmt.where(EnergyStat.use_date >= start_date)
    stmt = stmt.group_by(
        extract(group_date_by, EnergyStat.use_date), EnergyStat.surplus
    )
    # wouldnt use .scalars() here bc it will return the first column of each row
    results = await db_session.execute(stmt)
    return results
