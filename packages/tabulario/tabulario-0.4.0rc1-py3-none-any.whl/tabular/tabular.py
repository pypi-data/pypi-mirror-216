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
from dataclasses import dataclass
from typing import List

from pyiceberg.catalog import URI
from pyiceberg.catalog.rest import RestCatalog

from tab.oauth import ENVIRONMENT_URLS

ENVIRONMENT = "environment"
PROD = "prod"
WAREHOUSE = "warehouse"


@dataclass(frozen=True)
class Warehouse:
    id: str
    name: str
    region: str


class Tabular(RestCatalog):
    def __init__(self, name: str = "default", **properties: str):
        """Tabular Catalog.

        Args:
            name (str): Name to identify the catalog.
            properties (Dict[str, str]): Properties that are passed along to the configuration.
        """
        self.uri = properties.get(URI, ENVIRONMENT_URLS.get(properties.get(ENVIRONMENT, PROD)))
        self.name = name
        self.properties = properties
        if WAREHOUSE in self.properties:
            self._fetch_config()
        self._session = self._create_session()

    def list_warehouses(self) -> List[Warehouse]:
        url = self.url("warehouses", prefixed=False)
        response = self._session.get(url=url)
        response.raise_for_status()
        response_json = response.json()
        if not isinstance(response_json, list):
            raise ValueError(f"Expected list, got: {response_json}")
        return [Warehouse(**warehouse) for warehouse in response_json]
