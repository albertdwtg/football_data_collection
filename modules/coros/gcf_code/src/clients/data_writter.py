"""Module to write clean data into distincts environments"""

import json
import logging
import os
from typing import Optional

from google.cloud import storage
from tenacity import retry, stop_after_attempt, wait_exponential

from utils.constants import GCS_BUCKET, PROJECT_ID


class DataWritter:
    """Object that writes data to different locations based on parameters"""

    def __init__(self):
        self.gcs_client = storage.Client(PROJECT_ID)
    
    def write_contents(self, directory: str, content: list[dict], file_type: str):
        """Function that loads list of contents and write them to GCP bucket

        Args:
            directory (str): Path inside the bucket where files will be written
            content (list[dict]): list of dict containing data to write (data, request_uuid, metadata)
            file_type (str): extension of the file to write (ex: json)
        """
        if file_type.lower() == "json":
            for content in content:
                self.write_json(
                    json_content=content["data"],
                    directory=directory,
                    request_uuid=content["request_uuid"],
                    metadata=content.get("metadata")
                )

    @retry(
        stop = stop_after_attempt(3),
        wait = wait_exponential(multiplier=3),
        reraise = True
    )
    def write_json(
        self,
        json_content: dict,
        directory: str,
        request_uuid: str,
        metadata: Optional[dict] = None,
    ):
        """Function to write a dict into a JSON file

        Args:
            json_content (dict): variable/content to write
            directory (str): directory in which data will be written
            request_uuid (str): request_uuid of the operation
            metadata (dict, optional): Additional infos to add in the
                                        file content. Defaults to None.
        """
        output_file_name = f"{directory}/{request_uuid}.json"
        if metadata:
            json_content["metadata"] = metadata
        self.upload_blob(
            bucket_name=GCS_BUCKET,
            destination_blob_name=output_file_name,
            content=str(json_content),
        )
        logging.info("Content of request %s has been loaded", request_uuid)

    def upload_blob(self, bucket_name: str, destination_blob_name: str, content: str):
        """Uploads a file to the bucket.

        Args:
            bucket_name (str): Name of the bucket
            destination_blob_name (str): name of the file to upload in the bucket
            content (str): Content of the file to upload
        """
        bucket = self.gcs_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_string(content)
