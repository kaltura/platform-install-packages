binary: CURRENT = $(shell ../includes/build-revision.sh $(DEB_HOST_ARCH) inc)
binary: BUILD_REVISION := $(shell ../includes/build-revision.sh $(DEB_HOST_ARCH))
binary: debver := $(DEB_VERSION)
binary: DEB_VERSION = $(if $(CURRENT),$(debver)+b$(BUILD_REVISION),$(debver))
