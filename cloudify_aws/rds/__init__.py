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
'''
    RDS
    ~~~
    AWS RDS base interface
'''
# Cloudify AWS
from cloudify_aws.common import AWSResourceBase
from cloudify_aws.common.connection import Boto3Connection
from cloudify_aws.common.constants import AWS_CONFIG_PROPERTY
from cloudify_aws.common.utils import check_region_name

# pylint: disable=R0903


class RDSBase(AWSResourceBase):
    '''
        AWS RDS base interface
    '''
    def __init__(self, ctx_node, resource_id=None, client=None, logger=None):
        if not client:
            aws_config = ctx_node.properties.get(AWS_CONFIG_PROPERTY, dict())
            check_region_name(aws_config['region_name'])

        AWSResourceBase.__init__(
            self, client or Boto3Connection(ctx_node).client('rds'),
            resource_id=resource_id, logger=logger)

    @property
    def properties(self):
        '''Gets the properties of an external resource'''
        raise NotImplementedError()

    @property
    def status(self):
        '''Gets the status of an external resource'''
        raise NotImplementedError()

    def create(self, params):
        '''Creates a resource'''
        raise NotImplementedError()

    def delete(self, params=None):
        '''Deletes a resource'''
        raise NotImplementedError()
