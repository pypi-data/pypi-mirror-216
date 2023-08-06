import asyncio
import functools
import typing


def is_async_callable(obj: typing.Any) -> bool:
    while isinstance(obj, functools.partial):
        obj = obj.func

    return asyncio.iscoroutinefunction(obj) or (
        callable(obj) and asyncio.iscoroutinefunction(obj.__call__)
    )


def get_handler_name(message):
    """
    Looks at a message, checks it has a sensible type, and returns the
    handler name for that type.
    """
    # Check message looks OK
    if "type" not in message:
        raise ValueError("Incoming message has no 'type' attribute")
    # Extract type and replace . with _
    handler_name = message["type"].replace(".", "_")
    if handler_name.startswith("_"):
        raise ValueError("Malformed type in message (leading underscore)")
    return handler_name
