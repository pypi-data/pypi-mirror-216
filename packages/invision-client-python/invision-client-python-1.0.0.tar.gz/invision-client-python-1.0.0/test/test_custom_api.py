from unittest.mock import MagicMock
import pytest

from invision_client.api.forums_api import ForumsApi
from invision_client.api.members_api import MembersApi
from invision_client.api.topics_api import TopicsApi
from invision_client.invision_api import InvisionApi, get_api_client


@pytest.mark.parametrize("val", ["", None])
def test_invision_api_error(val):
    with pytest.raises(KeyError):
        _ = InvisionApi(val)


def test_invision_members_api(mocker):
    client = InvisionApi("abc")
    magic_members_api = MagicMock()
    client.apis[MembersApi.__name__] = magic_members_api
    call_get = mocker.patch.object(magic_members_api, 'core_members_get')
    _ = client.members_api.core_members_get()
    assert call_get.called


def test_invision_forums_api(mocker):
    client = InvisionApi("abc")
    magic_api = MagicMock()
    client.apis[ForumsApi.__name__] = magic_api
    call_get = mocker.patch.object(magic_api, 'forums_forums_get')
    _ = client.forums_api.forums_forums_get()
    assert call_get.called


def test_invision_topics_api(mocker):
    client = InvisionApi("abc")
    magic_api = MagicMock()
    client.apis[TopicsApi.__name__] = magic_api
    call_get = mocker.patch.object(magic_api, 'forums_topics_post')
    data = {'author': 11}
    _ = client.topics_api.forums_topics_post(1, 'a', 'b', **data)
    assert call_get.called
    assert call_get.call_args.args == (1, 'a', 'b')
    assert call_get.call_args.kwargs['author'] == 11


def test_api_client_defaults():
    client = get_api_client('abcdefghijklmnop')
    assert client.configuration.host == 'https://tech.forums.silabs.net/api'
    assert client.configuration.verify_ssl
    assert client.configuration.retries is None
    assert len(client.default_headers) == 2
    assert client.default_headers['Authorization'] == 'Basic YWJjZGVmZ2hpamtsbW5vcA=='


def test_api_client():
    client = get_api_client('abcdefghijklmnop', verify_ssl=False, retries=3, server_url="example.com")
    assert client.configuration.verify_ssl is False
    assert client.configuration.retries == 3
    assert client.configuration.host == 'example.com'
