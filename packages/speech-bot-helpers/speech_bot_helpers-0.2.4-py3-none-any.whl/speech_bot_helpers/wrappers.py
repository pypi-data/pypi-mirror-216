import wrapt

from speech_bot_helpers.exceptions import S3ClientException


@wrapt.decorator  # to save func signature
def catch(func):
    async def wrapper(*args, **kwargs):
        res = await func(*args, **kwargs)

        if not hasattr(res, "__getitem__"):  # check if subscriptable
            raise S3ClientException

        status_code = res.get("ResponseMetadata", {}).get("HTTPStatusCode")
        if status_code != 200:
            raise S3ClientException

        return res

    return wrapper
