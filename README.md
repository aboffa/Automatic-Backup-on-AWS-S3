# Automatic-Backup-on-AWS-S3
Simple python scriptm to backup files on AWS S3 storage service

### Requirements

To run Automatic-Backup-on-AWS-S3 needs: 

  - Correct configuration of [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)
  ```sh
    aws configure
  ```
  
  - [boto3](https://pypi.org/project/boto3/) 
  ``` sh 
    pip install boto3
  ```
  in order to connet to AWS 
  - [repyt](https://github.com/di/repyt) 
  
  ``` sh
    pip install repyt
  ```
  in order to run the script every change in the files

  
### Usage: 
``` sh
python3.6 Automatic-Backup-on-AWS-S3.py <bucket_name> --opt 
```
--opt can be : 
  - --schedule + (optional) integer n to automatically sync local directory and the cloud every n hour
  - --sync to automatically sync local directory and the cloud every change in the files
  
### Some info:
Versioning --> NO becuase for the porpous of this simple backup manager it's useless to have different version of the same object
Lifecycle --> Transition to Glacier after 30 day becuase it's cheap to maintain data in Glacier
