import boto3
from datetime import datetime, timezone, timedelta
import argparse
import numpy as np

# Set up argument parser to accept table_name and optionally region as command line arguments
parser = argparse.ArgumentParser(description="Fetch DynamoDB table metrics and information.")
parser.add_argument('table_name', type=str, help="Name of the DynamoDB table")
parser.add_argument('--region', type=str, default='us-east-2', help="AWS region (default: us-east-2)")
args = parser.parse_args()

# Get the table name and region from the command line arguments
table_name = args.table_name
region = args.region

# Initialize DynamoDB client
client = boto3.client('dynamodb', region_name=region)
backup_client = boto3.client('dynamodb', region_name=region)  # Backup client

# Initialize CloudWatch client to fetch metrics like latencies
cloudwatch = boto3.client('cloudwatch', region_name=region)

# Initialize DynamoDB resource for working with the table directly
dynamodb_resource = boto3.resource('dynamodb', region_name=region)
table = dynamodb_resource.Table(table_name)

# Fetch table metadata using describe_table() to get size information including indexes
response = client.describe_table(TableName=table_name)

# Extract total table size in bytes (includes indexes)
total_table_size_bytes = response['Table']['TableSizeBytes']

# Calculate table size without Global Secondary Indexes
if 'GlobalSecondaryIndexes' in response['Table']:
    gsi_sizes = {
        gsi['IndexName']: gsi['IndexSizeBytes']
        for gsi in response['Table']['GlobalSecondaryIndexes']
    }
    total_gsi_size = sum(gsi_sizes.values())
    table_size_without_gsi = total_table_size_bytes - total_gsi_size
else:
    gsi_sizes = {}
    total_gsi_size = 0
    table_size_without_gsi = total_table_size_bytes

# Fetch provisioned read and write capacity units
rcu = response['Table']['ProvisionedThroughput']["ReadCapacityUnits"]
wcu = response['Table']['ProvisionedThroughput']["WriteCapacityUnits"]

# Placeholder for reserved capacity (DynamoDB reserved capacity is managed differently)
reserved_capacity = ""  # Still needs to be fetched from the Cost Explorer API or manually

# Print basic table info
print("************")
print("Table Name: ", table_name)
print("Table Size (Bytes without GSIs):", table_size_without_gsi)
print("Total Table Size (Bytes including GSIs):", total_table_size_bytes)
print("************")

# Print table metadata (columns, data types, etc.)
print("Table Metadata:")
print("Attributes:")
for attribute in response['Table']['AttributeDefinitions']:
    print(f" - {attribute['AttributeName']}: {attribute['AttributeType']}")
print("************")

# Reserved capacity is a placeholder as it's fetched via Cost Explorer
print("Reserved Capacity (Not Implemented):")
print(reserved_capacity)

# Print the size of each Global Secondary Index (GSI), if any
print("************")
if gsi_sizes:
    print("Global Secondary Indexes and Sizes:")
    for gsi_name, gsi_size in gsi_sizes.items():
        print(f" - {gsi_name}: {gsi_size} bytes")
else:
    print("No Global Secondary Indexes (GSIs) found")

# Print table details
print("************")
print("Replica Settings:")
print(response['Table'].get('Replicas', []))

print("************")
print("Provisioned Throughput:")
print(f"Read Capacity Units (RCU): {rcu}")
print(f"Write Capacity Units (WCU): {wcu}")

print("************")

# Define time intervals
now = datetime.now(timezone.utc)
start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc)
start_of_day = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)
end_time = now

