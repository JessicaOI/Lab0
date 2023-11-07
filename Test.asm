.data
var1: .word 1          # Inicializa var1 con 1 (verdadero) o 0 (falso)
var2: .asciiz "intento"
var3: .word 0
prompt: .asciiz "El resultado es: "
newLine: .asciiz "\n"

.text
.globl main

main:
    # Verificar el valor de var1
    lw $t0, var1
    beqz $t0, else_branch   # Si var1 es 0, ir a la rama else

    # Rama then: llamar a sum(5, 7, 9)
    li $a0, 5
    li $a1, 7
    li $a2, 9
    jal sum
    sw $v0, var3          # Guardar el resultado de sum en var3

    # Imprimir el resultado de sum
    li $v0, 4
    la $a0, prompt
    syscall

    li $v0, 1
    lw $a0, var3
    syscall

    j end_main

else_branch:
    # Rama else: imprimir "intento"
    li $v0, 4
    la $a0, var2
    syscall

end_main:
    # Imprimir nueva línea
    li $v0, 4
    la $a0, newLine
    syscall

    # Terminar programa
    li $v0, 10
    syscall

# Función sum que calcula a + b * c
sum:
    mul $t0, $a1, $a2  # $t0 = b * c
    add $v0, $a0, $t0  # $v0 = a + ($t0 = b * c)
    jr $ra             # Retornar al llamador
