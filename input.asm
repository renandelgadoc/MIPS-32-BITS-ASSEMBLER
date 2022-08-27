.data
a: .word 0xfffffffa, 0x00000004, 0x00000010
b: .word 3, 2, 1

.text
Label:  add $t1,$t2, $t3
abacaxi
toq $t1, $t2  
xor $t4,           	$t1, $t2         		
		    sll    $t2,$t3, 10
srl $t2, $t3, 10
sub $t0, $s2, $t0
	and		 $t0,		 $s2, $t0
or $t0, $s2, $t0
nor $t0, $s2, $t0
slt $t1, $t2, $t3
	li $t1, 10
	addu $t1, $t2, $t3
subu $t1, $t2, $t3
mult $t1, $t2
div $t1, $t2
mfhi $t1
	mflo $t1
srav $t1, $t2, $t3
sra $t2, $t1, 10
sltu $t1, $t2, $t3
	jr $t0
jalr $t1
    jalr $t1, $t2
 add.d $f0, $f1, $f2
add.s $f0, $f1, $f2
     sub.d $f2, $f4, $f6
	sub.s $f0, $f1, $f3
mul.d $f2, $f4, $f6
	mul.s $f1,$f2, $f3
div.d $f2,$f4, $f6
div.s $f0, $f1, $f2
	    c.eq.d $f2, $f4
c.eq.s $f0, $f1
lw $t1, 0($t0)
sw $t4, 0($t0)
   beq $t1,$zero,Label
bne $t1, $zero, Label
  lb $t1, 100($t2)
  sb $t1, 100($t2)
   addiu $t5, $t4, 10
     slti $t1, $t2, -100
 sltiu $t1, $t2, -100
bgez $t1, Label
bgezal $t1, Label
j Label
jal Label1
clo $t1,$t2
madd $t1,$t2
msubu $t1, $t2
mul $t1, $t2,               $t5           
Label1: movn $t1, $t2, $t3
lui $t1, 10
xori $t6,$t5, -10
ori $t6, $t5, -10
addi $t5, $t4,            10
andi $t6, $t5, -10
la      $s0, a
li $t0, 0x10010000
teq $t1, $t1