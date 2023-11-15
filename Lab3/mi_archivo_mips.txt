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
    lw $t2, c
    add $t1, $t1, $t2
    lw $v0, $t1
    jr $ra
mul:
    lw $t3, b
    lw $t4, c
    mul $t2, $t3, $t4
    lw $t5, a
    add $t2, $t5, $t2
    lw $v0, $t2
    jr $ra
main:
    lw var1, var1
    beqz var1, L1
    li $a0, 5
    li $a1, 7
    subu $sp, $sp, 4
    sw $ra, 0($sp)
    jal sum
    lw $ra, 0($sp)
    addu $sp, $sp, 4
    move $t7, $v0
    j L2
-:
    li $a3, 5
    li $a4, 7
    subu $sp, $sp, 4
    sw $ra, 0($sp)
    jal mul
    lw $ra, 0($sp)
    addu $sp, $sp, 4
    move $t8, $v0
-:
    li $v0, 4
    la $a0, var4
    syscall

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