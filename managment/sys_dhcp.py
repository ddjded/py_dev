import subprocess

SCOPE = input("Scope DNS - ")
IP = input("IP - ")
MAC = input("MAC - ")
DESCRIPTION = input("Description - ")

netshcmd = subprocess.Popen('netsh ', shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE )
output, errors =  netshcmd.communicate()
if errors:
    print("WARNING: woow", errors)
else:
    print("SUCCESS: ok ", output)
