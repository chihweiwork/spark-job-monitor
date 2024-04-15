import requests
import json

from bs4 import BeautifulSoup
from typing import List, Generator
from abc import ABC, abstractmethod

from utils import function_daemonize

class FindSparkJob(ABC):
    @abstractmethod
    def gen_discover_file():
        pass

class SparkMasterJobDiscover(FindSparkJob):
    '''
    使用這個class從spark master上取得 spark job 的 url
    '''
    def __init__(self, spark_master_url: str) -> None:
        '''
        spark_master_url: url of spark master
        '''
        self.spark_master_url = spark_master_url

    def _get_spark_master_content(self) -> str:
        api_url = f"{self.spark_master_url}/api/v1/applications?status=running"
        response = requests.get(api_url)
        return response.text

    def _parser_spark_master_content(self, html_content: str) -> Generator[str, None, None]:
        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        # Find the table containing running applications
        ui_urls = (a['href'] for a in soup.find_all('a', href=True))
        return ui_urls

    def _get_monitor_targets(self, ui_urls:Generator[str, None, None]) -> List[str]:

        # Extract the application URLs from the table
        #spark_urls = [
        #    url.replace(
        #        'http://spark-master','localhost'
        #    ) for url in ui_urls if ('spark-master' in url) and ('http' in url)
        #]
        spark_urls = [
            url.replace(
                'http://',''
            ) for url in ui_urls if ('spark-master' in url) and ('http' in url)
        ]
        return spark_urls

    @function_daemonize(sleep_time=15)
    def gen_discover_file(self, output_file_path: str) -> None:
        html_content = self._get_spark_master_content()
        ui_urls = self._parser_spark_master_content(html_content)
        spark_targets = self._get_monitor_targets(ui_urls)

        discover_content = [{
            'labels': {'job':'spark'},
            'targets': spark_targets
        }]

        with open(output_file_path, 'w') as file_object:
            json.dump(discover_content, file_object, indent=4)
