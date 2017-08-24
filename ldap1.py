#!/usr/bin/python
import ldap
import time
import os
import sys
#needs python-ldap module for this script

try:
	if sys.argv[1] == "-u" or sys.argv[1] == "--user":
		if sys.argv[2] != "":
			user = sys.argv[2]
	elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
		print "-u	command line argument that takes in a common name (eg. cn) to compare against Active Directory."
		print "--user	command line arguement that is the same as -c"
		print "-h	displays the help page for this script"
		print "--help	displays the help page for this script"
except:
	print "Please execute script with -u option or use the -h option for a list of options"
	sys.exit()
	
	

try:
    l = ldap.initialize('<domain controller IP>')
    l.protocol_version = ldap.VERSION3
    l.set_option(ldap.OPT_REFERRALS, 0)
	# Replace 
    output = l.simple_bind('CSC3550-2\\<user name>,'<password>')
    time.sleep(1)
except ldap.LDAPError, e:
    print e

baseDN = "DC=CSC3550-2,DC=local"
searchScope = ldap.SCOPE_SUBTREE
## retrieve all attributes - again adjust to your needs - see documentation for more options
retrieveAttributes = None

if user == "":
	Filter = "cn=*<name>*"
else:
	Filter = "cn=*" + user + "*"

try:
	rslt_id = l.search(baseDN, searchScope, Filter, retrieveAttributes)
	reslt = []
	while 1:
		result_type, result_data = l.result(rslt_id, 0)
		if len(result_data) == 0:
		    break
		else:
		    print result_data
		    for i in range(len(result_data)):
		    	count = 0
			for entr in result_data[i]:
			    try:
					name = entr['cn'][0]
					email = entr['mail'][0]
					usr = entr['sAMAccountName'][0]
					phone = entr['telephoneNumber'][0]
					count = count + 1
					print str(count) + ".\tName: " + name + "\n\tE-mail: " + email + "\tPhone: " + phone + "\n\tUsername: " + usr
			    except:
				pass
except ldap.LDAPError, e:
	    print e
l.unbind_s()
