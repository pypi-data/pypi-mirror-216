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

import requests

from hugegraph.constants import Graph
from hugegraph.manager.gremlin_manager import GremlinManager
from hugegraph.utils.exceptions import NotFoundError
from hugegraph.manager.schema_manager import SchemaManager
from hugegraph.manager.graph_manager import GraphManager
from hugegraph.manager.common import HugeGraphBase
from hugegraph.utils.util import authorized


class PyHugeGraph(HugeGraphBase):
    def __init__(self, ip, port, graph, user, pwd, timeout=10):
        super().__init__(ip, port, graph, user, pwd, timeout)
        self._schema = None
        self._graph = None
        self._gremlin = None

    def schema(self):
        if self._schema:
            return self._schema
        self._schema = SchemaManager(self._ip, self._port, self._graph_name, self._user, self._pwd, self._timeout)
        return self._schema

    def gremlin(self):
        if self._gremlin:
            return self._gremlin
        self._gremlin = GremlinManager(self._ip, self._port, self._graph_name, self._user, self._pwd, self._timeout)
        return self._gremlin

    def graph(self):
        if self._graph:
            return self._graph
        self._graph = GraphManager(self._ip, self._port, self._graph_name, self._user, self._pwd, self._timeout)
        return self._graph

    def get_all_graphs(self):
        url = self._host + "/graphs"
        res = requests.get(url, auth=self._auth, headers=self._headers)
        if res.status_code == 200 and authorized(res):
            return str(res.content)
        else:
            raise NotFoundError(res.content)

    def get_version(self):
        url = self._host + "/versions"
        res = requests.get(url, auth=self._auth, headers=self._headers)
        if res.status_code == 200 and authorized(res):
            return str(res.content)
        else:
            raise NotFoundError(res.content)

    def get_graphinfo(self):
        url = self._host + "/graphs" + "/" + self._graph_name
        res = requests.get(url, auth=self._auth, headers=self._headers)
        if res.status_code == 200 and authorized(res):
            return str(res.content)
        else:
            raise NotFoundError(res.content)

    def clear_graph_all_data(self):
        url = self._host + "/graphs" + "/" + self._graph_name + "/clear?" + \
              "confirm_message=" + Graph.CONFORM_MESSAGE
        res = requests.delete(url, auth=self._auth, headers=self._headers)
        if res.status_code == 200 and authorized(res):
            return str(res.content)
        else:
            raise NotFoundError(res.content)

    def get_graph_config(self):
        url = self._host + "/graphs" + "/" + self._graph_name + "/conf"
        res = requests.get(url, auth=self._auth, headers=self._headers)
        if res.status_code == 200 and authorized(res):
            return str(res.content)
        else:
            raise NotFoundError(res.content)
