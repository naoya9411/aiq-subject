
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from collections import Counter
import spacy

from app.api import schemas
from app.api.models import Post


async def get_influencer_avg_stats(db: AsyncSession, influencer_id: int) -> schemas.InfluencerAvgStats:
    """
    特定のinfluencerの平均いいね、コメント数取得
    """

    query = await db.execute(
        select(
            func.avg(Post.likes).label('avg_likes'),
            func.avg(Post.comments).label('avg_comments'),
        ).where(
            Post.influencer_id == influencer_id
        )
    )
    avg_result = query.first()

    if avg_result.avg_likes is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given influencer's id not found",
        )

    return {
        'avg_likes': avg_result.avg_likes,
        'avg_comments': avg_result.avg_comments,
    }


async def get_top_influencers_by_likes(
    db: AsyncSession,
    limit: int,
) -> list[schemas.InfluencerAvgLikes]:
    """
    平均いいね数が多いinfluencer上位N件取得
    """

    query = await db.execute(
        select(
            Post.influencer_id,
            func.avg(Post.likes).label('avg_likes'),
        ).group_by(
            Post.influencer_id
        ).order_by(
            func.avg(Post.likes).desc()
        ).limit(limit)
    )
    top_influencers_by_likes = query.all()

    return top_influencers_by_likes


async def get_top_influencers_by_comments(
    db: AsyncSession,
    limit: int,
) -> list[schemas.InfluencerAvgComments]:
    """
    平均コメント数が多いinfluencer上位N件取得
    """

    query = await db.execute(
        select(
            Post.influencer_id,
            func.avg(Post.comments).label('avg_comments'),
        ).group_by(
            Post.influencer_id
        ).order_by(
            func.avg(Post.comments).desc()
        ).limit(limit)
    )
    top_influencers_by_comments = query.all()

    return top_influencers_by_comments


def _extract_nouns(text: str) -> list[str]:
    nlp = spacy.load("ja_core_news_sm")
    doc = nlp(text)
    nouns = [token.text for token in doc if token.pos_ == "NOUN"]
    return nouns


async def get_top_nouns_in_posts(
    db: AsyncSession,
    influencer_id: int,
    limit: int
) -> list[schemas.InfluencerNoun]:
    """
    特定のinfluencerの全投稿における各名詞出現回数の上位N件取得
    """

    # 対象インフルエンサーの全投稿内容取得
    query = await db.execute(
        select(Post.text).where(Post.influencer_id == influencer_id))
    texts = query.all()

    # 投稿内容を名詞毎に分割し出現回数の集計
    all_nouns = []
    for text in texts:
        all_nouns.extend(_extract_nouns(text[0]))
    noun_counts = Counter(all_nouns)

    # 上位N件絞り込み
    top_n_nouns = noun_counts.most_common(limit)

    return top_n_nouns
