from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import func
from club_league_tracker.db import Base
from club_league_tracker.models.enums.defaults import Defaults

class ClubMemberDetails(Base):
    __tablename__ = 'club_member_details'
    member_tag = Column(String(16), ForeignKey('club_member.member_tag'), nullable=False, primary_key=True)
    start_date = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    departure_date = Column(DateTime(timezone=True), nullable=True, server_default=None)
    victories_trios = Column(Integer, nullable=False, default=Defaults.INTEGER.value)
    victories_duos = Column(Integer, nullable=False, default=Defaults.INTEGER.value)
    victories_solo = Column(Integer, nullable=False, default=Defaults.INTEGER.value)

    @staticmethod
    def update(session: Session, new_tag:str, same_start_date: str, new_departure_date: str, \
        new_victories_trios: int, new_victories_duos: int, new_victories_solo: int):
        session.execute(
            insert(ClubMemberDetails).
            values(member_tag=new_tag, start_date=same_start_date, departure_date=new_departure_date, \
                victories_trios=new_victories_trios, victories_duos=new_victories_duos, victories_solo=new_victories_solo).
            on_conflict_do_update(
                constraint=ClubMemberDetails.__table__.primary_key,
                set_={"member_tag": new_tag, "start_date": same_start_date, "departure_date": new_departure_date, \
                    "victories_trios": new_victories_trios, "victories_duos": new_victories_duos, "victories_solo": new_victories_solo}
            )
        )

    def __repr__(self):
        return f"Club Member Details:\n" \
                f"|  member_tag({self.member_tag})\n" \
                f"|  start_date({self.start_date})\n" \
                f"|  departure_date({self.departure_date})\n" \
                f"|  victories_trios({self.victories_triosc})\n" \
                f"|  victories_duos({self.victories_duos}))\n" \
                f"|  victories_solo({self.victories_solo}))\n"
