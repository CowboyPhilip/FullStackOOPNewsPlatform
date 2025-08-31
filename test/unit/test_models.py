from app.models.user_model import User

def test_create_and_get_user(db_session):
    # 创建
    new_user = User(id="1", name="David")
    db_session.add(new_user)
    db_session.commit()

    # 查询
    db_user = db_session.query(User).filter_by(id="1").first()
    assert db_user is not None
    assert db_user.name == "David"
