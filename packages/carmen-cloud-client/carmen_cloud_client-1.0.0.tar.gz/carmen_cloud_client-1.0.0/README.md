# Carmen Cloud Client by Adaptive Recognition

Python client for [Carmen Cloud](https://cloud.adaptiverecognition.com/) by [Adaptive Recognition](https://adaptiverecognition.com/). This unified library provides you with access to both the **Vehicle API** and the **Transportation & Cargo API**.

## Supported API Versions

- Vehicle API: v1.4
- Transportation & Cargo API: v1.0

## 🛠️ How to Install

```sh
pip install adaptive-recognition-carmen-cloud-client
```

## 🚀 Usage

You can utilize either the Vehicle API or the Transportation & Cargo API based on your needs.

### 🚗 Vehicle API

```python
from carmen_cloud_client import VehicleAPIClient, SelectedServices,  Locations

client = VehicleAPIClient(
    api_key="<YOUR_API_KEY>",
    services=SelectedServices(anpr=True, mmr=True),
    input_image_location=Locations.Europe.Hungary,
    cloud_service_region="EU"
)

response = client.send("./car.jpg")
print(response)
```

### 🚚 Transportation & Cargo API

```python
from carmen_cloud_client import TransportAPIClient, CodeType

client = TransportAPIClient(
    api_key="<YOUR_API_KEY>",
    code_type=CodeType.ISO,
    cloud_service_region="EU"
)

response = client.send("./container.jpg")
print(response)
```

## 🔧 Development

For more information about developing and contributing to this project, see [DEVELOPMENT.md](DEVELOPMENT.md).
