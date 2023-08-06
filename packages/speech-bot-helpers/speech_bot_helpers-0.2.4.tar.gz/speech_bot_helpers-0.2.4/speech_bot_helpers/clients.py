from contextlib import asynccontextmanager
from io import BytesIO
from typing import AsyncGenerator

from aiobotocore.session import AioSession, get_session
from speech_bot_helpers.exceptions import S3ClientException
from speech_bot_helpers.wrappers import catch


class S3File:
    def __init__(self, file: BytesIO, key: str) -> None:
        self.file = file
        self.key = key


class S3:
    def __init__(
        self,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        s3_endpoint_url: str,
        region: str = "",
    ) -> None:
        self._aws_access_key_id = aws_access_key_id
        self._aws_secret_access_key = aws_secret_access_key
        self._region = region
        self._s3_endpoint_url = s3_endpoint_url

    @asynccontextmanager
    async def _connect(self) -> AsyncGenerator[AioSession, None]:
        session = get_session()
        async with session.create_client(
            service_name="s3",
            region_name=self._region,
            endpoint_url=self._s3_endpoint_url,
            aws_secret_access_key=self._aws_secret_access_key,
            aws_access_key_id=self._aws_access_key_id,
        ) as s3_client:
            yield s3_client

    @catch
    async def create_bucket(self, name: str) -> dict:
        async with self._connect() as client:
            return await client.create_bucket(Bucket=name)

    @catch
    async def get_obj(self, bucket_name: str, key: str) -> dict:
        async with self._connect() as client:
            res = await client.get_object(Bucket=bucket_name, Key=key)
            async with res["Body"] as stream:
                return {
                    "body": await stream.read(),
                    "headers": res["ResponseMetadata"]["HTTPHeaders"],
                }

    @catch
    async def delete_obj(self, bucket_name: str, key: str) -> None:
        async with self._connect() as client:
            await client.delete_object(Bucket=bucket_name, Key=key)

    @catch
    async def upload_obj(self, bucket_name: str, file: S3File) -> None:
        async with self._connect() as client:
            res = await client.put_object(
                ACL="public-read", Bucket=bucket_name, Key=file.key, Body=file.file
            )

            if not res["ResponseMetadata"]["HTTPStatusCode"] == 200:
                raise S3ClientException

    # TODO add exception handling
    async def upload_bulk(self, bucket_name: str, files: list[S3File]) -> None:
        async with self._connect() as client:
            for file in files:
                await client.put_object(
                    ACL="public-read", Bucket=bucket_name, Key=file.key, Body=file.file
                )
