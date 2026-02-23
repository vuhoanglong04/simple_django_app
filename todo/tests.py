from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Todo, Category, Tag, UserProfile
from datetime import datetime, timedelta


class CategoryModelTest(TestCase):
    """Test cases for Category model"""

    def setUp(self):
        self.category = Category.objects.create(
            name="Work",
            color="#3498db",
            description="Work-related tasks"
        )

    def test_category_creation(self):
        """Test creating a category"""
        self.assertEqual(self.category.name, "Work")
        self.assertEqual(self.category.color, "#3498db")
        self.assertTrue(isinstance(self.category, Category))

    def test_category_str(self):
        """Test category string representation"""
        self.assertEqual(str(self.category), "Work")

    def test_category_ordering(self):
        """Test categories are ordered by name"""
        Category.objects.create(name="Personal")
        Category.objects.create(name="Urgent")
        categories = Category.objects.all()
        self.assertEqual(categories[0].name, "Personal")
        self.assertEqual(categories[1].name, "Urgent")
        self.assertEqual(categories[2].name, "Work")

    def test_category_unique_name(self):
        """Test category names must be unique"""
        with self.assertRaises(Exception):
            Category.objects.create(name="Work")


class TagModelTest(TestCase):
    """Test cases for Tag model"""

    def setUp(self):
        self.tag = Tag.objects.create(name="urgent")

    def test_tag_creation(self):
        """Test creating a tag"""
        self.assertEqual(self.tag.name, "urgent")
        self.assertTrue(isinstance(self.tag, Tag))

    def test_tag_str(self):
        """Test tag string representation"""
        self.assertEqual(str(self.tag), "urgent")

    def test_tag_unique_name(self):
        """Test tag names must be unique"""
        with self.assertRaises(Exception):
            Tag.objects.create(name="urgent")


class TodoModelTest(TestCase):
    """Test cases for Todo model"""

    def setUp(self):
        self.category = Category.objects.create(name="Work")
        self.tag1 = Tag.objects.create(name="urgent")
        self.tag2 = Tag.objects.create(name="important")
        self.user = User.objects.create_user(username="testuser", password="testpass123")

        self.todo = Todo.objects.create(
            title="Test Todo",
            description="Test Description",
            priority="high",
            category=self.category,
            owner=self.user
        )
        self.todo.tags.add(self.tag1, self.tag2)

    def test_todo_creation(self):
        """Test creating a todo"""
        self.assertEqual(self.todo.title, "Test Todo")
        self.assertEqual(self.todo.description, "Test Description")
        self.assertEqual(self.todo.priority, "high")
        self.assertFalse(self.todo.completed)
        self.assertEqual(self.todo.category, self.category)
        self.assertEqual(self.todo.owner, self.user)

    def test_todo_str(self):
        """Test todo string representation"""
        self.assertEqual(str(self.todo), "Test Todo")

    def test_todo_default_values(self):
        """Test todo default values"""
        simple_todo = Todo.objects.create(title="Simple Todo")
        self.assertFalse(simple_todo.completed)
        self.assertEqual(simple_todo.priority, "medium")
        self.assertIsNone(simple_todo.category)
        self.assertIsNone(simple_todo.owner)

    def test_todo_tags_relationship(self):
        """Test many-to-many relationship with tags"""
        self.assertEqual(self.todo.tags.count(), 2)
        self.assertIn(self.tag1, self.todo.tags.all())
        self.assertIn(self.tag2, self.todo.tags.all())

    def test_todo_category_deletion(self):
        """Test todo survives category deletion (SET_NULL)"""
        self.category.delete()
        self.todo.refresh_from_db()
        self.assertIsNone(self.todo.category)

    def test_todo_owner_deletion(self):
        """Test todo is deleted when owner is deleted (CASCADE)"""
        user_id = self.user.id
        self.user.delete()
        with self.assertRaises(Todo.DoesNotExist):
            Todo.objects.get(owner_id=user_id)

    def test_todo_ordering(self):
        """Test todos are ordered by creation date descending"""
        todo1 = Todo.objects.create(title="First")
        todo2 = Todo.objects.create(title="Second")
        todos = Todo.objects.all()
        self.assertEqual(todos[0].title, "Second")


class UserProfileModelTest(TestCase):
    """Test cases for UserProfile model"""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.profile = UserProfile.objects.create(
            user=self.user,
            bio="Test bio",
            theme_preference="dark",
            email_notifications=False
        )

    def test_profile_creation(self):
        """Test creating a user profile"""
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.bio, "Test bio")
        self.assertEqual(self.profile.theme_preference, "dark")
        self.assertFalse(self.profile.email_notifications)

    def test_profile_str(self):
        """Test profile string representation"""
        self.assertEqual(str(self.profile), "testuser's profile")

    def test_profile_default_values(self):
        """Test profile default values"""
        user2 = User.objects.create_user(username="user2", password="pass123")
        profile2 = UserProfile.objects.create(user=user2)
        self.assertEqual(profile2.theme_preference, "light")
        self.assertTrue(profile2.email_notifications)

    def test_profile_deletion_with_user(self):
        """Test profile is deleted when user is deleted"""
        profile_id = self.profile.id
        self.user.delete()
        with self.assertRaises(UserProfile.DoesNotExist):
            UserProfile.objects.get(id=profile_id)


