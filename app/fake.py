from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker

from app import db
from app.models import User, Post


def user(amount=100):
    fake = Faker()
    i = 0
    for i in range(amount):
        u = User(username=fake.user_name(), email=fake.email(), password=fake.password(),
                 about_me=fake.text(), last_seen=fake.past_date())
        db.session.add(u)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def post(amount=100):
    fake = Faker()
    user_count = User.query.count()
    for i in range(amount):
        u = User.query.offset(randint(0, user_count - 1)).first()
        p = Post(body=fake.text(), author=u, timestamp=fake.past_date(), language='en')
        db.session.add(p)
    db.session.commit()
