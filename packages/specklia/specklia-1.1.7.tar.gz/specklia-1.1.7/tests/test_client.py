"""Unit tests for the Specklia Client."""
from datetime import datetime
from http import HTTPStatus
from typing import Dict
from unittest.mock import call
from unittest.mock import MagicMock
from unittest.mock import patch

import geopandas as gpd
import pytest
from shapely import Point
from shapely import Polygon

from specklia import Specklia


@pytest.fixture()
def example_geodataframe() -> gpd.GeoDataFrame:
    return gpd.GeoDataFrame({
        'geometry': [Point(lon, lat) for lon, lat in zip([1, 2, 3, 4, 5], [0, 1, 2, 3, 4])],
        'timestamp': [2, 3, 4, 5, 6]},
        crs="EPSG:4326")


@pytest.fixture()
def test_client():
    return Specklia(auth_token='fake_token', url='https://localhost')


def test_create_client(test_client: Specklia):
    assert test_client is not None


def test_user_id(test_client: Specklia, patched_requests_with_response: Dict[str, MagicMock]):
    patched_requests_with_response['response'].json.return_value = 'fake_user_id'
    returned_user_id = test_client.user_id
    patched_requests_with_response['requests'].post.assert_has_calls([
        call('https://localhost/users', headers={'Authorization': 'Bearer fake_token'})])
    assert returned_user_id == 'fake_user_id'


def test_list_users(test_client: Specklia, patched_requests_with_response: Dict[str, MagicMock]):
    patched_requests_with_response['response'].json.return_value = [{'name': 'fred', 'email': 'fred@fred.fred'}]
    test_client.list_users(group_id='hazbin')
    patched_requests_with_response['requests'].get.assert_has_calls([
        call('https://localhost/users', headers={'Authorization': 'Bearer fake_token'},
             params={"group_id": "hazbin"})])


def test_add_points_to_dataset(test_client: Specklia, example_geodataframe: gpd.GeoDataFrame):
    with (patch('specklia.client.simple_websocket') as mock_simple_websocket,
            patch('specklia.client._websocket_helpers') as mock_websocket_helpers):
        mock_client = MagicMock(name="mock_client")
        mock_simple_websocket.Client.return_value = mock_client
        mock_websocket_helpers.receive_object_from_websocket.return_value = {'status': HTTPStatus.OK}
        test_client.add_points_to_dataset(
            dataset_id='dummy_dataset', new_points=example_geodataframe, source_description={'reference': 'cheese'})

        mock_websocket_helpers.send_object_to_websocket.assert_called_with(
            mock_client, {
                'dataset_id': 'dummy_dataset', 'gdf': example_geodataframe, 'source': {'reference': 'cheese'}})


def test_query_dataset(test_client: Specklia):
    with (patch('specklia.client.simple_websocket') as mock_simple_websocket,
            patch('specklia.client._websocket_helpers') as mock_websocket_helpers):
        mock_client = MagicMock(name="mock_client")
        mock_simple_websocket.Client.return_value = mock_client
        mock_websocket_helpers.receive_object_from_websocket.return_value = {
            'status': HTTPStatus.OK, 'gdf': 'dummy', 'sources': {}}
        test_client.query_dataset(
            dataset_id='dummy_dataset',
            epsg4326_polygon=Polygon(((0, 0), (0, 1), (1, 1), (0, 0))),
            min_datetime=datetime(2020, 5, 6),
            max_datetime=datetime(2020, 5, 10),
            columns_to_return=['lat', 'lon'],
            additional_filters=[
                {'column': 'cheese', 'operator': '<', 'threshold': 6.57},
                {'column': 'wine', 'operator': '>=', 'threshold': -23}])

        mock_websocket_helpers.send_object_to_websocket.assert_called_with(
            mock_client, {
                'dataset_id': 'dummy_dataset', 'min_timestamp': 1588719600, 'max_timestamp': 1589065200,
                'epsg4326_search_area': {
                    'type': 'Polygon', 'coordinates': [[[0.0, 0.0], [0.0, 1.0], [1.0, 1.0], [0.0, 0.0]]]},
                'columns_to_return': ['lat', 'lon'],
                'additional_filters': [
                    {'column': 'cheese', 'operator': '<', 'threshold': 6.57},
                    {'column': 'wine', 'operator': '>=', 'threshold': -23}]})


def test_list_all_groups(patched_requests_with_response: Dict[str, MagicMock]):
    patched_requests_with_response['response'].json.return_value = ['ducks']
    Specklia(url='https://localhost', auth_token='fake_token').list_all_groups()
    patched_requests_with_response['requests'].get.assert_has_calls([
        call('https://localhost/groups', headers={'Authorization': 'Bearer fake_token'})])


def test_create_group(patched_requests_with_response: Dict[str, MagicMock]):
    Specklia(url='https://localhost', auth_token='fake_token').create_group("ducks")
    patched_requests_with_response['requests'].post.assert_has_calls([
        call('https://localhost/groups',
             json={"group_name": "ducks"},
             headers={'Authorization': 'Bearer fake_token'})])


