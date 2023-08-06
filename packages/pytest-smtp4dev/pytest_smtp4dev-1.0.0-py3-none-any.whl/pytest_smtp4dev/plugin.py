import os

import pytest
from _pytest.config import Config
from _pytest.fixtures import FixtureRequest

from pytest_smtp4dev.client import Smtp4devClient


@pytest.mark.tryfirst
def pytest_cmdline_main(config: Config):
    if hostname := os.getenv('SMTP4DEV_HOSTNAME'):
        config.stash['smtp4dev_adapter'] = {'hostname': hostname}
    else:
        raise EnvironmentError('Отсутствует переменная окружения "SMTP4DEV_HOSTNAME"')


@pytest.fixture(scope="session")
def smtp4dev_client(request: FixtureRequest) -> Smtp4devClient:
    return Smtp4devClient(request.config.stash['smtp4dev_adapter']['hostname'])
