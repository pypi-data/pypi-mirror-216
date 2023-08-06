#!/usr/bin/env bash

datamodel-codegen --input-file-type jsonschema --input assets/transport/response.schema.json --output carmen_cloud_client/transport/response.py
datamodel-codegen --input-file-type jsonschema --input assets/vehicle/response.schema.json --output carmen_cloud_client/vehicle/response.py
