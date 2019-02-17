import boto3
import subprocess
import os
import datetime
import time
import sys

if len(sys.argv) == 2:
    bucket_name = sys.argv[1]
else:
    exit(1)

#finding out file names in current directory
proc = subprocess.Popen("ls", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
output = proc.stdout.read().decode('utf-8')
list = output.split("\n")
del list[-1]
#map {name file = lastmodification} of the local files
ondevice = {}
for e in list:
    ondevice[e] = datetime.datetime.fromtimestamp(os.stat(e)[9])

#map {name file = lastmodification} of the files on the cloud
oncloud = {}
s3 = boto3.client("s3")
files = s3.list_objects_v2(Bucket = bucket_name)
if files['KeyCount'] != 0:
    for file in files['Contents'] :
            oncloud[file['Key']] = file['LastModified']

for key,val in ondevice.items():
    print("{} = {}".format(key, val))
    #converting dates
    local_time = time.strptime(val.strftime("%Y-%m-%dT%H:%M:%S.%f"), "%Y-%m-%dT%H:%M:%S.%f")
    local_seconds = time.mktime(local_time)
    utc_time = time.gmtime(local_seconds)
    dtondevice = datetime.datetime(*utc_time[:6])
    if key in oncloud:
        #the file in already in the cloud
        dtoncloud = oncloud[key].replace(tzinfo=None)
        #check for date last modification
        if dtondevice <= dtoncloud :
            print("UPLOAD NOT NEEDED " + str(key))
        else:
            print("UPLOADING FILE : " + str(key))
            s3.upload_file(str(key), bucket_name, str(key))
    else:
        print("UPLOADING NEW FILE : " + str(key))
        s3.upload_file(str(key), bucket_name, str(key))

