import json
import os
import time
from abc import ABC
from threading import Thread
from typing import List, Type

from loguru import logger

from nood import api, objects
from nood.monitor.exceptions import MonitorException
from nood.monitor.parser import Parser
from nood.monitor.scraper import Scraper


class Monitor(ABC):
    def __init__(
            self,
            api_key: str,
            monitor_id: int,
            scraper: Type[Scraper],
            parser: Type[Parser],
            url: str = None,
            pid: str = None,
            proxies: List[objects.Proxy] = None,
            retry_intervall: int = 5,
            timeout_on_error: int = 1,
            refresh_session_each_intervall: bool = False,
            refresh_session_on_error: bool = True,
    ):

        # init scraper and parser
        self.scraper = scraper(url=url, pid=pid, proxies=proxies)
        self.parser = parser()

        # sleep between each iteration of the run method that did not raise
        # an error
        self._retry_intervall = retry_intervall

        # sleep if an error occured
        self._timeout_on_error = timeout_on_error

        # refresh a request session within the scraper if an exception
        # is raised
        self._refresh_session_each_intervall = refresh_session_each_intervall
        self._refresh_session_on_error = refresh_session_on_error

        # module to send products to the api
        self._api = api.API(api_key=api_key, monitor_id=monitor_id)

    def _run(self):
        while True:
            try:
                # scrape html/json response
                response = self.scraper.download()
                logger.info(f"Response status: {response.status_code}")

                # parse the response and return 1 or many products
                products = self.parser._to_list(
                    self.parser.parse(response=response)
                )
                logger.info(f"Found {len(products)} products")

                self._api.ping_products(products=products)
                time.sleep(self._retry_intervall)
            except MonitorException:
                time.sleep(self._timeout_on_error)
            except TimeoutError as e:
                logger.error(f"Unknwon error occured in run method: {e}")
                time.sleep(self._timeout_on_error)
            else:
                if self._refresh_session_each_intervall:
                    logger.debug("Refreshing session for each intervall")
                    self.scraper.refresh_session()
                # only sleep if no exception occured
                time.sleep(self._retry_intervall)
            finally:
                # check if the session shall be refreshed at an error
                if self._refresh_session_on_error:
                    logger.debug("Refreshing session on error")
                    self.scraper.refresh_session()

    @classmethod
    def launch_tasks(
            cls,
            scraper: Type[Scraper],
            parser: Type[Parser],
            path_to_config_file: str = "config.json",
            retry_intervall: int = 5,
            timeout_on_error: int = 1,
            refresh_session_on_error: bool = True,
    ):

        # load config file
        if not os.path.exists(path_to_config_file):
            raise Exception(f"cannot find config file in path "
                            f"'{path_to_config_file}'")
        else:
            with open(path_to_config_file, "r") as f:
                config = json.load(f)
                proxies = [objects.Proxy.from_string(p)
                           for p in config.get("proxies", [])]
                logger.debug(f"loaded {len(proxies)} proxies from "
                             f"config.json")

        # launch URL tasks
        for url in config["urls"]:
            Thread(target=cls(
                api_key=config["api_key"],
                monitor_id=config["monitor_id"],
                scraper=scraper,
                parser=parser,
                url=url,
                proxies=proxies,
                retry_intervall=retry_intervall,
                timeout_on_error=timeout_on_error,
                refresh_session_on_error=refresh_session_on_error
            )._run, args=()).start()

        # launch PID tasks
        for pid in config["pids"]:
            Thread(target=cls(
                api_key=config["api_key"],
                monitor_id=config["monitor_id"],
                scraper=scraper,
                parser=parser,
                pid=pid,
                proxies=proxies,
                retry_intervall=retry_intervall,
                timeout_on_error=timeout_on_error,
                refresh_session_on_error=refresh_session_on_error
            )._run, args=()).start()