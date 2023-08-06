import uuid

from drb.nodes.logical_node import DrbLogicalNode
import os
import unittest
import drb.topics.resolver as topic_resolver
from drb.metadata import DrbMetadataResolver
from drb.topics.dao import ManagerDao


class TestMetadataResolver(unittest.TestCase):
    resource_dir = None
    resolver = None

    @classmethod
    def setUpClass(cls) -> None:
        test_dir = os.path.join(os.path.dirname(__file__))
        cls.resource_dir = os.path.join(test_dir, 'resources')
        cls.resolver = DrbMetadataResolver()

    def test_resolver_metadata(self):
        prd = 'S1A_IW_SLC__1SDV_20200801T101915_20200801T101942_033712_' \
              '03E840_2339.SAFE'
        node = DrbLogicalNode(os.path.join(self.resource_dir, prd))
        node = topic_resolver.create(node)
        metadata = self.resolver.get_metadata(node)
        self.assertEqual(7, len(metadata.keys()))
        self.assertEqual('Sentinel-1', metadata['platformName'].extract(node))
        self.assertEqual('SLC', metadata['productType'].extract(node))

        prd = 'S1A_RF_RAW__0SDH_20140513T012339_20140513T012340_000572_' \
              '000747_31E3.SAFE'
        node = DrbLogicalNode(os.path.join(self.resource_dir, prd))
        node = topic_resolver.create(node)
        metadata = self.resolver.get_metadata(node)
        self.assertEqual(8, len(metadata.keys()))
        self.assertEqual('Sentinel-1', metadata['platformName'].extract(node))
        self.assertEqual('RAW', metadata['productType'].extract(node))
        self.assertEqual('BAQ_5_BIT',
                         metadata['noiseCompressionType'].extract(node))

    def test_metadata(self):
        prd = 'S1A_IW_SLC__1SDV_20200801T101915_20200801T101942_033712_' \
              '03E840_2339.SAFE'
        path = os.path.join(self.resource_dir, prd)
        file_topic_id = uuid.UUID('99e6ce18-276f-11ec-9621-0242ac130002')
        topic = ManagerDao().get_drb_topic(file_topic_id)
        node = topic_resolver.create(path)
        metadata = self.resolver.get_metadata(node, topic=topic)
        self.assertEqual(1, len(metadata.keys()))
        self.assertEqual(True, metadata.get('isDirectory').extract(node))
