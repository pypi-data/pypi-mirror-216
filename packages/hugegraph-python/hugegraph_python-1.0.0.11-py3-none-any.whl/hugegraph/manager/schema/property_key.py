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


class PropertyKey(HugeGraphBase):
    def __init__(self, ip, port, graph_name, user, pwd, timeout):
        super().__init__(ip, port, graph_name, user, pwd, timeout)

    @decorator_params
    def asInt(self):
        self._parameter_holder.set("data_type", "INT")
        return self

    @decorator_params
    def asText(self):
        self._parameter_holder.set("data_type", "TEXT")
        return self

    @decorator_params
    def asDouble(self):
        self._parameter_holder.set("data_type", "DOUBLE")
        return self

    @decorator_params
    def asDate(self):
        self._parameter_holder.set("data_type", "DATE")
        return self

    @decorator_params
    def valueSingle(self):
        self._parameter_holder.set("cardinality", "SINGLE")
        return self

    @decorator_params
    def valueList(self):
        self._parameter_holder.set("cardinality", "LIST")
        return self

    @decorator_params
    def valueSet(self):
        self._parameter_holder.set("cardinality", "SET")
        return self

    @decorator_params
    def calcMax(self):
        self._parameter_holder.set("aggregate_type", "MAX")
        return self

    @decorator_params
    def calcMin(self):
        self._parameter_holder.set("aggregate_type", "MIN")
        return self

    @decorator_params
    def calcSum(self):
        self._parameter_holder.set("aggregate_type", "SUM")
        return self

    @decorator_params
    def calcOld(self):
        self._parameter_holder.set("aggregate_type", "OLD")
        return self

    @decorator_params
    def userdata(self, *args):
        user_data = self._parameter_holder.get_value("user_data")
        if not user_data:
            self._parameter_holder.set("user_data", dict())
            user_data = self._parameter_holder.get_value("user_data")
        i = 0
        while i < len(args):
            user_data[args[i]] = args[i + 1]
            i += 2
        return self

    def ifNotExist(self):
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/propertykeys" \
              + "/" + self._parameter_holder.get_value("name")
        response = requests.get(url)
        if response.status_code == 200 and authorized(response):
            self._parameter_holder.set("not_exist", False)
        return self

    @decorator_create
    def create(self):
        dic = self._parameter_holder.get_dic()
        propertykeys = {
            "name": dic["name"]
        }
        if "data_type" in dic:
            propertykeys["data_type"] = dic["data_type"]
        if "cardinality" in dic:
            propertykeys["cardinality"] = dic["cardinality"]
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/propertykeys"
        res = requests.post(url, data=json.dumps(propertykeys), auth=self._auth, headers=self._headers)
        self.clean_parameter_holder()
        if res.status_code == 201:
            return 'create PropertyKey success, Detail: {}'.format(res.content)
        else:
            raise CreateError('CreateError: "create PropertyKey failed", Detail: {}'.format(res.content))

    @decorator_params
    def append(self):
        property_name = self._parameter_holder.get_value("name")
        user_data = self._parameter_holder.get_value("user_data")
        if not user_data:
            user_data = dict()
        data = {
            "name": property_name,
            "user_data": user_data
        }
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/propertykeys" \
              + "/" + property_name + "?action=append"
        res = requests.put(url, data=json.dumps(data), auth=self._auth, headers=self._headers)
        self.clean_parameter_holder()
        if res.status_code == 200:
            return 'append PropertyKey success, Detail: {}'.format(res.content)
        else:
            raise UpdateError('UpdateError: "append PropertyKey failed", Detail: {}'.format(res.content))

    @decorator_params
    def eliminate(self):
        property_name = self._parameter_holder.get_value("name")
        user_data = self._parameter_holder.get_value("user_data")
        if not user_data:
            user_data = dict()
        data = {
            "name": property_name,
            "user_data": user_data
        }
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/propertykeys" \
              + "/" + property_name + "?action=eliminate"
        res = requests.put(url, data=json.dumps(data), auth=self._auth, headers=self._headers)
        self.clean_parameter_holder()
        if res.status_code == 200:
            return 'eliminate PropertyKey success, Detail: {}'.format(str(res.content))
        else:
            raise UpdateError('UpdateError: "eliminate PropertyKey failed", Detail: {}'.format(str(res.content)))

    @decorator_params
    def remove(self):
        dic = self._parameter_holder.get_dic()
        url = self._host + "/graphs" + "/" + self._graph_name + \
              "/schema/propertykeys" + "/" + dic["name"]
        res = requests.delete(url)
        self.clean_parameter_holder()
        if res.status_code == 204:
            return 'delete PropertyKey success, Detail: {}'.format(dic["name"])
        else:
            raise RemoveError('RemoveError: "delete PropertyKey failed", Detail: {}'.format(str(res.content)))
