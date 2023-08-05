#
# Copyright 2023 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
# pylint: disable=too-many-lines
from __future__ import annotations

import enum
import inspect
from typing import Any, Dict, List, Optional, TYPE_CHECKING, Union

from mypy_extensions import TypedDict
import trafaret as t

from datarobot._compat import Int, String
from datarobot.utils.pagination import unpaginate

from .api_object import APIObject

if TYPE_CHECKING:
    from ..models.project import Project


class DataSliceFiltersType(TypedDict):
    operand: str
    operator: str
    values: List[Union[str, int, float]]


class DataSlicesOperators(str, enum.Enum):
    EQUAL = "eq"
    CONTAINS = "in"
    LESS_THAN = "<"
    GREATER_THAN = ">"

    @classmethod
    def values_to_list(cls) -> List[str]:
        return [e.value for e in cls]


class DataSlice(APIObject):
    """
    Definition of a data slice

    Attributes
    -----------
    id : str
        The ID of the data slice
    name : str
        The name of the data slice definition
    filters : list[DataSliceFiltersType]
        The list of filters (dict) with params:
        - operand : str
            Name of the feature to use in the filter
        - operator : str
            Operator to use in the filter: 'eq', 'in', '<', '>'
        - values : Union[str, int, float]
            Values to use from the feature
    project_id : str
        The ID of the project that the model is part of
    """

    _base_data_slices_path_template = "dataSlices/"

    FilterDataSlicesDefinition = t.Dict(
        {
            t.Key("operand"): String,
            t.Key("operator"): t.Enum(*DataSlicesOperators.values_to_list()),
            t.Key("values"): t.List(t.Or(String, Int, t.Float), min_length=1, max_length=1000),
        }
    )

    _converter = t.Dict(
        {
            t.Key("id", optional=True): String,
            t.Key("name", optional=True): String,
            t.Key("filters", optional=True): t.List(
                FilterDataSlicesDefinition, min_length=1, max_length=3
            ),
            t.Key("project_id", optional=True): String,
        }
    ).ignore_extra("*")

    def __init__(
        self,
        id: Optional[str] = None,
        name: Optional[str] = None,
        filters: Optional[List[DataSliceFiltersType]] = None,
        project_id: Optional[str] = None,
    ) -> None:
        self.id = id
        self.name = name
        self.filters = filters
        self.project_id = project_id

    def __repr__(self) -> str:
        slice_dict = self.to_dict()
        data = ", ".join(f"{key}={value}" for key, value in slice_dict.items())
        return f"DataSlice({data})"

    def to_dict(self) -> Dict[str, Any]:
        return {
            attr[0]: attr[1]
            for attr in inspect.getmembers(self)
            if (
                not attr[0].startswith("_")
                and not inspect.ismethod(attr[1])
                and not isinstance(attr[1], type(self.FilterDataSlicesDefinition))
            )
        }

    @classmethod
    def list(
        cls,
        project: Union[str, Project],
        offset: Optional[int] = 0,
        limit: Optional[int] = 100,
    ) -> List[DataSlice]:
        """
        List the data slices in the same project

        Parameters
        ----------
        project : Union[str, Project]
          The ID of the project from which to list data slices,
          OR a Project object with project.id
        offset : int, optional
          The number of items to skip.
        limit : int, optional
          The number of items to return.

        Returns
        -------
        data_slices : list[DataSlice]
        """
        project_id = project if isinstance(project, str) else project.id
        url = f"projects/{project_id}/{cls._base_data_slices_path_template}"
        query_params: Dict[str, Union[Optional[int], Optional[str]]] = {
            "offset": offset,
            "limit": limit,
        }
        data_slices = [
            cls.from_server_data(item) for item in unpaginate(url, query_params, cls._client)
        ]

        return data_slices

    @classmethod
    def create(
        cls, name: str, filters: List[DataSliceFiltersType], project: Union[str, Project]
    ) -> DataSlice:
        """
        Creates a data slice in the project with the given name and filters

        Parameters
        -----------
        name : str
            Name of the data slice definition
        filters : list[DataSliceFiltersType]
            List of filters (dict) with params:
            - operand : str
                name of feature to use in filter
            - operator : str
                operator to use: 'eq', 'in', '<', '>'
            - values : Union[str, int, float]
                values to use from the feature
        project : Union[str, Project]
          The project id from which to list data slices,
          OR a Project object with project.id

        Returns
        -------
        data_slice : DataSlice
            The data slice object created
        """
        project_id = project if isinstance(project, str) else project.id
        data = {"name": name, "filters": filters, "project_id": project_id}
        response = cls._client.post(cls._base_data_slices_path_template, data=data)
        response_json = response.json()
        data_slice = DataSlice.from_server_data(response_json)
        return data_slice
