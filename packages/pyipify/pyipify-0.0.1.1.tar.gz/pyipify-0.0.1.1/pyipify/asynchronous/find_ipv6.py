"""This module contains the asynchronous function for finding the public IPv6 address"""
import aiohttp


async def find_ipv6():
    """Return the public IPv6 address of the system.
    This function is asynchronous.

    Returns:
        str: The IPv6 address of the client.

        Example:
            >>> import asyncio
            >>> from pyipify.asynchronous import find_ipv6
            >>> asyncio.run(find_ipv6())

    """
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api6.ipify.org?format=json') as response:
            return (await response.json())['ip']
