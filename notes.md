# Notes

here are some behaviors/bugs in the system that might be useful to know

## subscriber
must be started before task are given to marathon

## subscriber and theseus web uis
do not work until the first task is given to marathon. 
`/service` path not created in etcd until first task created.