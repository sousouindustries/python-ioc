# vim: noexpandtab:syntax=make
CWD	=$(shell pwd)
PYTHON =python3
PYTHON2=python2
PYTHON3_LIB_DIR =$(DESTDIR)/usr/lib/python3/dist-packages
PYTHON2_LIB_DIR=$(DESTDIR)/usr/lib/python2.7/dist-packages
PYTHON_MODULE_NAME=ioc


clean:
	@find . | grep -E "(__pycache__|\.pyc$\)" | xargs rm -rf
	@rm -rf dist build
	@rm -rf *.egg-info
	@rm -rf ../*.orig.tar.gz
	@rm -rf *.egg-info


links:
	@make purge
	@ln -s $(CWD)/$(PYTHON_MODULE_NAME) $(PYTHON3_LIB_DIR)/$(PYTHON_MODULE_NAME)
	@ln -s $(CWD)/$(PYTHON_MODULE_NAME) $(PYTHON2_LIB_DIR)/$(PYTHON_MODULE_NAME)


purge:
	@rm -rf $(PYTHON3_LIB_DIR)/$(PYTHON_MODULE_NAME)
	@rm -rf $(PYTHON2_LIB_DIR)/$(PYTHON_MODULE_NAME)
