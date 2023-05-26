from django.test import TestCase, Client
from django.contrib.sessions.backends.db import SessionStore
from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User
from .models import Catalog, File, Section, SectionStatusData
from django.db.models import QuerySet
from django.urls import reverse


class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.catalog = Catalog.objects.create(name='Test Catalog', user=self.user)
        self.file = File.objects.create(name='Test File', catalog=self.catalog)
        self.section_status_data = SectionStatusData.objects.create(info='Test Info')

    def test_catalog_deletion(self):
        catalog = Catalog.objects.get(name='Test Catalog')
        catalog.delete()
        self.assertTrue(catalog.is_deleted)
        self.assertIsNotNone(catalog.deleted_at)

        # Ensure associated files and nested catalogs are also deleted
        self.assertFalse(File.objects.filter(catalog=catalog).exists())
        self.assertFalse(Catalog.objects.filter(parent=catalog).exists())

    def test_file_creation(self):
        file = File.objects.create(name='New File', catalog=self.catalog, user=self.user)
        self.assertEqual(file.name, 'New File')
        self.assertEqual(file.catalog, self.catalog)
        self.assertEqual(file.user, self.user)

    def test_section_creation(self):
        section = Section.objects.create(
            name='Test Section',
            user=self.user,
            start_line=1,
            end_line=10,
            section_type='prc',
            section_status='ok',
            section_status_data=self.section_status_data,
            file=self.file
        )
        self.assertEqual(section.name, 'Test Section')
        self.assertEqual(section.user, self.user)
        self.assertEqual(section.file, self.file)

    def test_return_nested_objects(self):
        catalogs = self.catalog.return_nested_objects()[0]
        files = self.catalog.return_nested_objects()[1]

        self.assertTrue(isinstance(catalogs, QuerySet))
        self.assertTrue(isinstance(files, QuerySet))

    def test_section_status_data_creation(self):
        section_status_data = SectionStatusData.objects.create(info='New Info')
        self.assertEqual(section_status_data.info, 'New Info')


from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Catalog, File
from datetime import datetime

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.catalog = Catalog.objects.create(name='Test Catalog', user=self.user)
        self.file = File.objects.create(name='Test File', catalog=self.catalog, user=self.user)

    def test_index_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('compilerapp:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_add_catalog_view_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('compilerapp:add_catalog'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_catalog.html')

    def test_add_catalog_view_post(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('compilerapp:add_catalog'), {
            'catalog_name': 'New Catalog',
            'catalog_description': 'Catalog Description',
            'parent_catalog': self.catalog.id
        })
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertEqual(Catalog.objects.count(), 2)  # Check if a new catalog was created

    def test_add_file_view_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('compilerapp:add_file'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_file.html')

    def test_add_file_view_post(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('compilerapp:add_file'), {
            'file_name': 'New File',
            'file_description': 'File Description',
            'parent_catalog': self.catalog.id,
            'file_content': 'File Content'
        })
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertEqual(File.objects.count(), 2)  # Check if a new file was created

    def test_delete_file_view_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('compilerapp:delete_file'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_file.html')

    def test_delete_file_view_post(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('compilerapp:delete_file'), {
            'file_to_delete': self.file.id
        })
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.file.refresh_from_db()
        self.assertTrue(self.file.is_deleted)
        self.assertIsNotNone(self.file.deleted_at)

    def test_delete_catalog_view_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('compilerapp:delete_catalog'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_catalog.html')

    def test_delete_catalog_view_post(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('compilerapp:delete_catalog'), {
            'catalog_to_delete': self.catalog.id
        })
        self.assertEqual(response.status_code, 302)  # Redirect status code

    def tearDown(self):
        Catalog.objects.all().delete()
        File.objects.all().delete()
        self.user.delete()

    def test_compile_view(self):
        self.client.login(username='testuser', password='testpassword')
        session = self.client.session
        session['standard'] = 'c89'
        session['selected_optymalizations'] = ['opt1', 'opt2']
        session['file_id'] = 1
        session['procesor'] = 'procesor1'
        session['procesor_options'] = ['option1', 'option2']
        session.save()

        response = self.client.post(reverse('compilerapp:compile'))

        self.assertEqual(response.status_code, 200)
        # Add more assertions based on the expected behavior of the view

    def test_compile_and_save_view(self):
        self.client.login(username='testuser', password='testpassword')
        session = self.client.session
        session['standard'] = 'c89'
        session['selected_optymalizations'] = ['opt1', 'opt2']
        session['file_id'] = 1
        session['procesor'] = 'procesor1'
        session['procesor_options'] = ['option1', 'option2']
        session.save()

        response = self.client.get(reverse('compilerapp:compile_and_save'))

        self.assertEqual(response.status_code, 200)