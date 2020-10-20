from flask import Flask
from blog.models import Entry, db
from faker import Faker


app = Flask(__name__)


def create_posts(classid, number):
    fake = Faker()
    for x in range(number+1):
        if classid == Entry:
            post = Entry(title=fake.sentence(), body=fake.paragraph(10), is_published=True)  # noqa: E501
            db.session.add(post)
        db.session.commit()


create_posts(Entry, 10)
