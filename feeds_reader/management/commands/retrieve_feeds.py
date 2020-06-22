"""
This command retrieve feeds by urls which separated by commas.
"""
from django.core.management.base import BaseCommand

from feeds_reader.constants import MAX_ENTRIES_SAVED
from feeds_reader.models import Feed, Entry
from feeds_reader.feed_aggregator import retrieve_feed

import logging

logger = logging.getLogger('feeds_reader')


class Command(BaseCommand):
    help = 'Retrieve feed items by urls.'

    def add_arguments(self, parser):
        """
        Add named (optional) argument
        """
        parser.add_argument('urls', nargs='+',
                            help='List of xml urls to be retrieved feeds')
        parser.add_argument('--verbose', action='store_true', dest='verbose', default=False,
                            help='Print progress on command line')

    def handle(self, *args, **options):
        """
        Read through all the feeds urls looking for new entries.
        """
        verbose = options['verbose']
        feeds = options['urls']
        logger.info(type(feeds))
        logger.info(feeds)
        num_feeds = len(feeds)

        if verbose:
            logger.info('{} feeds to process'.format(num_feeds))

        for i, feed in enumerate(feeds):
            if verbose:
                logger.info('({0}/{1}) Processing Feed {2}'.format(i + 1, num_feeds, feed.title))

            retrieve_feed(feed, verbose)

            # Remove older entries
            entries = Entry.objects.filter(feed__xml_url=feed)[MAX_ENTRIES_SAVED:]

            for entry in entries:
                entry.delete()

            if verbose:
                logger.info('Deleted {} entries from feed {}'.format(len(entries), feed.title))

        logger.info('Feeds Reader retrieve_feeds completed successfully!')
