import random

def get_random_choice(ratio_list, choice_list):
	ratio_sum = 0
	r = (random.random() * 1000000) % 10000
	for i in range(len(ratio_list)):
		ratio_sum += ratio_list[i] * 10000
		if r <= ratio_sum:
			return choice_list[i]
	return choice_list[-1]