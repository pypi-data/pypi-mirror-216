import subprocess
import os
import logging
from typing import Type
from google.cloud import storage
from google.cloud.exceptions import NotFound
from xia_fields import StringField, OsEnvironField
from xia_engine import BaseDocument
from xia_engine_terraform import TerraformEngine, TerraformConnectParam, TerraformClient


class TerraformGcsConnectParam(TerraformConnectParam):
    """Save the GCS file into Google Cloud Storage"""
    state_bucket = StringField(description="State File Storage Bucket", required=True)
    state_prefix = StringField(description="State File Storage Prefix", required=True)


class TerraformGcsClient(TerraformClient):
    backend_tf = """terraform {
  backend "gcs" {
    bucket = "{{ state_bucket }}"
    prefix = "{{ tfstate_path }}"
  }
}"""

    def __init__(self, template_path: str, runtime_path: str,
                 state_bucket: str, state_prefix: str, tf_state_field: str = None, timeout: int = 60, **kwargs):
        super().__init__(template_path, runtime_path, timeout=timeout, tf_state_field=tf_state_field,
                         state_bucket=state_bucket, state_prefix=state_prefix, **kwargs)
        self.client = storage.Client()
        self.bucket = self.client.bucket(state_bucket)
        self.state_bucket = state_bucket
        self.state_prefix = state_prefix
        self.other_params = kwargs.copy()
        self.other_params["state_bucket"] = state_bucket

    def prepare_state(self, document_class: Type[BaseDocument], doc_id: str):
        """Prepare the location to store state

        Args:
            document_class: Document class
            doc_id: document ID

        Returns:
            state_path for the current document
        """
        return self.get_state_path(document_class, doc_id)

    def clean_state(self, document_class: Type[BaseDocument], doc_id: str):
        """Clean the state file

        Args:
            document_class: Document class
            doc_id: document ID
        """
        blobs = self.bucket.list_blobs(prefix=self.get_state_path(document_class, doc_id))
        for blob in blobs:
            blob.delete()

    def get_state_path(self, document_class: Type[BaseDocument], doc_id: str):
        if not document_class or not doc_id:
            raise ValueError("Resource Type and Document ID cannot be empty")
        resource_type = document_class.__name__
        state_path = "/".join([self.state_prefix, resource_type, doc_id])
        return state_path

    def output(self, document_class: Type[BaseDocument], doc_id: str) -> dict:
        """Get output data

        Args:
            document_class: Document class
            doc_id: Document id
        """
        resource_type = document_class.__name__
        runtime_path = self.runtime_path + "/" + resource_type + "/" + doc_id
        os.makedirs(runtime_path, exist_ok=True)
        remote_state_path = self.get_state_path(document_class, doc_id)
        try:
            blob = self.bucket.blob(f"{remote_state_path}/default.tfstate")
            blob.download_to_filename(f"{runtime_path}/stored.tfstate")
        except NotFound:
            return {}
        output_result = subprocess.run(['terraform', 'output', f"-state={runtime_path}/stored.tfstate", '-json'],
                                       check=True, capture_output=True, text=True)
        if output_result.returncode != 0:
            logging.error(f"{document_class.__name__}/{doc_id} tf-output failed: {output_result.stderr}")
            return {}  # In the case of error, nothing to return
        return self.parse_output(output_result.stdout)


class TerraformGcsEngine(TerraformEngine):
    engine_connector_class = TerraformGcsConnectParam
    engine_connector = TerraformGcsClient


# Afterward will be some predefined Parameters
# Scaleway
class ScwTerraformGcsConnectParam(TerraformGcsConnectParam):
    organization_id: str = StringField(description="Organization ID", required=True)
    project_id: str = StringField(description="Project ID")
    access_key: str = OsEnvironField(description="Project Access Key", prefix="SCW_", required=True)
    secret_key: str = OsEnvironField(description="Project Secret Key", prefix="SCW_", required=True)


class ScwTerraformGcsEngine(TerraformGcsEngine):
    engine_connector_class = ScwTerraformGcsConnectParam
