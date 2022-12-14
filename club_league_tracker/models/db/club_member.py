from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from club_league_tracker.db import Base
from club_league_tracker.models.enums.defaults import Defaults

class ClubMember(Base):
    __tablename__ = 'club_member'
    tag = Column('member_tag', String(16), primary_key=True)
    club_tag = Column('club_tag', String(16), nullable=False, default=Defaults.STRING)
    name = Column('member_name', String(32), nullable=False, default=Defaults.STRING)
    role = Column('member_role', String(32), nullable=False, default=Defaults.STRING)
    trophies = Column('member_trophies', Integer, nullable=False, default=Defaults.INTEGER)
    club_league_games = relationship('ClubLeagueGame', backref='club_member', lazy=True)
    club_member_details = relationship('ClubMemberDetails', backref='club_member', lazy=True)

    @staticmethod
    def update(session: Session, new_tag:str, new_club_tag: str, new_name: str, new_role: str, new_trophies: int):
        session.execute(
            insert(ClubMember).
            values(member_tag=new_tag, club_tag=new_club_tag, member_name=new_name, member_role=new_role, member_trophies=new_trophies).
            on_conflict_do_update(
                constraint=ClubMember.__table__.primary_key,
                set_={"member_tag": new_tag, "club_tag": new_club_tag, "member_name": new_name, "member_role": new_role, "member_trophies": new_trophies}
            )
        )

    def __repr__(self):
        return f"Club Member:\n" \
                f"|  tag({self.tag})\n" \
                f"|  clug_tag({self.club_tag})\n" \
                f"|  name({self.name})\n" \
                f"|  role({self.role})\n" \
                f"|  trophies({self.trophies}))\n"
