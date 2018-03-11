import subprocess

netshcmd=subprocess.Popen('netsh ', shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE )
output, errors =  netshcmd.communicate()
if errors:
    print "WARNING: ", errors
else:
    print "SUCCESS ", output
