TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS BELOW HERE

# Use typed rset structure (see 3.16.1 release notes)
USR_CPPFLAGS += -DUSE_TYPED_RSET

# xxxRecord.h will be created from xxxRecord.dbd
DBDINC += xxxRecord

# Install xxxSupport.dbd into <top>/dbd
DBD += xxxSupport.dbd

# Build an IOC support library
LIBRARY_IOC += example2Support

# Compile and add code to the support library
example2Support_SRCS += xxxRecord.c
example2Support_SRCS += devXxxSoft.c

# Link locally-provided code into the support library,
# rather than directly into the IOC application, that
# causes problems on Windows DLL builds
example2Support_SRCS += dbSubExample.c
example2Support_SRCS += devexample2Version.c
example2Support_SRCS += example2Hello.c
example2Support_SRCS += initTrace.c

example2Support_LIBS += $(EPICS_BASE_IOC_LIBS)

# Auto-generate a header file containing a version string.
# Version comes from the VCS if available, else date+time.
GENVERSION = example2Version.h
# Macro name
GENVERSIONMACRO = example2VERSION

# Build the IOC application
PROD_IOC = example2

# example2.dbd will be created and installed
DBD += example2.dbd

# example2.dbd will include these files:
example2_DBD += base.dbd
example2_DBD += xxxSupport.dbd
example2_DBD += dbSubExample.dbd
example2_DBD += devexample2Version.dbd
example2_DBD += example2Hello.dbd
example2_DBD += initTrace.dbd

# example2_registerRecordDeviceDriver.cpp derives from example2.dbd
example2_SRCS += example2_registerRecordDeviceDriver.cpp

# Build the main IOC entry point where needed
example2_SRCS_DEFAULT += example2Main.cpp
example2_SRCS_vxWorks += -nil-

# Link in the code from our support library
example2_LIBS += example2Support

# To build SNL programs, SNCSEQ must be defined
# in the <top>/configure/RELEASE file
ifneq ($(SNCSEQ),)
    # Build sncExample into example2Support
    sncExample_SNCFLAGS += +r
    example2_DBD += sncExample.dbd
    # A .stt sequence program is *not* pre-processed:
    example2Support_SRCS += sncExample.stt
    example2Support_LIBS += seq pv
    example2_LIBS += seq pv

    # Build sncProgram as a standalone program
    PROD_HOST += sncProgram
    sncProgram_SNCFLAGS += +m
    # A .st sequence program *is* pre-processed:
    sncProgram_SRCS += sncProgram.st
    sncProgram_LIBS += seq pv
    sncProgram_LIBS += $(EPICS_BASE_HOST_LIBS)
endif

# Link QSRV (pvAccess Server) if available
ifdef EPICS_QSRV_MAJOR_VERSION
    example2_LIBS += qsrv
    example2_LIBS += $(EPICS_BASE_PVA_CORE_LIBS)
    example2_DBD += PVAServerRegister.dbd
    example2_DBD += qsrv.dbd
endif

# Finally link IOC to the EPICS Base libraries
example2_LIBS += $(EPICS_BASE_IOC_LIBS)

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD EXTRA GNUMAKE RULES BELOW HERE

# Explicit dependency needed for generated header file
devexample2Version$(DEP): $(COMMON_DIR)/$(GENVERSION)
