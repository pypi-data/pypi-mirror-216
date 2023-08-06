import pytest
import os
from packaging import version
from carmen_cloud_client import TransportAPIClient, CodeType, TransportAPIOptions, CarmenAPIConfigError, InvalidImageError
from dotenv import load_dotenv
from carmen_cloud_client.test import extract_api_version_from_readme

current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)

load_dotenv()

# configure environment
api_key = os.getenv("TEST_DEV_API_KEY", "")
endpoint = os.getenv("TEST_DEV_ENDPOINT_URL", "")
eu_prod_api_key = os.getenv("TEST_EU_PROD_API_KEY", "")
us_prod_api_key = os.getenv("TEST_US_PROD_API_KEY", "")

test_options = TransportAPIOptions(
    api_key=api_key,
    type=CodeType.ACCR_USA,
    endpoint=endpoint
)

def test_invalid_options_throws():
    invalid_options = TransportAPIOptions(
        api_key=api_key,
        type=CodeType.ACCR_USA,
    )
    with pytest.raises(CarmenAPIConfigError):
        TransportAPIClient(invalid_options)

def test_maxreads_zero_throws():
    invalid_options = TransportAPIOptions(
        api_key=api_key,
        type=CodeType.ACCR_USA,
        max_reads=0,
        endpoint=endpoint,
    )
    with pytest.raises(CarmenAPIConfigError):
        TransportAPIClient(invalid_options)

def test_empty_imagedataorpaths_throws():
    client = TransportAPIClient(test_options)
    with pytest.raises(InvalidImageError):
        client.send()

def test_invalid_image_path_throws():
    client = TransportAPIClient(test_options)
    with pytest.raises(InvalidImageError):
        client.send("/invalid/path")

def test_single_image_return_expected():
    client = TransportAPIClient(test_options)
    response = client.send(os.path.join(current_directory, "accr_usa01.jpg"))
    assert response.data is not None
    assert response.data.codes is not None
    assert len(response.data.codes) == 1
    assert response.data.codes[0].code == "NFLZ049511"

def test_single_image_returns_one_result():
    client = TransportAPIClient(test_options)
    response = client.send(os.path.join(current_directory, "accr_usa01.jpg"))
    assert response.data is not None
    assert response.data.codes is not None
    assert len(response.data.codes) == 1
    assert response.data.codes[0].code == "NFLZ049511"
    assert response.data.codes[0].imageResults is not None
    assert len(response.data.codes[0].imageResults) == 1

def test_return_4_image_results_when_4_images_sent():
    client = TransportAPIClient(test_options)
    response = client.send(
        os.path.join(current_directory, "accr_usa01.jpg"),
        os.path.join(current_directory, "accr_usa02.jpg"),
        os.path.join(current_directory, "accr_usa03.jpg"),
        os.path.join(current_directory, "accr_usa20.jpg"),
    )
    assert response.data is not None
    assert response.data.codes is not None
    assert len(response.data.codes) == 1
    assert response.data.codes[0].code == "NFLZ049511"
    assert response.data.codes[0].imageResults is not None
    assert len(response.data.codes[0].imageResults) == 4

def test_can_read_ACCR_USA_codes():
    client = TransportAPIClient(test_options)
    response = client.send(
        os.path.join(current_directory, "accr_usa01.jpg"),
        os.path.join(current_directory, "accr_usa02.jpg"),
        os.path.join(current_directory, "accr_usa03.jpg"),
        os.path.join(current_directory, "accr_usa20.jpg"),
    )
    assert response.data is not None
    assert response.data.codes is not None
    assert len(response.data.codes) == 1
    assert response.data.codes[0].code == "NFLZ049511"
    assert response.data.codes[0].imageResults is not None
    assert len(response.data.codes[0].imageResults) == 4

def test_can_read_BRA_codes():
    client = TransportAPIClient(TransportAPIOptions(
        api_key=api_key,
        type=CodeType.BRA,
        endpoint=endpoint
    ))
    response = client.send(
        os.path.join(current_directory, "bra01.jpg"),
        os.path.join(current_directory, "bra02.jpg"),
        os.path.join(current_directory, "bra03.jpg"),
        os.path.join(current_directory, "bra20.jpg"),
    )
    assert response.data is not None
    assert response.data.codes is not None
    assert len(response.data.codes) == 1
    assert response.data.codes[0].code == "HFE0599760"
    assert response.data.codes[0].imageResults is not None
    assert len(response.data.codes[0].imageResults) == 4

