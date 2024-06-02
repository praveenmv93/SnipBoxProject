from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Snippet, Tag


# Create your tests here.


class SnippetViewSetTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_create_snippet(self):
        url = reverse('snippet-list')
        data = {'title': 'Test Snippet', 'note': 'This is a test snippet.', 'tags': [{'tag_title': 'test_tag'}]}

        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Snippet.objects.count(), 1)
        self.assertEqual(Snippet.objects.get().title, 'Test Snippet')

    def test_get_queryset(self):
        Snippet.objects.create(title='Test Snippet', note='This is a test snippet.', created_by=self.user)
        url = reverse('snippet-list')
        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['snippets']), 1)
        self.assertEqual(response.data['snippets'][0]['title'], 'Test Snippet')
        self.assertEqual(response.data['snippets'][0]['created_by'], self.user.id)

    def test_create_snippet_unauthenticated(self):
        url = reverse('snippet-list')
        data = {'title': 'Test Snippet', 'note': 'This is a test snippet.'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_snippet(self):
        snippet = Snippet.objects.create(title='Test Snippet', note='This is a test snippet.', created_by=self.user)
        url = reverse('snippet-detail', args=[snippet.id])

        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['snippet']['title'], 'Test Snippet')

    def test_retrieve_nonexistent_snippet(self):
        url = reverse('snippet-detail', args=[999])

        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_update_snippet(self):
        snippet = Snippet.objects.create(title='Test Snippet', note='This is a test snippet.', created_by=self.user)
        url = reverse('snippet-detail', args=[snippet.id])
        data = {'title': 'Updated Title', 'note': 'Updated note.', "tags": [
            {"tag_title": "u Tag 4"}
        ]}

        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Snippet.objects.get().title, 'Updated Title')

    def test_delete_snippet(self):
        snippet = Snippet.objects.create(title='Test Snippet', note='This is a test snippet.', created_by=self.user)
        url = reverse('snippet-detail', args=[snippet.id])

        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Snippet.objects.filter(id=snippet.id).exists())

    def test_list_snippets(self):
        Snippet.objects.create(title='Test Snippet', note='This is a test snippet.', created_by=self.user)
        url = reverse('snippet-list')

        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['snippets']), 1)

    def test_list_snippets_empty(self):
        url = reverse('snippet-list')

        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['snippets']), 0)

    def test_overview_snippets(self):
        Snippet.objects.create(title='Test Snippet', note='This is a test snippet.', created_by=self.user)
        url = reverse('snippet-overview')

        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_count'], 1)

class TagViewSetTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_list_tags(self):
        Tag.objects.create(tag_title='Test Tag')
        url = reverse('tag-list')
        self.client.force_authenticate(user=self.user)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_snippets_for_tag_with_snippets(self):
        tag = Tag.objects.create(tag_title='Test Tag')
        snippet = Snippet.objects.create(title='Test Snippet', note='This is a test snippet.', created_by=self.user)
        snippet.tags.add(tag)  # Correct way to associate tags with the snippet

        self.client.force_authenticate(user=self.user)

        url = reverse('tag-snippets', args=[tag.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], f'Snippets found for tag "{tag.tag_title}".')

    def test_snippets_for_tag_without_snippets(self):
        tag = Tag.objects.create(tag_title='Test Tag')
        self.client.force_authenticate(user=self.user)

        url = reverse('tag-snippets', args=[tag.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], f'No snippets found for tag "{tag.tag_title}".')

    def test_snippets_for_nonexistent_tag(self):
        url = reverse('tag-snippets', args=[999])
        self.client.force_authenticate(user=self.user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data['message'], 'An error occurred: No Tag matches the given query.')

    def test_create_tag_unauthenticated(self):
        url = reverse('tag-list')
        data = {'tag_title': 'Test Tag'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_method_not_allowed(self):
        Tag.objects.create(tag_title='Test Tag')
        url = reverse('tag-list')
        data = {'tag_title': 'Test Tag'}

        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_retrieve_tag(self):
        tag = Tag.objects.create(tag_title='Test Tag')
        url = reverse('tag-detail', args=[tag.id])

        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['tag_title'], 'Test Tag')

    def test_retrieve_nonexistent_tag(self):
        url = reverse('tag-detail', args=[999])

        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
