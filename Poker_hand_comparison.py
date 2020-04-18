#Check Hand Value
#
#
#variables I need to set
rank_list=[0,0,0,0,0]
rank_count=[0,0,0,0,0,0,0,0,0,0,0,0,0]
hand_value_temp=[0,0,0,0,0,0]
ph_value=[0,0]
hole = [[[0,'h'],[0,'h']],[[0,'h'],[0,'h']]]
board = [[0,'h'],[0,'h'],[0,'h'],[0,'h'],[0,'h']]

#import random function
import random

#define list of suit values
suit_list = ["s", "c", "h", "d"]

#populate deck of 52 cards
card_list = []
hole_cards = []
a=2
b=14
c=0
d=3
while c<=d:
	while a<=b:
		card_list.append([a,suit_list[c]])
		a+=1
	a=2
	b=14
	c+=1

#deal player 1 cards
for x in range(2):
	card = random.randint(0,(len(card_list)-1))
	hole[0][x] = card_list[card]
	del card_list[card]

#deal player 2 cards
for x in range(2):
	card = random.randint(0,(len(card_list)-1))
	hole[1][x] = card_list[card]
	del card_list[card]

#deal board
for x in range(5):
	card = random.randint(0,(len(card_list)-1))
	board[x] = card_list[card]
	del card_list[card]

#loop through all possible hand combinations for each player to
#set the best possible hand for each
for player in range(2):
	hand_value_best=[0,0,0,0,0,0]
	from itertools import combinations
	comb = combinations(hole[player]+board,5)
	for hand in comb:
		rank_list=[0,0,0,0,0]
		rank_count=[0,0,0,0,0,0,0,0,0,0,0,0,0]
		hand_value_temp=[0,0,0,0,0,0]
		hand=list(hand)
		
		#create ascending ordered hand
		hand.sort()

		#define Ace as low if straight could only be possible with a low Ace
		if hand[4][0] == 14 and hand[3][0] == 5:
			hand[4][0] = 1

		#reorder ascending hand
		hand.sort()

		#set straight variable as true or false
		for x in range(4):
			if hand[x+1][0] - hand[x][0] == 1:
				straight = True
			else:
				straight = False
			if straight == False:
				break

		#redefine Ace as high if no straight
		if straight == False and hand[0][0] == 1:
			hand[0][0] = 14

		#set flush variable as true or false
		for x in range(4):
			if hand[x+1][1] == hand[x][1]:
				flush = True
			else:
				flush = False
			if flush == False:
				break

		#create ordered ascending list of ranks of cards in hand
		for x in range(5):
			rank_list[x] = (hand[x][0])
			rank_list.sort

		#count frequency of each rank
		for x in range(2,15):
			rank_count[x-2] = rank_list.count(x)

		rank_count_unordered = rank_count.copy()

		#arrange rank frequency list in ascending order
		rank_count.sort()

		#
		#Determine value of hand
		#hand_value[0] determines hand tier
		#hand_value[1:6] determines tie breakers in descending order
		#

		#straight flush check
		if straight == True and flush == True:
			hand_value_temp[0] = 9
			hand_value_temp[1] = rank_list[4]

		#four of a kind check
		if rank_count[-1] == 4:
			hand_value_temp[0] = 8
			for x in range(13):
				if rank_count_unordered[x] == 4:
					hand_value_temp[1] = x+2
				elif rank_count_unordered[x] == 1:
					hand_value_temp[2] = x+2

		#full house check
		if rank_count[-1] == 3 and rank_count[-2] == 2:
			hand_value_temp[0] = 7
			for x in range(13):
				if rank_count_unordered[x] == 3:
					hand_value_temp[1] = x+2
				elif rank_count_unordered[x] == 2:
					hand_value_temp[2] = x+2

		#flush check
		if straight == False and flush == True:
			hand_value_temp[0] = 6
			hand_value_temp[1:6] = rank_list[::-1]

		#straight check
		if straight == True and flush == False:
			hand_value_temp[0] = 5
			hand_value_temp[1] = rank_list[4]

		#three of a kind check
		if rank_count[-1] == 3 and rank_count[-2] == 1:
			hand_value_temp[0] = 4
			for x in range(12,-1,-1):
				if rank_count_unordered[x] == 3:
					hand_value_temp[1] = x+2
				elif rank_count_unordered[x] == 1 and hand_value_temp[2] == 0:
					hand_value_temp[2] = x+2
				elif rank_count_unordered[x] == 1:
					hand_value_temp[3] = x+2

		#two pair check
		if rank_count[-1] == 2 and rank_count[-2] == 2:
			hand_value_temp[0] = 3
			for x in range(12,-1,-1):
				if rank_count_unordered[x] == 2 and hand_value_temp[1] == 0:
					hand_value_temp[1] = x+2
				elif rank_count_unordered[x] == 2:
					hand_value_temp[2] = x+2
				if rank_count_unordered[x] == 1:
					hand_value_temp[3] = x+2

		#one pair check
		if rank_count[-1] == 2 and rank_count[-2] == 1:
			hand_value_temp[0] = 2
			for x in range(12,-1,-1):
				if rank_count_unordered[x] == 2:
					hand_value_temp[1] = x+2
				elif rank_count_unordered[x] == 1 and hand_value_temp[2] == 0:
					hand_value_temp[2] = x+2
				elif rank_count_unordered[x] == 1 and hand_value_temp[3] == 0:
					hand_value_temp[3] = x+2
				elif rank_count_unordered[x] == 1:
					hand_value_temp[4] = x+2

		#High card check
		if rank_count[-1] == 1 and straight == False and flush == False:
			hand_value_temp[0] = 1
			hand_value_temp[1:6] = rank_list[::-1]

		#check to see if hand_value_best should be upgraded
		for x in range(6):
			if hand_value_best[x] < hand_value_temp[x]:
				hand_value_best = hand_value_temp.copy()
				break
			elif hand_value_best[x] > hand_value_temp[x]:
				break
	#set player[player]'s hand = to best possible hand given their hole cards
	ph_value[player] = hand_value_best.copy()

