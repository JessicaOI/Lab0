.data
prompt0: .asciiz "ingrese True para suma, ingrese false para multiplicacion: \n"
var1: .word 1
prompt1: .asciiz "Ingrese un numero: \n"
var3: .word 0
var4: .asciiz "El valor de la operacion es: \n"
var2: .word 0
.text
.globl main
sum:
    lw $t0, a
    lw $t1, b
    add $t1, $t0, $t1
    lw $t0, c
    add $t1, $t1, $t0
    lw $v0, $t1
    jr $ra
mul:
    lw $t0, b
    lw $t1, c
    mul $t2, $t0, $t1
    lw $t0, a
    add $t2, $t0, $t2
    lw $v0, $t2
    jr $ra
main:
    li $a0, 5
    li $a1, 7
    li $a2, 8
    jal sum
    sw $t7, var2
    li $a3, 5
    li $a4, 7
    li $a5, 8
    jal sum
    li $v0, 4
    la $a0, var4
    syscall

    li $v0, 1
    lw $a0, var2
    syscall

    li $v0, 11
    li $a0, 10
    syscall

    lw $v0, var2
    jr $ra
    li $v0, 10
    syscall