def test_can_read_chassis_codes():
    client = TransportAPIClient(TransportAPIOptions(
        api_key=api_key,
        type=CodeType.CHASSIS,
        endpoint=endpoint
    ))
    response = client.send(
        os.path.join(current_directory, "chassis01.jpg"),
        os.path.join(current_directory, "chassis02.jpg"),
        os.path.join(current_directory, "chassis03.jpg"),
        os.path.join(current_directory, "chassis20.jpg"),
    )
    assert response.data is not None
    assert response.data.codes is not None
    assert len(response.data.codes) == 1
    assert response.data.codes[0].code == "MAEC623857"
    assert response.data.codes[0].imageResults is not None
    assert len(response.data.codes[0].imageResults) == 4

def test_can_read_ilu_codes():
    client = TransportAPIClient(TransportAPIOptions(
        api_key=api_key,
        type=CodeType.ILU,
        endpoint=endpoint
    ))
    response = client.send(
        os.path.join(current_directory, "ilu01.jpg"),
        os.path.join(current_directory, "ilu02.jpg"),
        os.path.join(current_directory, "ilu03.jpg"),
        os.path.join(current_directory, "ilu20.jpg"),
    )
    assert response.data is not None
    assert response.data.codes is not None
    assert len(response.data.codes) == 1
    assert response.data.codes[0].code == "LKWA06011300WI1"
    assert response.data.codes[0].imageResults is not None
    assert len(response.data.codes[0].imageResults) == 4

def test_can_read_iso_codes():
    client = TransportAPIClient(TransportAPIOptions(
        api_key=api_key,
        type=CodeType.ISO,
        endpoint=endpoint
    ))
    response = client.send(
        os.path.join(current_directory, "iso01.jpg"),
        os.path.join(current_directory, "iso02.jpg"),
        os.path.join(current_directory, "iso03.jpg"),
        os.path.join(current_directory, "iso20.jpg"),
    )
    assert response.data is not None
    assert response.data.codes is not None
    assert len(response.data.codes) == 1
    assert response.data.codes[0].code == "NOSU2463454SG2210"
    assert response.data.codes[0].imageResults is not None
    assert len(response.data.codes[0].imageResults) == 4

def test_can_read_uic_codes():
    client = TransportAPIClient(TransportAPIOptions(
        api_key=api_key,
        type=CodeType.UIC,
        endpoint=endpoint
    ))
    response = client.send(
        os.path.join(current_directory, "uic01.jpg"),
        os.path.join(current_directory, "uic02.jpg"),
        os.path.join(current_directory, "uic03.jpg"),
        os.path.join(current_directory, "uic20.jpg"),
    )
    assert response.data is not None
    assert response.data.codes is not None
    assert len(response.data.codes) == 1
    assert response.data.codes[0].code == "818068616353"
    assert response.data.codes[0].imageResults is not None
    assert len(response.data.codes[0].imageResults) == 4

def test_can_read_usdot_codes():
    client = TransportAPIClient(TransportAPIOptions(
        api_key=api_key,
        type=CodeType.USDOT,
        endpoint=endpoint
    ))
    response = client.send(
        os.path.join(current_directory, "usdot01.jpg"),
        os.path.join(current_directory, "usdot02.jpg"),
        os.path.join(current_directory, "usdot03.jpg"),
        os.path.join(current_directory, "usdot20.jpg"),
    )
    assert response.data is not None
    assert response.data.codes is not None
    assert len(response.data.codes) == 1
    assert response.data.codes[0].code == "1201193"
    assert response.data.codes[0].imageResults is not None
    assert len(response.data.codes[0].imageResults) == 4

def test_has_a_package_version_that_matches_the_api_response_version():
    client = TransportAPIClient(test_options)
    response = client.send(
        os.path.join(current_directory, "accr_usa01.jpg"),
        os.path.join(current_directory, "accr_usa02.jpg"),
        os.path.join(current_directory, "accr_usa03.jpg"),
        os.path.join(current_directory, "accr_usa20.jpg"),
    )
    assert response.version is not None
    client_version = version.parse(client.supported_api_version + '.0')
    response_version = version.parse(response.version + '.0')
    readme_version = version.parse(extract_api_version_from_readme("Transportation & Cargo API") + '.0')
    assert client_version.major == response_version.major
    assert client_version.minor == response_version.minor
    assert client_version.major == readme_version.major
    assert client_version.minor == readme_version.minor
