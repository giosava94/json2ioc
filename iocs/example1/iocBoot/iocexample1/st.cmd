#!../../bin/linux-x86_64/example1

#- You may have to change example1 to something else
#- everywhere it appears in this file

#< envPaths

## Register all support components
dbLoadDatabase("../../dbd/example1.dbd",0,0)
example1_registerRecordDeviceDriver(pdbbase) 

## Load record instances
dbLoadRecords("../../db/example1.db","user=sava")

iocInit()

## Start any sequence programs
#seq sncexample1,"user=sava"
