from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.search_results_video import SearchResultsVideo
from ...types import UNSET, Response, Unset


def _get_kwargs(
    album: str,
    *,
    client: AuthenticatedClient,
    q: Union[Unset, None, str] = UNSET,
    caption: Union[Unset, None, str] = UNSET,
    token: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, int] = 1,
    page_size: Union[Unset, None, int] = 100,
) -> Dict[str, Any]:
    url = "{}/albums/{album}/videos".format(client.base_url, album=album)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["q"] = q

    params["caption"] = caption

    params["token"] = token

    params["page"] = page

    params["page_size"] = page_size

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Any, SearchResultsVideo]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = SearchResultsVideo.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = cast(Any, None)
        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Any, SearchResultsVideo]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    album: str,
    *,
    client: AuthenticatedClient,
    q: Union[Unset, None, str] = UNSET,
    caption: Union[Unset, None, str] = UNSET,
    token: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, int] = 1,
    page_size: Union[Unset, None, int] = 100,
) -> Response[Union[Any, SearchResultsVideo]]:
    """Video Find

     Find a video by filename, caption or token

    Args:
        album (str):
        q (Union[Unset, None, str]):
        caption (Union[Unset, None, str]):
        token (Union[Unset, None, str]):
        page (Union[Unset, None, int]):  Default: 1.
        page_size (Union[Unset, None, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, SearchResultsVideo]]
    """

    kwargs = _get_kwargs(
        album=album,
        client=client,
        q=q,
        caption=caption,
        token=token,
        page=page,
        page_size=page_size,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    album: str,
    *,
    client: AuthenticatedClient,
    q: Union[Unset, None, str] = UNSET,
    caption: Union[Unset, None, str] = UNSET,
    token: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, int] = 1,
    page_size: Union[Unset, None, int] = 100,
) -> Optional[Union[Any, SearchResultsVideo]]:
    """Video Find

     Find a video by filename, caption or token

    Args:
        album (str):
        q (Union[Unset, None, str]):
        caption (Union[Unset, None, str]):
        token (Union[Unset, None, str]):
        page (Union[Unset, None, int]):  Default: 1.
        page_size (Union[Unset, None, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, SearchResultsVideo]
    """

    return sync_detailed(
        album=album,
        client=client,
        q=q,
        caption=caption,
        token=token,
        page=page,
        page_size=page_size,
    ).parsed


async def asyncio_detailed(
    album: str,
    *,
    client: AuthenticatedClient,
    q: Union[Unset, None, str] = UNSET,
    caption: Union[Unset, None, str] = UNSET,
    token: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, int] = 1,
    page_size: Union[Unset, None, int] = 100,
) -> Response[Union[Any, SearchResultsVideo]]:
    """Video Find

     Find a video by filename, caption or token

    Args:
        album (str):
        q (Union[Unset, None, str]):
        caption (Union[Unset, None, str]):
        token (Union[Unset, None, str]):
        page (Union[Unset, None, int]):  Default: 1.
        page_size (Union[Unset, None, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, SearchResultsVideo]]
    """

    kwargs = _get_kwargs(
        album=album,
        client=client,
        q=q,
        caption=caption,
        token=token,
        page=page,
        page_size=page_size,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    album: str,
    *,
    client: AuthenticatedClient,
    q: Union[Unset, None, str] = UNSET,
    caption: Union[Unset, None, str] = UNSET,
    token: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, int] = 1,
    page_size: Union[Unset, None, int] = 100,
) -> Optional[Union[Any, SearchResultsVideo]]:
    """Video Find

     Find a video by filename, caption or token

    Args:
        album (str):
        q (Union[Unset, None, str]):
        caption (Union[Unset, None, str]):
        token (Union[Unset, None, str]):
        page (Union[Unset, None, int]):  Default: 1.
        page_size (Union[Unset, None, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, SearchResultsVideo]
    """

    return (
        await asyncio_detailed(
            album=album,
            client=client,
            q=q,
            caption=caption,
            token=token,
            page=page,
            page_size=page_size,
        )
    ).parsed
