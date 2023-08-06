"""This file contains the Specklia python client. It is designed to talk to the Specklia webservice."""
from __future__ import annotations

from datetime import datetime
from http import HTTPStatus
import json
import logging
from typing import Dict, List, Optional, Tuple, Union
import warnings

import geopandas as gpd
import pandas as pd
import requests
from shapely import Polygon, to_geojson
import simple_websocket

from specklia import _websocket_helpers

_log = logging.getLogger(__name__)


class Specklia:
    """
    Client for the Specklia webservice.

    Specklia is a geospatial point cloud database designed for Academic use.
    Further details are available at https://specklia.earthwave.co.uk.
    """

    def __init__(
            self: Specklia,
            auth_token: str,
            url: Optional[str] = 'https://specklia.earthwave.co.uk') -> None:
        """
        Create a new Specklia client object.

        This object is a Python client for connecting to Specklia's API.

        Parameters
        ----------
        auth_token : str
            The authentication token to use to authorise calls to Specklia.
            Obtained via the official specklia website, which is currently https://specklia.earthwave.co.uk.
        url : Optional[str]
            The url where Specklia is running, by default the URL of the Specklia server.
        """
        self.server_url = url
        self.auth_token = auth_token
        self._data_streaming_timeout_s = 3600
        _log.info('New Specklia client created.')

    @property
    def user_id(self: Specklia) -> str:
        """
        Retrieve your unique user ID.

        Giving this to another user will allow them to add you to private groups.
        Please quote this ID when contacting support@earthwave.co.uk.

        Returns
        -------
        str
            Your unique user ID.
        """
        response = requests.post(
            self.server_url + "/users",
            headers={"Authorization": "Bearer " + self.auth_token})
        _check_response_ok(response)
        user_id = response.json()
        _log.info('retrieved own user_id %s.', user_id)
        return user_id

    def list_users(self: Specklia, group_id: str) -> pd.DataFrame:
        """
        List users within a group.

        You must have ADMIN permissions within the group in order to do this.

        Parameters
        ----------
        group_id : str
            The UUID of the group for which to list users.

        Returns
        -------
        pd.DataFrame
            A dataframe describing users within a group.
        """
        response = requests.get(
            self.server_url + "/users",
            headers={"Authorization": "Bearer " + self.auth_token},
            params={'group_id': group_id})
        _check_response_ok(response)
        _log.info('listed users within group_id %s.', group_id)
        return pd.DataFrame(response.json()).convert_dtypes()

    def query_dataset(self: Specklia, dataset_id: str, epsg4326_polygon: Polygon,  # noqa: CFQ002
                      min_datetime: datetime, max_datetime: datetime,
                      columns_to_return: List[str],
                      additional_filters: List[Dict[str, Union[float, str]]]) -> Tuple[gpd.GeoDataFrame, Dict]:
        """
        Query data within a dataset.

        You must be part of the group that owns the dataset in order to do this.

        All provided conditions are applied to the dataset via logical AND
        (i.e. only points that meet all of the conditions will be returned).

        Parameters
        ----------
        dataset_id : str
            The UUID of the dataset to query.
        epsg4326_polygon : Polygon
            The geospatial polygon to query. Only points within this polygon will be returned.
            The edges of the polygon are interpreted as geodesics on the WGS84 ellipsoid.
            The points must be in the order (longitude, latitude).
        min_datetime : datetime
            The minimum datetime for the query. Only points occurring after this datetime will be returned.
        max_datetime : datetime
            The maximum datetime for the query. Only points occurring before this datetime will be returned.
        columns_to_return : List[str]
            A list of dataset columns to return. If empty, all columns are returned.
        additional_filters: List[Dict[str, Union[float, str]]]
            Additional filters to apply to the data. These operate on additional rows in the data.
            A list of dicts of the form {'column': str, 'operator': str, 'threshold': Union[float, str]} where:
                'column' is the name of a column that occurs within the dataset
                'operator' is a comparison operator, one of '>', '<', '=', '!=', '>=', '<='
                'threshold' is the value the column will be compared against.
            These conditions are applied to the data using logical AND.

        Raises
        ------
        RuntimeError
            If the query failed for some reason.

        Returns
        -------
        Tuple[gpd.GeoDataFrame, Dict]
            The data resulting from the query
            Metadata for the query, including a list of sources for the data
        """
        # note the use of json.loads() here, so effectively converting the geojson
        # back into a dictionary of JSON-compatible types to avoid "double-JSONing" it.
        ws = simple_websocket.Client(
            self.server_url.replace("http://", "ws://") + "/query",
            headers={"Authorization": "Bearer " + self.auth_token})
        _websocket_helpers.send_object_to_websocket(ws, {
            'dataset_id': dataset_id,
            'min_timestamp': int(min_datetime.timestamp()),
            'max_timestamp': int(max_datetime.timestamp()),
            'epsg4326_search_area': json.loads(to_geojson(epsg4326_polygon)),
            'columns_to_return': columns_to_return,
            'additional_filters': additional_filters})

        response = _websocket_helpers.receive_object_from_websocket(ws, self._data_streaming_timeout_s)
        if response['status'] == HTTPStatus.OK:
            _log.info('queried dataset with ID %s.', dataset_id)
            return response['gdf'], response['sources']
        else:
            _log.error('Failed to interact with Specklia server, error was %s', str(response))
            raise RuntimeError(str(response))

    def update_points_in_dataset(
            self: Specklia, _dataset_id: str, _new_points: pd.DataFrame, _source_description: Dict) -> None:
        """
        Update previously existing data within a dataset.

        You must have READ_WRITE or ADMIN permissions within the group that owns the dataset in order to do this.
        Should be called once for each separate source of data.

        Parameters
        ------
        _dataset_id : str
            The UUID of the dataset to update.
        _new_points : pd.DataFrame
            A dataframe containing the new values for the points.
            The columns within this dataframe must match the columns within the dataset.
            In particular, the row_id column must match row_ids that already occur within the dataset,
            as this indicates which points will be replaced.
        _source_description : Dict
            A dictionary describing the source of the data.

        Raises
        ------
        NotImplementedError
            This route is not yet implemented.
        """
        _log.error('this method is not yet implemented.')
        raise NotImplementedError()

    def add_points_to_dataset(
            self: Specklia, dataset_id: str, new_points: gpd.GeoDataFrame, source_description: Dict) -> None:
        """
        Add new data to a dataset.

        You must have READ_WRITE or ADMIN permissions within the group that owns the dataset in order to do this.

        Note that Ingests are temporarily restricted to those that have READ_WRITE permissions
        within the all_users group (i.e. Specklia is read-only to the general public).
        This restriction will be lifted once we have per-user billing in place for Specklia.

        Parameters
        ----------
        dataset_id : str
            The UUID of the dataset to add data to.
        new_points : gpd.GeoDataFrame
            A GeoDataFrame containing the points to add to the dataset.
            Must contain at minimum the columns 'geometry' and 'timestamp'.
            The timestamp column must contain POSIX timestamps.
            Must have its CRS specified as EPSG 4326.
        source_description : Dict
            A dictionary describing the source of the data.

        Raises
        ------
        RuntimeError
            If the ingest failed for some reason.
        """
        ws = simple_websocket.Client(
            self.server_url.replace("http://", "ws://") + "/ingest",
            headers={"Authorization": "Bearer " + self.auth_token})

        _websocket_helpers.send_object_to_websocket(ws, {
            'dataset_id': dataset_id,
            'gdf': new_points,
            'source': source_description})

        response = _websocket_helpers.receive_object_from_websocket(ws, self._data_streaming_timeout_s)
        if response['status'] == HTTPStatus.OK:
            _log.info('Added new data to specklia dataset ID %s.', dataset_id)
        else:
            _log.error('Failed to interact with Specklia server, error was %s', str(response))
            raise RuntimeError(str(response))

    def delete_points_in_dataset(self: Specklia, _dataset_id: str, _row_ids_to_delete: List[str]) -> None:
        """
        Delete data from a dataset.

        You must have READ_WRITE or ADMIN permissions within the group that owns the dataset in order to do this.
        Note that this does not delete the dataset itself. Instead, this method is for deleting specific rows within
        the dataset.

        Parameters
        ----------
        _dataset_id : str
            The UUID of the dataset to delete data from.
        _row_ids_to_delete : List[str]
            A list of row_ids indicating which rows of data to delete.

        Raises
        ------
        NotImplementedError
            This route is not yet implemented.
        """
        _log.error('this method is not yet implemented.')
        raise NotImplementedError()

    def list_all_groups(self: Specklia) -> pd.DataFrame:
        """
        List all groups.

        You must have ADMIN permissions within the special all_users group in order to do this.

        Returns
        -------
        pd.DataFrame
            A dataframe describing all groups
        """
        response = requests.get(
            self.server_url + "/groups", headers={"Authorization": "Bearer " + self.auth_token})
        _check_response_ok(response)
        _log.info('listing all groups within Specklia.')
        return pd.DataFrame(response.json()).convert_dtypes()

    def create_group(self: Specklia, group_name: str) -> str:
        """
        Create a new Specklia group.

        If you want to share a specific group of datasets with a specific group of users, you should create a
        Specklia group to do so, then use Specklia.add_user_to_group() and Specklia.update_dataset_ownership()
        to move users and datasets respectively into the group.

        Parameters
        ----------
        group_name : str
            The new group's name. Must contain alphanumeric characters, spaces, underscores and hyphens only.

        Returns
        -------
        str
            The unique ID of the newly created group
        """
        response = requests.post(self.server_url + "/groups", json={'group_name': group_name},
                                 headers={"Authorization": "Bearer " + self.auth_token})
        _check_response_ok(response)
        _log.info('created new group with name %s.', group_name)
        return response.text.strip('\n"')

    def update_group_name(self: Specklia, group_id: str, new_group_name: str) -> str:
        """
        Update the name of a group.

        You must have ADMIN permissions within the group in order to do this.

        Parameters
        ----------
        group_id : str
            UUID of group
        new_group_name : str
            Desired new name of group. Must contain alphanumeric characters, spaces, underscores and hyphens only.

        Returns
        -------
        str
            Response from server
        """
        response = requests.put(
            self.server_url + "/groups",
            json={'group_id': group_id, 'new_group_name': new_group_name},
            headers={"Authorization": "Bearer " + self.auth_token})
        _check_response_ok(response)
        _log.info('updated name of group ID %s to %s.', group_id, new_group_name)
        return response.text.strip('\n"')

    def delete_group(self: Specklia, group_id: str) -> str:
        """
        Delete an existing group.

        You must have ADMIN permissions within the group in order to do this.

        Parameters
        ----------
        group_id : str
            The UUID of group to delete

        Returns
        -------
        str
            The response from the server.
        """
        response = requests.delete(
            self.server_url + "/groups", headers={"Authorization": "Bearer " + self.auth_token},
            json={'group_id': group_id})
        _check_response_ok(response)
        _log.info('deleted group ID %s', group_id)
        return response.text.strip('\n"')

    def list_groups(self: Specklia) -> pd.DataFrame:
        """
        List all of the groups that you are part of.

        Returns
        -------
        pd.DataFrame
            A dataframe describing the groups the user is part of.
        """
        response = requests.get(
            self.server_url + "/groupmembership", headers={"Authorization": "Bearer " + self.auth_token})
        _check_response_ok(response)
        _log.info('listed groups that user is part of.')
        return pd.DataFrame(response.json()).convert_dtypes()

    def add_user_to_group(self: Specklia, group_id: str, user_to_add_id: str) -> str:
        """
        Add a user to an existing group.

        You must have ADMIN permissions within the group in order to do this.
        The user will initially be granted READ_ONLY permissions within the group.
        Use Specklia.update_user_privileges() to change this after you have moved them into the group.

        Parameters
        ----------
        group_id: str
            The group's UUID

        user_to_add_id : str
            UUID of user to add to group

        Returns
        -------
        str
            The response from the server
        """
        response = requests.post(self.server_url + "/groupmembership",
                                 json={'group_id': group_id, "user_to_add_id": user_to_add_id},
                                 headers={"Authorization": "Bearer " + self.auth_token})
        _check_response_ok(response)
        _log.info('added user ID %s to group ID %s', user_to_add_id, group_id)
        return response.text.strip('\n"')

    def update_user_privileges(self: Specklia, group_id: str, user_to_update_id: str, new_privileges: str) -> str:
        """
        Update a user's privileges within a particular group.

        You must have ADMIN permissions within the group in order to do this.

        These privileges determine what a user can do with the datasets and users in the group:
        - READ_ONLY means that the user can read the datasets, but cannot write to them,
          or change properties of the group.
        - READ_WRITE means that the user can write to existing datasets as well as read from them,
          but cannot change the properties of the group. Users with READ_WRITE permissions cannot create or destroy
          whole datasets within a group.
        - ADMIN means that the user can add and remove other users from the group, can change their privileges,
          and can add and remove datasets from the group.

        Parameters
        ----------
        group_id : str
            The group's UUID
        user_to_update_id : str
            UUID of user to update privileges for
        new_privileges : str
            New privileges of the users. Must be 'READ_ONLY', 'READ_WRITE' or 'ADMIN'.

        Returns
        -------
        str
            Response from server
        """
        response = requests.put(
            self.server_url + "/groupmembership",
            json={'group_id': group_id,
                  "user_to_update_id": user_to_update_id,
                  'new_privileges': new_privileges},
            headers={"Authorization": "Bearer " + self.auth_token})
        _check_response_ok(response)
        _log.info('Updated user ID %s privileges to %s within group ID %s.',
                  user_to_update_id, new_privileges, group_id)
        return response.text.strip('\n"')

    def delete_user_from_group(self: Specklia, group_id: str, user_to_delete_id: str,) -> str:
        """
        Remove a user from an existing group.

        You must have ADMIN permissions within the group in order to do this.

        Parameters
        ----------
        group_id : str
            The group's UUID
        user_to_delete_id : str
            UUID of user to delete from group

        Returns
        -------
        str
            The response from the server.
        """
        response = requests.delete(
            self.server_url + "/groupmembership", headers={"Authorization": "Bearer " + self.auth_token},
            json={'group_id': group_id, "user_to_delete_id": user_to_delete_id})
        _check_response_ok(response)
        _log.info('Deleted user ID %s from group ID %s.', user_to_delete_id, group_id)
        return response.text.strip('\n"')

    def list_datasets(self: Specklia) -> pd.DataFrame:
        """
        List all of the datasets the user has permission to read.

        The output will describe datasets within all the groups that the user is part of.

        Returns
        -------
        pd.DataFrame
            A dataframe describing the datasets that the user can read.
        """
        response = requests.get(
            self.server_url + "/metadata", headers={"Authorization": "Bearer " + self.auth_token}
        )
        _check_response_ok(response)
        _log.info('listed Specklia datasets that the current user can read.')
        return pd.DataFrame(response.json()).convert_dtypes()

    def create_dataset(
            self: Specklia, dataset_name: str, description: str,
            columns: Optional(List[Dict[str, str]]) = None) -> str:
        """
        Create a dataset.

        Specklia datasets contain point cloud data.
        When you create the dataset, you must specify the fields within the data.
        After you have created the dataset, you'll probably want to add data to it
        using Specklia.add_points_to_dataset()

        When a dataset is first created, it will be owned by a group with its group_name matching your user ID.
        You have ADMIN permissions within this group. In order for other people to access this dataset, you must
        either move it into another group using Specklia.update_dataset_ownership(), or add a user to your personal
        group using Specklia.add_user_to_group().

        Parameters
        ---------
        dataset_name : str
            The name the user provides for the dataset.
            Must contain alphanumeric characters, spaces, underscores and hyphens only.
        description : str
            A description of the dataset.
            Must contain alphanumeric characters, spaces, underscores and hyphens only.
        columns : Optional(List[Dict[str, str]])),
            A list where each item is an additional column the user wishes to add to the dataset,
            beyond the mandatory columns of 'lat', 'lon' and 'timestamp',
            which are EPSG4326 latitude, longitude and POSIX timestamp as an integer respectively.
            A list of columns should follow the format: [
                {'name': 'elevation', 'type': 'float', 'description': 'elevation', 'unit': 'metres'},
                {'name': 'remarks', 'type': 'str', 'description': 'per-row remarks', 'unit': 'NA'}]
            Where valid values for 'type' are 'string', 'float' and 'int' and the other three fields are strings,
            which must contain alphanumeric characters, spaces, underscores and hyphens only.
            Please do not create explicit EPSG:4326 columns (e.g. 'lat', 'lon') or POSIX timestamp columns
            as these are unnecessary repetitions of Specklia default columns.

        Returns
        -------
        str
            The unique ID of the newly created dataset.
        """
        if columns and any(x in ['lat', 'lon', 'long', 'latitude', 'longitude', 'timestamp', 'posix']
                           for x in [col['name'].lower() for col in columns]):
            message = ("Please refrain from creating explicit EPSG:4326 or POSIX timestamp columns "
                       "as these are repetitious of Specklia's default columns.")
            _log.warning(message)
            warnings.warn(message, stacklevel=1)

        response = requests.post(
            self.server_url + "/metadata",
            json={'dataset_name': dataset_name,
                  'description': description,
                  'columns': columns},
            headers={"Authorization": "Bearer " + self.auth_token}
        )
        _check_response_ok(response)
        _log.info("Created a new dataset with name '%s'", dataset_name)
        return response.text.strip('\n"')

    def update_dataset_ownership(
            self: Specklia, dataset_id: str, new_owning_group_id: str) -> str:
        """
        Transfer the ownership of a dataset to a different Specklia group.

        You must have ADMIN permissions within both the group that currently owns the dataset _and_ the group into
        which you wish to transfer the dataset in order to do this.

        Parameters
        ---------
        dataset_id : str
            The UUID of the dataset the user wishes to update
        new_owning_group_id : str
            The group UUID the user wishes to change the dataset ownership tot

        Returns
        -------
        str
            The response from the server
        """
        response = requests.put(
            self.server_url + "/metadata",
            json={'dataset_id': dataset_id,
                  'new_owning_group_id': new_owning_group_id},
            headers={"Authorization": "Bearer " + self.auth_token}
        )
        _check_response_ok(response)
        _log.info('set owning group for dataset ID %s to group ID %s', dataset_id, new_owning_group_id)
        return response.text.strip('\n"')

    def delete_dataset(self: Specklia, dataset_id: str) -> str:
        """
        Delete a dataset.

        You must be an ADMIN of the group that owns the dataset in order to do this.

        Parameters
        ---------
        dataset_id : str
            The UUID of the dataset the user wishes to delete

        Returns
        -------
        str
            The response from the server
        """
        response = requests.delete(
            self.server_url + "/metadata",
            json={'dataset_id': dataset_id},
            headers={"Authorization": "Bearer " + self.auth_token}
        )
        _check_response_ok(response)
        _log.info('Deleted dataset with ID %s', dataset_id)
        return response.text.strip('\n"')


def _check_response_ok(response: requests.Response) -> None:
    """
    Check that a response is OK and raise an error if not.

    Parameters
    ----------
    response : requests.Response
        the response to check

    Raises
    ------
    RuntimeError
        If the Specklia server did not behave as expected.
    """
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        try:
            response_content = response.json()
        except requests.exceptions.JSONDecodeError:
            response_content = response.text
        _log.error('Failed to interact with Specklia server, error was: %s, %s', str(err), response_content)
        raise RuntimeError(
            f"Failed to interact with Specklia server, error was: {str(err)}, {response_content}") from None
