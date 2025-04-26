from unittest import TestCase
from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test_db'
app.config['TESTING'] = True
app.config['SQLALCHEMY_ECHO'] = False

class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Clean up existing users & add test data."""
        with app.app_context():
            db.drop_all()
            db.create_all()

            user = User(first_name="Test", last_name="User", image_url="https://example.com/image.jpg")
            db.session.add(user)
            db.session.commit()

            self.test_user_id = user.id

    def tearDown(self):
        """Clean up fouled transactions."""
        with app.app_context():
            db.session.rollback()

    def test_homepage_shows_recent_posts(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Recent Posts", html)

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test User", html)

    def test_user_detail(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.test_user_id}")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test User", html)

    def test_add_user(self):
        with app.test_client() as client:
            data = {"first_name": "New", "last_name": "Person", "image_url": ""}
            resp = client.post("/users/new", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("New Person", html)

    def test_edit_user(self):
        with app.test_client() as client:
            data = {"first_name": "Edited", "last_name": "User", "image_url": ""}
            resp = client.post(f"/users/{self.test_user_id}/edit", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Edited User", html)

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post(f"/users/{self.test_user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)

            # Confirm the flash message appeared
            self.assertIn("deleted successfully", html)

            # Check the user is actually deleted from the DB
            with app.app_context():
                self.assertIsNone(User.query.get(self.test_user_id))

    def test_user_detail_not_found(self):
        with app.test_client() as client:
            resp = client.get("/users/9999")
            self.assertEqual(resp.status_code, 404)

    def test_edit_user_cancel_redirect(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.test_user_id}/edit")
            html = resp.get_data(as_text=True)
            self.assertIn(f'href="/users/{self.test_user_id}"', html)

class PostViewsTestCase(TestCase):
    """Tests for views for Posts."""

    def setUp(self):
        with app.app_context():
            db.drop_all()
            db.create_all()

            user = User(first_name="Posty", last_name="McPoster", image_url=None)
            db.session.add(user)
            db.session.commit()

            self.user_id = user.id

            post = Post(title="First Post", content="This is a post.", user_id=self.user_id)
            db.session.add(post)
            db.session.commit()

            self.post_id = post.id

    def tearDown(self):
        with app.app_context():
            db.session.rollback()

    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("First Post", html)

    def test_add_post(self):
        with app.test_client() as client:
            data = {"title": "Another Post", "content": "More content"}
            resp = client.post(f"/users/{self.user_id}/posts/new", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Another Post", html)

    def test_edit_post(self):
        with app.test_client() as client:
            data = {"title": "Updated Title", "content": "Updated content"}
            resp = client.post(f"/posts/{self.post_id}/edit", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Updated Title", html)

    def test_delete_post(self):
        with app.test_client() as client:
            resp = client.post(f"/posts/{self.post_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("deleted successfully", html)  # Check for the flash message

            # Check the post is actually deleted from the DB
            with app.app_context():
                self.assertIsNone(Post.query.get(self.post_id))

    def test_post_not_found(self):
        with app.test_client() as client:
            resp = client.get("/posts/9999")
            self.assertEqual(resp.status_code, 404)