"""
#############################################################
#    server side encryption - kms clean up for usecase-1    #
#############################################################
"""
from pathlib import Path
import subprocess
import sys
import os 
import json
import boto3

def main():
    """
    #######################################################
    #     Cleaning up all S3 buckets and files created    #
    #######################################################
    """
    try:
        print("\n This step takes about 5 seconds to complete")
        s3_client = boto3.client('s3')
        response = s3_client.list_buckets()
        for bucket_name in response['Buckets']:
            if bucket_name['Name'].startswith('dp-workshop'):
                try:
                    response = s3_client.get_bucket_tagging(
                        Bucket=bucket_name['Name']
                    )
                except:
                    pass
        
                if 'TagSet' in response: 
                    if (response['TagSet'][0]['Key'] == 'workshop') and (response['TagSet'][0]['Value'] == 'data-protection'):
                        # Delete the objects stored in S3 within dp-workshop-bucket
                        response = s3_client.list_objects(
                            Bucket=bucket_name['Name'],
                            )
                            
                        if 'Contents' in response:    
                            for object_name in response['Contents']:    
                                response = s3_client.delete_object(
                                    Bucket=bucket_name['Name'],
                                    Key=object_name['Key']
                                )
                        
                        response = s3_client.delete_bucket(
                            Bucket=bucket_name['Name']
                        )
            
        # Remove any files that were created as part of usecase-1
        current_directory = os.path.dirname(os.path.realpath(__file__)) + '/'
        plaintext_cycled_filename_path = current_directory + 'plaintext_cycled_u.txt'
        
        if Path(plaintext_cycled_filename_path).exists():
            os.remove(plaintext_cycled_filename_path)
            
        kms_client = boto3.client('kms')
        
        response = kms_client.list_aliases(
            Limit=100
        )
        
        alias_exists = False
        for alias in response['Aliases']:
            if alias['AliasName'] == 'alias/kms_key_sse_usecase_1':
                alias_exists = True
        
        if alias_exists:
            response = kms_client.describe_key(
                KeyId='alias/kms_key_sse_usecase_1'
            )
            
            kms_key_id = response['KeyMetadata']['KeyId']
            
            if response['KeyMetadata']['KeyState'] != 'PendingDeletion':
                response = kms_client.schedule_key_deletion(
                    KeyId=kms_key_id,
                    PendingWindowInDays=7
                )
            
            # Delete the alias so that a use can run this use-case multiplt times with the same alias
            kms_client.delete_alias(
                AliasName='alias/kms_key_sse_usecase_1'
            )
    
        print("\n Cleanup Successful") 
        print("\n Step 3 cleanup completed successfully")
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    else:
        exit(0)

if __name__ == "__main__":
    main()
    