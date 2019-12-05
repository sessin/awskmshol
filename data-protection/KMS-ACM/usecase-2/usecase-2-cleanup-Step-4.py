"""
###########################################################################
#   CLIENT SIDE ENCRYPTION - KMS  CLEAN-UP  FOR USECASE-2                 #
#   LET'S DELETE THE BUCKET AND THE OBJECTS THAT WE CREATED FOR USECASE-2 #
#   LET's ALSO DELETE THE FILES LOCALLY CREATED IN THE FILESYSTEM         #
###########################################################################
"""
import subprocess
import sys
from pathlib import Path
import os 
import boto3


def main():
    """
    #######################################################
    #   Cleanup all data created for kms-cse-usecase-2    #
    #######################################################
    """
    try:
        s3_client = boto3.client('s3')
        
        ###########################################################################
        #   Remove all the files created in the local file system for usecase-2   #
        ###########################################################################
        current_directory_path = os.path.dirname(os.path.realpath(__file__)) + '/'
        encrypted_filename_path = current_directory_path + 'encrypted_e.txt'
        plaintext_cycled_filename_path = current_directory_path + 'plaintext_u_cycled.txt'
    
        if Path(encrypted_filename_path).exists():
            os.remove(encrypted_filename_path)
            
        if Path(plaintext_cycled_filename_path).exists():
            os.remove(plaintext_cycled_filename_path)
    
        response = s3_client.list_buckets()
        for bucket_name in response['Buckets']:
            if bucket_name['Name'].startswith('dp-workshop') or bucket_name['Name'].startswith('dp-workshop-bucket-cw-event'):
                try:
                    response = s3_client.get_bucket_tagging(
                        Bucket=bucket_name['Name']
                    )
                except:
                    pass
        
                if 'TagSet' in response: 
                    if (response['TagSet'][0]['Key'] == 'workshop') and (response['TagSet'][0]['Value'] == 'data-protection'):
                        # Delete the objects stored in S3 within dp-workshops-bucket
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
                        
                if 'TagSet' in response: 
                    if (response['TagSet'][0]['Key'] == 'whatfor') and (response['TagSet'][0]['Value'] == 'usecase-2-cse'):
                        # Delete the objects stored in S3 within buckets that start with dp-workshop-bucket-cw-event
                        response = s3_client.delete_bucket(
                            Bucket=bucket_name['Name']
                        )
                        
        ########################################################
        #   Delete the kms key alias kms_key_cse_usecase_2     #
        #   Schedule the key for deletion                      #                         
        ########################################################
        kms_client = boto3.client('kms')
        response = kms_client.list_aliases(
            Limit=100
        )
        
        alias_exists = False
        for alias in response['Aliases']:
            if alias['AliasName'] == 'alias/kms_key_cse_usecase_2':
                alias_exists = True
        
        if alias_exists:
            response = kms_client.describe_key(
                KeyId='alias/kms_key_cse_usecase_2'
            )
            
            kms_key_id = response['KeyMetadata']['KeyId']
            if response['KeyMetadata']['KeyState'] != 'PendingDeletion':
                response = kms_client.schedule_key_deletion(
                    KeyId=kms_key_id,
                    PendingWindowInDays=7
                )
            
            # Delete the alias so that a use can run this use-case multiplt times with the same alias
            response_del_alias = kms_client.delete_alias(
                AliasName='alias/kms_key_cse_usecase_2'
            )
        
        # Cleanup the cloudformation stack 
        cf_client = boto3.client('cloudformation')
        
        print("\n Cleanup Successful") 
        print("\n Step 4 completed successfully")

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    else:
        exit(0)

if __name__ == "__main__":
    main()
    