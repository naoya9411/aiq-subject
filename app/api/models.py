from sqlalchemy import Column, ForeignKey, String, Integer, BigInteger, DateTime, text

from app.database import Base


class DatetimeMixin(object):
    created_at = Column(DateTime(timezone=True),
                        server_default=text('current_timestamp'),
                        nullable=False)
    updated_at = Column(DateTime(timezone=True),
                        server_default=text('current_timestamp'),
                        onupdate=text('current_timestamp'),
                        nullable=False)


class Influencer(Base, DatetimeMixin):
    __tablename__ = "influencers"

    id = Column(Integer, primary_key=True)


class Post(Base, DatetimeMixin):
    __tablename__ = "posts"

    id = Column(BigInteger, primary_key=True)
    influencer_id = Column(Integer, ForeignKey("influencers.id"))
    shortcode = Column(String, nullable=True)
    likes = Column(Integer, nullable=False, default=0)
    comments = Column(Integer, nullable=False, default=0)
    thumbnail = Column(String, nullable=True)
    text = Column(String, nullable=True)
