import requests
import random
from string import digits as digit
from time import sleep as gumaw
from json import loads as jsn_vai
from concurrent.futures import ThreadPoolExecutor as speed
from os import system as phone
from os import remove as delete
from bs4 import BeautifulSoup as dsoup

class DCCSUtils:
    @staticmethod
    def gpt(url, **kwargs):
        return requests.get(url, **kwargs)

    @staticmethod
    def pst(url, data=None, json=None, **kwargs):
        return requests.post(url, data=data, json=json, **kwargs)

    @staticmethod
    def rnd_choice(sequence):
        return random.choice(sequence)

    @staticmethod
    def rnd_range(start, stop=None, step=1):
        return random.randrange(start, stop, step)

    @staticmethod
    def slp(seconds):
        gumaw(seconds)

    @staticmethod
    def jld(string, **kwargs):
        return jsn_vai(string, **kwargs)

    @staticmethod
    def tpe(max_workers=None):
        return speed(max_workers)

    @staticmethod
    def exe(command):
        return phone(command)

    @staticmethod
    def dl_file(url, file_path):
        response = requests.get(url, stream=True)
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)

    @staticmethod
    def fnd_links(url):
        response = requests.get(url)
        soup = dsoup(response.text, 'html.parser')
        links = soup.find_all('a')
        link_urls = [link.get('href') for link in links]
        return link_urls

    @staticmethod
    def get_ip():
        response = requests.get('https://api.ipify.org/?format=json')
        if response.status_code == 200:
            data = response.json()
            ip_address = data.get('ip')
            return ip_address
        return None

    @staticmethod
    def rnd_element(sequence):
        return random.choice(sequence)

    @staticmethod
    def get_content(response):
        return response.content

    @staticmethod
    def get_headers(response):
        return response.headers

    @staticmethod
    def get_status_code(response):
        return response.status_code

    @staticmethod
    def get_cookies(response):
        return response.cookies

    @staticmethod
    def set_timeout(timeout):
        return timeout

    @staticmethod
    def set_proxy(proxy):
        return proxy

    @staticmethod
    def set_headers(headers):
        return headers

    @staticmethod
    def get_title(url):
        response = requests.get(url)
        soup = dsoup(response.text, 'html.parser')
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.string.strip()
        return None

    @staticmethod
    def download(url, file_path):
        response = requests.get(url, stream=True)
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)

    @staticmethod
    def find_links(url):
        response = requests.get(url)
        soup = dsoup(response.text, 'html.parser')
        links = soup.find_all('a')
        link_urls = [link.get('href') for link in links]
        return link_urls

    @staticmethod
    def get_ip_address():
        response = requests.get('https://api.ipify.org/?format=json')
        if response.status_code == 200:
            data = response.json()
            ip_address = data.get('ip')
            return ip_address
        return None

    @staticmethod
    def get_random_element(sequence):
        return random.choice(sequence)

    @staticmethod
    def get_response_content(response):
        return response.content

    @staticmethod
    def get_response_headers(response):
        return response.headers

    @staticmethod
    def get_response_status_code(response):
        return response.status_code

    @staticmethod
    def get_response_cookies(response):
        return response.cookies

    @staticmethod
    def set_request_timeout(timeout):
        return timeout

    @staticmethod
    def set_request_proxy(proxy):
        return proxy

    @staticmethod
    def set_request_headers(headers):
        return headers

    @staticmethod
    def get_request_url(request):
        return request.url

    @staticmethod
    def get_request_method(request):
        return request.method

    @staticmethod
    def get_request_headers(request):
        return request.headers

    @staticmethod
    def get_request_body(request):
        return request.body

    @staticmethod
    def get_request_text(request):
        return request.text

    @staticmethod
    def get_request_status_code(request):
        return request.status_code

    @staticmethod
    def get_request_cookies(request):
        return request.cookies

    @staticmethod
    def get_request_content(request):
        return request.content

    @staticmethod
    def set_request_timeout(request, timeout):
        request.timeout = timeout

    @staticmethod
    def set_request_proxy(request, proxies):
        request.proxies = proxies

    @staticmethod
    def set_request_headers(request, headers):
        request.headers = headers

    @staticmethod
    def set_request_body(request, data):
        request.data = data

    @staticmethod
    def set_request_files(request, files):
        request.files = files

    @staticmethod
    def set_request_session(request, session):
        request.session = session

    @staticmethod
    def set_request_hooks(request, hooks):
        request.hooks = hooks

    @staticmethod
    def set_request_params_encoding(request, encoding):
        request.params.encoding = encoding

    @staticmethod
    def set_request_allow_redirects(request, allow_redirects):
        request.allow_redirects = allow_redirects

    @staticmethod
    def set_request_prepared(request, prepared_request):
        request.prepared = prepared_request

    @staticmethod
    def set_request_history(request, history):
        request.history = history

    @staticmethod
    def set_request_original_request(request, original_request):
        request.original_request = original_request

    @staticmethod
    def set_request_is_redirect(request, is_redirect):
        request.is_redirect = is_redirect

    @staticmethod
    def set_request_is_permanent_redirect(request, is_permanent_redirect):
        request.is_permanent_redirect = is_permanent_redirect

    @staticmethod
    def send_request(request):
        request.send()
        