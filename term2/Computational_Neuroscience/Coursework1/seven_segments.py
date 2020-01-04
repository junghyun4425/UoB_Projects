#for the submission uncomment the submission statements
#see submission.README

from math import *
from submission import *
import numpy as np

def seven_segment(pattern):

    def to_bool(a):
        if a==1:
            return True
        return False
    

    def hor(d):
        if d:
            print(" _ ")
        else:
            print("   ")
    
    def vert(d1,d2,d3):
        word=""

        if d1:
            word="|"
        else:
            word=" "
        
        if d3:
            word+="_"
        else:
            word+=" "
        
        if d2:
            word+="|"
        else:
            word+=" "
        
        print(word)



    pattern_b=list(map(to_bool,pattern))

    hor(pattern_b[0])
    vert(pattern_b[1],pattern_b[2],pattern_b[3])
    vert(pattern_b[4],pattern_b[5],pattern_b[6])

    number=0
    for i in range(0,4):
        if pattern_b[7+i]:
            number+=pow(2,i)
    print(int(number))

def create_matrix(vec):
    vec_len = len(vec)
    w = np.zeros([vec_len, vec_len])

    for i in range(vec_len):
        for j in range(vec_len):
            if i == j:
                w[i,j] = 0
            else:
                w[i,j] = vec[i] * vec[j]
    return w

def compute_energy(vec, weights):
    vec_len = len(vec)
    e = 0

    for i in range(vec_len):
       for j in range(vec_len):
           e -= ((vec[i] * weights[i][j] * vec[j]) / 2.0)
    return e

def update_weight(vec, weights):
    w = []
    vec_len = len(vec)
    theta = 0

    for i in range(vec_len):
        m = 0
        for j in range(vec_len):
            m += weights[i][j] * vec[j]

        if m > theta:
            w.append(1)
        else:
            w.append(-1)
    return w

submission=Submission("Jeonghyun Kim")
submission.header("Jeonghyun Kim")

six=[1,1,-1,1,1,1,1,-1,1,1,-1]
three=[1,-1,1,1,-1,1,1,1,1,-1,-1]
one=[-1,-1,1,-1,-1,1,-1,1,-1,-1,-1]

seven_segment(three)
seven_segment(six)
seven_segment(one)

weight_mat = (create_matrix(six) + create_matrix(three) + create_matrix(one)) / 3.0

##this assumes you have called your weight matrix "weight_matrix"
submission.section("Weight Matrix")
submission.matrix_print("W",weight_mat)

## Energy Pattern ordered by six, three, one
submission.section("Energy Pattern")
submission.print_number(compute_energy(six, weight_mat))
submission.print_number(compute_energy(three, weight_mat))
submission.print_number(compute_energy(one, weight_mat))

## Test 1 results
print("test1")
submission.section("Test 1")

test=[1,-1,1,1,-1,1,1,-1,-1,-1,-1]

init_e = compute_energy(test, weight_mat)
submission.seven_segment(test)

submission.qquad()
submission.print_number(init_e)

submission.qquad()

pre_e = 0
while(True):
    test = update_weight(test, weight_mat)
    curr_e = compute_energy(test, weight_mat)
    seven_segment(test)
    
    if pre_e != curr_e:
        submission.seven_segment(test)
        submission.qquad()

        submission.print_number(curr_e)
        submission.qquad()

        pre_e = curr_e
    else:
        break



## Test 2 results
print("test2")
submission.section("Test 2")

test=[1,1,1,1,1,1,1,-1,-1,-1,-1]

init_e = compute_energy(test, weight_mat)
submission.seven_segment(test)

submission.qquad()
submission.print_number(init_e)

submission.qquad()

pre_e = 0
while(True):
    test = update_weight(test, weight_mat)
    curr_e = compute_energy(test, weight_mat)
    seven_segment(test)
    
    if pre_e != curr_e:
        submission.seven_segment(test)
        submission.qquad()

        submission.print_number(curr_e)
        submission.qquad()

        pre_e = curr_e
    else:
        break



submission.bottomer()