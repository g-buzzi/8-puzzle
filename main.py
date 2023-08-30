from evaluator import Evaluator

evaluator = Evaluator()

puzzle = input("Digite seu puzzle: ")

#print(evaluator.min_dist_error(8, [0,1,3,4]))

print("A_Dumb: " + str(evaluator.h_a_dumb(puzzle)))
print()
print("A_Simple: " + str(evaluator.h_a_simple(puzzle)))
print()
print("A_1: " + str(evaluator.h_a1(puzzle)))
print()
print("A_2: " + str(evaluator.h_a2(puzzle)))
print()
print("A_3: " + str(evaluator.h_a3(puzzle)))
print()
print("A_4: " + str(evaluator.h_a4(puzzle)))
