import datetime
from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.get_all_reimbursementcdrs_order_by import GetAllReimbursementcdrsOrderBy
from ...models.longship_error import LongshipError
from ...models.reimbursement_cdr_dto import ReimbursementCdrDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    skip: Union[Unset, None, int] = UNSET,
    take: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    providerexclude: Union[Unset, None, str] = UNSET,
    order_by: Union[Unset, None, GetAllReimbursementcdrsOrderBy] = GetAllReimbursementcdrsOrderBy.STARTDATETIME,
    descending: Union[Unset, None, bool] = UNSET,
    from_: Union[Unset, None, datetime.datetime] = UNSET,
    to: Union[Unset, None, datetime.datetime] = UNSET,
) -> Dict[str, Any]:
    url = "{}/v1/reimbursementcdrs".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["skip"] = skip

    params["take"] = take

    params["search"] = search

    params["providerexclude"] = providerexclude

    json_order_by: Union[Unset, None, str] = UNSET
    if not isinstance(order_by, Unset):
        json_order_by = order_by.value if order_by else None

    params["orderBy"] = json_order_by

    params["descending"] = descending

    json_from_: Union[Unset, None, str] = UNSET
    if not isinstance(from_, Unset):
        json_from_ = from_.isoformat() if from_ else None

    params["from"] = json_from_

    json_to: Union[Unset, None, str] = UNSET
    if not isinstance(to, Unset):
        json_to = to.isoformat() if to else None

    params["to"] = json_to

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


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[List["ReimbursementCdrDto"], LongshipError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for componentsschemasreimbursement_cdr_dto_array_item_data in _response_200:
            componentsschemasreimbursement_cdr_dto_array_item = ReimbursementCdrDto.from_dict(
                componentsschemasreimbursement_cdr_dto_array_item_data
            )

            response_200.append(componentsschemasreimbursement_cdr_dto_array_item)

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


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[List["ReimbursementCdrDto"], LongshipError]]:
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
    providerexclude: Union[Unset, None, str] = UNSET,
    order_by: Union[Unset, None, GetAllReimbursementcdrsOrderBy] = GetAllReimbursementcdrsOrderBy.STARTDATETIME,
    descending: Union[Unset, None, bool] = UNSET,
    from_: Union[Unset, None, datetime.datetime] = UNSET,
    to: Union[Unset, None, datetime.datetime] = UNSET,
) -> Response[Union[List["ReimbursementCdrDto"], LongshipError]]:
    """Get a list of reimbursementcdrs.

     Get a paged list of reimbursementcdrs, taken the filters into account.

    Args:
        skip (Union[Unset, None, int]):
        take (Union[Unset, None, int]):
        search (Union[Unset, None, str]):
        providerexclude (Union[Unset, None, str]):
        order_by (Union[Unset, None, GetAllReimbursementcdrsOrderBy]):  Default:
            GetAllReimbursementcdrsOrderBy.STARTDATETIME.
        descending (Union[Unset, None, bool]):
        from_ (Union[Unset, None, datetime.datetime]):
        to (Union[Unset, None, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[List['ReimbursementCdrDto'], LongshipError]]
    """

    kwargs = _get_kwargs(
        client=client,
        skip=skip,
        take=take,
        search=search,
        providerexclude=providerexclude,
        order_by=order_by,
        descending=descending,
        from_=from_,
        to=to,
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
    providerexclude: Union[Unset, None, str] = UNSET,
    order_by: Union[Unset, None, GetAllReimbursementcdrsOrderBy] = GetAllReimbursementcdrsOrderBy.STARTDATETIME,
    descending: Union[Unset, None, bool] = UNSET,
    from_: Union[Unset, None, datetime.datetime] = UNSET,
    to: Union[Unset, None, datetime.datetime] = UNSET,
) -> Optional[Union[List["ReimbursementCdrDto"], LongshipError]]:
    """Get a list of reimbursementcdrs.

     Get a paged list of reimbursementcdrs, taken the filters into account.

    Args:
        skip (Union[Unset, None, int]):
        take (Union[Unset, None, int]):
        search (Union[Unset, None, str]):
        providerexclude (Union[Unset, None, str]):
        order_by (Union[Unset, None, GetAllReimbursementcdrsOrderBy]):  Default:
            GetAllReimbursementcdrsOrderBy.STARTDATETIME.
        descending (Union[Unset, None, bool]):
        from_ (Union[Unset, None, datetime.datetime]):
        to (Union[Unset, None, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[List['ReimbursementCdrDto'], LongshipError]
    """

    return sync_detailed(
        client=client,
        skip=skip,
        take=take,
        search=search,
        providerexclude=providerexclude,
        order_by=order_by,
        descending=descending,
        from_=from_,
        to=to,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    skip: Union[Unset, None, int] = UNSET,
    take: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    providerexclude: Union[Unset, None, str] = UNSET,
    order_by: Union[Unset, None, GetAllReimbursementcdrsOrderBy] = GetAllReimbursementcdrsOrderBy.STARTDATETIME,
    descending: Union[Unset, None, bool] = UNSET,
    from_: Union[Unset, None, datetime.datetime] = UNSET,
    to: Union[Unset, None, datetime.datetime] = UNSET,
) -> Response[Union[List["ReimbursementCdrDto"], LongshipError]]:
    """Get a list of reimbursementcdrs.

     Get a paged list of reimbursementcdrs, taken the filters into account.

    Args:
        skip (Union[Unset, None, int]):
        take (Union[Unset, None, int]):
        search (Union[Unset, None, str]):
        providerexclude (Union[Unset, None, str]):
        order_by (Union[Unset, None, GetAllReimbursementcdrsOrderBy]):  Default:
            GetAllReimbursementcdrsOrderBy.STARTDATETIME.
        descending (Union[Unset, None, bool]):
        from_ (Union[Unset, None, datetime.datetime]):
        to (Union[Unset, None, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[List['ReimbursementCdrDto'], LongshipError]]
    """

    kwargs = _get_kwargs(
        client=client,
        skip=skip,
        take=take,
        search=search,
        providerexclude=providerexclude,
        order_by=order_by,
        descending=descending,
        from_=from_,
        to=to,
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
    providerexclude: Union[Unset, None, str] = UNSET,
    order_by: Union[Unset, None, GetAllReimbursementcdrsOrderBy] = GetAllReimbursementcdrsOrderBy.STARTDATETIME,
    descending: Union[Unset, None, bool] = UNSET,
    from_: Union[Unset, None, datetime.datetime] = UNSET,
    to: Union[Unset, None, datetime.datetime] = UNSET,
) -> Optional[Union[List["ReimbursementCdrDto"], LongshipError]]:
    """Get a list of reimbursementcdrs.

     Get a paged list of reimbursementcdrs, taken the filters into account.

    Args:
        skip (Union[Unset, None, int]):
        take (Union[Unset, None, int]):
        search (Union[Unset, None, str]):
        providerexclude (Union[Unset, None, str]):
        order_by (Union[Unset, None, GetAllReimbursementcdrsOrderBy]):  Default:
            GetAllReimbursementcdrsOrderBy.STARTDATETIME.
        descending (Union[Unset, None, bool]):
        from_ (Union[Unset, None, datetime.datetime]):
        to (Union[Unset, None, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[List['ReimbursementCdrDto'], LongshipError]
    """

    return (
        await asyncio_detailed(
            client=client,
            skip=skip,
            take=take,
            search=search,
            providerexclude=providerexclude,
            order_by=order_by,
            descending=descending,
            from_=from_,
            to=to,
        )
    ).parsed
