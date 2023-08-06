from io import BytesIO
from packaging import version
import pytest
import os
from carmen_cloud_client import VehicleAPIClient, VehicleAPIOptions, SelectedServices, Locations, CarmenAPIConfigError, InvalidImageError, RegionOfInterest, CloudServiceRegion
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

test_options = VehicleAPIOptions(
    api_key=api_key,
    services=SelectedServices(anpr=True),
    input_image_location=Locations.Europe.Hungary,
    endpoint=endpoint
)

def test_endpoint_cloud_service_region_none_throws():
    invalid_options = VehicleAPIOptions(
        api_key=api_key,
        services=SelectedServices(anpr=True),
        input_image_location=Locations.Europe.Hungary,
    )
    with pytest.raises(CarmenAPIConfigError):
        VehicleAPIClient(invalid_options)

def test_invalid_imagedataorpath_throws():
    client = VehicleAPIClient(test_options)
    with pytest.raises(InvalidImageError):
        client.send("/invalid/path")

def test_no_services_requested_throws():
    with pytest.raises(CarmenAPIConfigError):
        invalid_options = VehicleAPIOptions(
            api_key=api_key,
            input_image_location=Locations.Europe.Hungary,
            services=SelectedServices(),
            endpoint=endpoint
        )
        VehicleAPIClient(invalid_options) # this should never be reached

def test_only_plate_result_if_only_anpr():
    client = VehicleAPIClient(test_options)
    response = client.send(os.path.join(current_directory, "test.jpg"))
    assert response.data is not None
    assert response.data.vehicles is not None
    assert len(response.data.vehicles) == 1
    assert response.data.vehicles[0].mmr is None
    assert response.data.vehicles[0].markings is None
    assert response.data.vehicles[0].plate is not None
    assert response.data.vehicles[0].plate.unicodeText == "LMF462"

def test_only_mmr_result_if_only_mmr():
    client = VehicleAPIClient(
        VehicleAPIOptions(
            api_key=api_key,
            services=SelectedServices(mmr=True),
            input_image_location=Locations.Europe.Hungary,
            endpoint=endpoint
        )
    )
    response = client.send(os.path.join(current_directory, "test.jpg"))
    assert response.data is not None
    assert response.data.vehicles is not None
    assert len(response.data.vehicles) == 1
    assert response.data.vehicles[0].mmr is not None
    assert response.data.vehicles[0].markings is None
    assert response.data.vehicles[0].plate is None

def test_returns_mmr_and_anpr_result_if_both_are_requested():
    client = VehicleAPIClient(
        VehicleAPIOptions(
            api_key=api_key,
            services=SelectedServices(mmr=True, anpr=True),
            input_image_location=Locations.Europe.Hungary,
            endpoint=endpoint
        )
    )
    response = client.send(os.path.join(current_directory, "test.jpg"))
    assert response.data is not None
    assert response.data.vehicles is not None
    assert len(response.data.vehicles) == 1
    assert response.data.vehicles[0].mmr is not None
    assert response.data.vehicles[0].markings is None
    assert response.data.vehicles[0].plate is not None
    assert response.data.vehicles[0].plate.unicodeText == "LMF462"

def test_only_adr_result_if_only_adr_is_requested():
    client = VehicleAPIClient(
        VehicleAPIOptions(
            api_key=api_key,
            services=SelectedServices(adr=True),
            input_image_location=Locations.Europe.Hungary,
            endpoint=endpoint
        )
    )
    response = client.send(os.path.join(current_directory, "adr-test.jpg"))
    assert response.data is not None
    assert response.data.vehicles is not None
    assert len(response.data.vehicles) == 1
    assert response.data.vehicles[0].mmr is None
    assert response.data.vehicles[0].markings is not None
    assert response.data.vehicles[0].plate is None

def test_accepts_image_as_a_stream():
    client = VehicleAPIClient(test_options)
    with open(os.path.join(current_directory, "test.jpg"), "rb") as file:
        stream = BytesIO(file.read())
        response = client.send(stream)
    assert response.data is not None
    assert response.data.vehicles is not None
    assert len(response.data.vehicles) == 1

def test_passes_maxreads_parameter():
    options = VehicleAPIOptions(
        api_key=api_key,
        services=SelectedServices(anpr=True),
        input_image_location=Locations.Europe.Hungary,
        endpoint=endpoint,
        max_reads=5
    )
    client = VehicleAPIClient(options)
    with open(os.path.join(current_directory, "many_plates_hun.jpg"), "rb") as file:
        stream = BytesIO(file.read())
        response = client.send(stream)
    assert response.data is not None
    assert response.data.vehicles is not None
    assert len(response.data.vehicles) == 5

def test_passes_roi_parameter():
    options = VehicleAPIOptions(
        api_key=api_key,
        services=SelectedServices(anpr=True),
        input_image_location=Locations.Europe.Hungary,
        endpoint=endpoint,
        max_reads=1,
        region_of_interest=RegionOfInterest(
            top_left=(162, 458),
            top_right=(320, 458),
            bottom_right=(320, 520),
            bottom_left=(162, 520)
        )
    )
    client = VehicleAPIClient(options)
    with open(os.path.join(current_directory, "many_plates_hun.jpg"), "rb") as file:
        stream = BytesIO(file.read())
        response = client.send(stream)
    assert response.data is not None
    assert response.data.vehicles is not None
    assert len(response.data.vehicles) == 1
    assert response.data.vehicles[0].plate is not None
    assert response.data.vehicles[0].plate.unicodeText == "KPS127"

def test_has_a_package_version_that_matches_the_api_response_version():
    options = VehicleAPIOptions(
        api_key=api_key,
        services=SelectedServices(anpr=True, mmr=True),
        input_image_location=Locations.Europe.Hungary,
        endpoint=endpoint
    )
    client = VehicleAPIClient(options)
    response = client.send(os.path.join(current_directory, "adr-test.jpg"))
    assert response.version is not None
    client_version = version.parse(client.supported_api_version + '.0')
    response_version = version.parse(response.version + '.0')
    readme_version = version.parse(extract_api_version_from_readme("Vehicle API") + '.0')
    assert client_version.major == response_version.major
    assert client_version.minor == response_version.minor
    assert client_version.major == readme_version.major
    assert client_version.minor == readme_version.minor

def test_works_correctly_if_cloudServiceRegion_is_EU():
    options = VehicleAPIOptions(
        api_key=eu_prod_api_key,
        services=SelectedServices(anpr=True),
        input_image_location=Locations.Europe.Hungary,
        cloud_service_region=CloudServiceRegion.EU
    )
    client = VehicleAPIClient(options)
    response = client.send(os.path.join(current_directory, "test.jpg"))
    assert response.data is not None
    assert response.data.vehicles is not None
    assert len(response.data.vehicles) == 1

def test_works_correctly_if_cloudServiceRegion_is_US():
    options = VehicleAPIOptions(
        api_key=us_prod_api_key,
        services=SelectedServices(anpr=True),
        input_image_location=Locations.Europe.Hungary,
        cloud_service_region=CloudServiceRegion.US
    )
    client = VehicleAPIClient(options)
    response = client.send(os.path.join(current_directory, "test.jpg"))
    assert response.data is not None
    assert response.data.vehicles is not None
    assert len(response.data.vehicles) == 1

