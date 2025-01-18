"""Module to write clean data into distincts environments"""

import json
import logging
import os

from google.cloud import storage

from utils.constants import GCS_BUCKET, PROJECT_ID


class DataWritter:
    """Object that writes data to different locations based on parameters"""

    def __init__(self, mode: str):
        self.mode = mode
        self.gcs_client = storage.Client(PROJECT_ID)

    def write_json(
        self,
        json_content: dict,
        directory: str,
        request_uuid: str,
        metadata: dict = None,
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
        if self.mode.upper() == "LOCAL":
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(output_file_name, "w", encoding="UTF-8") as output_file:
                json.dump(json_content, output_file)
        if self.mode.upper() == "CLOUD":
            self.upload_blob(
                bucket_name=GCS_BUCKET,
                destination_blob_name=output_file_name,
                content=str(json_content),
            )
        logging.info("Content of request %s has been loaded", request_uuid)

    def upload_blob(self, bucket_name: str, destination_blob_name: str, content):
        """Uploads a file to the bucket."""
        bucket = self.gcs_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_string(content)
