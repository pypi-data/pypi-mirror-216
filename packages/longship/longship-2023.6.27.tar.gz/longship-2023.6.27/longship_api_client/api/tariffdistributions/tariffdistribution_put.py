from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.longship_error import LongshipError
from ...models.tariff_distribution_get_dto import TariffDistributionGetDto
from ...models.tariff_distribution_put_dto import TariffDistributionPutDto
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    client: Client,
    json_body: TariffDistributionPutDto,
) -> Dict[str, Any]:
    url = "{}/v1/tariffdistributions/{id}".format(client.base_url, id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
    }


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[LongshipError, TariffDistributionGetDto]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = TariffDistributionGetDto.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = LongshipError.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = LongshipError.from_dict(response.json())

        return response_422
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = LongshipError.from_dict(response.json())

        return response_404
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
) -> Response[Union[LongshipError, TariffDistributionGetDto]]:
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
    json_body: TariffDistributionPutDto,
) -> Response[Union[LongshipError, TariffDistributionGetDto]]:
    """Updates a tariffdistribution.

     Updates a tariffdistribution.

    Args:
        id (str):
        json_body (TariffDistributionPutDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[LongshipError, TariffDistributionGetDto]]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        json_body=json_body,
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
    json_body: TariffDistributionPutDto,
) -> Optional[Union[LongshipError, TariffDistributionGetDto]]:
    """Updates a tariffdistribution.

     Updates a tariffdistribution.

    Args:
        id (str):
        json_body (TariffDistributionPutDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[LongshipError, TariffDistributionGetDto]
    """

    return sync_detailed(
        id=id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Client,
    json_body: TariffDistributionPutDto,
) -> Response[Union[LongshipError, TariffDistributionGetDto]]:
    """Updates a tariffdistribution.

     Updates a tariffdistribution.

    Args:
        id (str):
        json_body (TariffDistributionPutDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[LongshipError, TariffDistributionGetDto]]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: Client,
    json_body: TariffDistributionPutDto,
) -> Optional[Union[LongshipError, TariffDistributionGetDto]]:
    """Updates a tariffdistribution.

     Updates a tariffdistribution.

    Args:
        id (str):
        json_body (TariffDistributionPutDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[LongshipError, TariffDistributionGetDto]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            json_body=json_body,
        )
    ).parsed
