from app import app
from models import db, User, Post

# Drop all and recreate tables
with app.app_context():
    db.drop_all()
    db.create_all()

    # Create users
    user1 = User(first_name="Luna", last_name="Lovegood", image_url="https://i.imgur.com/1tYcK7G.png")
    user2 = User(first_name="Remus", last_name="Lupin")
    user3 = User(first_name="Tonks", last_name="Nymphadora", image_url="https://i.imgur.com/x9hJ5GV.jpg")

    db.session.add_all([user1, user2, user3])
    db.session.commit()

    # Create posts
    post1 = Post(title="On Wrackspurts", content="They make your brain go fuzzy.", user_id=user1.id)
    post2 = Post(title="The Full Moon", content="A reflection on control and compassion.", user_id=user2.id)
    post3 = Post(title="Hair Color Magic", content="Sometimes I’m bubblegum pink. Sometimes teal. Magic!", user_id=user3.id)
    post4 = Post(title="Dumbledore's Army", content="We never disbanded.", user_id=user1.id)

    db.session.add_all([post1, post2, post3, post4])
    db.session.commit()
    print("Database seeded!")
