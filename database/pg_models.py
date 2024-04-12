from sqlalchemy import Column, Integer, String, Float, Date, Time, Boolean
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from uuid import UUID
from datetime import date, time
from sqlalchemy.dialects.postgresql import UUID

PG_BASE = declarative_base()

class EnergyStats(PG_BASE):
    __tablename__ = "energy_stats"
    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, server_default=func.gen_random_uuid())
    use_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    kwh: Mapped[float] = mapped_column(Float, nullable=False)
    surplus: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
