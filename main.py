from rich import print as rprint
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from os import system, name

console = Console()
console_width = console.size.width
text_center_format_expression = '{:^' + str(console_width) + '}'
choices = ["Start the game", "View High Score"]
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
quit = False

# Assume we are on a UNIX system per default
clear_command = 'clear'

if name == 'nt':
	clear_command = 'cls'


def generate_random_dungeon():
	# TODO: Try generating dungeon with Drunkwards Way algorithm...
	dungeon = [
		["*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*"],
		["*", ".", ".", ".", ".", ".", ".", ".", ".", ".", "*"],
		["*", ".", ".", ".", ".", ".", ".", ".", ".", ".", "*"],
		["*", ".", ".", ".", ".", ".", ".", ".", ".", ".", "*"],
		["*", ".", ".", ".", ".", ".", ".", ".", ".", ".", "*"],
		["*", ".", ".", ".", ".", ".", ".", ".", ".", ".", "*"],
		["*", ".", ".", ".", ".", ".", ".", ".", ".", ".", "*"],
		["*", ".", ".", ".", ".", ".", ".", ".", ".", ".", "*"],
		["*", ".", ".", ".", ".", ".", ".", ".", ".", ".", "*"],
		["*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*"],
	]

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
	dungeon = generate_random_dungeon()
	introduction()
	print_new_lines(2)
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