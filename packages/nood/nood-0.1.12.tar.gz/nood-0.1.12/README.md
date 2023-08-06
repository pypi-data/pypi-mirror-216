# nood - Notifications On Demand

A wrapping library for web crawlers automation.

The main objective of this service is to easily enable developers to build and
run monitors. Basically, developers only have to write a download function and
a corresponding parse function to run a monitor.

## Prerequisites

To use `nood`, you need an API key.
[Please join our Discord](https://discord.gg/yMYnGcKKnR) and contact
`turner#0069`.

We also encourage you to use `pm2` ([click here for more information](https://www.npmjs.com/package/pm2)) to 
run your monitors.

## Installation

Install `nood` with pip.

```
pip install nood
```

## Configuration

The configuration for each monitor is stored in a json file. The default
directory for the config file is the same as the monitor's script directory.
The default name for the config file is `config.json`, but can be configured
individually.

```json
{
  "monitor_id": 1234,
  "api_key": "abcdefg1234567890",
  "proxies": [
    "ip:port:user:pass"
  ],
  "urls": [
    "https://example.com/1",
    "https://example.com/2"
  ],
  "pids": [
    "example-pid-1",
    "example-pid-2"
  ]
}
```

## Example Scraper with Config

For each monitor, the `Scraper` and `Parser` class must be defined. The
monitoring logic is managed in the `Monitor` class which is defined by `nood`.

```python
import requests

from nood import monitor, objects


class MMSScraper(monitor.Scraper):
    def __init__(self, url: str, **kwargs):
        super(MMSScraper, self).__init__(url=url, **kwargs)

    def download(self) -> requests.Response:
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/108.0.0.0 Safari/537.36'
        }
        response = self._s.get(
            url=self.url,
            proxies=self.get_static_proxy(),
            headers=headers
        )

        return response


class MMSParser(monitor.Parser):
    def __init__(self):
        super().__init__()

    def parse(self, *, response: requests.Response):
        name = response.text.split('<title data-rh="true">')[1].split("|")[0]
        turl = response.text.split('"og:image" content="')[1].split('"')[0]
        variants = []
        if "</div>In den Warenkorb</button>" in response.text:
            variants.append(objects.Variant(value="OS"))

        return objects.Product(
            url=response.url,
            name=name,
            variants=variants,
            thumbnail_url=turl
        )


if __name__ == "__main__":
    monitor.Monitor.launch_tasks(scraper=MMSScraper, parser=MMSParser)
```

The configuration file for Mediamarkt would look like this:

```json
{
  "monitor_id": 1234,
  "api_key": "abcdefg1234567890",
  "proxies": [],
  "urls": [
    "https://www.mediamarkt.de/de/product/_apple-airpods-mit-ladecase-2-generation-2539111.html"
  ],
  "pids": []
}
```

To run and keep track of the monitoring script with `pm2`, you can use the 
following commands:

```shell
pm2 start mms.py
pm2 monit
```

To stop the script, use

```shell
pm2 stop mm2.py
```