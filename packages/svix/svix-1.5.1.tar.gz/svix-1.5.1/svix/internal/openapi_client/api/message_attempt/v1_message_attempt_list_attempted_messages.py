import datetime
import random
from http import HTTPStatus
from time import sleep
from typing import Any, Dict, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_error import HttpError
from ...models.http_validation_error import HTTPValidationError
from ...models.list_response_endpoint_message_out import ListResponseEndpointMessageOut
from ...models.message_status import MessageStatus
from ...types import UNSET, Response, Unset

SLEEP_TIME = 0.05
NUM_RETRIES = 3


def _get_kwargs(
    app_id: str,
    endpoint_id: str,
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, None, int] = UNSET,
    iterator: Union[Unset, None, str] = UNSET,
    channel: Union[Unset, None, str] = UNSET,
    status: Union[Unset, None, MessageStatus] = UNSET,
    before: Union[Unset, None, datetime.datetime] = UNSET,
    after: Union[Unset, None, datetime.datetime] = UNSET,
    with_content: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/api/v1/app/{app_id}/endpoint/{endpoint_id}/msg/".format(
        client.base_url, app_id=app_id, endpoint_id=endpoint_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["limit"] = limit

    params["iterator"] = iterator

    params["channel"] = channel

    json_status: Union[Unset, None, int] = UNSET
    if not isinstance(status, Unset):
        json_status = status.value if status else None

    params["status"] = json_status

    json_before: Union[Unset, None, str] = UNSET
    if not isinstance(before, Unset):
        json_before = before.isoformat() if before else None

    params["before"] = json_before

    json_after: Union[Unset, None, str] = UNSET
    if not isinstance(after, Unset):
        json_after = after.isoformat() if after else None

    params["after"] = json_after

    params["with_content"] = with_content

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


def _parse_response(*, client: Client, response: httpx.Response) -> ListResponseEndpointMessageOut:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListResponseEndpointMessageOut.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        raise HttpError.init_exception(response.json(), response.status_code)
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        raise HttpError.init_exception(response.json(), response.status_code)
    if response.status_code == HTTPStatus.FORBIDDEN:
        raise HttpError.init_exception(response.json(), response.status_code)
    if response.status_code == HTTPStatus.NOT_FOUND:
        raise HttpError.init_exception(response.json(), response.status_code)
    if response.status_code == HTTPStatus.CONFLICT:
        raise HttpError.init_exception(response.json(), response.status_code)
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        raise HTTPValidationError.init_exception(response.json(), response.status_code)
    if response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
        raise HttpError.init_exception(response.json(), response.status_code)
    raise errors.UnexpectedStatus(response.status_code, response.content)


def _build_response(*, client: Client, response: httpx.Response) -> Response[ListResponseEndpointMessageOut]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    app_id: str,
    endpoint_id: str,
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, None, int] = UNSET,
    iterator: Union[Unset, None, str] = UNSET,
    channel: Union[Unset, None, str] = UNSET,
    status: Union[Unset, None, MessageStatus] = UNSET,
    before: Union[Unset, None, datetime.datetime] = UNSET,
    after: Union[Unset, None, datetime.datetime] = UNSET,
    with_content: Union[Unset, None, bool] = False,
) -> Response[ListResponseEndpointMessageOut]:
    """List Attempted Messages

     List messages for a particular endpoint. Additionally includes metadata about the latest message
    attempt.

    The `before` parameter lets you filter all items created before a certain date and is ignored if an
    iterator is passed.

    Args:
        app_id (str): The app's ID or UID Example: unique-app-identifier.
        endpoint_id (str): The ep's ID or UID Example: unique-ep-identifier.
        limit (Union[Unset, None, int]):
        iterator (Union[Unset, None, str]): The msg's ID Example: msg_1srOrx2ZWZBpBUvZwXKQmoEYga2.
        channel (Union[Unset, None, str]):  Example: project_1337.
        status (Union[Unset, None, MessageStatus]): The sending status of the message:
            - Success = 0
            - Pending = 1
            - Fail = 2
            - Sending = 3
        before (Union[Unset, None, datetime.datetime]):
        after (Union[Unset, None, datetime.datetime]):
        with_content (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListResponseEndpointMessageOut]
    """

    kwargs = _get_kwargs(
        app_id=app_id,
        endpoint_id=endpoint_id,
        client=client,
        limit=limit,
        iterator=iterator,
        channel=channel,
        status=status,
        before=before,
        after=after,
        with_content=with_content,
    )

    kwargs["headers"] = {"svix-req-id": f"{random.getrandbits(32)}", **kwargs["headers"]}

    for retry_count in range(NUM_RETRIES):
        response = httpx.request(
            verify=client.verify_ssl,
            **kwargs,
        )
        if response.status_code >= 500:
            kwargs["headers"]["svix-retry-count"] = str(retry_count)
            sleep(SLEEP_TIME * (2**retry_count))
        else:
            break

    return _build_response(client=client, response=response)


