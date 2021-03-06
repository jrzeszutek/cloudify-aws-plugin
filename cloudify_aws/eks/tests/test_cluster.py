# Copyright (c) 2018 Cloudify Platform Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Standard imports
import unittest

# Third party imports
from mock import patch, MagicMock

# Local imports
from cloudify_aws.common._compat import reload_module
from cloudify_aws.common.tests.test_base import (
    TestBase,
    mock_decorator
)
from cloudify_aws.eks.resources.cluster import EKSCluster
from cloudify_aws.eks.resources import cluster
from cloudify_aws.common import constants


class TestEKSCluster(TestBase):

    def setUp(self):
        super(TestEKSCluster, self).setUp()

        self.cluster = EKSCluster("ctx_node", resource_id=True,
                                  client=True, logger=None)
        self.mock_resource = patch(
            'cloudify_aws.common.decorators.aws_resource', mock_decorator
        )
        self.mock_resource.start()
        reload_module(cluster)

    def tearDown(self):
        self.mock_resource.stop()

        super(TestEKSCluster, self).tearDown()

    def test_class_properties(self):
        effect = self.get_client_error_exception(name=cluster.RESOURCE_TYPE)
        self.cluster.client = self.make_client_function('describe_cluster',
                                                        side_effect=effect)
        self.assertIsNone(self.cluster.properties)

        response = \
            {
                cluster.CLUSTER:
                    {
                        'arn': 'test_cluster_arn',
                        'name': 'test_cluster_name',
                        'status': 'test_status',
                    },
            }

        self.cluster.describe_param = {
            cluster.CLUSTER_NAME: 'test_cluster_name'
        }
        self.cluster.client = self.make_client_function('describe_cluster',
                                                        return_value=response)

        self.assertEqual(
            self.cluster.properties[cluster.CLUSTER_NAME],
            'test_cluster_name'
        )

    def test_class_status(self):
        response = {
            cluster.CLUSTER: {
                'arn': 'test_cluster_arn',
                'name': 'test_cluster_name',
                'status': 'test_status',
            },
        }
        self.cluster.client = self.make_client_function('describe_cluster',
                                                        return_value=response)

        self.assertEqual(self.cluster.status, 'test_status')

    def test_class_status_empty(self):
        response = {cluster.CLUSTER: {}}
        self.cluster.client = self.make_client_function('describe_cluster',
                                                        return_value=response)

        self.assertIsNone(self.cluster.status)

    def test_class_create(self):
        params = {cluster.CLUSTER_NAME: 'test_cluster_name'}
        response = \
            {
                cluster.CLUSTER: {
                    'arn': 'test_cluster_arn',
                    'name': 'test_cluster_name',
                    'status': 'test_status',
                },
            }
        self.cluster.client = self.make_client_function(
            'create_cluster', return_value=response)

        self.assertEqual(
            self.cluster.create(params)[cluster.CLUSTER],
            response.get(cluster.CLUSTER))

    def test_class_delete(self):
        params = {cluster.CLUSTER: 'test_cluster_name'}
        response = \
            {
                cluster.CLUSTER: {
                    'arn': 'test_cluster_arn',
                    'name': 'test_cluster_name',
                    'status': 'test_status',
                },
            }

        self.cluster.client = self.make_client_function(
            'delete_cluster', return_value=response)

        self.assertEqual(self.cluster.delete(params), response)

    def test_prepare(self):
        ctx = self.get_mock_ctx("Cluster")
        cluster.prepare(ctx, 'config')
        self.assertEqual(
            ctx.instance.runtime_properties['resource_config'],
            'config')

    def test_create(self):
        ctx = self.get_mock_ctx("Cluster")
        config = {cluster.CLUSTER_NAME: 'test_cluster_name'}
        ctx.node.properties['store_kube_config_in_runtime'] = False
        iface = MagicMock()
        response = \
            {
                cluster.CLUSTER: {
                    'arn': 'test_cluster_arn',
                    'name': 'test_cluster_name',
                    'status': 'test_status',
                },
            }

        iface.create = self.mock_return(response)
        cluster.create(ctx, iface, config)
        self.assertEqual(
            ctx.instance.runtime_properties[constants.EXTERNAL_RESOURCE_ID],
            'test_cluster_name'
        )

    def test_delete(self):
        ctx = self.get_mock_ctx("Cluster")
        iface = MagicMock()
        cluster.delete(ctx, iface, {})
        self.assertTrue(iface.delete.called)


if __name__ == '__main__':
    unittest.main()
