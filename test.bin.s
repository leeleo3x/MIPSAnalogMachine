add $s1 $s2 $s3 
beq $s1 $s2 2 
sw $s1 48($s1) 
sub $s1 $s2 $s3 
add $s1 $s2 $zero 
j 16 