def test_update_group_name(patched_requests_with_response: Dict[str, MagicMock]):
    Specklia(url='https://localhost', auth_token='fake_token').update_group_name(
        group_id="ducks",
        new_group_name="pigeons")
    patched_requests_with_response['requests'].put.assert_has_calls([
        call('https://localhost/groups',
             json={"group_id": "ducks", "new_group_name": "pigeons"},
             headers={'Authorization': 'Bearer fake_token'})])


def test_delete_group(patched_requests_with_response: Dict[str, MagicMock]):
    Specklia(url='https://localhost', auth_token='fake_token').delete_group(group_id="ducks")
    patched_requests_with_response['requests'].delete.assert_has_calls([
        call('https://localhost/groups', headers={'Authorization': 'Bearer fake_token'},
             json={"group_id": "ducks"})])


def test_list_groups(patched_requests_with_response: Dict[str, MagicMock]):
    patched_requests_with_response['response'].json.return_value = ['ducks']
    Specklia(url='https://localhost', auth_token='fake_token').list_groups()
    patched_requests_with_response['requests'].get.assert_has_calls([
        call('https://localhost/groupmembership', headers={'Authorization': 'Bearer fake_token'})])


def test_add_user_to_group(patched_requests_with_response: Dict[str, MagicMock]):
    Specklia(url='https://localhost', auth_token='fake_token').add_user_to_group(group_id='ducks',
                                                                                 user_to_add_id='donald')
    patched_requests_with_response['requests'].post.assert_has_calls([
        call('https://localhost/groupmembership',
             json={"group_id": "ducks", "user_to_add_id": "donald"},
             headers={'Authorization': 'Bearer fake_token'})])


def test_update_user_privileges(patched_requests_with_response: Dict[str, MagicMock]):
    Specklia(url='https://localhost', auth_token='fake_token').update_user_privileges(group_id="ducks",
                                                                                      user_to_update_id="donald",
                                                                                      new_privileges="ADMIN")
    patched_requests_with_response['requests'].put.assert_has_calls([
        call('https://localhost/groupmembership',
             json={"group_id": "ducks", "user_to_update_id": "donald", "new_privileges": "ADMIN"},
             headers={'Authorization': 'Bearer fake_token'})])


def test_delete_user_from_group(patched_requests_with_response: Dict[str, MagicMock]):
    Specklia(url='https://localhost', auth_token='fake_token').delete_user_from_group(group_id="ducks",
                                                                                      user_to_delete_id="donald")
    patched_requests_with_response['requests'].delete.assert_has_calls([
        call('https://localhost/groupmembership', headers={'Authorization': 'Bearer fake_token'},
             json={"group_id": "ducks", "user_to_delete_id": "donald"})])


def test_list_datasets(patched_requests_with_response: Dict[str, MagicMock]):
    patched_requests_with_response['response'].json.return_value = [{'dataset_name': 'am'}, {'dataset_name': 'humbug'}]
    Specklia(url='https://localhost', auth_token='fake_token').list_datasets()
    patched_requests_with_response['requests'].get.assert_has_calls([
        call('https://localhost/metadata', headers={'Authorization': 'Bearer fake_token'})])


def test_create_dataset(patched_requests_with_response: Dict[str, MagicMock]):
    Specklia(url='https://localhost', auth_token='fake_token').create_dataset(
        dataset_name='am', description='wibble', columns=[
            {'name': 'hobbits', 'type': 'halflings', 'description': 'concerning hobbits'},
            {'name': 'cats', 'type': 'pets', 'description': 'concerning cats'}])

    patched_requests_with_response['requests'].post.assert_has_calls([
        call('https://localhost/metadata',
             json={'dataset_name': 'am',
                   'description': 'wibble',
                   'columns':
                   [{'name': 'hobbits', 'type': 'halflings', 'description': 'concerning hobbits'},
                    {'name': 'cats', 'type': 'pets', 'description': 'concerning cats'}]},
             headers={'Authorization': 'Bearer fake_token'})])


def test_update_dataset_ownership(patched_requests_with_response: Dict[str, MagicMock]):
    Specklia(url='https://localhost', auth_token='fake_token').update_dataset_ownership(
        dataset_id='bside', new_owning_group_id='arctic monkeys'
    )
    patched_requests_with_response['requests'].put.assert_has_calls([
        call('https://localhost/metadata',
             json={'dataset_id': 'bside',
                   'new_owning_group_id': 'arctic monkeys'},
             headers={'Authorization': 'Bearer fake_token'})
    ])


def test_delete_dataset(patched_requests_with_response: Dict[str, MagicMock]):
    Specklia(url='https://localhost', auth_token='fake_token').delete_dataset(
        dataset_id='bside'
    )
    patched_requests_with_response['requests'].delete.assert_has_calls([
        call('https://localhost/metadata',
             json={'dataset_id': 'bside'},
             headers={'Authorization': 'Bearer fake_token'})
    ])
