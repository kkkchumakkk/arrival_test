import pytest
from arrival_test.utils.alaska_api_utils import AlaskaApiUtils
from arrival_test.utils.logger import Logger


@pytest.fixture(scope="session", autouse=True)
def check_application_status():
    try:
        Logger.info("Checking if application is running")
        status_code, _ = AlaskaApiUtils.get_app_info()
    except WindowsError:
        Logger.error(f'Application was not started!')
        pytest.exit(f"Application was not started!")
    else:
        yield
