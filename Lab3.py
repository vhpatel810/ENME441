import random

def generate():
	return[str(random.randint(1,6)) for _ in range(4)]
def check(order, guess):
	copyorder = order[:]
	guesscopy = list(guess)

	completematch = 0
	partialmatch = 0
	for a in range(4):
		if guesscopy[a] == copyorder[a]:
			completematch +=1
			copyorder[a] = None
			guesscopy[a] = None
	for a in range(4):
		if guesscopy[a] is not None and guesscopy[a] in copyorder:
			partialmatch+=1
			copyorder[copyorder.index(guesscopy[a])] = None
	return "\u25CF" * completematch + "\u25CB" * partialmatch
def mastermindplay():
	print("Guess a sequence 4 values from 1-6")
	print("\u25CB" , "\u25CF")
	order = generate()
	for item in range (1,13):
		guess = input(f"Guess {item} of 12: ")
		if list(guess) == order:
			print("\u25CF" *4)
			print("Correct - you win!")
			return
		print(check(order,guess))
	print("You lose!")
	print("Correct order:","".join(order))

if __name__ == "__main__":
	mastermindplay()






