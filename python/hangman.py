import random
print("Greetings")
lists=["Apple","bannana","grapes"]
secret_word=random.choice(lists) 
print(secret_word)
print("Your get 5 guesses")
display_word=[]
for letters in secret_word:
    display_word += "_"
   
print(display_word)

num=0

game_over=False
while not game_over:
    guess=input("will u guess any letter?")
    guess=guess.lower()
    
    for position  in range(len(secret_word)):
        letter=secret_word[position]
        if letter ==guess:
            display_word[position]=letter
    if guess not in secret_word:
        num +=1
        gues_left=5 -num
        print(f"you have {gues_left} guess left")
        if num>=5:
                print("You loser")
                game_over=True
    else:
        print("You win")
    print(display_word)    
    if "_" not in display_word:
        exit()