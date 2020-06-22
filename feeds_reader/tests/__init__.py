"""feeds_reader Unit Test."""
from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth import get_user_model

from ..factories import GroupFactory, FeedFactory, EntryFactory
from ..models import Options
from ..spl_test_server import (PORT, setUpModule as server_setup, tearDownModule as server_teardown)

from mock import patch

def setUpModule():
    server_setup()


def tearDownModule():
    server_teardown()


class WorkingURLsTest(TestCase):
    """
    Visit various URLs in feeds_reader to ensure they are working.
    """

    def setUp(self):
        """Create data and login"""
        entry = EntryFactory.create()
        group = GroupFactory.create()
        feed = FeedFactory.create()
        feed.xml_url = 'http://localhost:%s/test/feed' % PORT
        feed.group = group
        feed.save()

        self.user = get_user_model().objects.create_user('thao', 'ardtimeit@gmail.com', 'password123')
        self.user.is_staff = True
        self.user.save()
        self.client = Client()
        self.client.login(username='thao', password='password123')


class TestRetrieveFeedsCommand(TestCase):
    """
    Test the command which polls the feeds.
    """

    def setUp(self):
        """Create data"""
        entry = EntryFactory.create()
        group = GroupFactory.create()
        feed = FeedFactory.create()
        feed.xml_url = 'http://localhost:%s/test/feed' % PORT
        feed.group = group
        feed.save()

    def test_retrieve_feeds(self):
        """Test retrieve_feeds command."""
        args = []
        opts = {'verbose': True}

        # Ensure some Entries are deleted
        feeds_reader_options = Options.manager.get_options()
        feeds_reader_options.max_entries_saved = 1
        feeds_reader_options.save()
        with patch('sys.stdout', new=StringIO()):  # Suppress printed output from test
            call_command('retrieve_feeds', *args, **opts)

        # Default Options created if none are found
        Options.objects.all().delete()
        with patch('sys.stdout', new=StringIO()):  # Suppress printed output from test
            call_command('retrieve_feeds', *args, **opts)
