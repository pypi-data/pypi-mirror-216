import pytest
from pytest_mock import MockFixture

from fiddler import FiddlerClient
from fiddler.exceptions import NotSupported
from fiddler.v2.schema.server_info import ServerInfo, Version


def test_get_server_info_without_server_version(mocker: MockFixture):
    mocker.patch('fiddler.connection.Connection.check_connection', return_value='OK')

    server_info_dict = {
        'feature_flags': {
            'fairness': False,
        },
    }

    mock_get_server_info = mocker.patch.object(FiddlerClient, '_get_server_info')
    mock_get_server_info.return_value = ServerInfo(**server_info_dict)

    client = FiddlerClient('https://test.fiddler.ai', 'test', 'foo-token')

    assert client.server_info.server_version is None
    assert client.server_info.feature_flags == server_info_dict['feature_flags']


def test_get_server_info_with_server_version(mocker: MockFixture):
    mocker.patch('fiddler.connection.Connection.check_connection', return_value='OK')

    server_info_dict = {
        'feature_flags': {
            'fairness': False,
        },
        'server_version': '23.2.0',
    }

    mock_get_server_info = mocker.patch.object(FiddlerClient, '_get_server_info')
    mock_get_server_info.return_value = ServerInfo(**server_info_dict)

    client = FiddlerClient('https://test.fiddler.ai', 'test', 'foo-token')

    assert client.server_info.server_version == Version.parse(
        server_info_dict['server_version']
    )
    assert client.server_info.feature_flags == server_info_dict['feature_flags']


def test_check_semver_incorrect_version(mocker: MockFixture):
    mocker.patch('fiddler.connection.Connection.check_connection', return_value='OK')
    server_info_dict = {
        'feature_flags': {
            'fairness': False,
        },
        'server_version': '22.1.0',
    }

    mock_get_server_info = mocker.patch.object(FiddlerClient, '_get_server_info')
    mock_get_server_info.return_value = ServerInfo(**server_info_dict)

    with pytest.raises(NotSupported):
        FiddlerClient('https://test.fiddler.ai', 'test', 'foo-token')