class TodoViewsTest(TestCase):
    """Test cases for Todo views"""

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Work", color="#3498db")
        self.tag = Tag.objects.create(name="urgent")

    def test_index_view_get(self):
        """Test GET request to index view"""
        response = self.client.get(reverse('todo_index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/index.html')
        self.assertIn('todos', response.context)
        self.assertIn('categories', response.context)
        self.assertIn('tags', response.context)

    def test_index_view_post_create_todo(self):
        """Test POST request to create a todo"""
        data = {
            'title': 'New Todo',
            'description': 'Test description',
            'priority': 'high',
            'category': self.category.id,
            'tags': 'urgent,important'
        }
        response = self.client.post(reverse('todo_index'), data)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertTrue(Todo.objects.filter(title='New Todo').exists())
        
        todo = Todo.objects.get(title='New Todo')
        self.assertEqual(todo.description, 'Test description')
        self.assertEqual(todo.priority, 'high')
        self.assertEqual(todo.category, self.category)
        self.assertTrue(todo.tags.filter(name='urgent').exists())

    def test_index_view_post_without_title(self):
        """Test POST request without title"""
        data = {'description': 'Test'}
        response = self.client.post(reverse('todo_index'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), 0)

    def test_toggle_todo_view(self):
        """Test toggling todo completion status"""
        todo = Todo.objects.create(title="Test Todo", completed=False)
        response = self.client.post(reverse('toggle_todo', args=[todo.id]))
        self.assertEqual(response.status_code, 200)
        
        todo.refresh_from_db()
        self.assertTrue(todo.completed)
        
        # Toggle again
        response = self.client.post(reverse('toggle_todo', args=[todo.id]))
        todo.refresh_from_db()
        self.assertFalse(todo.completed)

    def test_toggle_todo_invalid_id(self):
        """Test toggling non-existent todo"""
        response = self.client.post(reverse('toggle_todo', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_delete_todo_view(self):
        """Test deleting a todo"""
        todo = Todo.objects.create(title="Test Todo")
        todo_id = todo.id
        response = self.client.post(reverse('delete_todo', args=[todo_id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Todo.objects.filter(id=todo_id).exists())

    def test_delete_todo_invalid_id(self):
        """Test deleting non-existent todo"""
        response = self.client.post(reverse('delete_todo', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_manage_categories_view_get(self):
        """Test GET request to manage categories view"""
        response = self.client.get(reverse('manage_categories'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/categories.html')
        self.assertIn('categories', response.context)

    def test_manage_categories_view_post(self):
        """Test POST request to create a category"""
        data = {
            'name': 'Personal',
            'color': '#e74c3c',
            'description': 'Personal tasks'
        }
        response = self.client.post(reverse('manage_categories'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Category.objects.filter(name='Personal').exists())
        
        category = Category.objects.get(name='Personal')
        self.assertEqual(category.color, '#e74c3c')
        self.assertEqual(category.description, 'Personal tasks')


class TodoIntegrationTest(TestCase):
    """Integration tests for the full todo workflow"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass123")

    def test_complete_todo_workflow(self):
        """Test creating, updating, and deleting a todo"""
        # Create category
        category_data = {'name': 'Work', 'color': '#3498db', 'description': 'Work tasks'}
        self.client.post(reverse('manage_categories'), category_data)
        category = Category.objects.get(name='Work')

        # Create todo
        todo_data = {
            'title': 'Complete project',
            'description': 'Finish the Django project',
            'priority': 'high',
            'category': category.id,
            'tags': 'urgent,work'
        }
        self.client.post(reverse('todo_index'), todo_data)
        todo = Todo.objects.get(title='Complete project')
        
        self.assertFalse(todo.completed)
        self.assertEqual(todo.category, category)
        self.assertEqual(todo.tags.count(), 2)

        # Toggle completion
        self.client.post(reverse('toggle_todo', args=[todo.id]))
        todo.refresh_from_db()
        self.assertTrue(todo.completed)

        # Delete todo
        self.client.post(reverse('delete_todo', args=[todo.id]))
        self.assertFalse(Todo.objects.filter(id=todo.id).exists())

    def test_multiple_todos_with_same_category(self):
        """Test multiple todos can share the same category"""
        category = Category.objects.create(name='Work')
        
        Todo.objects.create(title='Todo 1', category=category)
        Todo.objects.create(title='Todo 2', category=category)
        Todo.objects.create(title='Todo 3', category=category)
        
        self.assertEqual(category.todos.count(), 3)


class TodoQueryOptimizationTest(TestCase):
    """Test query optimization for todo views"""

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Work')
        self.tag = Tag.objects.create(name='urgent')
        
        # Create multiple todos
        for i in range(10):
            todo = Todo.objects.create(
                title=f'Todo {i}',
                category=self.category,
                priority='medium'
            )
            todo.tags.add(self.tag)

    def test_index_view_uses_select_related(self):
        """Test that index view uses select_related for performance"""
        with self.assertNumQueries(3):  # Should be minimal queries
            response = self.client.get(reverse('todo_index'))
            todos = list(response.context['todos'])
            # Access related category and tags (should not trigger additional queries)
            for todo in todos:
                _ = todo.category
                _ = list(todo.tags.all())
