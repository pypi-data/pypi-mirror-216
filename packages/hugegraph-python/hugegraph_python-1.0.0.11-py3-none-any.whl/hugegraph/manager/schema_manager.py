# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.


import json

import requests

from hugegraph.models.property_key_data import PropertyKeyData
from hugegraph.models.edge_label_data import EdgeLabelData
from hugegraph.models.index_label_data import IndexLabelData
from hugegraph.models.vertex_label_data import VertexLabelData

from hugegraph.manager.common import HugeGraphBase
from hugegraph.manager.schema.property_key import PropertyKey
from hugegraph.manager.schema.edge_label import EdgeLabel
from hugegraph.manager.schema.vertex_label import VertexLabel
from hugegraph.manager.schema.index_label import IndexLabel
from hugegraph.utils.exceptions import NotFoundError
from hugegraph.utils.util import authorized


class SchemaManager(HugeGraphBase):
    def __init__(self, ip, port, graph_name, user, pwd, timeout):
        super().__init__(ip, port, graph_name, user, pwd, timeout)

    def propertyKey(self, property_name):
        property_key = PropertyKey(self._ip, self._port, self._graph_name, self._user, self._pwd, self._timeout)
        property_key.create_parameter_holder()
        property_key.add_parameter("name", property_name)
        property_key.add_parameter("not_exist", True)
        return property_key

    def getPropertyKey(self, property_name):
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/propertykeys" \
              + "/" + property_name
        response = requests.get(url)
        if response.status_code == 200 and authorized(response):
            property_keys_data = PropertyKeyData(json.loads(response.content))
            return property_keys_data
        else:
            raise NotFoundError("PorpertyKey not found: {}".format(response.content))

    def getPropertyKeys(self):
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/propertykeys"
        response = requests.get(url)
        res = []
        if authorized(response):
            for item in json.loads(response.content)["propertykeys"]:
                res.append(PropertyKeyData(item))
            return res

    def vertexLabel(self, vertex_name):
        vertex_label = VertexLabel(self._ip, self._port, self._graph_name, self._user, self._pwd, self._timeout)
        vertex_label.create_parameter_holder()
        vertex_label.add_parameter("name", vertex_name)
        # vertex_label.add_parameter("id_strategy", "AUTOMATIC")
        vertex_label.add_parameter("not_exist", True)
        return vertex_label

    def getVertexLabel(self, name):
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/vertexlabels/" + name
        response = requests.get(url, auth=self._auth, headers=self._headers)
        if response.status_code == 200 and authorized(response):
            res = VertexLabelData(json.loads(response.content))
            return res
        else:
            raise NotFoundError("VertexLabel not found: {}".format(response.content))

    def getVertexLabels(self):
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/vertexlabels/"
        response = requests.get(url, auth=self._auth, headers=self._headers)
        res = []
        if authorized(response):
            for item in json.loads(response.content)["vertexlabels"]:
                res.append(VertexLabelData(item))
            return res

    def edgeLabel(self, name):
        edge_label = EdgeLabel(self._ip, self._port, self._graph_name, self._user, self._pwd, self._timeout)
        edge_label.create_parameter_holder()
        edge_label.add_parameter("name", name)
        edge_label.add_parameter("not_exist", True)
        return edge_label

    def getEdgeLabel(self, label_name):
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/edgelabels" + "/" + label_name
        response = requests.get(url, auth=self._auth, headers=self._headers)
        if response.status_code == 200 and authorized(response):
            res = EdgeLabelData(json.loads(response.content))
            return res
        else:
            raise NotFoundError("EdgeLabel not found: {}".format(response.content))

    def getEdgeLabels(self):
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/edgelabels"
        response = requests.get(url, auth=self._auth, headers=self._headers)
        res = []
        if authorized(response):
            for item in json.loads(response.content)["edgelabels"]:
                res.append(EdgeLabelData(item))
            return res

    def indexLabel(self, name):
        index_label = IndexLabel(self._ip, self._port, self._graph_name, self._user, self._pwd, self._timeout)
        index_label.create_parameter_holder()
        index_label.add_parameter("name", name)
        return index_label

    def getIndexLabel(self, name):
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/indexlabels" + "/" + name
        response = requests.get(url, auth=self._auth, headers=self._headers)
        if response.status_code == 200 and authorized(response):
            res = IndexLabelData(json.loads(response.content))
            return res
        else:
            raise NotFoundError("IndexLabel not found: {}".format(response.content))

    def getIndexLabels(self):
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/indexlabels"
        response = requests.get(url, auth=self._auth, headers=self._headers)
        res = []
        if authorized(response):
            for item in json.loads(response.content)['indexlabels']:
                res.append(IndexLabelData(item))
            return res