def sync(
    app_id: str,
    endpoint_id: str,
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, None, int] = UNSET,
    iterator: Union[Unset, None, str] = UNSET,
    channel: Union[Unset, None, str] = UNSET,
    status: Union[Unset, None, MessageStatus] = UNSET,
    before: Union[Unset, None, datetime.datetime] = UNSET,
    after: Union[Unset, None, datetime.datetime] = UNSET,
    with_content: Union[Unset, None, bool] = False,
) -> ListResponseEndpointMessageOut:
    """List Attempted Messages

     List messages for a particular endpoint. Additionally includes metadata about the latest message
    attempt.

    The `before` parameter lets you filter all items created before a certain date and is ignored if an
    iterator is passed.

    Args:
        app_id (str): The app's ID or UID Example: unique-app-identifier.
        endpoint_id (str): The ep's ID or UID Example: unique-ep-identifier.
        limit (Union[Unset, None, int]):
        iterator (Union[Unset, None, str]): The msg's ID Example: msg_1srOrx2ZWZBpBUvZwXKQmoEYga2.
        channel (Union[Unset, None, str]):  Example: project_1337.
        status (Union[Unset, None, MessageStatus]): The sending status of the message:
            - Success = 0
            - Pending = 1
            - Fail = 2
            - Sending = 3
        before (Union[Unset, None, datetime.datetime]):
        after (Union[Unset, None, datetime.datetime]):
        with_content (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListResponseEndpointMessageOut
    """

    return sync_detailed(
        app_id=app_id,
        endpoint_id=endpoint_id,
        client=client,
        limit=limit,
        iterator=iterator,
        channel=channel,
        status=status,
        before=before,
        after=after,
        with_content=with_content,
    ).parsed


async def asyncio_detailed(
    app_id: str,
    endpoint_id: str,
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, None, int] = UNSET,
    iterator: Union[Unset, None, str] = UNSET,
    channel: Union[Unset, None, str] = UNSET,
    status: Union[Unset, None, MessageStatus] = UNSET,
    before: Union[Unset, None, datetime.datetime] = UNSET,
    after: Union[Unset, None, datetime.datetime] = UNSET,
    with_content: Union[Unset, None, bool] = False,
) -> Response[ListResponseEndpointMessageOut]:
    """List Attempted Messages

     List messages for a particular endpoint. Additionally includes metadata about the latest message
    attempt.

    The `before` parameter lets you filter all items created before a certain date and is ignored if an
    iterator is passed.

    Args:
        app_id (str): The app's ID or UID Example: unique-app-identifier.
        endpoint_id (str): The ep's ID or UID Example: unique-ep-identifier.
        limit (Union[Unset, None, int]):
        iterator (Union[Unset, None, str]): The msg's ID Example: msg_1srOrx2ZWZBpBUvZwXKQmoEYga2.
        channel (Union[Unset, None, str]):  Example: project_1337.
        status (Union[Unset, None, MessageStatus]): The sending status of the message:
            - Success = 0
            - Pending = 1
            - Fail = 2
            - Sending = 3
        before (Union[Unset, None, datetime.datetime]):
        after (Union[Unset, None, datetime.datetime]):
        with_content (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListResponseEndpointMessageOut]
    """

    kwargs = _get_kwargs(
        app_id=app_id,
        endpoint_id=endpoint_id,
        client=client,
        limit=limit,
        iterator=iterator,
        channel=channel,
        status=status,
        before=before,
        after=after,
        with_content=with_content,
    )

    kwargs["headers"] = {"svix-req-id": f"{random.getrandbits(32)}", **kwargs["headers"]}

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        for retry_count in range(NUM_RETRIES):
            response = await _client.request(**kwargs)
            if response.status_code >= 500:
                kwargs["headers"]["svix-retry-count"] = str(retry_count)
                sleep(SLEEP_TIME * (2**retry_count))
            else:
                break

    return _build_response(client=client, response=response)


async def asyncio(
    app_id: str,
    endpoint_id: str,
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, None, int] = UNSET,
    iterator: Union[Unset, None, str] = UNSET,
    channel: Union[Unset, None, str] = UNSET,
    status: Union[Unset, None, MessageStatus] = UNSET,
    before: Union[Unset, None, datetime.datetime] = UNSET,
    after: Union[Unset, None, datetime.datetime] = UNSET,
    with_content: Union[Unset, None, bool] = False,
) -> ListResponseEndpointMessageOut:
    """List Attempted Messages

     List messages for a particular endpoint. Additionally includes metadata about the latest message
    attempt.

    The `before` parameter lets you filter all items created before a certain date and is ignored if an
    iterator is passed.

    Args:
        app_id (str): The app's ID or UID Example: unique-app-identifier.
        endpoint_id (str): The ep's ID or UID Example: unique-ep-identifier.
        limit (Union[Unset, None, int]):
        iterator (Union[Unset, None, str]): The msg's ID Example: msg_1srOrx2ZWZBpBUvZwXKQmoEYga2.
        channel (Union[Unset, None, str]):  Example: project_1337.
        status (Union[Unset, None, MessageStatus]): The sending status of the message:
            - Success = 0
            - Pending = 1
            - Fail = 2
            - Sending = 3
        before (Union[Unset, None, datetime.datetime]):
        after (Union[Unset, None, datetime.datetime]):
        with_content (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListResponseEndpointMessageOut
    """

    return (
        await asyncio_detailed(
            app_id=app_id,
            endpoint_id=endpoint_id,
            client=client,
            limit=limit,
            iterator=iterator,
            channel=channel,
            status=status,
            before=before,
            after=after,
            with_content=with_content,
        )
    ).parsed
