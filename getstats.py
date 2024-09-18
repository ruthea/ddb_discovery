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
