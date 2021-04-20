TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#=============================
# Build the IOC application

PROD_IOC = example1
# example1.dbd will be created and installed
DBD += example1.dbd

# example1.dbd will be made up from these files:
example1_DBD += base.dbd

# Include dbd files from all support applications:
#example1_DBD += xxx.dbd

# Add all the support libraries needed by this IOC
#example1_LIBS += xxx

# example1_registerRecordDeviceDriver.cpp derives from example1.dbd
example1_SRCS += example1_registerRecordDeviceDriver.cpp

# Build the main IOC entry point on workstation OSs.
example1_SRCS_DEFAULT += example1Main.cpp
example1_SRCS_vxWorks += -nil-

# Add support from base/src/vxWorks if needed
#example1_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# Finally link to the EPICS Base libraries
example1_LIBS += $(EPICS_BASE_IOC_LIBS)

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

