import os

#
# pluggable method
# 
def service_change(service, delta):
	print 'service has changed: '+str(service)
	print '\t'+'delta is '+str(delta)