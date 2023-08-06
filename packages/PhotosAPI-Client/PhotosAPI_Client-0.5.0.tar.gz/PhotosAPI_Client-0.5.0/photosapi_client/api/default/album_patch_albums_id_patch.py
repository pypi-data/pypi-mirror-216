from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.album_modified import AlbumModified
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    client: AuthenticatedClient,
    name: Union[Unset, None, str] = UNSET,
    title: Union[Unset, None, str] = UNSET,
    cover: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/albums/{id}".format(client.base_url, id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["name"] = name

    params["title"] = title

    params["cover"] = cover

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "patch",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "params": params,
    }


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[AlbumModified, Any, HTTPValidationError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = AlbumModified.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == HTTPStatus.NOT_ACCEPTABLE:
        response_406 = cast(Any, None)
        return response_406
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[AlbumModified, Any, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    name: Union[Unset, None, str] = UNSET,
    title: Union[Unset, None, str] = UNSET,
    cover: Union[Unset, None, str] = UNSET,
) -> Response[Union[AlbumModified, Any, HTTPValidationError]]:
    """Album Patch

     Modify album's name or title by id

    Args:
        id (str):
        name (Union[Unset, None, str]):
        title (Union[Unset, None, str]):
        cover (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AlbumModified, Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        name=name,
        title=title,
        cover=cover,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: AuthenticatedClient,
    name: Union[Unset, None, str] = UNSET,
    title: Union[Unset, None, str] = UNSET,
    cover: Union[Unset, None, str] = UNSET,
) -> Optional[Union[AlbumModified, Any, HTTPValidationError]]:
    """Album Patch

     Modify album's name or title by id

    Args:
        id (str):
        name (Union[Unset, None, str]):
        title (Union[Unset, None, str]):
        cover (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AlbumModified, Any, HTTPValidationError]
    """

    return sync_detailed(
        id=id,
        client=client,
        name=name,
        title=title,
        cover=cover,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    name: Union[Unset, None, str] = UNSET,
    title: Union[Unset, None, str] = UNSET,
    cover: Union[Unset, None, str] = UNSET,
) -> Response[Union[AlbumModified, Any, HTTPValidationError]]:
    """Album Patch

     Modify album's name or title by id

    Args:
        id (str):
        name (Union[Unset, None, str]):
        title (Union[Unset, None, str]):
        cover (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AlbumModified, Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        name=name,
        title=title,
        cover=cover,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
    name: Union[Unset, None, str] = UNSET,
    title: Union[Unset, None, str] = UNSET,
    cover: Union[Unset, None, str] = UNSET,
) -> Optional[Union[AlbumModified, Any, HTTPValidationError]]:
    """Album Patch

     Modify album's name or title by id

    Args:
        id (str):
        name (Union[Unset, None, str]):
        title (Union[Unset, None, str]):
        cover (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AlbumModified, Any, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            name=name,
            title=title,
            cover=cover,
        )
    ).parsed
