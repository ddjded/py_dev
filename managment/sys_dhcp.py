import subprocess

SERVER = input("DNS Server - ")
SCOPE = input("Scope DNS - ")
IP = input("IP - ")
MAC = input("MAC - ")
NAME = input("Name - ")
DESCRIPTION = input("Description - ")

res = 'netsh dhcp server ' + SERVER + ' scope ' + SCOPE + ' add reservedip ' + IP + ' ' + MAC + ' ' + NAME + ' ' + DESCRIPTION + ' "" BOTH'

print(res)

netshcmd = subprocess.Popen(
    'netsh dhcp server ' + SERVER + ' scope ' 
    + SCOPE + ' add reservedip ' 
    + IP + ' ' 
    + MAC + ' ' 
    + NAME + ' '
    + DESCRIPTION + ' BOTH', shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
output, errors = netshcmd.communicate()
if errors:
    print("WARNING: ", errors)
else:
    print("SUCCESS: ", output)
