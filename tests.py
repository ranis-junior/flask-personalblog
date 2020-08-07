from datetime import datetime, timedelta
import unittest

from app import create_app, db
from app.models import User, Post
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    ELASTICSEARCH_URL = None


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='Test User')
        u.password = 'fly to the moon'
        self.assertFalse(u.check_password('I fall'))
        self.assertTrue(u.check_password('fly to the moon'))

    def test_avatar(self):
        u = User(username='Icarus', email='hardsun@test.com')
        self.assertEqual(u.avatar(128),
                         'https://www.gravatar.com/avatar/3daac35e1acd188e34240e0fe82b047f?d=robohash&s=128')

    def test_follow(self):
        u1 = User(username='User1', email='user1@email.com')
        u2 = User(username='User2', email='user2@email.com')

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)

        db.session.commit()

        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'User2')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'User1')

        u1.unfollow(u2)

        db.session.commit()

        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        u1 = User(username='User1', email='user1@testmail.com')
        u2 = User(username='User2', email='user2@testmail.com')
        u3 = User(username='User3', email='user3@testmail.com')
        u4 = User(username='User4', email='user4@testmail.com')

        db.session.add_all([u1, u2, u3, u4])

        now = datetime.utcnow()

        p1 = Post(body='body from user 1', author=u1, timestamp=now + timedelta(seconds=1))
        p2 = Post(body='body from user 2', author=u2, timestamp=now + timedelta(seconds=2))
        p3 = Post(body='body from user 3', author=u3, timestamp=now + timedelta(seconds=3))
        p4 = Post(body='body from user 4', author=u4, timestamp=now + timedelta(seconds=4))

        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        u1.follow(u2)
        u1.follow(u4)
        u2.follow(u3)
        u3.follow(u4)
        db.session.commit()

        fp1 = u1.followed_posts().all()
        fp2 = u2.followed_posts().all()
        fp3 = u3.followed_posts().all()
        fp4 = u4.followed_posts().all()

        self.assertEqual(fp1, [p4, p2, p1])
        self.assertEqual(fp2, [p3, p2])
        self.assertEqual(fp3, [p4, p3])
        self.assertEqual(fp4, [p4])


if __name__ == '__main__':
    unittest.main(verbosity=2)
