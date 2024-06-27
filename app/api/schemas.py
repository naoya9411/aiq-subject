from pydantic import BaseModel
from decimal import Decimal
    

class InfluencerAvgStats(BaseModel):
    avg_likes: Decimal
    avg_comments: Decimal


class InfluencerAvgLikes(BaseModel):
    influencer_id: int
    avg_likes: Decimal


class InfluencerAvgComments(BaseModel):
    influencer_id: int
    avg_comments: Decimal


class InfluencerNoun(BaseModel):
    noun: str
    count: int