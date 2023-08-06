import aiohttp
import json
from mbnk.utils import data_builder


def async_get_request(url):
    def outer(func):
        async def inner(self, *args, **kwargs):
            params = data_builder(**kwargs)

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url=url.format(
                        base_url=self.__base_url__
                    ),
                    headers=self.__headers__,
                    params=params
                ) as response:
                    response_data = await response.json()

                    return func(self, *args, **kwargs, response_data=response_data)

        return inner

    return outer


def async_post_request(url):
    def outer(func):
        async def inner(self, *args, **kwargs):
            data = data_builder(**kwargs)

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url=url.format(
                        base_url=self.__base_url__
                    ),
                    headers=self.__headers__,
                    data=json.dumps(data)
                ) as response:
                    response_data = await response.json()

                    return func(self, *args, **kwargs, response_data=response_data)

        return inner

    return outer


def async_delete_request(url):
    def outer(func):
        async def inner(self, *args, **kwargs):
            data = data_builder(**kwargs)

            async with aiohttp.ClientSession() as session:
                async with session.delete(
                    url=url.format(
                        base_url=self.__base_url__
                    ),
                    headers=self.__headers__,
                    params=data
                ) as response:
                    response_data = await response.json()

                    return func(self, *args, **kwargs, response_data=response_data)

        return inner

    return outer
