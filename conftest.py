import requests
import json
import pytest


@pytest.fixture(scope="module")
def get_black_list_ip():
    ip = "185.68.16.0/25"
    return ip


@pytest.fixture(scope="module")
def get_white_list_ip():
    ip = "80.249.239.20"
    return ip


@pytest.fixture(scope="function")
def get_country_ip():
    ip = "93.125.30.0/25"
    return ip


@pytest.fixture(scope="function")
def get_ip_info():
    def _get_ip(ip):
        ip_dict = {
            "ip": ip,
            "listedInfo": None,
            "country_code": None,
            "anonymous": None,
            "response_code": 0
        }
        link = "http://ip-resolver.pre.spb.play.dc/v1/ip-info/" + ip
        response = requests.get(link)
        response_code = response.status_code
        if response_code == 200:
            ip_dict["ip"] = response.json()["ip"]
            ip_dict["listedInfo"] = response.json()["listedInfo"]
            ip_dict["country_code"] = response.json()["countryAndAnonymity"]["countryCode"]
            ip_dict["anonymous"] = response.json()["countryAndAnonymity"]["anonymous"]
            ip_dict["response_code"] = response_code
        else:
            ip_dict["response_code"] = response_code
        return ip_dict
    return _get_ip

@pytest.fixture(scope="function")
def get_listed_ip_link():
    link = "http://ip-resolver.pre.spb.play.dc/v1/listed-ip"
    return link


@pytest.fixture(scope="function")
def get_country_ip_link():
    link = "http://ip-resolver.pre.spb.play.dc/v1/country-ip"
    return link