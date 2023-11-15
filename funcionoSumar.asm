.data
prompt1:    .asciiz "Ingrese el primer numero: "
prompt2:    .asciiz "Ingrese el segundo numero: "
sum_result: .asciiz "El resultado de la suma es: "
sub_result: .asciiz "El resultado de la resta es: "
newline:    .asciiz "\n"


.globl main 
.text

main:
    # Solicitar al usuario el primer número
    li $v0, 4
    la $a0, prompt1
    syscall

    # Leer el primer número
    li $v0, 5
    syscall
    move $t0, $v0  # Mover el resultado a $t0

    # Solicitar al usuario el segundo número
    li $v0, 4
    la $a0, prompt2
    syscall

    # Leer el segundo número
    li $v0, 5
    syscall
    move $t1, $v0  # Mover el resultado a $t1

    # Sumar los números
    add $t2, $t0, $t1

    # Restar los números
    sub $t3, $t0, $t1

    # Imprimir el mensaje de resultado de la suma
    li $v0, 4
    la $a0, sum_result
    syscall

    # Imprimir el resultado de la suma
    li $v0, 1
    move $a0, $t2
    syscall

    # Imprimir salto de línea
    li $v0, 4
    la $a0, newline
    syscall

    # Imprimir el mensaje de resultado de la resta
    li $v0, 4
    la $a0, sub_result
    syscall

    # Imprimir el resultado de la resta
    li $v0, 1
    move $a0, $t3
    syscall

    # Imprimir salto de línea
    li $v0, 4
    la $a0, newline
    syscall

    # Salir del programa
    li $v0, 10
    syscall

