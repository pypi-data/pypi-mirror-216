from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.get_all_sessions_order_by import GetAllSessionsOrderBy
from ...models.longship_error import LongshipError
from ...models.session_dto import SessionDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    skip: Union[Unset, None, int] = UNSET,
    take: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    connector_number: Union[Unset, None, int] = UNSET,
    chargepoint_id: Union[Unset, None, str] = UNSET,
    running_only: Union[Unset, None, bool] = UNSET,
    completed_only: Union[Unset, None, bool] = UNSET,
    order_by: Union[Unset, None, GetAllSessionsOrderBy] = GetAllSessionsOrderBy.START,
    descending: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    url = "{}/v1/sessions".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["skip"] = skip

    params["take"] = take

    params["search"] = search

    params["connectorNumber"] = connector_number

    params["chargepointId"] = chargepoint_id

    params["runningOnly"] = running_only

    params["completedOnly"] = completed_only

    json_order_by: Union[Unset, None, str] = UNSET
    if not isinstance(order_by, Unset):
        json_order_by = order_by.value if order_by else None

    params["orderBy"] = json_order_by

    params["descending"] = descending

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[List["SessionDto"], LongshipError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for componentsschemassession_dto_array_item_data in _response_200:
            componentsschemassession_dto_array_item = SessionDto.from_dict(componentsschemassession_dto_array_item_data)

            response_200.append(componentsschemassession_dto_array_item)

        return response_200
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = LongshipError.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = LongshipError.from_dict(response.json())

        return response_500
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = LongshipError.from_dict(response.json())

        return response_403
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[List["SessionDto"], LongshipError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    skip: Union[Unset, None, int] = UNSET,
    take: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    connector_number: Union[Unset, None, int] = UNSET,
    chargepoint_id: Union[Unset, None, str] = UNSET,
    running_only: Union[Unset, None, bool] = UNSET,
    completed_only: Union[Unset, None, bool] = UNSET,
    order_by: Union[Unset, None, GetAllSessionsOrderBy] = GetAllSessionsOrderBy.START,
    descending: Union[Unset, None, bool] = UNSET,
) -> Response[Union[List["SessionDto"], LongshipError]]:
    """Get a list of sessions.

     Get a paged list of sessions, taken the filters into account.

    Args:
        skip (Union[Unset, None, int]):
        take (Union[Unset, None, int]):
        search (Union[Unset, None, str]):
        connector_number (Union[Unset, None, int]):
        chargepoint_id (Union[Unset, None, str]):
        running_only (Union[Unset, None, bool]):
        completed_only (Union[Unset, None, bool]):
        order_by (Union[Unset, None, GetAllSessionsOrderBy]):  Default:
            GetAllSessionsOrderBy.START.
        descending (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[List['SessionDto'], LongshipError]]
    """

    kwargs = _get_kwargs(
        client=client,
        skip=skip,
        take=take,
        search=search,
        connector_number=connector_number,
        chargepoint_id=chargepoint_id,
        running_only=running_only,
        completed_only=completed_only,
        order_by=order_by,
        descending=descending,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    skip: Union[Unset, None, int] = UNSET,
    take: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    connector_number: Union[Unset, None, int] = UNSET,
    chargepoint_id: Union[Unset, None, str] = UNSET,
    running_only: Union[Unset, None, bool] = UNSET,
    completed_only: Union[Unset, None, bool] = UNSET,
    order_by: Union[Unset, None, GetAllSessionsOrderBy] = GetAllSessionsOrderBy.START,
    descending: Union[Unset, None, bool] = UNSET,
) -> Optional[Union[List["SessionDto"], LongshipError]]:
    """Get a list of sessions.

     Get a paged list of sessions, taken the filters into account.

    Args:
        skip (Union[Unset, None, int]):
        take (Union[Unset, None, int]):
        search (Union[Unset, None, str]):
        connector_number (Union[Unset, None, int]):
        chargepoint_id (Union[Unset, None, str]):
        running_only (Union[Unset, None, bool]):
        completed_only (Union[Unset, None, bool]):
        order_by (Union[Unset, None, GetAllSessionsOrderBy]):  Default:
            GetAllSessionsOrderBy.START.
        descending (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[List['SessionDto'], LongshipError]
    """

    return sync_detailed(
        client=client,
        skip=skip,
        take=take,
        search=search,
        connector_number=connector_number,
        chargepoint_id=chargepoint_id,
        running_only=running_only,
        completed_only=completed_only,
        order_by=order_by,
        descending=descending,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    skip: Union[Unset, None, int] = UNSET,
    take: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    connector_number: Union[Unset, None, int] = UNSET,
    chargepoint_id: Union[Unset, None, str] = UNSET,
    running_only: Union[Unset, None, bool] = UNSET,
    completed_only: Union[Unset, None, bool] = UNSET,
    order_by: Union[Unset, None, GetAllSessionsOrderBy] = GetAllSessionsOrderBy.START,
    descending: Union[Unset, None, bool] = UNSET,
) -> Response[Union[List["SessionDto"], LongshipError]]:
    """Get a list of sessions.

     Get a paged list of sessions, taken the filters into account.

    Args:
        skip (Union[Unset, None, int]):
        take (Union[Unset, None, int]):
        search (Union[Unset, None, str]):
        connector_number (Union[Unset, None, int]):
        chargepoint_id (Union[Unset, None, str]):
        running_only (Union[Unset, None, bool]):
        completed_only (Union[Unset, None, bool]):
        order_by (Union[Unset, None, GetAllSessionsOrderBy]):  Default:
            GetAllSessionsOrderBy.START.
        descending (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[List['SessionDto'], LongshipError]]
    """

    kwargs = _get_kwargs(
        client=client,
        skip=skip,
        take=take,
        search=search,
        connector_number=connector_number,
        chargepoint_id=chargepoint_id,
        running_only=running_only,
        completed_only=completed_only,
        order_by=order_by,
        descending=descending,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    skip: Union[Unset, None, int] = UNSET,
    take: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    connector_number: Union[Unset, None, int] = UNSET,
    chargepoint_id: Union[Unset, None, str] = UNSET,
    running_only: Union[Unset, None, bool] = UNSET,
    completed_only: Union[Unset, None, bool] = UNSET,
    order_by: Union[Unset, None, GetAllSessionsOrderBy] = GetAllSessionsOrderBy.START,
    descending: Union[Unset, None, bool] = UNSET,
) -> Optional[Union[List["SessionDto"], LongshipError]]:
    """Get a list of sessions.

     Get a paged list of sessions, taken the filters into account.

    Args:
        skip (Union[Unset, None, int]):
        take (Union[Unset, None, int]):
        search (Union[Unset, None, str]):
        connector_number (Union[Unset, None, int]):
        chargepoint_id (Union[Unset, None, str]):
        running_only (Union[Unset, None, bool]):
        completed_only (Union[Unset, None, bool]):
        order_by (Union[Unset, None, GetAllSessionsOrderBy]):  Default:
            GetAllSessionsOrderBy.START.
        descending (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[List['SessionDto'], LongshipError]
    """

    return (
        await asyncio_detailed(
            client=client,
            skip=skip,
            take=take,
            search=search,
            connector_number=connector_number,
            chargepoint_id=chargepoint_id,
            running_only=running_only,
            completed_only=completed_only,
            order_by=order_by,
            descending=descending,
        )
    ).parsed
