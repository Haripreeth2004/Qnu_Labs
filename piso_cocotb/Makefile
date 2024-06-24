PWD				:= $(shell pwd)
TOPLEVEL_LANG = verilog

VERILOG_SOURCES = $(shell pwd)/piso_shift_register.v


GUI=1
LIBPYTHON_LOC = /usr/lib/x86_64-linux-gnu/libpython3.8.so

TOPLEVEL=piso_shift_register
MODULE=test_piso_shift_register

COCOTB_HDL_TIMEPRECISION = 1ns
COCOTB_HDL_TIMEPRECISION=1ps

include $(shell cocotb-config --makefiles)/Makefile.sim


