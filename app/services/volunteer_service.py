from datetime import date
from calendar import monthrange
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from ..models.user_points import UserPointsSummary, PeriodType
from ..schemas.volunteer import VolunteerSummaryOut

from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from ..models.user_points import UserPointsSummary, PeriodType

class VolunteerService:

    @staticmethod
    def get_top_volunteers_all_honors(db: Session, period: Optional[str] = None,
                                       year: Optional[int] = None,
                                       month: Optional[int] = None):
        top_volunteers = []

        if period:
            try:
                period_types = [PeriodType(period)]
            except ValueError:
                raise ValueError(f"Invalid period type: {period}")
        else:
            period_types = list(PeriodType)

        for period_enum in period_types:
            query = db.query(UserPointsSummary.period_start, UserPointsSummary.period_end)\
                      .filter(UserPointsSummary.period_type == period_enum)

            if period_enum == PeriodType.YEAR and year:
                query = query.filter(extract('year', UserPointsSummary.period_start) == year)

            elif period_enum == PeriodType.SMONTH and year:
                query = query.filter(extract('year', UserPointsSummary.period_start) == year)

            elif period_enum == PeriodType.MONTH:
                if year is not None and month is not None:
                    query = query.filter(
                        extract('year', UserPointsSummary.period_start) == year,
                        extract('month', UserPointsSummary.period_start) == month
                    )
                elif year is not None:
                    query = query.filter(extract('year', UserPointsSummary.period_start) == year)

            periods = query.distinct().all()

            for start, end in periods:
                max_points = (
                    db.query(func.max(UserPointsSummary.total_points))
                    .filter(
                        UserPointsSummary.period_type == period_enum,
                        UserPointsSummary.period_start == start,
                        UserPointsSummary.period_end == end,
                    )
                    .scalar()
                )

                top_in_period = (
                    db.query(UserPointsSummary)
                    .filter(
                        UserPointsSummary.period_type == period_enum,
                        UserPointsSummary.period_start == start,
                        UserPointsSummary.period_end == end,
                        UserPointsSummary.total_points == max_points,
                    )
                    .join(UserPointsSummary.user)
                    .all()
                )

                for summary in top_in_period:
                    top_volunteers.append({
                        "user_id": summary.user.id,
                        "full_name": f"{summary.user.first_name} {summary.user.last_name}",
                        "image": summary.user.profile_picture,
                        "total_points": summary.total_points,
                        "period_type": period_enum.value,
                        "period_start": str(start),
                        "period_end": str(end),
                    })

        return top_volunteers
