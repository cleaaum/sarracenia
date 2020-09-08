import sarra.moth
import copy
from sarra.flow import Flow
import logging

logger = logging.getLogger(__name__)

default_options = {'accept_unmatched': True, 'suppress_duplicates': 0}


class Report(Flow):
    @classmethod
    def assimilate(cls, obj):
        obj.__class__ = Report

    def name(self):
        return 'report'

    def __init__(self):

        self.plugins['load'].append('sarra.plugin.gather.message.Message')

        if hasattr(self.o, 'post_exchange'):
            self.plugins['load'].append('sarra.plugin.post.message.Message')

        Report.assimilate(self)
