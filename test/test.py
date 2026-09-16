# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    # Set the input values you want to test
    dut.ui_in.value = 240
    dut.uio_in.value = 30

    # Wait for one clock cycle to see the output values
    await ClockCycles(dut.clk, 1)

    # The following assersion is just an example of how to check the output values.
    # Change it to match the actual expected output of your module:
    assert dut.uo_out.value == 0

    # Keep testing the module by changing the input values, waiting for
    # one or more clock cycles, and asserting the expected output values.
    for i in range(4):
        await ClockCycles(dut.clk, 1)
        assert dut.uo_out.value == i+1, f"Expected {i+1}, got {dut.uo_out.value}"
    
    dut._log.info("Reset")
    dut.rst_n.value = 0
    for i in range(10):
        await ClockCycles(dut.clk, 1)
        assert dut.uo_out.value == dut.ui_in.value, f"Expected {dut.ui_in.value}, got {dut.uo_out.value}"
    dut.rst_n.value = 1

    # dut._log.info(dut.uo_out.value)
    # await ClockCycles(dut.clk, 1)
    # dut._log.info(dut.uo_out.value)
    # await ClockCycles(dut.clk, 30)
    # dut._log.info(dut.uo_out.value)
    
    for i in range(16):
        await ClockCycles(dut.clk, 1)
        assert dut.uo_out.value == int(dut.ui_in.value)+i, f"Expected {int(dut.ui_in.value)+i}, got {dut.uo_out.value}"
    
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0, f"Expected 0, got {dut.uo_out.value}"

    for i in range(4):
        await ClockCycles(dut.clk, 1)
        assert dut.uo_out.value == i+1, f"Expected {i+1}, got {dut.uo_out.value}"
    