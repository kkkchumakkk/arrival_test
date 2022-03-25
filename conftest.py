import pytest

from arrival_test.alaska_api.alaska_api_utils import AlaskaApiUtils
from arrival_test.utils.logger import Logger as logger


@pytest.fixture(scope="session", autouse=True)
def check_application_status():
    try:
        logger.info("Checking if application is running")
        status_code, _ = AlaskaApiUtils.get_all_bears()
    except WindowsError:
        logger.error(f'Application was not started!')
        pytest.exit(f"Application was not started!")
    else:
        yield
