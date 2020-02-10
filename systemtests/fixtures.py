import os
import pytest

from typing import Dict, Any

from datetime import date
import datetime


@pytest.fixture
def headers():
    return {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }


@pytest.fixture
def request_headers() -> Dict[str, Any]:
    return dict()


@pytest.fixture
def base_url() -> str:
    return ""


@pytest.fixture
def request_body() -> Dict[str, Any]:
    return dict()


@pytest.fixture
def dataset():
    return []


@pytest.fixture
def tablename():
    pass


@pytest.fixture
def flags():
    return []



@pytest.fixture
def conditions():
    return ''


@pytest.fixture
def bucket_name():
    pass


@pytest.fixture
def queue_url():
    pass


@pytest.fixture
def upload_date():
    return date.today().strftime('%Y-%m-%d')


@pytest.fixture
def client():
    pass