#define when each player wins or splits
for tiebreak in range(6):
	if ph_value[0][tiebreak] > ph_value[1][tiebreak]:
		winner = "Player one wins with "
		winner_hand = ph_value[0].copy()
		break
	elif ph_value[0][tiebreak] < ph_value[1][tiebreak]:
		winner = "Player two wins with "
		winner_hand = ph_value[1].copy()
		break
else:
	winner = "Player one and Player two split with "
	winner_hand = ph_value[0].copy()

#list for labeling winning hand
winner_name = [
	0,
	"High card",
	"One pair",
	"Two pair",
	"Three of a kind",
	"Straight",
	"Flush",
	"Full house",
	"Four of a kind",
	"Straight flush"]

#some lists for converting ints to string equivalents
card_name = [
	"null",
	"ace",
	"deuce",
	"three",
	"four",
	"five",
	"six",
	"seven",
	"eight",
	"nine",
	"ten",
	"jack",
	"queen",
	"king",
	"ace"]

card_name_def = [
	"null",
	"an ace",
	"a deuce",
	"a three",
	"a four",
	"a five",
	"a six",
	"a seven",
	"an eight",
	"a nine",
	"a ten",
	"a jack",
	"a queen",
	"a king",
	"an ace"]

card_name_plur = [
	"null",
	"aces",
	"deuces",
	"threes",
	"fours",
	"fives",
	"sixes",
	"sevens",
	"eights",
	"nines",
	"tens",
	"jacks",
	"queens",
	"kings",
	"aces"]

#create winner message
kicker = ""
if winner_hand[0] == 9:
	message = f"{winner}{card_name_def[winner_hand[1]]}-high straight flush!"
elif winner_hand[0] == 8:
	if tiebreak > 1:
		kicker = f", {card_name[winner_hand[tiebreak]]} kicker"
	message = f"{winner}four {card_name_plur[winner_hand[1]]}{kicker}!"
elif winner_hand[0] == 7:
	message = f"{winner}a full house, {card_name_plur[winner_hand[1]]} full of {card_name_plur[winner_hand[2]]}!"
elif winner_hand[0] == 6:
	if tiebreak > 1:
		kicker = f", {card_name[winner_hand[tiebreak]]} kicker"
	message = f"{winner}{card_name_def[winner_hand[1]]}-high flush!"
elif winner_hand[0] == 5:
	message = f"{winner}{card_name_def[winner_hand[1]]}-high straight!"
elif winner_hand[0] == 4:
	if tiebreak > 1:
		kicker = f", {card_name[winner_hand[tiebreak]]} kicker"
	message = f"{winner}three {card_name_plur[winner_hand[1]]}{kicker}!"
elif winner_hand[0] == 3:
	if tiebreak > 2:
		kicker = f", {card_name[winner_hand[tiebreak]]} kicker"
	message = f"{winner}two pair, {card_name_plur[winner_hand[1]]} and {card_name_plur[winner_hand[2]]}{kicker}!"
elif winner_hand[0] == 2:
	if tiebreak > 1:
		kicker = f", {card_name[winner_hand[tiebreak]]} kicker"
	message = f"{winner}a pair of {card_name_plur[winner_hand[1]]}{kicker}!"
elif winner_hand[0] == 1:
	if tiebreak > 1:
		kicker = f", {card_name[winner_hand[tiebreak]]} kicker"
	message = f"{winner}{card_name[winner_hand[1]]}-high{kicker}!"

#format player one's hole cards to properly display face cards 
for x in range(2):
	if hole[0][x][0] == 11:
		hole[0][x][0] = "J"
	elif hole[0][x][0] == 12:
		hole[0][x][0] = "Q"
	elif hole[0][x][0] == 13:
		hole[0][x][0] = "K"
	elif hole[0][x][0] == 14:
		hole[0][x][0] = "A"

#format player two's hole cards to properly display face cards 
for x in range(2):
	if hole[1][x][0] == 11:
		hole[1][x][0] = "J"
	elif hole[1][x][0] == 12:
		hole[1][x][0] = "Q"
	elif hole[1][x][0] == 13:
		hole[1][x][0] = "K"
	elif hole[1][x][0] == 14:
		hole[1][x][0] = "A"

#format board cards to properly display face cards 
for x in range(5):
	if board[x][0] == 11:
		board[x][0] = "J"
	elif board[x][0] == 12:
		board[x][0] = "Q"
	elif board[x][0] == 13:
		board[x][0] = "K"
	elif board[x][0] == 14:
		board[x][0] = "A"

#print hole cards, board cards, and winner message
print(f"Player one's hole cards: {hole[0][0][0]}{hole[0][0][1]} {hole[0][1][0]}{hole[0][1][1]}")
print(f"Player two's hole cards: {hole[1][0][0]}{hole[1][0][1]} {hole[1][1][0]}{hole[1][1][1]}")
print(f"Board: {board[0][0]}{board[0][1]} {board[1][0]}{board[1][1]} {board[2][0]}{board[2][1]} {board[3][0]}{board[3][1]} {board[4][0]}{board[4][1]}")
print(message)

