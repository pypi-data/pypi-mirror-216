from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.body_video_upload_albums_album_videos_post import BodyVideoUploadAlbumsAlbumVideosPost
from ...models.http_validation_error import HTTPValidationError
from ...models.video import Video
from ...types import UNSET, Response, Unset


def _get_kwargs(
    album: str,
    *,
    client: AuthenticatedClient,
    multipart_data: BodyVideoUploadAlbumsAlbumVideosPost,
    caption: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/albums/{album}/videos".format(client.base_url, album=album)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["caption"] = caption

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    multipart_multipart_data = multipart_data.to_multipart()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "files": multipart_multipart_data,
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Any, HTTPValidationError, Video]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Video.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Any, HTTPValidationError, Video]]:
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
    multipart_data: BodyVideoUploadAlbumsAlbumVideosPost,
    caption: Union[Unset, None, str] = UNSET,
) -> Response[Union[Any, HTTPValidationError, Video]]:
    """Video Upload

     Upload a video to album

    Args:
        album (str):
        caption (Union[Unset, None, str]):
        multipart_data (BodyVideoUploadAlbumsAlbumVideosPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, Video]]
    """

    kwargs = _get_kwargs(
        album=album,
        client=client,
        multipart_data=multipart_data,
        caption=caption,
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
    multipart_data: BodyVideoUploadAlbumsAlbumVideosPost,
    caption: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Any, HTTPValidationError, Video]]:
    """Video Upload

     Upload a video to album

    Args:
        album (str):
        caption (Union[Unset, None, str]):
        multipart_data (BodyVideoUploadAlbumsAlbumVideosPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, Video]
    """

    return sync_detailed(
        album=album,
        client=client,
        multipart_data=multipart_data,
        caption=caption,
    ).parsed


async def asyncio_detailed(
    album: str,
    *,
    client: AuthenticatedClient,
    multipart_data: BodyVideoUploadAlbumsAlbumVideosPost,
    caption: Union[Unset, None, str] = UNSET,
) -> Response[Union[Any, HTTPValidationError, Video]]:
    """Video Upload

     Upload a video to album

    Args:
        album (str):
        caption (Union[Unset, None, str]):
        multipart_data (BodyVideoUploadAlbumsAlbumVideosPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, Video]]
    """

    kwargs = _get_kwargs(
        album=album,
        client=client,
        multipart_data=multipart_data,
        caption=caption,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    album: str,
    *,
    client: AuthenticatedClient,
    multipart_data: BodyVideoUploadAlbumsAlbumVideosPost,
    caption: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Any, HTTPValidationError, Video]]:
    """Video Upload

     Upload a video to album

    Args:
        album (str):
        caption (Union[Unset, None, str]):
        multipart_data (BodyVideoUploadAlbumsAlbumVideosPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, Video]
    """

    return (
        await asyncio_detailed(
            album=album,
            client=client,
            multipart_data=multipart_data,
            caption=caption,
        )
    ).parsed
