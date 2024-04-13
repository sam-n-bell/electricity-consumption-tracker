from datetime import date, time
from sqlalchemy import Boolean, Date, Float, Time, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column

PG_BASE = declarative_base()


class EnergyStat(PG_BASE):
    __tablename__ = "energy_stat"
    id: Mapped[UUID] = mapped_column(
        UUID, primary_key=True, server_default=func.gen_random_uuid()
    )
    use_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    kwh: Mapped[float] = mapped_column(Float, nullable=False)
    surplus: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
