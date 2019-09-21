import requests
import json
import pytest
import allure_pytest
import allure


@allure.title("Getting russian ip")
def test_get_ip_ru(get_ip_info):
    ip = "93.153.171.126"
    response = get_ip_info(ip)
    assert response["response_code"] == 200
    assert response["ip"] == ip
    assert response["country_code"] == "RU"


@allure.title("Getting belarussian ip")
def test_get_ip_by(get_ip_info):
    ip = "93.125.30.201"
    response = get_ip_info(ip)
    assert response["response_code"] == 200
    assert response["ip"] == ip
    assert response["country_code"] == "BY"


@allure.title("Getting anonymous ip")
def test_get_ip_anonymous(get_ip_info):
    ip = "217.160.83.67"
    response = get_ip_info(ip)
    assert response["response_code"] == 200
    assert response["ip"] == ip
    assert response["anonymous"] is True


