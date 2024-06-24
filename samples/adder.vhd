-- File: adder.vhd
-- Generated by MyHDL 0.11.46
-- Date: Mon Jun 10 11:58:09 2024


library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;
use std.textio.all;

use work.pck_myhdl_011.all;

entity adder is
    port (
        a: in unsigned(3 downto 0);
        b: in unsigned(3 downto 0);
        c: out unsigned(4 downto 0)
    );
end entity adder;


architecture MyHDL of adder is




begin





c <= (resize(a, 5) + b);

end architecture MyHDL;
