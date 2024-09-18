import boto3
from datetime import datetime, timezone
import argparse

# Set up argument parser to accept table_name as a command line argument
parser = argparse.ArgumentParser(description="Fetch DynamoDB table metrics and information.")
parser.add_argument('table_name', type=str, help="Name of the DynamoDB table")
args = parser.parse_args()

# Get the table name from the command line arguments
table_name = args.table_name

# Initialize DynamoDB client
client = boto3.client('dynamodb', region_name='us-east-2')

# Initialize CloudWatch client to fetch metrics like RCUs and WCUs
cloudwatch = boto3.client('cloudwatch', region_name='us-east-2')

# Initialize DynamoDB resource for working with the table directly
dynamodb_resource = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb_resource.Table(table_name)

# Fetch table metadata using describe_table() to get size information including indexes
response = client.describe_table(TableName=table_name)

# Extract table size in bytes (includes indexes)
table_size_bytes = response['Table']['TableSizeBytes']

# Check if the table has any global secondary indexes and get their sizes
if 'GlobalSecondaryIndexes' in response['Table']:
    gsi_sizes = {
        gsi['IndexName']: gsi['IndexSizeBytes'] 
        for gsi in response['Table']['GlobalSecondaryIndexes']
    }
else:
    gsi_sizes = {}

# Fetch provisioned read and write capacity units
rcu = response['Table']['ProvisionedThroughput']["ReadCapacityUnits"]
wcu = response['Table']['ProvisionedThroughput']["WriteCapacityUnits"]

# Placeholder for reserved capacity (DynamoDB reserved capacity is managed differently)
reserved_capacity = ""  # Still needs to be fetched from the Cost Explorer API or manually

# Print basic table info
print("************")
print("Table Name: ", table_name)
print("Total Table Size (Bytes including indexes):", table_size_bytes)
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
print("Billing Mode Summary:")
print(response['Table'].get('BillingModeSummary', {}))

print("************")

# Get the start of the current month
now = datetime.now(timezone.utc)
start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc)

# Get the current time
end_time = now

# Fetch consumed RCUs for the current month-to-date
rcu_response = cloudwatch.get_metric_statistics(
    Namespace='AWS/DynamoDB',
    MetricName='ConsumedReadCapacityUnits',
    Dimensions=[
        {'Name': 'TableName', 'Value': table_name}
    ],
    StartTime=start_of_month,
    EndTime=end_time,
    Period=86400,  # 1-day intervals
    Statistics=['Sum'],  # Summing consumed RCUs
    Unit='Count'
)

# Fetch consumed WCUs for the current month-to-date
wcu_response = cloudwatch.get_metric_statistics(
    Namespace='AWS/DynamoDB',
    MetricName='ConsumedWriteCapacityUnits',
    Dimensions=[
        {'Name': 'TableName', 'Value': table_name}
    ],
    StartTime=start_of_month,
    EndTime=end_time,
    Period=86400,  # 1-day intervals
    Statistics=['Sum'],  # Summing consumed WCUs
    Unit='Count'
)

# Sum up the consumed RCUs and WCUs from CloudWatch data points
total_rcus = sum(dp['Sum'] for dp in rcu_response['Datapoints'])
total_wcus = sum(dp['Sum'] for dp in wcu_response['Datapoints'])

# Print total consumed RCUs and WCUs month-to-date
print(f"Total Consumed RCUs for {table_name} (Month to Date): {total_rcus}")
print(f"Total Consumed WCUs for {table_name} (Month to Date): {total_wcus}")

print("************")

# Uncomment below if you want to see attribute definitions of the table using describe_table
# print("Table Attribute Definitions:", response["Table"]["AttributeDefinitions"])
