
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.api import schemas, crud

router = APIRouter(prefix='', tags=[''])


@router.get('/influencers/{influencer_id}/avg_stats', response_model=schemas.InfluencerAvgStats)
async def get_influencer_avg_stats(influencer_id: int, db: AsyncSession = Depends(get_db)):
    """
    特定のinfluencerの平均いいね、コメント数取得
    """

    return await crud.get_influencer_avg_stats(db, influencer_id)


@router.get("/influencers/top-likes/{limit}", response_model=list[schemas.InfluencerAvgLikes])
async def get_top_influencers_by_likes(limit: int, db: AsyncSession = Depends(get_db)):
    """
    平均いいね数が多いinfluencer上位N件取得
    """

    return await crud.get_top_influencers_by_likes(db, limit)


@router.get("/influencers/top-comments/{limit}", response_model=list[schemas.InfluencerAvgComments])
async def get_top_influencers_by_comments(limit: int, db: AsyncSession = Depends(get_db)):
    """
    平均コメント数が多いinfluencer上位N件取得
    """

    return await crud.get_top_influencers_by_comments(db, limit)


@router.get("/influencers/{influencer_id}/top-nouns/{limit}", response_model=list[schemas.InfluencerNoun])
async def get_top_nouns_in_posts(influencer_id: int,
                                 limit: int,
                                 db: AsyncSession = Depends(get_db)):
    """
    特定のinfluencerの全投稿における各名詞出現回数の上位N件取得
    """

    return await crud.get_top_nouns_in_posts(db, influencer_id, limit)
