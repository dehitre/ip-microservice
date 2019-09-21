import requests
import json
import pytest
import urllib.parse
import allure_pytest
import allure


def find_ip(response, ip):
    ip_list = response["collection"]
    found_ip = {}
    for i in ip_list:
        if i["ip"] == ip:
            found_ip = i
    return found_ip


@allure.title("Add ip to country list")
def test_add_to_country_list(get_country_ip_link, get_country_ip):
    data = {"countryCode": "RU"}
    headers = {'Content-Type': 'application/json'}
    add_ip_response = requests.post(get_country_ip_link+"/"+urllib.parse.quote(get_country_ip, safe=""), headers=headers, data=json.dumps(data))
    assert add_ip_response.status_code == 200


@allure.title("Getting country list")
def test_country_list(get_country_ip_link, get_country_ip):
    headers = {'Content-Type': 'application/json'}
    get_ips_response = requests.get(get_country_ip_link, headers=headers)
    assert get_ips_response.status_code == 200
    found_ip = find_ip(get_ips_response.json(), get_country_ip)
    assert found_ip["countryCode"] == "RU"
    assert found_ip["ip"] == get_country_ip


@allure.title("Getting listed ips(contains)")
def test_contains_list(get_country_ip_link, get_country_ip):
    path_true = "/93.125.30.20/contains"
    path_false = "/93.125.30.171/contains"
    headers = {'Content-Type': 'application/json'}
    get_ip_response_true = requests.get(get_country_ip_link+path_true, headers=headers)
    assert get_ip_response_true.status_code == 200
    assert get_ip_response_true.json()["collection"][0]["ip"] == get_country_ip
    get_ip_response_false = requests.get(get_country_ip_link + path_false, headers=headers)
    assert get_ip_response_false.status_code == 200
    assert len(get_ip_response_false.json()["collection"]) == 0


@allure.title("Deleting from country list")
def test_delete_ip(get_country_ip_link, get_country_ip):
    headers = {'Content-Type': 'application/json'}
    delete_ip_response = requests.delete(get_country_ip_link+"/"+urllib.parse.quote(get_country_ip, safe=""), headers=headers)
    assert delete_ip_response.status_code == 200
    assert delete_ip_response.json() == 1
    get_ips_response = requests.get(get_country_ip_link, headers=headers)
    found_ip = find_ip(get_ips_response.json(), get_country_ip)
    assert found_ip == {}


