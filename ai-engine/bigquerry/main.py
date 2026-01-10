import os
import json
from google.cloud import bigquery_storage_v1
from google.cloud.bigquery_storage_v1 import types, writer

# Setup
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"
project_id = "ai-trade-analyzer-483909"
dataset_id = "trading_data"
table_id = "dummy_table"

write_client = bigquery_storage_v1.BigQueryWriteClient()

# 1. The 'parent' must point to the specific stream
# The '_default' stream is what allows for the free 2TB/month ingestion
parent = f"projects/{project_id}/datasets/{dataset_id}/tables/{table_id}"
stream_name = f"{parent}/streams/_default"

# 2. Create the Request Template (Fixes the TypeError)
request_template = types.AppendRowsRequest()
request_template.write_stream = stream_name

# 3. Initialize the Stream Writer
stream_writer = writer.AppendRowsStream(write_client, request_template)

# 4. Prepare data (Serialize JSON to Bytes)
rows_to_insert = [
    {"full_name": "Phani", "age": 25},
    {"full_name": "Assistant", "age": 2}
]

proto_rows = types.ProtoRows()
for row in rows_to_insert:
    # The API expects serialized bytes of the row
    row_bytes = json.dumps(row).encode("utf-8")
    proto_rows.serialized_rows.append(row_bytes)

# 5. Build the actual request
request = types.AppendRowsRequest()
proto_data = types.AppendRowsRequest.ProtoData()
proto_data.rows = proto_rows
request.proto_rows = proto_data

# 6. Send
append_future = stream_writer.append_rows(request)
result = append_future.result() # Wait for confirmation

print("Data successfully streamed to BigQuery!")
