import subprocess
import time
import sys

def usage():
    print("USAGE: python3.6 Automatic-Backup-on-AWS-S3.py <bucket_name> --opt ")
    print(" --opt can be : \n --schedule + (optional) n to automatically sync every n hour")
    print(" --sync  to automatically sync every change in the files")

if len(sys.argv) >= 3:
    bucket_name = sys.argv[1]
    mode = sys.argv[2]
    if mode == "--schedule" :
        if len(sys.argv) == 4:
            nhour = sys.argv[3]
        else:
            #deafualt value
            nhour = 1
        if nhour < 1:
            usage()
            exit(1)
        #start backupAWS every nhour
        torun = "python3.6 backupAWS.py " + bucket_name
        while 1:
            proc = subprocess.Popen(torun, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            error = proc.stderr.read().decode("utf-8")
            if error != "":
                print("Error --> " + error)
            else:
                time.sleep(3600 * nhour)
    else:
        if mode == "--sync" :
            torun = "repyt -c 'python3.6 backupAWS.py' " + bucket_name
            proc = subprocess.Popen(torun, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            error = proc.stderr.read().decode("utf-8")
            if error != "":
                print("Error --> " + error)
        else:
            usage()
            exit(1)
else:
    usage()
    exit(1)

