import boto3
import datetime

# Set up boto3 clients
dynamodb = boto3.client('dynamodb',region_name="us-east-2")
cloudwatch = boto3.client('cloudwatch',region_name="us-east-2")

# Define the table name and time range
table_name = 'Books'
start_time = datetime.datetime.now() - datetime.timedelta(days=1)
end_time = datetime.datetime.now()

# 1. Get provisioned capacity for the table
table_description = dynamodb.describe_table(TableName=table_name)
provisioned_rcu = table_description['Table']['ProvisionedThroughput']['ReadCapacityUnits']
provisioned_wcu = table_description['Table']['ProvisionedThroughput']['WriteCapacityUnits']

print(f"Provisioned RCU: {provisioned_rcu}, Provisioned WCU: {provisioned_wcu}")

# 2. Get Consumed Read Capacity Units (RCUs) from CloudWatch
response_rcu = cloudwatch.get_metric_statistics(
    Namespace='AWS/DynamoDB',
    MetricName='ConsumedReadCapacityUnits',
    Dimensions=[{'Name': 'TableName', 'Value': table_name}],
    StartTime=start_time,
    EndTime=end_time,
    Period=86400,  # 1 day in seconds
    Statistics=['Sum']
)

# 3. Get Consumed Write Capacity Units (WCUs) from CloudWatch
response_wcu = cloudwatch.get_metric_statistics(
    Namespace='AWS/DynamoDB',
    MetricName='ConsumedWriteCapacityUnits',
    Dimensions=[{'Name': 'TableName', 'Value': table_name}],
    StartTime=start_time,
    EndTime=end_time,
    Period=86400,  # 1 day in seconds
    Statistics=['Sum']
)

# 4. Get Throttled Requests from CloudWatch
response_throttled = cloudwatch.get_metric_statistics(
    Namespace='AWS/DynamoDB',
    MetricName='ThrottledRequests',
    Dimensions=[{'Name': 'TableName', 'Value': table_name}],
    StartTime=start_time,
    EndTime=end_time,
    Period=86400,  # 1 day in seconds
    Statistics=['Sum']
)

# Print the metrics
consumed_rcu = response_rcu['Datapoints'][0]['Sum'] if response_rcu['Datapoints'] else 0
consumed_wcu = response_wcu['Datapoints'][0]['Sum'] if response_wcu['Datapoints'] else 0
throttled_requests = response_throttled['Datapoints'][0]['Sum'] if response_throttled['Datapoints'] else 0

print(f"Consumed RCU: {consumed_rcu}")
print(f"Consumed WCU: {consumed_wcu}")
print(f"Throttled Requests: {throttled_requests}")

# Compare consumed capacity to provisioned capacity
if consumed_rcu > provisioned_rcu:
    print(f"Read Capacity exceeded provisioned capacity by: {consumed_rcu - provisioned_rcu} units")

if consumed_wcu > provisioned_wcu:
    print(f"Write Capacity exceeded provisioned capacity by: {consumed_wcu - provisioned_wcu} units")

