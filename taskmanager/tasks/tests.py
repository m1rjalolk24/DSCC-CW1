import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from tasks.models import Task, Category, Tag


@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='testpass123')


@pytest.fixture
def other_user(db):
    return User.objects.create_user(username='otheruser', password='testpass123')


@pytest.fixture
def category(db, user):
    return Category.objects.create(name='Work', user=user)


@pytest.fixture
def task(db, user, category):
    return Task.objects.create(
        title='Test Task',
        description='A test task',
        priority='high',
        user=user,
        category=category,
    )


# ── Model tests ──────────────────────────────────────────────────────────────

@pytest.mark.django_db
def test_task_str(task):
    assert str(task) == 'Test Task'


@pytest.mark.django_db
def test_category_str(category):
    assert str(category) == 'Work'


@pytest.mark.django_db
def test_tag_str(db):
    tag = Tag.objects.create(name='urgent')
    assert str(tag) == 'urgent'


@pytest.mark.django_db
def test_task_default_not_completed(task):
    assert task.completed is False


@pytest.mark.django_db
def test_task_belongs_to_user(task, user):
    assert task.user == user


@pytest.mark.django_db
def test_task_category_relationship(task, category):
    assert task.category == category
    assert task in category.tasks.all()


@pytest.mark.django_db
def test_task_tag_many_to_many(db, task):
    tag1 = Tag.objects.create(name='backend')
    tag2 = Tag.objects.create(name='frontend')
    task.tags.add(tag1, tag2)
    assert task.tags.count() == 2
    assert tag1 in task.tags.all()


# ── View tests ───────────────────────────────────────────────────────────────

@pytest.mark.django_db
def test_task_list_redirects_unauthenticated(client):
    response = client.get(reverse('task-list'))
    assert response.status_code == 302
    assert '/accounts/login/' in response['Location']


@pytest.mark.django_db
def test_task_list_authenticated(client, user, task):
    client.login(username='testuser', password='testpass123')
    response = client.get(reverse('task-list'))
    assert response.status_code == 200
    assert b'Test Task' in response.content


@pytest.mark.django_db
def test_task_create(client, user, category):
    client.login(username='testuser', password='testpass123')
    response = client.post(reverse('task-create'), {
        'title': 'New Task',
        'description': 'Created in test',
        'priority': 'medium',
        'category': category.pk,
        'tags': [],
    })
    assert response.status_code == 302
    assert Task.objects.filter(title='New Task', user=user).exists()


@pytest.mark.django_db
def test_task_update(client, user, task):
    client.login(username='testuser', password='testpass123')
    response = client.post(reverse('task-update', args=[task.pk]), {
        'title': 'Updated Task',
        'description': task.description,
        'priority': 'low',
        'tags': [],
    })
    assert response.status_code == 302
    task.refresh_from_db()
    assert task.title == 'Updated Task'
    assert task.priority == 'low'


@pytest.mark.django_db
def test_task_delete(client, user, task):
    client.login(username='testuser', password='testpass123')
    pk = task.pk
    response = client.post(reverse('task-delete', args=[pk]))
    assert response.status_code == 302
    assert not Task.objects.filter(pk=pk).exists()


@pytest.mark.django_db
def test_user_cannot_see_other_users_tasks(client, user, other_user, db):
    Task.objects.create(title='Private Task', user=other_user, priority='medium')
    client.login(username='testuser', password='testpass123')
    response = client.get(reverse('task-list'))
    assert b'Private Task' not in response.content


@pytest.mark.django_db
def test_category_list_authenticated(client, user, category):
    client.login(username='testuser', password='testpass123')
    response = client.get(reverse('category-list'))
    assert response.status_code == 200
    assert b'Work' in response.content


@pytest.mark.django_db
def test_category_create(client, user):
    client.login(username='testuser', password='testpass123')
    response = client.post(reverse('category-list'), {'name': 'Personal'})
    assert response.status_code == 302
    assert Category.objects.filter(name='Personal', user=user).exists()
