# -*- coding: utf-8 -*-

"""Testing for CX and NDEx import/export."""

import logging
import os
import time
import unittest

import networkx as nx

from pybel import from_path
from pybel.constants import *
from pybel.io.ndex_utils import NDEX_PASSWORD, NDEX_USERNAME
from pybel.testing.cases import TemporaryCacheClsMixin
from pybel.testing.constants import test_bel_slushy, test_bel_thorough
from pybel.testing.mocks import mock_bel_resources
from pybel.utils import hash_node
from pybel_cx import from_cx, from_cx_jsons, from_ndex, to_cx, to_cx_jsons, to_ndex
from tests.constants import BelReconstitutionMixin

logging.getLogger('requests').setLevel(logging.WARNING)
log = logging.getLogger(__name__)


def do_remapping(original, reconstituted):
    """Remap nodes to use the reconstitution tests.
    
    :param BELGraph original: The original bel graph 
    :param BELGraph reconstituted: The reconstituted BEL graph from CX input/output
    """
    node_mapping = dict(enumerate(sorted(original, key=hash_node)))
    try:
        nx.relabel.relabel_nodes(reconstituted, node_mapping, copy=False)
    except KeyError as e:
        missing_nodes = set(node_mapping) - set(reconstituted)
        log.exception('missing %s', [node_mapping[n] for n in missing_nodes])
        raise e


class TestInterchange(TemporaryCacheClsMixin, BelReconstitutionMixin):
    """A test case for CX and NDEx import/export."""

    @classmethod
    def setUpClass(cls):
        """Set up a class with example graphs."""
        super(TestInterchange, cls).setUpClass()

        with mock_bel_resources:
            cls.thorough_graph = from_path(test_bel_thorough, manager=cls.manager, allow_nested=True)
            cls.slushy_graph = from_path(test_bel_slushy, manager=cls.manager)

    def test_thorough_cx(self):
        """Test the round trip on CX output with the thorough graph."""
        reconstituted = from_cx(to_cx(self.thorough_graph))
        do_remapping(self.thorough_graph, reconstituted)
        self.bel_thorough_reconstituted(reconstituted, check_warnings=False)

    def test_thorough_cxs(self):
        """Test the round trip on CX string output with the thorough graph."""
        reconstituted = from_cx_jsons(to_cx_jsons(self.thorough_graph))
        do_remapping(self.thorough_graph, reconstituted)
        self.bel_thorough_reconstituted(reconstituted, check_warnings=False)

    @unittest.skipUnless(NDEX_USERNAME in os.environ and NDEX_PASSWORD in os.environ, 'Need NDEx credentials')
    def test_thorough_ndex(self):
        """Test that a document can be uploaded and downloaded.

        This test sleeps in the middle so that NDEx can process."""
        network_id = to_ndex(self.thorough_graph)
        time.sleep(10)
        reconstituted = from_ndex(network_id)

        do_remapping(self.thorough_graph, reconstituted)

        self.bel_thorough_reconstituted(reconstituted, check_warnings=False, check_citation_name=False)

    def test_slushy_cx(self):
        """Test the round trip on CX output with the slushy graph."""
        reconstituted = from_cx(to_cx(self.slushy_graph))
        do_remapping(self.slushy_graph, reconstituted)
        self.bel_slushy_reconstituted(reconstituted)

    def test_slushy_cxs(self):
        """Test the round trip on CX string output with the slushy graph."""
        reconstituted = from_cx_jsons(to_cx_jsons(self.slushy_graph))
        do_remapping(self.slushy_graph, reconstituted)
        self.bel_slushy_reconstituted(reconstituted)


if __name__ == '__main__':
    unittest.main()
