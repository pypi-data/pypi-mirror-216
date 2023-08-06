import datetime
from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.longship_error import LongshipError
from ...models.message_log_dto import MessageLogDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    client: Client,
    skip: Union[Unset, None, int] = UNSET,
    take: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    from_: Union[Unset, None, datetime.datetime] = UNSET,
    to: Union[Unset, None, datetime.datetime] = UNSET,
    transaction_id: Union[Unset, None, str] = UNSET,
    response_only: Union[Unset, None, bool] = UNSET,
    request_only: Union[Unset, None, bool] = UNSET,
    charger_to_cpo_only: Union[Unset, None, bool] = UNSET,
    cpo_to_charger_only: Union[Unset, None, bool] = UNSET,
    message_id: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/v1/chargepoints/{id}/messages".format(client.base_url, id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["skip"] = skip

    params["take"] = take

    params["search"] = search

    json_from_: Union[Unset, None, str] = UNSET
    if not isinstance(from_, Unset):
        json_from_ = from_.isoformat() if from_ else None

    params["from"] = json_from_

    json_to: Union[Unset, None, str] = UNSET
    if not isinstance(to, Unset):
        json_to = to.isoformat() if to else None

    params["to"] = json_to

    params["transactionId"] = transaction_id

    params["responseOnly"] = response_only

    params["requestOnly"] = request_only

    params["chargerToCpoOnly"] = charger_to_cpo_only

    params["cpoToChargerOnly"] = cpo_to_charger_only

    params["messageId"] = message_id

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
) -> Optional[Union[List["MessageLogDto"], LongshipError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for componentsschemasmessage_log_dto_array_item_data in _response_200:
            componentsschemasmessage_log_dto_array_item = MessageLogDto.from_dict(
                componentsschemasmessage_log_dto_array_item_data
            )

            response_200.append(componentsschemasmessage_log_dto_array_item)

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
) -> Response[Union[List["MessageLogDto"], LongshipError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: Client,
    skip: Union[Unset, None, int] = UNSET,
    take: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    from_: Union[Unset, None, datetime.datetime] = UNSET,
    to: Union[Unset, None, datetime.datetime] = UNSET,
    transaction_id: Union[Unset, None, str] = UNSET,
    response_only: Union[Unset, None, bool] = UNSET,
    request_only: Union[Unset, None, bool] = UNSET,
    charger_to_cpo_only: Union[Unset, None, bool] = UNSET,
    cpo_to_charger_only: Union[Unset, None, bool] = UNSET,
    message_id: Union[Unset, None, str] = UNSET,
) -> Response[Union[List["MessageLogDto"], LongshipError]]:
    """Get a list of chargepointmessages.

     Get a paged list of chargepointmessages, taken the filters into account.

    Args:
        id (str):
        skip (Union[Unset, None, int]):
        take (Union[Unset, None, int]):
        search (Union[Unset, None, str]):
        from_ (Union[Unset, None, datetime.datetime]):
        to (Union[Unset, None, datetime.datetime]):
        transaction_id (Union[Unset, None, str]):
        response_only (Union[Unset, None, bool]):
        request_only (Union[Unset, None, bool]):
        charger_to_cpo_only (Union[Unset, None, bool]):
        cpo_to_charger_only (Union[Unset, None, bool]):
        message_id (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[List['MessageLogDto'], LongshipError]]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        skip=skip,
        take=take,
        search=search,
        from_=from_,
        to=to,
        transaction_id=transaction_id,
        response_only=response_only,
        request_only=request_only,
        charger_to_cpo_only=charger_to_cpo_only,
        cpo_to_charger_only=cpo_to_charger_only,
        message_id=message_id,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: Client,
    skip: Union[Unset, None, int] = UNSET,
    take: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    from_: Union[Unset, None, datetime.datetime] = UNSET,
    to: Union[Unset, None, datetime.datetime] = UNSET,
    transaction_id: Union[Unset, None, str] = UNSET,
    response_only: Union[Unset, None, bool] = UNSET,
    request_only: Union[Unset, None, bool] = UNSET,
    charger_to_cpo_only: Union[Unset, None, bool] = UNSET,
    cpo_to_charger_only: Union[Unset, None, bool] = UNSET,
    message_id: Union[Unset, None, str] = UNSET,
) -> Optional[Union[List["MessageLogDto"], LongshipError]]:
    """Get a list of chargepointmessages.

     Get a paged list of chargepointmessages, taken the filters into account.

    Args:
        id (str):
        skip (Union[Unset, None, int]):
        take (Union[Unset, None, int]):
        search (Union[Unset, None, str]):
        from_ (Union[Unset, None, datetime.datetime]):
        to (Union[Unset, None, datetime.datetime]):
        transaction_id (Union[Unset, None, str]):
        response_only (Union[Unset, None, bool]):
        request_only (Union[Unset, None, bool]):
        charger_to_cpo_only (Union[Unset, None, bool]):
        cpo_to_charger_only (Union[Unset, None, bool]):
        message_id (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[List['MessageLogDto'], LongshipError]
    """

    return sync_detailed(
        id=id,
        client=client,
        skip=skip,
        take=take,
        search=search,
        from_=from_,
        to=to,
        transaction_id=transaction_id,
        response_only=response_only,
        request_only=request_only,
        charger_to_cpo_only=charger_to_cpo_only,
        cpo_to_charger_only=cpo_to_charger_only,
        message_id=message_id,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Client,
    skip: Union[Unset, None, int] = UNSET,
    take: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    from_: Union[Unset, None, datetime.datetime] = UNSET,
    to: Union[Unset, None, datetime.datetime] = UNSET,
    transaction_id: Union[Unset, None, str] = UNSET,
    response_only: Union[Unset, None, bool] = UNSET,
    request_only: Union[Unset, None, bool] = UNSET,
    charger_to_cpo_only: Union[Unset, None, bool] = UNSET,
    cpo_to_charger_only: Union[Unset, None, bool] = UNSET,
    message_id: Union[Unset, None, str] = UNSET,
) -> Response[Union[List["MessageLogDto"], LongshipError]]:
    """Get a list of chargepointmessages.

     Get a paged list of chargepointmessages, taken the filters into account.

    Args:
        id (str):
        skip (Union[Unset, None, int]):
        take (Union[Unset, None, int]):
        search (Union[Unset, None, str]):
        from_ (Union[Unset, None, datetime.datetime]):
        to (Union[Unset, None, datetime.datetime]):
        transaction_id (Union[Unset, None, str]):
        response_only (Union[Unset, None, bool]):
        request_only (Union[Unset, None, bool]):
        charger_to_cpo_only (Union[Unset, None, bool]):
        cpo_to_charger_only (Union[Unset, None, bool]):
        message_id (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[List['MessageLogDto'], LongshipError]]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        skip=skip,
        take=take,
        search=search,
        from_=from_,
        to=to,
        transaction_id=transaction_id,
        response_only=response_only,
        request_only=request_only,
        charger_to_cpo_only=charger_to_cpo_only,
        cpo_to_charger_only=cpo_to_charger_only,
        message_id=message_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: Client,
    skip: Union[Unset, None, int] = UNSET,
    take: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    from_: Union[Unset, None, datetime.datetime] = UNSET,
    to: Union[Unset, None, datetime.datetime] = UNSET,
    transaction_id: Union[Unset, None, str] = UNSET,
    response_only: Union[Unset, None, bool] = UNSET,
    request_only: Union[Unset, None, bool] = UNSET,
    charger_to_cpo_only: Union[Unset, None, bool] = UNSET,
    cpo_to_charger_only: Union[Unset, None, bool] = UNSET,
    message_id: Union[Unset, None, str] = UNSET,
) -> Optional[Union[List["MessageLogDto"], LongshipError]]:
    """Get a list of chargepointmessages.

     Get a paged list of chargepointmessages, taken the filters into account.

    Args:
        id (str):
        skip (Union[Unset, None, int]):
        take (Union[Unset, None, int]):
        search (Union[Unset, None, str]):
        from_ (Union[Unset, None, datetime.datetime]):
        to (Union[Unset, None, datetime.datetime]):
        transaction_id (Union[Unset, None, str]):
        response_only (Union[Unset, None, bool]):
        request_only (Union[Unset, None, bool]):
        charger_to_cpo_only (Union[Unset, None, bool]):
        cpo_to_charger_only (Union[Unset, None, bool]):
        message_id (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[List['MessageLogDto'], LongshipError]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            skip=skip,
            take=take,
            search=search,
            from_=from_,
            to=to,
            transaction_id=transaction_id,
            response_only=response_only,
            request_only=request_only,
            charger_to_cpo_only=charger_to_cpo_only,
            cpo_to_charger_only=cpo_to_charger_only,
            message_id=message_id,
        )
    ).parsed
