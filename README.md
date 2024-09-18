# DynamoDB Metrics and Metadata Fetcher

This script fetches and displays various metrics and metadata for a specified DynamoDB table. It includes details such as table size, provisioned throughput, consumed capacity units, latency metrics, and table metadata.

## Features

- **Table Size**: Displays the total size of the table, including and excluding Global Secondary Indexes (GSIs).
- **Table Metadata**: Lists attributes and their types.
- **Provisioned Throughput**: Shows read and write capacity units.
- **Consumed Capacity Units**: Provides monthly and daily consumed read and write capacity units (RCUs and WCUs).
- **Latency Metrics**: Calculates average, maximum, 95th percentile (p95), and 99th percentile (p99) latencies for successful requests.

## Requirements

- Python 3.x
- `boto3` library
- `numpy` library

You can install the required libraries using pip:

```bash
pip install boto3 numpy
```

## Usage

To run the script, provide the table name and optionally specify the AWS region. The default region is `us-east-2`.

### Command Line Arguments

- `table_name`: The name of the DynamoDB table (required).
- `--region`: The AWS region where the DynamoDB table is located (optional, default is `us-east-2`).

### Example

```bash
python your_script.py MyTableName --region us-west-1
```

Replace `your_script.py` with the name of your script file and `MyTableName` with the name of your DynamoDB table.

## Sample Output

```
************
Table Name:  MyTableName
Table Size (Bytes without GSIs): 12345678
Total Table Size (Bytes including GSIs): 23456789
************
Table Metadata:
Attributes:
 - id: S
 - name: S
 - createdAt: N
************
Reserved Capacity (Not Implemented):

************
Global Secondary Indexes and Sizes:
 - MyIndexName: 987654 bytes
************
Replica Settings:
[]
************
Provisioned Throughput:
Read Capacity Units (RCU): 5
Write Capacity Units (WCU): 5
************
Total Consumed RCUs for MyTableName (Month to Date): 12345
Total Consumed WCUs for MyTableName (Month to Date): 67890
Total Consumed RCUs for MyTableName (Current Day): 1234
Total Consumed WCUs for MyTableName (Current Day): 5678
************
Average SuccessfulRequestLatency for MyTableName (Month to Date): 25.0 ms
Maximum SuccessfulRequestLatency for MyTableName (Month to Date): 100.0 ms
95th Percentile (p95) of SuccessfulRequestLatency: 50.0 ms
99th Percentile (p99) of SuccessfulRequestLatency: 75.0 ms
************
```

## Notes

- Ensure that your AWS credentials are configured properly.
- Reserved capacity is managed differently and is not implemented in this script.
```

Feel free to adjust any details as needed for your specific use case!
