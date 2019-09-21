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
        if i["ipAddress"] == ip:
            found_ip = i
    return found_ip

@allure.title("Add ip to the black list")
def test_add_to_black_list(get_listed_ip_link, get_black_list_ip):
    data = {"ipAddresses": [get_black_list_ip], "blackList": True, "comment": "test"}
    headers = {'Content-Type': 'application/json'}
    add_ip_response = requests.post(get_listed_ip_link, headers=headers, data=json.dumps(data))
    assert add_ip_response.status_code == 200


@allure.title("Add ip to the white list")
def test_add_to_white_list(get_listed_ip_link, get_white_list_ip):
    data = {"ipAddresses": [get_white_list_ip], "blackList": False, "comment": "test"}
    headers = {'Content-Type': 'application/json'}
    add_ip_response = requests.post(get_listed_ip_link, headers=headers, data=json.dumps(data))
    assert add_ip_response.status_code == 200


@allure.title("Getting blacklist")
def test_black_list(get_listed_ip_link, get_black_list_ip):
    payload = {"isBlackList": True}
    headers = {'Content-Type': 'application/json'}
    get_ips_response = requests.get(get_listed_ip_link, params=payload, headers=headers)
    assert get_ips_response.status_code == 200
    found_ip = find_ip(get_ips_response.json(), get_black_list_ip)
    assert found_ip["blacklisted"] is True
    assert found_ip["ipAddress"] == get_black_list_ip


@allure.title("Getting whitelist")
def test_white_list(get_listed_ip_link, get_white_list_ip):
    payload = {"isBlackList": False}
    headers = {'Content-Type': 'application/json'}
    get_ips_response = requests.get(get_listed_ip_link, params=payload, headers=headers)
    assert get_ips_response.status_code == 200
    found_ip = find_ip(get_ips_response.json(), get_white_list_ip)
    assert found_ip["blacklisted"] is False
    assert found_ip["ipAddress"] == get_white_list_ip


@allure.title("Getting listed ips(contains)")
def test_contains_list(get_listed_ip_link, get_black_list_ip):
    """Getting listed ips, each of which contains given ip address"""
    path_true = "/185.68.16.20/contains"
    path_false = "/185.68.16.171/contains"
    headers = {'Content-Type': 'application/json'}
    get_ip_response_true = requests.get(get_listed_ip_link+path_true, headers=headers)
    assert get_ip_response_true.status_code == 200
    assert get_ip_response_true.json()["collection"][0]["ipAddress"] == get_black_list_ip
    get_ip_response_false = requests.get(get_listed_ip_link + path_false, headers=headers)
    assert get_ip_response_false.status_code == 200
    assert len(get_ip_response_false.json()["collection"]) == 0


@allure.title("Getting listed ips(contained by)")
def test_is_contained_list(get_listed_ip_link, get_white_list_ip):
    """Get listed ips, each of which is contained by given ip address"""
    path_true = "/80.249.239.20" + urllib.parse.quote("/25", safe="") + "/is-contained-by"
    path_false = "/80.249.239.171" + urllib.parse.quote("/25", safe="") + "/is-contained-by"
    headers = {'Content-Type': 'application/json'}
    get_ip_response_true = requests.get(get_listed_ip_link+path_true, headers=headers)
    assert get_ip_response_true.status_code == 200
    assert get_ip_response_true.json()["collection"][0]["ipAddress"] == get_white_list_ip
    get_ip_response_false = requests.get(get_listed_ip_link + path_false, headers=headers)
    assert get_ip_response_false.status_code == 200
    assert len(get_ip_response_false.json()["collection"]) == 0


@allure.title("Getting listed ips(contains/contained) 1")
def test_contains_or_is_contained_contains_list(get_listed_ip_link, get_black_list_ip):
    """Getting listed ips, each of which contains or is contained by given ip address. In this case, ips contains by
     given ip address"""
    path_contains_true = "/185.68.16.20/contains-or-is-contained-by"
    path_contains_false = "/185.68.16.171/contains-or-is-contained-by"
    headers = {'Content-Type': 'application/json'}
    get_ip_response_true = requests.get(get_listed_ip_link + path_contains_true, headers=headers)
    assert get_ip_response_true.status_code == 200
    assert get_ip_response_true.json()["collection"][0]["ipAddress"] == get_black_list_ip
    get_ip_response_false = requests.get(get_listed_ip_link + path_contains_false, headers=headers)
    assert get_ip_response_false.status_code == 200
    assert len(get_ip_response_false.json()["collection"]) == 0


@allure.title("Getting listed ips(contains/contained) 2")
def test_contains_or_is_contained_contained_list(get_listed_ip_link, get_white_list_ip):
    """Getting listed ips, each of which contains or is contained by given ip address. In this case, ips are contained
     by given ip address"""
    path_contained_true = "/80.249.239.20" + urllib.parse.quote("/25", safe="") + "/contains-or-is-contained-by"
    path_contained_false = "/80.249.239.171" + urllib.parse.quote("/25", safe="") + "/contains-or-is-contained-by"
    headers = {'Content-Type': 'application/json'}
    get_ip_response_true = requests.get(get_listed_ip_link + path_contained_true, headers=headers)
    assert get_ip_response_true.status_code == 200
    assert get_ip_response_true.json()["collection"][0]["ipAddress"] == get_white_list_ip
    get_ip_response_false = requests.get(get_listed_ip_link + path_contained_false, headers=headers)
    assert get_ip_response_false.status_code == 200
    assert len(get_ip_response_false.json()["collection"]) == 0


@allure.title("Deleting from blacklist")
def test_delete_black_list(get_listed_ip_link, get_black_list_ip):
    path = "/deletion"
    headers = {'Content-Type': 'application/json'}
    payload = {"isBlackList": False}
    data = [get_black_list_ip]
    delete_ip_response = requests.post(get_listed_ip_link+path, headers=headers, data=json.dumps(data))
    assert delete_ip_response.status_code == 200
    get_ips_response = requests.get(get_listed_ip_link, params=payload, headers=headers)
    found_ip = find_ip(get_ips_response.json(), get_black_list_ip)
    assert found_ip == {}


@allure.title("Deleting from whitelist")
def test_delete_white_list(get_listed_ip_link, get_white_list_ip):
    """Deleting from whitelist"""
    path = "/deletion"
    headers = {'Content-Type': 'application/json'}
    payload = {"isBlackList": False}
    data = [get_white_list_ip]
    delete_ip_response = requests.post(get_listed_ip_link+path, headers=headers, data=json.dumps(data))
    assert delete_ip_response.status_code == 200
    get_ips_response = requests.get(get_listed_ip_link, params=payload, headers=headers)
    found_ip = find_ip(get_ips_response.json(), get_white_list_ip)
    assert found_ip == {}
