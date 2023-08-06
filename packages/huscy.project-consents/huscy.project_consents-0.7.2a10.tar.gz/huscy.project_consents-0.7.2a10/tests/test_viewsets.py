import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from django.contrib.auth.models import Permission
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from huscy.projects.services import create_membership

scenarios('viewsets')

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()


@given('I am admin user', target_fixture='client')
def admin_client(admin_user, api_client):
    api_client.login(username=admin_user.username, password='password')
    return api_client


@given('I am staff user', target_fixture='client')
def staff_user_client(staff_user, api_client):
    api_client.login(username=staff_user.username, password='password')
    return api_client


@given('I am normal user', target_fixture='client')
def user_client(user, api_client):
    api_client.login(username=user.username, password='password')
    return api_client


@given('I am anonymous user', target_fixture='client')
def anonymous_client(api_client):
    return api_client


@given(parsers.parse('I have {codename} permission'), target_fixture='codename')
def assign_permission(user, codename):
    permission = Permission.objects.get(codename=codename)
    user.user_permissions.add(permission)


@given('I am project coordinator')
def coordinator_membership(user, project):
    create_membership(project, user, is_coordinator=True)


@given('I am project member with write permission')
def membership_with_write_permission(user, project):
    create_membership(project, user, has_write_permission=True)


@given('I am project member with read permission')
def membership_with_read_permission(user, project):
    create_membership(project, user)


@when('I try to create a project consent', target_fixture='request_result')
def create_project_consent(client, project, paragraph):
    return client.post(
        reverse('projectconsent-list', kwargs=dict(project_pk=project.pk)),
        data=dict(text_fragments=[paragraph]),
        format='json'
    )


@when('I try to create a project consent category', target_fixture='request_result')
def create_project_consent_category(client, text_fragments):
    return client.post(
        reverse('projectconsentcategory-list'),
        data=dict(name='foobar', template_text_fragments=text_fragments),
        format='json'
    )


@when('I try to delete a project consent', target_fixture='request_result')
def delete_project_consent(client, project, project_consent):
    return client.delete(
        reverse('projectconsent-detail', kwargs=dict(project_pk=project.pk, pk=project_consent.pk))
    )


@when('I try to delete a project consent category', target_fixture='request_result')
def delete_project_consent_category(client, project_consent_category):
    return client.delete(
        reverse('projectconsentcategory-detail', kwargs=dict(pk=project_consent_category.pk))
    )


@when('I try to list project consents', target_fixture='request_result')
def list_project_consents(client, project):
    return client.get(reverse('projectconsent-list', kwargs=dict(project_pk=project.pk)))


@when('I try to list project consent categories', target_fixture='request_result')
def list_project_consent_categories(client):
    return client.get(reverse('projectconsentcategory-list'))


@when('I try to patch a project consent category', target_fixture='request_result')
def partial_update_project_consent_category(client, project_consent_category):
    return client.patch(
        reverse('projectconsentcategory-detail', kwargs=dict(pk=project_consent_category.pk))
    )


@when('I try to partial update a project consent', target_fixture='request_result')
def partial_update_project_consent(client, project, project_consent, checkbox):
    return client.patch(
        reverse('projectconsent-detail', kwargs=dict(project_pk=project.pk, pk=project_consent.pk)),
        data=dict(text_fragments=[checkbox]),
        format='json'
    )


@when('I try to retrieve a project consent', target_fixture='request_result')
def retrieve_project_consent(client, project, project_consent):
    return client.get(
        reverse('projectconsent-detail', kwargs=dict(project_pk=project.pk, pk=project_consent.pk))
    )


@when('I try to retrieve a project consent category', target_fixture='request_result')
def retrieve_project_consent_category(client, project_consent_category):
    return client.get(
        reverse('projectconsentcategory-detail', kwargs=dict(pk=project_consent_category.pk))
    )


@when('I try to update a project consent', target_fixture='request_result')
def update_project_consent(client, project, project_consent, paragraph):
    return client.put(
        reverse('projectconsent-detail', kwargs=dict(project_pk=project.pk, pk=project_consent.pk)),
        data=dict(text_fragments=[paragraph]),
        format='json'
    )


@when('I try to update a project consent category', target_fixture='request_result')
def update_project_consent_category(client, project_consent_category):
    return client.put(
        reverse('projectconsentcategory-detail', kwargs=dict(pk=project_consent_category.pk)),
        data=dict(
            name='new name',
            template_text_fragments=project_consent_category.template_text_fragments,
        ),
        format='json'
    )


@then(parsers.parse('I get status code {status_code:d}'))
def assert_status_code(request_result, status_code):
    assert request_result.status_code == status_code, request_result.content
