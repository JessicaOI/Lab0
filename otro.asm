# MIPS Assembly Language Program with 'sumar' function and user input

.data
input_msg:   .asciiz "Enter the third number: "   # Prompt for user input
result_msg:  .asciiz "\nThe sum is: "            # String to be printed before the result
number_msg:  .asciiz "The entered number is: "   # String to print entered number

.text
.globl main


main:
    # Initialize the first two arguments with some values
    li $a0, 10           # a = 10
    li $a1, 20           # b = 20

    # Prompt for user input for the third argument
    li $v0, 4            # syscall number for print_str
    la $a0, input_msg    # load address of input_msg
    syscall              # print input_msg

    # Read the third number from user
    li $v0, 5            # syscall number for read_int
    syscall              # read integer from user into $v0

    # Print the entered number for verification
    li $v0, 4            # syscall number for print_str
    la $a0, number_msg   # load address of number_msg
    syscall              # print number_msg
    move $a0, $v0        # Move entered number into $a0
    li $v0, 1            # syscall number for print_int
    syscall              # print the entered number

    # Move the user input to $a2 before calling 'sumar'
    move $a2, $v0        # Move user input to $a2

    # Call the 'sumar' function with the arguments
    jal sumar            # Call 'sumar' function

    # Print the sum for verification
    li $v0, 4            # syscall number for print_str
    la $a0, result_msg   # load address of result_msg
    syscall              # print result_msg
    move $a0, $v0        # Move sum result into $a0 for printing
    li $v0, 1            # syscall number for print_int
    syscall              # print the sum result

    # Exit the program
    li $v0, 10           # syscall number for exit
    syscall              # exit program


# Function 'sumar' definition
# Assumes arguments a, b, c are in $a0, $a1, $a2
# Returns the sum in $v0
sumar:
    add $t0, $a0, $a1    # $t0 = a + b
    add $v0, $t0, $a2    # $v0 = $t0 + c (sum of a, b, c)
    jr $ra               # Return to the caller
