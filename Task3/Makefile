PWD				:= $(shell pwd)
SIM ?= icarus
TOPLEVEL_LANG = verilog

VERILOG_SOURCES = $(shell pwd)/piso_shift_register.v


GUI=1

TOPLEVEL=piso_shift_register
MODULE=test_hp

#COCOTBHDLPRECISION = 1ns
#COCOTBHDLPRECISION = 1ps


include $(shell cocotb-config --makefiles)/Makefile.sim


