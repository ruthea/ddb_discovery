# DynamoDB Metrics and Table Information Script

This Python script fetches and displays various metrics and information about an Amazon DynamoDB table. It provides insights into table size, provisioned throughput, consumed capacity units, and latency metrics. The script also prints detailed metadata about the table's attributes.

## Features

- Fetches and prints table size, both with and without Global Secondary Indexes (GSIs).
- Displays the size of each Global Secondary Index (GSI).
- Shows provisioned read and write capacity units (RCU and WCU).
- Retrieves and prints consumed RCUs and WCUs for the current day and month-to-date.
- Calculates and displays average, maximum, 95th percentile (p95), and 99th percentile (p99) for latency metrics.
- Prints table metadata, including column names and data types.

## Prerequisites

- Python 3.x
- AWS SDK for Python (Boto3)
- AWS credentials configured on your machine
- **NumPy** (for numerical operations)

## Installation

1. Clone this repository:
   ```sh
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

2. Install the required Python packages:
   ```sh
   pip install boto3 numpy
   ```

## Usage

Run the script from the command line and provide the DynamoDB table name as a parameter:

```sh
python script.py <table_name>
```

Replace `<table_name>` with the name of your DynamoDB table.

### Example

```sh
python script.py Books
```

## Script Details

### Script Overview

- **Imports**:
  - `boto3`: AWS SDK for Python
  - `datetime`: For working with dates and times
  - `argparse`: For command-line argument parsing
  - `numpy`: For numerical operations (e.g., calculating percentiles)

- **Functions**:
  - `get_metric_statistics(metric_name, start_time, end_time)`: Fetches metric statistics from CloudWatch.
  - `calculate_total_consumed_units(metric_name, start_time, end_time)`: Calculates the total consumed units for a given metric.
  - `calculate_percentiles(data_points, percentiles)`: Calculates specified percentiles from data points.
  - `print_metrics(metric_name)`: Retrieves and prints latency metrics, including average, maximum, and percentiles.
  - `print_consumed_units()`: Retrieves and prints the total consumed RCUs and WCUs for the current day and month-to-date.

### Sections

- **Table Size and GSIs**:
  - Displays total table size and size without GSIs.
  - Lists the size of each GSI.

- **Provisioned Throughput**:
  - Shows the read and write capacity units.

- **Table Metadata**:
  - Prints attribute names and data types.

- **Consumed Units**:
  - Displays RCUs and WCUs consumed for the current day and month-to-date.

- **Latency Metrics**:
  - Provides average, maximum, p95, and p99 for latency metrics.

## Notes

- Ensure your AWS credentials are configured properly.
- Install `numpy` using `pip install numpy` if not already installed.
- Modify the script if needed to fit your specific use case or metric requirements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

This updated `README.md` now includes instructions for installing the `numpy` dependency along with the other required packages.
