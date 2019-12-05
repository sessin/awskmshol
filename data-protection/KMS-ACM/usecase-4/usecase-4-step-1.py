"""
####################################################################################################
# Create DynamoDB table called shared_variables_crypto_builders or storing key value               #
# pairs shared across multiple python modulesshared variables can be private keys,variables        #
# needed for ACM certs etc.Since the nature of stored data is sensitive,the DDB table is encrypted #
####################################################################################################
"""
import subprocess
import sys
import boto3

def main():
    """
    ###################################################################################
    #  DynamoDB table  shared_variables_crypto_builders for storing shared variables  #
    ###################################################################################
    """
    try:
        ddb_client = boto3.client('dynamodb')
        # Create DynamoDB table for storing shared variables across python modules
        try:
            ddb_client.describe_table(TableName='shared_variables_crypto_builders')
            print("shared_variables_crypto_builders Table already exists, please delete it before re-running this module")
        except ddb_client.exceptions.ResourceNotFoundException:
            # Since table does not exist create it
            ddb_client.create_table(
                TableName='shared_variables_crypto_builders',
                KeySchema=[
                    {
                        'AttributeName': 'shared_variables',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'session',
                        'KeyType': 'RANGE'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'shared_variables',
                        'AttributeType': 'N'
                    },
                    {
                        'AttributeName': 'session',
                        'AttributeType': 'N'
                    },
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                },
                SSESpecification={
                    'Enabled': True,
                }
            )
            
            print("Pending DynamoDB table creation for storing shared variables")
            print("\nThis step will take about 30 seconds to complete")
            waiter = ddb_client.get_waiter('table_exists')
            waiter.wait(TableName='shared_variables_crypto_builders')
            ddb_client.put_item(TableName='shared_variables_crypto_builders', \
                                Item={'shared_variables':{'N':'1000'}, 'session':{'N':'1000'}})
            print("\nshared_variables_crypto_builders DynamoDB table created")
            print("\nStep-1 has been successfully completed \n")

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    else:
        exit(0)

if __name__ == "__main__":
    main()
    