import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from django_testing.settings import MAX_STUDENTS_PER_COURSE

from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.mark.django_db
# проверка получения курса
def test_retrieve_course(client, course_factory):
    course = course_factory()
    url = f'/api/v1/courses/1/'
    response = client.get(url)
    data = response.json()
    assert response.status_code == 200
    assert data == {
        'id': 1,
        'name': course.name,
        'students': []
    }


@pytest.mark.django_db
# проверка получения списка курсов
def test_list_courses(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get('/api/v1/courses/')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)
    for i, course in enumerate(courses):
        assert data[i] == {
            'id': course.id,
            'name': course.name,
            'students': []
        }


@pytest.mark.django_db
# проверка фильтрации списка курсов по id
def test_filter_courses_by_id(client, course_factory):
    courses = course_factory(_quantity=10)
    url = f'/api/v1/courses/?id={courses[0].id}'
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data == [
        {
            'id': courses[0].id,
            'name': courses[0].name,
            'students': []
        }
    ]


@pytest.mark.django_db
# проверка фильтрации списка курсов по name
def test_filter_courses_by_name(client, course_factory):
    courses = course_factory(_quantity=10)
    filtered_course = courses[3]
    url = f'/api/v1/courses/?name={filtered_course.name}'
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['id'] == filtered_course.id
    assert data[0]['name'] == filtered_course.name
    assert data[0]['students'] == []


@pytest.mark.django_db
# тест успешного создания курса
def test_create_course(client):
    count = Course.objects.count()
    response = client.post('/api/v1/courses/', data={'name': 'Data Science'})
    assert response.status_code == 201
    data = response.json()
    assert data['name'] == 'Data Science'
    assert data.get('id') is not None
    assert Course.objects.count() == count + 1
    assert len(data['students']) == 0


@pytest.mark.django_db
# тест успешного обновления курса
def test_update_course(client, course_factory):
    course = course_factory(name='Python programming')
    url = f'/api/v1/courses/{course.id}/'
    response = client.patch(url, data={'name': 'Advanced Python programming'})
    assert response.status_code == 200
    data = response.json()
    assert data == {
        'id': course.id,
        'name': 'Advanced Python programming',
        'students': []
    }


@pytest.mark.django_db
# тест успешного удаления курс
def test_delete_course(client, course_factory):
    course = course_factory(name='Python programming')
    url = f'/api/v1/courses/{course.id}/'
    response = client.delete(url)
    assert response.status_code == 204
    assert not Course.objects.filter(id=course.id).exists()


@pytest.fixture
def settings_max_students_per_course(settings):
    settings.MAX_STUDENTS_PER_COURSE = 20
    return settings


@pytest.mark.django_db
@pytest.mark.parametrize('students_count, expected_status', [
    (19, 201),  # Максимально допустимое число студентов, успешное создание
    (20, 201),  # Максимально допустимое число студентов, успешное создание
    (21, 400),  # Превышено максимальное число студентов, ошибка
])
def test_limit_create_students(client, settings_max_students_per_course, student_factory, students_count,
                               expected_status):
    count = Course.objects.count()
    students = student_factory(_quantity=students_count)
    students_ids = [student.id for student in students]
    response = client.post('/api/v1/courses/', data={'name': 'Data Science', 'students': students_ids})
    assert response.status_code == expected_status
    if expected_status == 201:
        data = response.json()
        assert data['name'] == 'Data Science'
        assert data.get('id') is not None
        assert Course.objects.count() == count + 1
        assert len(data['students']) == students_count
        assert set(data['students']) == set(students_ids)
    else:
        assert Course.objects.count() == count
