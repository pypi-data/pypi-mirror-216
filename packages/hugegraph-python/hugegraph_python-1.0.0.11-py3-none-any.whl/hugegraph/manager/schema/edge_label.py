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

from hugegraph.manager.common import HugeGraphBase
from hugegraph.utils.huge_decorator import decorator_params, decorator_create
from hugegraph.utils.exceptions import CreateError, UpdateError, RemoveError
from hugegraph.utils.util import authorized


class EdgeLabel(HugeGraphBase):
    def __init__(self, ip, port, graph_name, user, pwd, timeout):
        super().__init__(ip, port, graph_name, user, pwd, timeout)

    @decorator_params
    def link(self, source_label, target_label):
        self._parameter_holder.set("source_label", source_label)
        self._parameter_holder.set("target_label", target_label)
        return self

    @decorator_params
    def sourceLabel(self, source_label):
        self._parameter_holder.set("source_label", source_label)
        return self

    @decorator_params
    def targetLabel(self, target_label):
        self._parameter_holder.set("target_label", target_label)
        return self

    @decorator_params
    def userdata(self, *args):
        if not self._parameter_holder.get_value("user_data"):
            self._parameter_holder.set('user_data', dict())
        user_data = self._parameter_holder.get_value("user_data")
        i = 0
        while i < len(args):
            user_data[args[i]] = args[i+1]
            i += 2
        return self

    @decorator_params
    def properties(self, *args):
        self._parameter_holder.set("properties", list(args))
        return self

    @decorator_params
    def singleTime(self):
        self._parameter_holder.set("frequency", "SINGLE")
        return self

    @decorator_params
    def multiTimes(self):
        self._parameter_holder.set("frequency", "MULTIPLE")
        return self

    @decorator_params
    def sortKeys(self, *args):
        self._parameter_holder.set("sort_keys", list(args))
        return self

    @decorator_params
    def nullableKeys(self, *args):
        nullable_keys = set(args)
        self._parameter_holder.set("nullable_keys", list(nullable_keys))
        return self

    @decorator_params
    def ifNotExist(self):
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/edgelabels" \
              + "/" + self._parameter_holder.get_value("name")
        response = requests.get(url)
        if response.status_code == 200 and authorized(response):
            self._parameter_holder.set("not_exist", False)
        return self

    @decorator_create
    def create(self):
        dic = self._parameter_holder.get_dic()
        data = dict()
        keys = ['name', 'source_label', 'target_label', 'nullable_keys', 'properties',
                'enable_label_index', 'sort_keys', 'user_data', 'frequency']
        for key in keys:
            if key in dic:
                data[key] = dic[key]
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/edgelabels"
        response = requests.post(url, data=json.dumps(data), auth=self._auth, headers=self._headers)
        self.clean_parameter_holder()
        if response.status_code == 201:
            return 'create EdgeLabel success, Detail: "{}"'.format(str(response.content))
        else:
            raise CreateError('CreateError: "create EdgeLabel failed", Detail:  "{}"'
                              .format(str(response.content)))

    @decorator_params
    def remove(self):
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/edgelabels" + "/" + \
              self._parameter_holder.get_value("name")
        res = requests.delete(url, auth=self._auth, headers=self._headers)
        self.clean_parameter_holder()
        if res.status_code == 202:
            return 'remove EdgeLabel success, Detail: "{}"'.format(str(res.content))
        else:
            raise RemoveError('RemoveError: "remove EdgeLabel failed", Detail:  "{}"'
                              .format(str(res.content)))

    @decorator_params
    def append(self):
        dic = self._parameter_holder.get_dic()
        data = dict()
        keys = ['name', 'nullable_keys', 'properties', 'user_data']
        for key in keys:
            if key in dic:
                data[key] = dic[key]
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/edgelabels" \
              + "/" + data["name"] + "?action=append"
        res = requests.put(url, data=json.dumps(data), auth=self._auth, headers=self._headers)
        self.clean_parameter_holder()
        if res.status_code == 200:
            return 'append EdgeLabel success, Detail: "{}"'.format(str(res.content))
        else:
            raise UpdateError('UpdateError: "append EdgeLabel failed", Detail: "{}"'.format(str(res.content)))

    @decorator_params
    def eliminate(self):
        name = self._parameter_holder.get_value("name")
        user_data = self._parameter_holder.get_value("user_data") if \
            self._parameter_holder.get_value("user_data") else {}
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/edgelabels" \
              + "/" + self._parameter_holder.get_value("name") + "?action=eliminate"
        data = {
            "name": name,
            "user_data": user_data
        }
        res = requests.put(url, data=json.dumps(data), auth=self._auth, headers=self._headers)
        self.clean_parameter_holder()
        if res.status_code == 200:
            return 'eliminate EdgeLabel success, Detail: "{}"'.format(str(res.content))
        else:
            raise UpdateError('UpdateError: "eliminate EdgeLabel failed", Detail: "{}"'.format(str(res.content)))
