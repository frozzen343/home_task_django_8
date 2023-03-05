import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from students.models import Course, Student


URL = '/api/v1/courses/'


@pytest.fixture 
def client():
    return APIClient()


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_get_course(client, course_factory):
    """Test to get the first course."""
    course = course_factory()

    response = client.get(URL)
    data = response.json()

    assert response.status_code == 200
    assert data[0]['name'] == course.name


@pytest.mark.django_db
def test_get_list_courses(client, course_factory):
    """Test to get a list of courses."""
    courses = course_factory(_quantity=10)

    response = client.get(URL)
    data = response.json()

    assert response.status_code == 200
    assert len(data) == len(courses)
    for i, course in enumerate(data):
        assert course['name'] == courses[i].name


@pytest.mark.django_db
def test_id_name_filter(client, course_factory):
    """Test to check course filter by id and name."""
    course = course_factory()

    response = client.get(URL, data={'id': course.id})
    data = response.json()

    assert response.status_code == 200
    assert data[0]['id'] == course.id

    response = client.get(URL, data={'name': course.name})

    assert data[0]['name'] == course.name


@pytest.mark.django_db
def test_crud_courses(client, course_factory):
    """Test to create, read, update courses."""
    response = client.post(URL, data={'name': 'django_course'})
    data = response.json()
    assert response.status_code == 201
    assert data['name'] == 'django_course'

    course = course_factory()
    course_url = URL + str(course.id) + '/'
    response = client.patch(course_url, data={'name': 'django_tests_course'})
    data = response.json()
    assert response.status_code == 200
    assert data['name'] == 'django_tests_course'

    response = client.delete(course_url)
    get_deleted_course = Course.objects.filter(name='django_tests_course').first()
    assert response.status_code == 204
    assert get_deleted_course == None