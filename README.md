# DynamoDB Table Metrics & Information Fetcher

This Python script retrieves and displays key metrics and information about an Amazon DynamoDB table. It uses AWS Boto3 to gather detailed data such as the table's size (including Global Secondary Indexes), provisioned capacity, consumed read/write capacity, and other DynamoDB table attributes.

## Features

- **Table Size**: Fetches the size of the DynamoDB table in bytes, including any Global Secondary Indexes (GSIs).
- **Provisioned Capacity**: Displays the provisioned Read Capacity Units (RCUs) and Write Capacity Units (WCUs).
- **Consumed Capacity**: Retrieves month-to-date consumed RCUs and WCUs using CloudWatch metrics.
- **Billing Mode**: Provides the billing mode of the table (e.g., `PROVISIONED` or `PAY_PER_REQUEST`).
- **Global Secondary Indexes**: Lists each GSI and its respective size.
- **Replica Information**: Displays the table's replica settings if applicable.
- **Command-line Input**: The table name is provided as a command-line argument for flexibility.

## Prerequisites

To use this script, ensure you have the following:

- **Python 3.6+** (Tested on Python 3.12)
- **Boto3** (AWS SDK for Python)
  
  You can install Boto3 using:
  
  ```bash
  pip install boto3
  ```

- **AWS Credentials**: You must have valid AWS credentials configured on your machine. The credentials should allow access to DynamoDB and CloudWatch.

## Usage

To run the script, you need to provide the DynamoDB table name as a command-line argument.

### Command

```bash
python3 dynamodb_metrics.py <table_name>
```

Replace `<table_name>` with the name of your DynamoDB table.

### Example

```bash
python3 dynamodb_metrics.py Books
```

This command will fetch and display information about the `Books` table.

## Output

The script prints out detailed information about the DynamoDB table in the following sections:

- **Table Size**: Total size of the table, including Global Secondary Indexes.
- **Provisioned Capacity**: The provisioned RCUs and WCUs of the table.
- **Consumed Capacity**: Month-to-date consumed RCUs and WCUs, fetched from CloudWatch.
- **Billing Mode**: Billing mode details.
- **Global Secondary Indexes (GSIs)**: A list of each GSI along with its size.
- **Replica Settings**: Any replica configurations for the table.

### Sample Output

```bash
************
Table Name: Books
Total Table Size (Bytes including indexes): 51200
************
Reserved Capacity (Not Implemented):

************
Global Secondary Indexes and Sizes:
 - TitleIndex: 20480 bytes
************
Replica Settings:
[]
************
Provisioned Throughput:
Read Capacity Units (RCU): 5
Write Capacity Units (WCU): 5
************
Billing Mode Summary:
{'BillingMode': 'PROVISIONED'}
************
Total Consumed RCUs for Books (Month to Date): 1024
Total Consumed WCUs for Books (Month to Date): 512
************
```

## How It Works

1. **Table Metadata**: The script uses the `describe_table` method from Boto3 to retrieve the table's metadata, such as size and GSIs.
2. **Provisioned Capacity**: Extracts the provisioned throughput settings (RCU/WCU) directly from the table's metadata.
3. **Consumed Capacity**: Uses the `get_metric_statistics` method from CloudWatch to fetch the consumed capacity units for the table for the current month-to-date.
4. **Global Secondary Indexes (GSIs)**: If the table has any GSIs, their size in bytes is also retrieved and displayed.
5. **Billing and Replicas**: The script shows the billing mode (e.g., `PROVISIONED`) and any replica configurations if present.

## AWS Permissions Required

Make sure your AWS credentials allow the following permissions:

- `dynamodb:DescribeTable`
- `cloudwatch:GetMetricStatistics`

You can modify your AWS IAM policy to include these permissions for the user running this script.

## Contribution

If you'd like to contribute:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-branch-name`).
3. Commit your changes (`git commit -m "Add some feature"`).
4. Push to the branch (`git push origin feature-branch-name`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

With this `README.md`, users will have clear instructions on how to set up, run, and understand the script. It also covers the prerequisites and provides an example output, making it user-friendly.