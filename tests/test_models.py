from tests.test_base import BaseTestInit
from tests.common_methods import currentDay
from app.models import db, User

class Users(BaseTestInit):
    """
    just an example test
    """
    def test_example_test(self):
        u = User(email='w.smith@gmail.com', name="Winston Smith", password="password")
        db.session.add(u)
        db.session.commit()

        self.assertEqual(u.id, 1)
        self.assertEqual(u.dateCreated.day, currentDay())
