"""
###############################################################################
#  Cleanup all resources created within python modules for ACM usecase-4      #
#                                                                             #
#  1. S3 buckets used for CRL(Certificate revocation list)                    #
#                                                                             #
#  2. The private certifiate authority is deleted                             #
#                                                                             #
#  3. All the files created in the filesystem is deleted                      #
#                                                                             #
###############################################################################
"""
import os
import subprocess
import sys
from pathlib import Path
import time
import boto3

def main():
    """
    ###########################################
    # Cleanup all resources that were created #
    ###########################################
    """
    try:
        s3_client = boto3.client('s3')
        acm_pca_client = boto3.client('acm-pca')
        ddb_client = boto3.client('dynamodb')
        
        ####################################################################################
        #  Remove all the files created in the local filesystem as part of this usecase    #
        ####################################################################################
    
        current_directory_path = os.path.dirname(os.path.realpath(__file__)) + '/'
        print("This step will take about 1 minute to complete\n")

        self_signed_cert_filename_path = current_directory_path + 'self-signed-cert.pem'
        signed_subordinate_ca_cert_filename_path = current_directory_path + 'signed_subordinate_ca_cert.pem'
        webserver_cert_path = current_directory_path + 'webserver_cert.pem'
        webserver_cert_chain_path = current_directory_path + 'webserver_cert_chain.pem'
        webserver_privkey_path = current_directory_path + 'webserver_privkey.pem'
    
        if Path(self_signed_cert_filename_path).exists():
            os.remove(self_signed_cert_filename_path)
            
        if Path(signed_subordinate_ca_cert_filename_path).exists():
            os.remove(signed_subordinate_ca_cert_filename_path)
            
        if Path(webserver_cert_path).exists():
            os.remove(webserver_cert_path)   
            
        if Path(webserver_cert_chain_path).exists():
            os.remove(webserver_cert_chain_path)    
            
        if Path(webserver_privkey_path).exists():
            os.remove(webserver_privkey_path) 
            
        ##########################################
        #  Delete the subordinate pca created    #
        ##########################################
        subordinate_pca_arn = None 
        try:
            response = ddb_client.describe_table(TableName='shared_variables_crypto_builders')
            if response is not None:
                response = ddb_client.get_item(TableName='shared_variables_crypto_builders', \
                    Key={
                            'shared_variables': {
                                'N': '1000',
                            },
                            'session': {
                                'N': '1000',
                            },
                        },
                )
                                
                if  'subordinate_pca_arn' in response['Item']:
                    subordinate_pca_arn = response['Item']['subordinate_pca_arn']['S']
                
                ddb_client = boto3.client('dynamodb')
      
                # Delete the DDB Table that stores key value pairs shared across multiple python modules
                response = ddb_client.delete_table(
                    TableName='shared_variables_crypto_builders'
                )
        except ddb_client.exceptions.ResourceNotFoundException:
            print("No DDB table found to delete !! that's OK")
            
        if subordinate_pca_arn is not None:
            response = acm_pca_client.describe_certificate_authority(
                CertificateAuthorityArn=subordinate_pca_arn
            )
            
            if response['CertificateAuthority']['Status'] != 'DELETED':
                if response['CertificateAuthority']['Status'] == 'ACTIVE':
                    response = acm_pca_client.update_certificate_authority(
                        CertificateAuthorityArn=subordinate_pca_arn,
                        Status='DISABLED'
                    )
                
                response = acm_pca_client.delete_certificate_authority(
                    CertificateAuthorityArn=subordinate_pca_arn,
                    PermanentDeletionTimeInDays=7
                )
                time.sleep(20)
        
        ###################################################
        #   remove all the s3 buckets that were created   #
        ###################################################
        response = s3_client.list_buckets()
        for bucket_name in response['Buckets']:
            if bucket_name['Name'].startswith('builder-acm-pca-usecase-4-bucket-pca-crl') :
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
                        
        print("\nEverything cleaned up ,you are all good !!\n")
        print("\nStep-10 cleanup has been successfully completed \n")
    
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    else:
        exit(0)
 

if __name__ == "__main__":
    main()
    