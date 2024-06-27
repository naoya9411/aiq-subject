from fastapi.testclient import TestClient
from app.main import app
from app.api.models import Influencer, Post

client = TestClient(app)


async def test_single_post(test_db):
    """
    正常
    対象のインフルエンサーの投稿が1件存在
    """

    # テストデータ投入
    influencer1 = Influencer(id=1)
    post1 = Post(
        id=1,
        influencer_id=1,
        shortcode='test',
        likes=1000,
        comments=100,
        thumbnail='https://test.com/test',
        text='test text',
    )
    await test_db.add_all([influencer1, post1])
    await test_db.flush()
    await test_db.commit()

    # API実行
    response = await client.get('/influencers/1/avg_stats')

    # 処理結果確認
    assert response.status_code == 200
    data = response.json()
    assert 'average_likes' in data
    assert 'average_comments' in data


async def test_multiple_posts(test_db):
    """
    正常
    対象のインフルエンサーの投稿が複数件存在
    """

    pass


async def test_zero_like_and_comment(test_db):
    """
    正常
    対象のインフルエンサーの平均いいね＆コメント数が0
    """

    pass


async def test_no_posts(test_db):
    """
    異常
    対象のインフルエンサーの投稿が存在しない
    """

    pass


async def test_no_influencer_id_in_path_param(test_db):
    """
    異常
    パスパラメータにインフルエンサーIDの指定がない場合
    """

    pass


async def test_influencer_id_of_string(test_db):
    """
    異常
    パスパラメータのインフルエンサーIDに文字列が指定された場合
    """

    pass
