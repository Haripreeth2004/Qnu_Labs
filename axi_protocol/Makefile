# Set the simulator. Options include: icarus, modelsim, questa, vcs, ius, xsim, verilator
SIM ?= icarus
TOPLEVEL_LANG ?= verilog
VERILOG_SOURCES +=$(shell pwd)/top_level_design.v
TOPLEVEL=axistream
MODULE=tb_axi
# Path to libpython
LIBPYTHON_LOC = /usr/lib/x86_64-linux-gnu/libpython3.8.so
include $(shell cocotb-config --makefiles)/Makefile.sim