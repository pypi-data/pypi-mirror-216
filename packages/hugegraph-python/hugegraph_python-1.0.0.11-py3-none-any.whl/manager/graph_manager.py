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

from hugegraph.utils.huge_requests import HugeSession
from hugegraph.manager.common import HugeGraphBase
from hugegraph.models.vertex_data import VertexData
from hugegraph.models.edge_data import EdgeData
from hugegraph.utils.exceptions import NotFoundError, CreateError, RemoveError, UpdateError
from hugegraph.utils.util import create_exception, authorized


class GraphManager(HugeGraphBase):
    def __init__(self, ip, port, graph_name, user, pwd, timeout):
        super().__init__(ip, port, graph_name, user, pwd, timeout)
        self.session = None
        self.set_session(HugeSession.new_session())

    def set_session(self, session):
        self.session = session

    def close_session(self):
        if self.session:
            self.session.close()

    def close(self):
        self.close_session()

    def addVertex(self, label, properties):
        data = dict()
        data['label'] = label
        data["properties"] = properties
        url = self._host + "/graphs" + "/" + self._graph_name + "/graph/vertices"
        response = self.session.post(url, data=json.dumps(data), auth=self._auth,
                                     headers=self._headers, timeout=self._timeout)
        if response.status_code == 201 and authorized(response):
            res = VertexData(json.loads(response.content))
            return res
        else:
            raise CreateError("create vertex failed: {}".format(response.content))

    def addVertices(self, input_data):
        url = self._host + "/graphs" + "/" + self._graph_name + "/graph/vertices/batch"
        data = []
        for item in input_data:
            data.append({'label': item[0], 'properties': item[1]})
        response = self.session.post(url, data=json.dumps(data), auth=self._auth,
                                     headers=self._headers, timeout=self._timeout)
        if response.status_code == 201 and authorized(response):
            res = []
            for item in json.loads(response.content):
                res.append(VertexData({"id": item}))
            return res
        else:
            raise CreateError("create vertexes failed: {}".format(response.content))

    def appendVertex(self, vertex_id, properties):
        url = self._host + "/graphs" + "/" + self._graph_name \
              + "/graph/vertices/\"" + vertex_id + "\"?action=append"
        data = {
            "properties": properties
        }
        response = self.session.put(url, data=json.dumps(data), auth=self._auth,
                                    headers=self._headers, timeout=self._timeout)
        if response.status_code == 200 and authorized(response):
            res = VertexData(json.loads(response.content))
            return res
        else:
            raise UpdateError("append vertex failed: {}".format(response.content))

    def eliminateVertex(self, vertex_id, properties):
        url = self._host + "/graphs" + "/" + self._graph_name \
              + "/graph/vertices/\"" + vertex_id + "\"?action=eliminate"
        data = {
            "properties": properties
        }
        response = self.session.put(url, data=json.dumps(data), auth=self._auth, headers=self._headers, timeout=self._timeout)
        if response.status_code == 200 and authorized(response):
            res = VertexData(json.loads(response.content))
            return res
        else:
            raise UpdateError("eliminate vertex failed: {}".format(response.content))

    def getVertexById(self, vertex_id):
        url = self._host + "/graphs" + "/" + self._graph_name + "/graph/vertices/\"" + vertex_id + "\""
        response = self.session.get(url, auth=self._auth, headers=self._headers, timeout=self._timeout)
        if response.status_code == 200 and authorized(response):
            res = VertexData(json.loads(response.content))
            return res
        else:
            raise NotFoundError("Vertex not found: {}".format(response.content))

    def getVertexByPage(self, label, limit, page, properties=None):
        url = self._host + "/graphs" + "/" + self._graph_name + "/graph/vertices?"
        para = ""
        para = para + "&label=" + label
        if properties:
            para = para + "&properties=" + json.dumps(properties)
        if page:
            para += '&page={}'.format(page)
        else:
            para += '&page'
        para = para + "&limit=" + str(limit)
        url = url + para[1:]
        response = self.session.get(url, auth=self._auth, headers=self._headers, timeout=self._timeout)
        if response.status_code == 200 and authorized(response):
            res = []
            for item in json.loads(response.content)["vertices"]:
                res.append(VertexData(item))
            next_page = json.loads(response.content)["page"]
            return res, next_page
        else:
            raise NotFoundError("Vertex not found: {}".format(response.content))

    def getVertexByCondition(self, label="",  limit=0, page='', properties=None):
        url = self._host + "/graphs" + "/" + self._graph_name + "/graph/vertices?"
        para = ""
        if label:
            para = para + "&label=" + label
        if properties:
            para = para + "&properties=" + json.dumps(properties)
        if limit > 0:
            para = para + "&limit=" + str(limit)
        if page:
            para += '&page={}'.format(page)
        else:
            para += '&page'
        url = url + para[1:]
        response = self.session.get(url, auth=self._auth, headers=self._headers, timeout=self._timeout)
        if response.status_code == 200 and authorized(response):
            res = []
            for item in json.loads(response.content)["vertices"]:
                res.append(VertexData(item))
            return res
        else:
            raise NotFoundError("Vertex not found: {}".format(response.content))

    def removeVertexById(self, vertex_id):
        url = self._host + "/graphs" + "/" + self._graph_name + "/graph/vertices/\"" + vertex_id + "\""
        response = self.session.delete(url, auth=self._auth, headers=self._headers, timeout=self._timeout)
        if response.status_code == 204 and authorized(response):
            return response.content
        else:
            raise RemoveError("remove vertex failed: {}".format(response.content))

    def addEdge(self, edge_label, out_id, in_id, properties):
        url = self._host + "/graphs" + "/" + self._graph_name + "/graph/edges"
        data = {
            "label": edge_label,
            "outV": out_id,
            "inV": in_id,
            "properties": properties
        }
        response = self.session.post(url, data=json.dumps(data), auth=self._auth,
                                     headers=self._headers, timeout=self._timeout)
        if response.status_code == 201 and authorized(response):
            res = EdgeData(json.loads(response.content))
            return res
        else:
            raise CreateError("created edge failed: {}".format(response.content))

    def addEdges(self, input_data):
        url = self._host + "/graphs" + "/" + self._graph_name + "/graph/edges/batch"
        data = []
        for item in input_data:
            data.append({'label': item[0], 'outV': item[1], 'inV': item[2], 'outVLabel': item[3],
                         'inVLabel': item[4], 'properties': item[5]})
        response = self.session.post(url, data=json.dumps(data), auth=self._auth,
                                     headers=self._headers, timeout=self._timeout)
        if response.status_code == 201 and authorized(response):
            res = []
            for item in json.loads(response.content):
                res.append(EdgeData({"id": item}))
            return res
        else:
            raise CreateError("created edges failed:  {}".format(response.content))

    def appendEdge(self, edge_id, properties):
        url = self._host + "/graphs" + "/" + self._graph_name \
              + "/graph/edges/" + edge_id + "?action=append"
        data = {
            "properties": properties
        }
        response = self.session.put(url, data=json.dumps(data), auth=self._auth,
                                    headers=self._headers, timeout=self._timeout)
        if response.status_code == 200 and authorized(response):
            res = EdgeData(json.loads(response.content))
            return res
        else:
            raise UpdateError("append edge failed: {}".format(response.content))

    def eliminateEdge(self, edge_id, properties):
        url = self._host + "/graphs" + "/" + self._graph_name \
              + "/graph/edges/" + edge_id + "?action=eliminate"
        data = {
            "properties": properties
        }
        response = self.session.put(url, data=json.dumps(data), auth=self._auth,
                                    headers=self._headers, timeout=self._timeout)
        if response.status_code == 200 and authorized(response):
            res = EdgeData(json.loads(response.content))
            return res
        else:
            raise UpdateError("eliminate edge failed: {}".format(response.content))

    def getEdgeById(self, edge_id):
        url = self._host + "/graphs" + "/" + self._graph_name + "/graph/edges/" + edge_id
        response = self.session.get(url, auth=self._auth, headers=self._headers, timeout=self._timeout)
        if response.status_code == 200 and authorized(response):
            res = EdgeData(json.loads(response.content))
            return res
        else:
            raise NotFoundError("not found edge: {}".format(response.content))

    def getEdgeByPage(self, label=None, vertex_id=None, direction=None, limit=0, page=None, properties=None):
        url = self._host + "/graphs" + "/" + self._graph_name + "/graph/edges?"
        para = ""
        if vertex_id:
            if direction:
                para = para + "&vertex_id=\"" + vertex_id + "\"&direction=" + direction
            else:
                raise NotFoundError("Direction can not be empty.")
        if label:
            para = para + "&label=" + label
        if properties:
            para = para + "&properties=" + json.dumps(properties)
        if page is not None:
            if page:
                para += '&page={}'.format(page)
            else:
                para += '&page'
        if limit > 0:
            para = para + "&limit=" + str(limit)
        url = url + para[1:]
        response = self.session.get(url, auth=self._auth, headers=self._headers, timeout=self._timeout)
        if response.status_code == 200 and authorized(response):
            res = []
            for item in json.loads(response.content)["edges"]:
                res.append(EdgeData(item))
            return res, json.loads(response.content)["page"]
        else:
            raise NotFoundError("not found edges: {}".format(response.content))

    def removeEdgeById(self, edge_id):
        url = self._host + "/graphs" + "/" + self._graph_name + "/graph/edges/" + edge_id
        response = self.session.delete(url, auth=self._auth, headers=self._headers, timeout=self._timeout)
        if response.status_code == 204 and authorized(response):
            return response.content
        else:
            raise RemoveError("remove edge failed: {}".format(response.content))

    def getVerticesById(self, vertex_ids):
        if not vertex_ids:
            return []
        url = self._host + "/graphs" + "/" + self._graph_name \
              + "/traversers/vertices?"
        for vertex_id in vertex_ids:
            url += 'ids="{}"&'.format(vertex_id)
        url = url.rstrip("&")
        response = self.session.get(url, auth=self._auth, headers=self._headers, timeout=self._timeout)
        if response.status_code == 200 and authorized(response):
            res = []
            for item in json.loads(response.content)["vertices"]:
                res.append(VertexData(item))
            return res
        else:
            create_exception(response.content)

    def getEdgesById(self, edge_ids):
        if not edge_ids:
            return []
        url = self._host + "/graphs" + "/" + self._graph_name \
              + "/traversers/edges?"
        for vertex_id in edge_ids:
            url += 'ids={}&'.format(vertex_id)
        url = url.rstrip("&")
        response = self.session.get(url, auth=self._auth, headers=self._headers, timeout=self._timeout)
        if response.status_code == 200 and authorized(response):
            res = []
            for item in json.loads(response.content)["edges"]:
                res.append(EdgeData(item))
            return res
        else:
            create_exception(response.content)
