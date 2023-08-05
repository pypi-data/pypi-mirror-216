# Copyright 2021 Element Analytics, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
A connector class includes methods needed for connectors.
"""
import csv
import logging
from unify.connectors import ArtifactType, LogType
from unifyconnectorframework.logging import UnifyHandler
from unifyconnectorframework.organization_client import OrganizationClient, DatasetOperation

class Connector:
    """
    Common connector class
    """
    def __init__(
            self,
            account_id,
            password,
            org_id,
            hostname,
            id="",
            labels=None,
            version="0.0.0",
            logger = None,
        ):
        """
        Initiate a new connector

        :type account_id: string
        :param account_id: Service account identifier
        :type password: string
        :param password: Content to upload
        :type org_id: string
        :param org_id: Content to upload
        :type hostname: string
        :param hostname: Content to upload
        :type id: GUID
        :param id: Connector identifier
        :type labels: dict
        :param labels: Labels related to connector, in format {"category": "[connector_category]"}
        :type version: string
        :param version: Connector version
        :type logger: logging.Logger
        :param logger: instance of logger to be used
        """

        if logger is None:
            self.log = logging.getLogger("unifyconnectorframework")
            self.log.setLevel(logging.INFO)
            fmt = logging.Formatter('%(asctime)s - [%(levelname)s] %(message)s')
            hdl = logging.StreamHandler()
            hdl.setFormatter(fmt)
            self.log.addHandler(hdl)
        else:
            self.log = logger

        self.id = id
        self.labels = labels
        # Note that the default value for labels is set to None rather than a default dictionary.
        # The "default" dictionary gets created as a persistent object so every invocation of a
        # Connector that does not specify an extra param will use the same dictionary.
        if labels is None:
            self.labels = {"category": ""}
        self.version = version
        self.account_id = account_id
        self.connector_params = {
            "connector_id": self.id,
            "account_id": self.account_id,
            "labels": self.labels.get("category"),
            "version": self.version
        }
        self.organization_client = OrganizationClient(
            user_name=self.account_id,
            password=password,
            org_id=org_id,
            cluster=hostname,
            connector_params=self.connector_params,
            logger=self.log
        )

        if logger is None:
            hdl = UnifyHandler(self)
            hdl.setFormatter(fmt)
            self.log.addHandler(hdl)

    def list_datasets(self):
        """
        Retrieve all datasets.
        """
        return self.organization_client.list_datasets()

    def list_datasets_by_labels(self, labels):
        """
        Retrieve all datasets by labels.

        :type labels: list of strings
        :param labels: list of dataset labels. Example ["label1", "label2"]
        """
        return self.organization_client.list_datasets_by_labels(labels=labels)

    def get_dataset(self, dataset_id):
        """
        Retrieve dataset contents.

        :type dataset_id: string or dict
        :param dataset_id: id of dataset
        """
        dataset_id_str = self.organization_client.resolve_dataset_id(dataset_id)
        return self.organization_client.get_dataset(dataset_id=dataset_id_str)

    def create_dataset(self, name, dataset_csv, wait_until_ready=False):
        """
        Create a new dataset.

        :type name: string
        :param name: Name of dataset
        :type dataset_csv: string
        :param dataset_csv: Content to upload
        :type wait_until_ready: bool
        :param wait_until_ready: Determines if the method should wait until the dataset is
            successfuly uploaded to Unify
        """
        dataset_info = self.organization_client.create_dataset(name, dataset_csv, wait_until_ready)
        self.check_or_set_artifact(dataset_info['data_set_id'], ArtifactType.DATASET, name)
        return dataset_info

    def update_dataset(self, dataset_csv, dataset_name=None, dataset_id=None):
        """
        Update a dataset. If dataset does not exist, create a new dataset.

        :type dataset_csv: string
        :param dataset_csv: Content to upload
        :type dataset_name: string
        :param dataset_name: Name of dataset
        :type dataset_id: string or dict
        :param dataset_id: Existing dataset id
        """
        dataset_id_str = self.organization_client.resolve_dataset_id(dataset_id)
        result_id, result_name = self.organization_client.update_dataset(
            dataset_csv,
            dataset_name,
            dataset_id_str
        )
        self.check_or_set_artifact(result_id, ArtifactType.DATASET, result_name)
        return result_id

    def truncate_dataset(self, dataset_id, wait_until_ready=False):
        """
        Truncate a dataset.

        :type dataset_id: string or dict
        :param dataset_id: Existing dataset id
        :type wait_until_ready: bool
        :param wait_until_ready: Determines if the method should wait until the dataset is
            successfuly truncated
        """
        dataset_id_str = self.organization_client.resolve_dataset_id(dataset_id)
        result = self.organization_client.truncate_dataset(dataset_id_str, wait_until_ready)
        dataset_name = [x['name'] for x in self.list_datasets() if x['id']['id']==dataset_id_str][0]
        self.check_or_set_artifact(dataset_id_str, ArtifactType.DATASET, dataset_name)
        return result

    def append_dataset(self, dataset_id, dataset_csv, wait_until_ready=False):
        """
        Append a dataset.

        :type dataset_csv: string
        :param dataset_csv: Content to upload
        :type dataset_id: string or dict
        :param dataset_id: Existing dataset id
        :type wait_until_ready: bool
        :param wait_until_ready: Determines if the method should wait until the dataset is
            successfuly appended
        """
        dataset_id_str = self.organization_client.resolve_dataset_id(dataset_id)
        result = self.organization_client.append_dataset(
            dataset_id_str,
            dataset_csv,
            wait_until_ready
        )
        dataset_name = [x['name'] for x in self.list_datasets() if x['id']['id']==dataset_id_str][0]
        self.check_or_set_artifact(dataset_id_str, ArtifactType.DATASET, dataset_name)
        return result

    def update_dataset_labels(self, dataset_id, labels):
        """
        Updates labels for a dataset.

        :type dataset_id: string or dict
        :param dataset_id: Existing dataset id
        :type labels: str or list[str]
        :param labels: Labels
        """
        dataset_id_str = self.organization_client.resolve_dataset_id(dataset_id)
        if isinstance(labels, str):
            result = self.organization_client.update_dataset_labels(dataset_id_str, [labels])
        elif isinstance(labels, list):
            result = self.organization_client.update_dataset_labels(dataset_id_str, labels)
        else:
            raise ValueError('Labels should be an instance of str or list')
        dataset_name = [x['name'] for x in self.list_datasets() if x['id']['id']==dataset_id_str][0]
        self.check_or_set_artifact(dataset_id_str, ArtifactType.DATASET, dataset_name)
        return result

    def operate_dataset(
        self,
        dataset_csv,
        dataset_id=None,
        dataset_name=None,
        operation=DatasetOperation.UPDATE
    ):
        """
        Operate dataset on given dataset_id. If dataset_id is not given, create a dataset first.
        If dataset is not valid, throw an error.

        :type dataset_csv: string
        :param dataset_csv: Content to upload
        :type dataset_name: string
        :param dataset_name: Name of dataset
        :type dataset_id: string or dict
        :param dataset_id: Existing dataset id
        :type operation: Enum
        :param operation: Operation on dataset, update or append
        """
        dataset_id_str = self.organization_client.resolve_dataset_id(dataset_id)
        result = self.organization_client.operate_dataset(
            dataset_csv,
            dataset_id_str,
            dataset_name,
            operation
        )
        dataset_name = [x['name'] for x in self.list_datasets() if x['id']['id']==result][0]
        self.check_or_set_artifact(result, ArtifactType.DATASET, dataset_name)
        return result

    def get_datastream_info(self, datastream_id, sequence_nr=0):
        """
        Returns the information of the events starting in the event sequene number provided

        :type datastream_id: str
        :param datastream_id: Id of the datastream to return its events
        :type sequence_nr: int
        :param sequence_nr: number of the firts event to be returned
        """
        datastream_id_str = self.organization_client.resolve_dataset_id(datastream_id)
        return self.organization_client.get_datastream_info(
            datastream_id=datastream_id_str,
            sequence_nr=sequence_nr
        )

    def get_datastream_data(self, datastream_id, sequence_nr):
        """
        Returns the data from a specific datastream event

        :type datastream_id: str
        :param datastream_id: Id of the datastream to return its events
        :type sequence_nr: int
        :param sequence_nr: Number of the event to be returned
        """
        datastream_id_str = self.organization_client.resolve_dataset_id(datastream_id)
        return self.organization_client.get_datastream_data(
            datastream_id=datastream_id_str,
            sequence_nr=sequence_nr
        )

    def upload_template(self, template_csv):
        """
        Upload asset template definition csv.

        :type template_csv: string
        :param template_csv: asset template definition in csv format
        """
        result = self.organization_client.upload_template(template_csv)
        all_templates = [(x['id'], x['name']) for x in self.list_templates()]
        templates_updated = {x['Template Name'] for x in csv.DictReader(template_csv.splitlines())}
        for template in all_templates:
            if template[1] in templates_updated:
                self.check_or_set_artifact(template[0], ArtifactType.TEMPLATE, template[1])
        return result

    def upload_template_configuration(self, config_csv):
        """
        Upload asset template configuration parameter definition csv.

        :type config_csv: string
        :param config_csv: asset template configuration parameter definition in csv format
        """
        result = self.organization_client.upload_template_configuration(config_csv)
        all_templates = [(x['id'], x['name']) for x in self.list_templates()]
        templates_updated = {x['template'] for x in csv.DictReader(config_csv.splitlines())}
        for template in all_templates:
            if template[1] in templates_updated:
                self.check_or_set_artifact(template[0], ArtifactType.TEMPLATE, template[1])
        return result

    def update_template_categories(self, template_id, template_name, version, categories):
        """
        Update categories to an asset template.

        :type template_id: string
        :param template_id: Existing template id
        :type template_name: string
        :param template_name: Existing template name
        :type version: string
        :param version: Existing template id
        :type categories: dict
        :param categories: Labels
        """
        result = self.organization_client.update_template_categories(
            template_id,
            template_name,
            version,
            categories
        )
        self.check_or_set_artifact(template_id, ArtifactType.TEMPLATE, template_name)
        return result

    def list_templates(self):
        """
        Retrieve all asset templates
        """
        return self.organization_client.list_templates()

    def list_graphs(self):
        """
        Retrieve all graphs.
        """
        return self.organization_client.list_graphs()

    def get_graph(self, graph_id, query=None):
        """
        Retrieve graph.

        :type graph_id: string
        :param graph_id: id of graph
        :type query: string
        :param query: graph cypher query
        """
        return self.organization_client.get_graph(graph_id=graph_id, query=query)

    def get_connector_info(self):
        """
        Retrieves the information of the connector
        """
        return self.organization_client.get_connector(self.id)

    def set_connector_config(self, config):
        """
        Sets the connector configuration object

        :type config: dict
        :param config: connector configuration object
        """
        return self.organization_client.set_connector_config(self.id, config)

    def set_connector_status(self, status, metadata=''):
        """
        Sets the connector status

        :type status: unify.connectors.ConnStatus
        :param status: Status of the connector
        :type metadata: str
        :param metadata: Metadata of the status
        """
        return self.organization_client.set_connector_status(self.id, status, metadata)

    def write_log(self, message, timestamp=None, log_type=LogType.INFO, metadata=''):
        """
        Writes a log entry in the Unify connector service

        :type message: str
        :param message: Log message
        :type timestamp: int
        :param timestamp: POSIX timestamp in milisencods (miliseconds since 01/01/1970 00:00:00)
        :type logtype: Unify.connectors.LogType
        :param logtype: Severity of the log
        :type metadata: str
        :param metadata: Log message metadata
        """
        self.organization_client.write_log(self.id, message, timestamp, log_type, metadata)

    def write_logs(self, log_list):
        """
        Writes a list of log entries in theUnify connector service

        :type log_list: list[dict]
        :param log_list: log messages in list of dicts with keys: "timestamp", "type", "message",
        "metadata"
        """
        self.organization_client.write_logs(self.id, log_list)

    def check_or_set_artifact(self, artifact_id, artifact_type, artifact_name):
        """
        Checks if the artifact is already created otherwise it will create it

        :type artifact_id: str
        :param artifact_id: Id of the artifact to be checked or created
        :type artifact_type: str
        :param artifact_type: Type of the artifact to set in case it is not created yet
        :type artifact_name: str
        :param artifact_name: Artifact name to use in case it is not created yet
        """
        self.organization_client.check_or_set_artifact(
            self.id, artifact_id, artifact_type, artifact_name
        )

    def get_artifacts(self):
        """
        Retrieves all the artifacts associated with the connector
        """
        return self.organization_client.get_artifacts(self.id)
