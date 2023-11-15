.data
str0: .asciiz ""Hello"

.text
.globl main
.text
.globl main
main:
    li $v0, 4
    la $a0, str0
    syscall
    li $v0, 10
    syscall