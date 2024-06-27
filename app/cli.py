import pandas as pd
from sqlalchemy import select

from app.database import SessionLocal
from app.api.models import Influencer, Post
import click

@click.command()
@click.argument('csv_file')
def import_csv(csv_file):
    df = pd.read_csv(csv_file)
    db = SessionLocal()
    influencer_ids: list = db.execute(select(Influencer.id).distinct()).scalars().all()
    print(influencer_ids)
    print(type(influencer_ids))

    for _, row in df.iterrows():
        influencer_id = row['influencer_id']
        # influencersテーブルにinfluencerが存在しない場合は追加
        if influencer_id not in influencer_ids:
            influencer = Influencer(id=influencer_id)
            db.add(influencer)
            influencer_ids.append(influencer_id)

        # postsテーブルに投稿追加
        post = Post(
            id=row['post_id'],
            influencer_id=influencer_id,
            shortcode=row['shortcode'],
            likes=row['likes'],
            comments=row['comments'],
            thumbnail=row['thumbnail'],
            text=row['text'],
            # text='foo',
        )
        db.add(post)
    db.commit()
    db.close()

if __name__ == "__main__":
    import_csv()
