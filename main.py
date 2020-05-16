from rich import print as rprint
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from os import system, name
import random

console = Console()
console_width = console.size.width
text_center_format_expression = '{:^' + str(console_width) + '}'
choices = ["Start the game", "View High Score", "Random dungeon Generator"]
player = {
	"name": "",
	"attack": 15,
	"defence": 20,
	"items": {},
	"equipped_weapon": "",
	"row_index": 5,
	"col_index": 5,
	"symbol": "x"
}

# Assume we are on a UNIX system per default
clear_command = 'clear'

if name == 'nt':
	clear_command = 'cls'


def generate_full_dungeon(width, height):
	dungeon = []
	for i in range(height):
		row = []
		for j in range(width):
			row.append("*")
		dungeon.append(row)
	return dungeon


def get_number_between(min, max, number):
	if number < min:
		return min
	elif number > max:
		return max
	return number

def generate_random_dungeon(width, height, number_of_empty_cells):
	# Generating dungeon with Drunkwards Way algorithm...
	# Pick a random cell on the grid as a starting point
	# If we have carved out enough empty spots, we are done...
	# Walk one step in a random direction (north, south, east, west) and carve out a new spot
	# Repeat until number of empty cells have been reached...
	
	# Make a full dungeon (only walls)
	dungeon = generate_full_dungeon(width, height)

	current_empty_cells = 0

	# Choose a random starting point
	starting_point_x = random.randint(0, width - 1)
	starting_point_y = random.randint(0, height - 1)

	directions = ["south", "east", "north", "west"]

	while current_empty_cells < number_of_empty_cells:
		# Choose a random direction
		random_direction_index = random.randint(0, len(directions) - 1)

		if directions[random_direction_index] == "south":
			starting_point_y = starting_point_y + 1
		elif directions[random_direction_index] == "east":
			starting_point_x = starting_point_x + 1
		elif directions[random_direction_index] == "north":
			starting_point_y = starting_point_y - 1
		elif directions[random_direction_index] == "west":
			starting_point_x = starting_point_x - 1

		# Make sure that we do not go out of bounds
		starting_point_x = get_number_between(0, width - 1, starting_point_x)
		starting_point_y = get_number_between(0, height - 1, starting_point_y)

		# Carve out an empty spot but only if it is not empty already
		if dungeon[starting_point_y][starting_point_x] != ".":
			dungeon[starting_point_y][starting_point_x] = "."
			current_empty_cells = current_empty_cells + 1

	print(current_empty_cells)

	return dungeon


def center_text(text):
	return text_center_format_expression.format(text)

def print_new_lines(num_new_lines):
	for i in range(num_new_lines):
		console.print('\n')

def print_title():		
	title = Text()
	subtitle = Text()
	title.append(center_text("Welcome to Rich Adventures"), style="bold #eca9a9")
	subtitle.append(center_text("a dungeon crawler like you  never experienced before"), style="italic #d1e3bc")
	
	console.print(title)
	console.print(subtitle)

def print_title_selection(choices):
	console.print(center_text("Now what is your choice young hero..."))
	for index, choice in enumerate(choices):
		choice_num = index + 1
		choice_text = Text()
		choice_text.append(center_text(str(choice_num) + " " + choice))
		console.print(choice_text)

def get_title_selection(choices):
	print_title_selection(choices)
	print_new_lines(2)
	choice_text = Text()
	choice_text.append("Your Choice: ", style="bold")
	return console.input(choice_text)

def print_error_centered(error_text):
		text = Text()
		text.append(center_text(error_text), style="bold red")
		console.print(text)

def introduction():
	print_new_lines(2)
	introduction_text = Text()
	introduction_text.append(center_text("Brave one, you will embark on a dangerous adventure full of monsters but also treasures"))
	console.print(introduction_text)

	name_text = Text()
	name_text.append("Tell me your name: ", style="bold")
	print_new_lines(2)
	player_name = console.input(name_text)

	# Save the player name...
	player["name"] = player_name

	print_new_lines(2)
	console.print("[bold yellow]" + player["name"] + "[/bold yellow]" + " nice to meet you, you will now embark on your journey, if you ever feel lost just juse the [bold white] help[/bold white] command.")
	
def draw_map(map):
	for row_index, rowList in enumerate(map):
		row_string = ""
		for col_index, col in enumerate(rowList):
			if row_index == player["row_index"] and col_index == player["col_index"]:
				# Draw the player.
				row_string = row_string + player["symbol"]
			else:
				row_string = row_string + map[row_index][col_index]
		console.print(row_string)

def draw_player_information():
	player_table = Table(title="Player Information")
	player_table.add_column("Name")
	player_table.add_column("Attack")
	player_table.add_column("Defence")
	player_table.add_column("Equipped Weapon")
	
	player_table.add_row(player["name"], str(player["attack"]), str(player["defence"]), player["equipped_weapon"])

	console.print(player_table)

def start_game():
	dungeon = generate_random_dungeon(15, 15, 150)
	introduction()
	print_new_lines(2)

	quit = False
	while not quit:
		system(clear_command)
		draw_map(dungeon)
		print_new_lines(1)

		draw_player_information()
		print_new_lines(1)

		action = console.input("Your Command: ")

		# Update player position depending on action (up, down right left etc.)
		
		# Move up
		if action.lower() == "w":
			player["row_index"] = player["row_index"] - 1
		# Move down
		elif action.lower() == "s":
			player["row_index"] = player["row_index"] + 1
		# Move right
		elif action.lower() == "d":
			player["col_index"] = player["col_index"] + 1
		# Move left
		elif action.lower() == "a":
			player["col_index"] = player["col_index"] - 1


def view_highscore():
	console.print("Viewing highscore...")


print_title()

valid_selection = False
selection = 0
# Wait on the main menu till the user has made a valid choice
while not valid_selection:
	try:
		print_new_lines(5)
		selection = int(get_title_selection(choices))

		if selection <= len(choices):
			valid_selection = True
		else:
			system(clear_command)
			print_error_centered("This is not a choice you should make...")
	except ValueError:
		system(clear_command)
		print_error_centered("This is not a choice you should make...")

# At this point the user has made a valid choice, figure out which one

system(clear_command)
# Start the game
if selection == 1:
	start_game()
# View High Score
elif selection == 2:
	view_highscore()
# Random dungeon generator
elif selection == 3:
	number_of_dungeons = int(console.input("How many random dungeons should be generated: "))
	width = int(console.input("How many cells for the width : "))
	height = int(console.input("How many cells for the height : "))
	empty = int(console.input("How many empty cells : "))

	for i in range(number_of_dungeons):
		dungeon = generate_random_dungeon(width, height, empty)
		console.print(Panel(center_text("Dungeon # " + str(i + 1))))
		draw_map(dungeon)
		print_new_lines(1)