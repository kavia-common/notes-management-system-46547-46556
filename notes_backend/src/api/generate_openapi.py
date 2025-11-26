import json
import os

from src.api.main import app

"""
Utility script to generate and persist the OpenAPI schema to interfaces/openapi.json.
Run this after modifying API routes to keep the published spec up-to-date.
"""

# Force rebuild of OpenAPI schema
app.openapi_schema = None  # reset any cached schema
openapi_schema = app.openapi()

# Write to file
output_dir = "interfaces"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "openapi.json")

with open(output_path, "w") as f:
    json.dump(openapi_schema, f, indent=2)
