import base64
from typing import Optional

from urllib3 import Retry

from invision_client import ApiClient, Configuration
from invision_client.api.forums_api import ForumsApi
from invision_client.api.members_api import MembersApi
from invision_client.api.topics_api import TopicsApi

__all__ = ["get_api_client", "InvisionApi"]


def get_api_client(api_key, server_url=None, retries=None, verify_ssl=True):
    if api_key is None or api_key == "":
        raise KeyError('Please provide the api_key parameter')
    config = Configuration().get_default_copy()
    config.host = server_url if server_url else config.host
    config.retries = retries if retries else config.retries
    config.verify_ssl = verify_ssl
    token_bytes = base64.b64encode(api_key.encode('ascii'))
    token = token_bytes.decode()
    return ApiClient(config, header_name="Authorization", header_value=f"Basic {token}")


class InvisionApi:
    """
    InvisionApi is a wrapper class around the invision library that provides access to all Rest API end points.
    """

    def __init__(
            self,
            api_key: str,
            server_url: Optional[str] = None,
            verify_ssl: Optional[bool] = True,
            retries: Optional[Retry] = None,
    ):
        self.client = get_api_client(api_key, server_url, retries, verify_ssl)
        self.apis = {MembersApi.__name__: MembersApi(self.client),
                     ForumsApi.__name__: ForumsApi(self.client),
                     TopicsApi.__name__: TopicsApi(self.client)}

    @property
    def members_api(self) -> MembersApi:
        return self.apis.get(MembersApi.__name__)

    @property
    def forums_api(self) -> ForumsApi:
        return self.apis.get(ForumsApi.__name__)

    @property
    def topics_api(self) -> TopicsApi:
        return self.apis.get(TopicsApi.__name__)
