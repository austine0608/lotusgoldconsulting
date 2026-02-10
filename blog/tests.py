from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post, Category, Tag, Comment


class CategoryModelTest(TestCase):
    def test_category_creation(self):
        category = Category.objects.create(name='Technology', description='Tech posts')
        self.assertEqual(category.name, 'Technology')
        self.assertEqual(category.slug, 'technology')

    def test_category_str(self):
        category = Category.objects.create(name='Python')
        self.assertEqual(str(category), 'Python')


class TagModelTest(TestCase):
    def test_tag_creation(self):
        tag = Tag.objects.create(name='Django')
        self.assertEqual(tag.name, 'Django')
        self.assertEqual(tag.slug, 'django')

    def test_tag_str(self):
        tag = Tag.objects.create(name='Tutorial')
        self.assertEqual(str(tag), 'Tutorial')


class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.category = Category.objects.create(name='Test Category')
        self.tag = Tag.objects.create(name='Test Tag')

    def test_post_creation(self):
        post = Post.objects.create(
            title='Test Post',
            author=self.user,
            content='Test content',
            category=self.category,
            status='published'
        )
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.slug, 'test-post')
        self.assertEqual(post.status, 'published')

    def test_post_with_tags(self):
        post = Post.objects.create(
            title='Tagged Post',
            author=self.user,
            content='Content with tags',
            status='published'
        )
        post.tags.add(self.tag)
        self.assertEqual(post.tags.count(), 1)

    def test_post_ordering(self):
        post1 = Post.objects.create(title='First Post', author=self.user, content='First', status='published')
        post2 = Post.objects.create(title='Second Post', author=self.user, content='Second', status='published')
        posts = list(Post.objects.all())
        self.assertEqual(posts[0], post2)
        self.assertEqual(posts[1], post1)

    def test_post_get_absolute_url(self):
        post = Post.objects.create(title='URL Test', author=self.user, content='Test', status='published')
        self.assertEqual(post.get_absolute_url(), f'/post/{post.slug}/')


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='commenter', password='testpass123')
        self.author = User.objects.create_user(username='author', password='authorpass123')
        self.post = Post.objects.create(
            title='Post to Comment',
            author=self.author,
            content='Content',
            status='published'
        )

    def test_comment_creation(self):
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Great post!'
        )
        self.assertEqual(comment.content, 'Great post!')
        self.assertFalse(comment.approved)

    def test_comment_str(self):
        comment = Comment.objects.create(post=self.post, author=self.user, content='Nice!')
        self.assertIn(self.user.username, str(comment))
        self.assertIn(self.post.title, str(comment))


class ViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='blogger', password='blogpass123')
        self.category = Category.objects.create(name='Views Category')
        self.post = Post.objects.create(
            title='Test View Post',
            author=self.user,
            content='View test content',
            category=self.category,
            status='published'
        )

    def test_post_list_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_post_detail_view(self):
        response = self.client.get(f'/post/{self.post.slug}/')
        self.assertEqual(response.status_code, 200)

    def test_category_posts_view(self):
        response = self.client.get(f'/category/{self.category.slug}/')
        self.assertEqual(response.status_code, 200)

    def test_tag_posts_view(self):
        tag = Tag.objects.create(name='View Tag')
        self.post.tags.add(tag)
        response = self.client.get(f'/tag/{tag.slug}/')
        self.assertEqual(response.status_code, 200)

    def test_post_create_requires_login(self):
        response = self.client.get('/post/create/')
        self.assertEqual(response.status_code, 302)

    def test_post_create_logged_in(self):
        self.client.login(username='blogger', password='blogpass123')
        response = self.client.get('/post/create/')
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_post_update(self):
        other_user = User.objects.create_user(username='other', password='otherpass123')
        self.client.login(username='other', password='otherpass123')
        response = self.client.get(f'/post/{self.post.slug}/update/')
        self.assertEqual(response.status_code, 302)

    def test_authorized_post_update(self):
        self.client.login(username='blogger', password='blogpass123')
        response = self.client.get(f'/post/{self.post.slug}/update/')
        self.assertEqual(response.status_code, 200)
