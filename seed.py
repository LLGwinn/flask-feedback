from app import app
from models import db, User, Feedback
from flask_bcrypt import Bcrypt


db.drop_all()
db.create_all()

bcrypt = Bcrypt()
hash = bcrypt.generate_password_hash('testpassword')
hash_utf8 = hash.decode('utf8')

test_user = User(
    username="testusername",
    password=hash_utf8,
    email="testemail@testemail.com",
    first_name="testfirstname",
    last_name="testlastname"
)

db.session.add(test_user)
db.session.commit()

test_feedback = Feedback(
    title='testtitle',
    content='testcontent blah blah blah blah blah blah blah',
    username='testusername'
)

db.session.add(test_feedback)
db.session.commit()