# Function to get metric statistics
def get_metric_statistics(metric_name, start_time, end_time):
    return cloudwatch.get_metric_statistics(
        Namespace='AWS/DynamoDB',
        MetricName=metric_name,
        Dimensions=[
            {'Name': 'TableName', 'Value': table_name}
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=86400,  # 1-day intervals
        Statistics=['Sum'],  # Summing consumed RCUs/WCUs
        Unit='Count'
    )

# Function to calculate total consumed units
def calculate_total_consumed_units(metric_name, start_time, end_time):
    response = get_metric_statistics(metric_name, start_time, end_time)
    data_points = response['Datapoints']
    return sum(dp['Sum'] for dp in data_points) if data_points else 0

# Retrieve and print the consumed RCUs and WCUs for current day and month-to-date
def print_consumed_units():
    # Month-to-date consumption
    total_rcu_mtd = calculate_total_consumed_units('ConsumedReadCapacityUnits', start_of_month, end_time)
    total_wcu_mtd = calculate_total_consumed_units('ConsumedWriteCapacityUnits', start_of_month, end_time)
    
    # Current day consumption
    total_rcu_day = calculate_total_consumed_units('ConsumedReadCapacityUnits', start_of_day, end_time)
    total_wcu_day = calculate_total_consumed_units('ConsumedWriteCapacityUnits', start_of_day, end_time)
    
    print(f"Total Consumed RCUs for {table_name} (Month to Date): {total_rcu_mtd}")
    print(f"Total Consumed WCUs for {table_name} (Month to Date): {total_wcu_mtd}")
    print(f"Total Consumed RCUs for {table_name} (Current Day): {total_rcu_day}")
    print(f"Total Consumed WCUs for {table_name} (Current Day): {total_wcu_day}")

print("************")
print_consumed_units()
print("************")

# Define the latency metrics to retrieve
latency_metrics = {
    'SuccessfulRequestLatency': 'SuccessfulRequestLatency'
}

# Function to calculate percentiles
def calculate_percentiles(data_points, percentiles):
    if not data_points:
        return {p: None for p in percentiles}
    
    values = [dp['Average'] for dp in data_points if 'Average' in dp]
    if not values:
        return {p: None for p in percentiles}
    
    sorted_values = sorted(values)
    results = {}
    for p in percentiles:
        idx = int(p / 100.0 * len(sorted_values)) - 1
        results[p] = sorted_values[max(0, min(idx, len(sorted_values) - 1))]
    return results

# Retrieve metrics and calculate required statistics
def print_metrics(metric_name):
    response = get_metric_statistics(metric_name, start_of_month, end_time)
    data_points = response['Datapoints']
    
    # Calculate average and maximum
    average = sum(dp['Average'] for dp in data_points if 'Average' in dp) / len(data_points) if data_points else 0
    maximum = max(dp['Maximum'] for dp in data_points if 'Maximum' in dp) if data_points else 0
    
    # Calculate percentiles
    percentiles = [95, 99]
    percentile_values = calculate_percentiles(data_points, percentiles)

    print(f"Average {metric_name} for {table_name} (Month to Date): {average} ms")
    print(f"Maximum {metric_name} for {table_name} (Month to Date): {maximum} ms")
    print(f"95th Percentile (p95) of {metric_name}: {percentile_values[95]} ms")
    print(f"99th Percentile (p99) of {metric_name}: {percentile_values[99]} ms")

print("************")
print_metrics('SuccessfulRequestLatency')
print("************")

# Function to get the latest backup and its size
def get_latest_backup_size():
    try:
        # List backups with a limit to get the latest one
        response = backup_client.list_backups(TableName=table_name, Limit=1)
        
        # Print the full response to check its structure
        print("Backup List Response:", response)
        
        if 'Backups' in response and response['Backups']:
            # Assuming the response returns backups in a sorted order
            latest_backup = response['Backups'][0]
            backup_arn = latest_backup['BackupArn']
            
            # Describe the latest backup to get its details
            backup_description = backup_client.describe_backup(BackupArn=backup_arn)
            backup_size = backup_description['BackupDescription']['BackupDetails'].get('BackupSizeBytes', 'Size not available')
            
            return backup_size
        return 'No backups found'
    
    except Exception as e:
        print(f"Error retrieving backup size: {e}")
        return 'Error retrieving backup size'

# Fetch and print the latest backup size
print("************")
latest_backup_size = get_latest_backup_size()
print(f"Latest Backup Size: {latest_backup_size} bytes")
print("************")
