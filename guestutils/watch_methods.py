import os

#
# pluggable method
# 
def service_change(service, delta):
	print 'executing default method'
	print '\tservice has changed: '+str(service)
	print '\t'+'delta is '+str(delta)