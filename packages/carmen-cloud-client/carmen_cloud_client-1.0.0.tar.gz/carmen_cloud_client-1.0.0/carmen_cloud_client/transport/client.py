import os
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from typing import List, Union
from io import BytesIO
from requests.exceptions import RetryError
from urllib.parse import urljoin
from carmen_cloud_client.errors import CarmenAPIConfigError, InvalidImageError
from .options import TransportAPIOptions
from .response import TransportationCargoApiResponse

class TransportAPIClient:
    """
    A client for the Adaptive Recognition Cloud Transportation & Cargo API.
    Use it to send images of containers, railway wagons and vehicles with US DOT
    codes to the API and get the recognized codes back.

    Args:
        options (TransportAPIOptions): An instance of TransportAPIOptions containing
            the necessary options for the API  request.

    Raises:
        TransportAPIConfigError: If the provided options are invalid.
    """

    supported_api_version: str = "1.0"

    def __init__(self, options: TransportAPIOptions):
        self.options = options
        self.validate_options()
        self.api_url = self.get_parametrized_api_url()

    def send(self, *image_data_or_paths: Union[str, bytes, BytesIO]) -> TransportationCargoApiResponse:
        """
        Sends one or more images to the API and returns the recognized codes.

        Args:
            *image_data_or_paths (Union[str, bytes, BytesIO]): One or more image paths
            or bytes-like objects to send to the API.

        Returns:
            dict: A dictionary containing the recognized codes.

        Raises:
            TransportAPIConfigError: If the provided options are invalid or if the API
                request fails.
        """
        if not image_data_or_paths:
            raise InvalidImageError("At least one image must be specified.")

        form_data = self.create_form_data(list(image_data_or_paths))
        headers = self.create_headers(form_data.content_type)

        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"],
            backoff_factor=1
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)

        response = None
        try:
            response = session.post(self.api_url, headers=headers, data=form_data)
            response.raise_for_status()
        except RetryError as e:
            raise CarmenAPIConfigError(f"Failed to send request after {self.options.retry_count} retries: {e}")

        return TransportationCargoApiResponse.parse_obj(response.json())

    def validate_options(self):
        if self.options.max_reads is not None and self.options.max_reads < 1:
            raise CarmenAPIConfigError(f"max_reads must be at least 1, was: {self.options.max_reads}.")

    def get_image_bytes(self, image_data_or_path: Union[str, bytes, BytesIO]) -> Union[bytes, BytesIO]:
        if isinstance(image_data_or_path, bytes) or isinstance(image_data_or_path, BytesIO):
            return image_data_or_path
        elif isinstance(image_data_or_path, str) and os.path.exists(image_data_or_path):
            with open(image_data_or_path, "rb") as f:
                return BytesIO(f.read())
        else:
            raise InvalidImageError(f"Argument must be either a valid file path, BytesIO or bytes, but was: '{image_data_or_path}'.")

    def create_headers(self, content_type) -> dict:
        headers = {
            "Content-Type": content_type,
            "X-Api-Key": self.options.api_key,
        }
        if self.options.disable_iso_code:
            headers["x-disable-iso-code"] = "true"
        if self.options.disable_checksum_check:
            headers["x-disable-checksum-check"] = "true"
        if self.options.enable_full_us_accr_code:
            headers["x-enable-full-us-accr-code"] = "true"
        if self.options.disable_image_resizing:
            headers["x-disable-image-resizing"] = "true"
        if self.options.enable_wide_range_analysis:
            headers["x-enable-wide-range-analysis"] = "true"

        return headers

    def create_form_data(self, image_data_or_paths: List[Union[str, bytes, BytesIO]]) -> MultipartEncoder:
        fields = []
        if self.options.max_reads is not None:
            fields.append(("maxreads", str(self.options.max_reads)))

        i = 0
        for image_data_or_path in image_data_or_paths:
            image_bytes = self.get_image_bytes(image_data_or_path)
            fields.append((f"image", (f"image{i}.jpg", image_bytes, "image/jpeg")))
            i += 1

        return MultipartEncoder(fields=fields)

    def get_parametrized_api_url(self) -> str:
        base_url = self.select_api_base_url()
        return urljoin(base_url, f"/transport/{self.options.type.value}")

    def select_api_base_url(self) -> str:
        if self.options.endpoint:
            return self.options.endpoint
        if self.options.cloud_service_region == "EU":
            return "https://api.cloud.adaptiverecognition.com"
        if self.options.cloud_service_region == "US":
            return "https://api.us.cloud.adaptiverecognition.com"
        raise CarmenAPIConfigError("Either 'endpoint' or 'cloud_service_region' must be specified.")
