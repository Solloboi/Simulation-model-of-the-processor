Basic principles of operation:
Interpretation of the program is done in a text file where each line represents a single command.

Minimum of three commands: load, add, load memory.

State register must at least hold the sign of the command execution result.
Command execution cycle: first cycle - command is loaded into the command register, second cycle - operation is executed and result is stored.

Commands:
load [register] [value] - stores the specified value into the specified register.
loadMem [address] [value] - stores the specified value into the specified memory.
add [register1] [register2] - integer addition of values from the two specified registers.

Registers:
R(1-4) - general-purpose registers.
Ins - command register.
PS - status register (contains the sign of the last result).
PC - command counter register.
TC - clock cycle counter register.




