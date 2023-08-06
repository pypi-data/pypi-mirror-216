import requests

from openxlab.model.common.constants import paths
from openxlab.model.common.response_dto import ReturnDto
from openxlab.model.common.meta_file_util import get_meta_payload
import os


class ModelApiClient(object):
    def __init__(self, endpoint, token):
        self.token = token
        self.endpoint = endpoint

    def get_inference_result(self, payload):
        """
        get inference result
        """
        result = self.http_post_response_dto(payload)
        return result

    def http_post_response_dto(self, payload):
        headers = self.http_common_header()
        response = requests.post(self.endpoint, files=payload["files"], data={'texts': payload['texts']}, headers=headers)
        response.raise_for_status()
        return response.content

    def http_common_header(self):
        header_dict = {
            "Authorization": f"Bearer {self.token}"
        }
        return header_dict
