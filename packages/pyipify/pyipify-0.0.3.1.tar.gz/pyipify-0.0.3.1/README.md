
# Pyipify

ipify-py is a python module that allows you to interact with the ipify API in synchronous and asynchronous ways. It also provides a command-line interface for easy access.

The ipify API is a simple service that returns your public IP address. You can use it to find out your IP address from any device or platform.





![languages](https://img.shields.io/github/languages/count/SigireddyBalasai/Pyipify)
![SearchHits](https://img.shields.io/github/search/SigireddyBalasai/Pyipify/ipify)
![Top Language](https://img.shields.io/github/languages/top/SigireddyBalasai/Pyipify)
![Dependencies Status](https://img.shields.io/librariesio/github/SigireddyBalasai/Pyipify)
![Total Issues](https://img.shields.io/github/issues/SigireddyBalasai/pyipify)
![Open Issues](https://img.shields.io/github/issues-raw/SigireddyBalasai/Pyipify)
![License](https://img.shields.io/github/license/SigireddyBalasai/Pyipify)


## Features

- Supports both IPv4 and IPv6 addresses
- Supports both sync and async requests using requests and aiohttp libraries
- Provides a CLI tool to get your IP address from the terminal
- Provides a simple and intuitive interface
## Installation

Install my-project with npm

```py
pip install Pyipify
```


    
## Examples

get ip address synchronous

```py
from Pyipify.synchronous import find_ipv4,find_ipv6
ipv4_address = find_ipv4()
ipv6_address = find_ipv6()
print(ipv4_address,ipv6_address)
```

get ip address asynchronously
```py
from Pyipify.asynchronous import find_ipv4,find_ipv6
import asyncio
async def main():
    ipv4_address = await find_ipv4()
    ipv6_address = await find_ipv6()
    return ipv4_address,ipv6_address
asyncio.run(main())
```

use cli to get ip address
``` python -m ipify -h```
to get started




## Contributing

Contributions are always welcome!

See `contributing.md` for ways to get started.

Please adhere to this project's `code of conduct`.


## License

[Apache 2.0](https://choosealicense.com/licenses/apache-2.0/)


## Support

For support, email sigireddybalasai@gmail.com or open an issue here

