"""
################################################
#  Server side encryption using KMS usecase-1  #
################################################
"""
import os 
import sys
import json
import random
import subprocess
import boto3

def main():
    """
    #######################################
    #     Server side encryption on S3    #
    #######################################
    """
    try:

        #########################################################
        #   creating a s3 bucket with some name randomization   #
        #########################################################
        s3_client = boto3.client('s3')
        bucket_name = 'dp-workshop-bucket' + str(random.randint(1, 100000))
        
        # Note: if statement necessary because locationconstraint does not support all regions today
        region = boto3.Session().region_name
        if 'us-east-1' in region:
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={
                    'LocationConstraint': region
                }
            )
        waiter = s3_client.get_waiter('bucket_exists')
        waiter.wait(Bucket=bucket_name)
        response = s3_client.put_bucket_tagging(
            Bucket=bucket_name,
            Tagging={
                'TagSet': [
                    {
                        'Key': 'workshop',
                        'Value': 'data-protection'
                    },
                ]
            }
        )
        
        ################################################################
        #   referencing the unencrypted text file plaintext_u on disk  #
        ################################################################
        current_directory = os.path.dirname(os.path.realpath(__file__)) + '/'
        plaintext_filename_path = current_directory  + 'plaintext_u.txt'
        
        ###############################################################################################
        #   uploading the unencrypted file to S3 and telling S3 to server side encrypt it             #
        #   you can see that the put_object S3 API is being used here                                 #
        #   data flows over TLS to s3 and then S3 service encrypt it using the KMS key you provided   #
        ###############################################################################################
        encrypted_filename = 'encrypted_e.txt'
        response = s3_client.put_object(
            Body=open(plaintext_filename_path, 'rb'),
            Bucket=bucket_name,
            Key=encrypted_filename,
            ServerSideEncryption='aws:kms',
            SSEKMSKeyId='alias/kms_key_sse_usecase_1'
        )
         
        #####################################################################################
        #   Do a S3 getobject on the encrypted file encrypted_e.txt that's stored on S3     #
        #   The unencrypted cycled file plaintext_cycled_u.txt is stored in the filesystem  #
        #####################################################################################
        response = s3_client.get_object(
            Bucket=bucket_name,
            Key=encrypted_filename
        )
        
        current_directory = os.path.dirname(os.path.realpath(__file__)) + '/'
        plaintext_cycled_filename_path = current_directory + 'plaintext_cycled_u.txt'
        
        with open(plaintext_cycled_filename_path, 'wb') as f:
            f.write(response['Body'].read())
            
        print("\nModule run was successful !!")
        print("\nplaintext_u.txt was successfully uploaded to S3,server side encrypted and stored as encrypted_e.txt!!")
        print("\n Step 2 completed successfully")
        
        
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    else:
        exit(0)

if __name__ == "__main__":
    main()
    