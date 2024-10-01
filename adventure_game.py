#sp23-bai-003
import json

SAVE_FILE_PATH = "save_file.json"

#SP23_bai_002

game_state = {
    "current_room": "Foggy Courtyard",  # Starting room
    "inventory": [],
    "hints_used": 0,  # Keep track of hints used

    # task Needed to perform during the game play 
    "tasks": {
        "Alchemy Lab": {"status": "incomplete", "description": "You need a Magical Potion to brew in the cauldron.", "item": "MagicalPotion"},
        "Library": {"status": "incomplete", "description": "Use the Enchanted Quill to reveal the hidden word.", "item": "EnchantedQuill"},
        "Tower": {"status": "incomplete", "description": "Solve the constellation puzzle using the Star Chart.", "item": "StarChart"},
    },

    # Items in the game
    "items": {
        "MagicalPotion": {"description": "A potion that can complete the alchemy task."},
        "EnchantedQuill": {"description": "A magical quill that can reveal hidden words."},
        "StarChart": {"description": "A star chart that helps solve the Tower puzzle."},
        "Torch": {"description": "A torch that can provide light."},
    },

    # Hints for each room
    "hints": {
        "Foggy Courtyard": ["There's a grand hall to the north.", "Look for keys; they might open something."],
        "Grand Hall": ["There are more exits from this room.", "Look around carefully. Something might help unlock the basement."],
        "Library": ["Examine the quill on the desk.", "Books can hold secrets, some locked by puzzles."],
        "Alchemy Lab": ["You need a potion to brew here.", "Look for ingredients in nearby rooms."],
        "Tower": ["Solve the constellation puzzle.", "Use the Star Chart to help align the stars."]
    },

    # Rooms Information
    "rooms": {
        "Foggy Courtyard": {
            "description": "You are in the foggy courtyard. A rusty gate blocks your way to the castle's entrance. To the north, you see the Grand Hall.",
            "exits": {"north": "Grand Hall"},
            "items": [],
            "locked": False,
            "task_req": ""
        },
        "Grand Hall": {
            "description": "You enter the Grand Hall. There are exits to the east (Library), west (Alchemy Lab), and north (Tower).",
            "exits": {
                "south": "Foggy Courtyard",
                "east": "Library",
                "west": "Alchemy Lab",
                "north": {
                    "room": "Tower",
                    "locked": True,
                    "puzzle": {
                        "question": "What has keys but can't open locks?",
                        "answer": "piano"
                    }
                }
            },
            "items": []
        },
        "Library": {
            "description": "You step into the Enchanted Library. Shelves of ancient books surround you, and a mysterious quill glows on a desk.",
            "exits": {"west": "Grand Hall"},
            "items": ["EnchantedQuill"],
            "locked": False,
            "task_req": ""
        },
        "Alchemy Lab": {
            "description": "The Alchemy Lab is filled with bubbling potions and strange equipment. A cauldron sits in the middle of the room.",
            "exits": {"east": "Grand Hall"},
            "items": ["MagicalPotion"],
            "locked": False,
            "task_req": ""
        },
        "Tower": {
            "description": "You stand at the top of the Tower Observatory. A celestial map lies on the floor, and the stars seem to form a puzzle.",
            "exits": {"south": "Grand Hall"},
            "items": ["StarChart"],
            "locked": True,
            "task_req": "Solve the constellation puzzle using the Star Chart."
        }
    }
}

# Function to display a hint, 2 hints per game
def give_hint():
    if game_state["hints_used"] >= 2:
        print("You've used all available hints.")
        return
    current_room = game_state["current_room"]
    hints_for_room = game_state["hints"].get(current_room, [])
    
    if hints_for_room:
        hint = hints_for_room[game_state["hints_used"]]
        print(f"\nHint: {hint}")
        game_state["hints_used"] += 1
    else:
        print("No hints available for this room.")

# Function to move between rooms
def move(direction):
    current_room = game_state["current_room"]

    # for user friendly usign abbrevations 
    direction_map = {
        'N': 'north', 'n': 'north',
        'S': 'south', 's': 'south',
        'E': 'east', 'e': 'east',
        'W': 'west', 'w': 'west',
        'U': 'up', 'u': 'up',
        'D': 'down', 'd': 'down'
    }

    try:
        full_direction = direction_map[direction] 
    except KeyError:
        print("Invalid direction. Please use N/n, S/s, E/e, W/w, U/u, or D/d.")
        return False 

    if full_direction in game_state["rooms"][current_room]["exits"]:
        exit_info = game_state["rooms"][current_room]["exits"][full_direction]

        # Check if exit is locked
        if isinstance(exit_info, dict):

            if exit_info.get("locked", False):
                # If there is  puzzle to solve 
                if "puzzle" in exit_info:
                    # If puzzle solved
                    if show_riddle(exit_info["puzzle"]):  
                        exit_info["locked"] = False
                        game_state["current_room"] = exit_info["room"]
                        log_move(f"Moved {full_direction} to {exit_info['room']}")
                        # info about new room 
                        look() 
                        return True
                    else:
                        print("You cannot proceed until the puzzle is solved.")
                        return False
                    
                # if there is task to solve
                elif "task_req" in exit_info:
                    solve_task()  
                    if game_state["tasks"][current_room]["status"] == "complete":
                        game_state["current_room"] = exit_info["room"]
                        log_move(f"Moved {full_direction} to {exit_info['room']}")
                        # info about new room 
                        look() 
                        return True
                    else:
                        print("You haven't completed the task required to proceed.")
                        return False
                    
            else:
                game_state["current_room"] = exit_info["room"]
                log_move(f"Moved {full_direction} to {exit_info['room']}")
                # info about new room 
                look()  
                return True
        else:
            game_state["current_room"] = exit_info
            log_move(f"Moved {full_direction} to {exit_info}")
            # info about new room 
            look()  
            return True
    else:
        #Invalid direction 
        print("You can't go that way!")
        return False

# Function to show riddle when a player tries to move to a locked room with a puzzle
def show_riddle(puzzle_info):
    print(f"\nPuzzle: {puzzle_info['question']}")
    answer = input("Your answer: ").lower()
    if answer == puzzle_info["answer"]:
        print("Correct! The door unlocks.")
         # indicate the puzzle was solved
        return True 
    else:
        print("Incorrect answer. The door remains locked.")
        # if puzzle not solved 
        return False  
    # Function to show the 
# current room description and tasks
def look():

    current_room = game_state["current_room"]
    print(f"\nYou are in {current_room}.")
    print(game_state["rooms"][current_room]["description"])

    # Show items in the room
    if game_state["rooms"][current_room]['items']:
        print("\nItems in this room:")

        for item in game_state["rooms"][current_room]['items']:
            print(f"- {item}")

    # Show exits and directions
    print("\nExits and directions you can move:")
    for direction, exit_info in game_state["rooms"][current_room]["exits"].items():
        direction_name = direction.capitalize()

        if isinstance(exit_info, str):
            print(f"- {direction_name}: To {exit_info}")
        else:
            target_room = exit_info["room"]
            if exit_info.get("locked", False):
                print(f"- {direction_name}: To {target_room} (Locked)")
            else:
                print(f"- {direction_name}: To {target_room}")

# Function to handle tasks 
def solve_task():
    current_room = game_state["current_room"]
    if current_room in game_state["tasks"]:
        task = game_state["tasks"][current_room]

        # if task is already completed
        if task["status"] == "complete":
            print("Task already completed in this room.")
            return

        required_item = task["item"]
        if required_item in game_state["inventory"]:
            print(f"\nYou use the {required_item} to complete the task.")
            # Mark task as complete
            task["status"] = "complete"  
            drop(required_item)  
            
        else:
            print(f"You need the {required_item} to complete the task.")
    else:
        print("There is no task in this room.")

# Function to take items 
def take():
    current_room = game_state["current_room"]
    items_in_room = game_state["rooms"][current_room]["items"]

    # Check if there are any items in the room
    if not items_in_room:
        print("\nThere are no items to take here.")
        return

    # If there's only one item, automatically pick it up
    if len(items_in_room) == 1:
        item = items_in_room[0]
        game_state["inventory"].append(item)
        game_state["rooms"][current_room]["items"].remove(item)
        log_move(f"Took {item}")
        print(f"\nYou picked up the {item}.")
    else:
        # In case of  multiple items
        #  ask the player which one they want to take
        print("\nThere are multiple items in the room:")
        for i, item in enumerate(items_in_room, 1):
            print(f"{i}. {item}")
        choice = input("Which item would you like to take? (Enter the number): ")

        try:
            item_index = int(choice) - 1
            if 0 <= item_index < len(items_in_room):
                item = items_in_room[item_index]
                game_state["inventory"].append(item)
                game_state["rooms"][current_room]["items"].remove(item)
                log_move(f"Took {item}")
                print(f"\nYou picked up the {item}.")
            else:
                print("\nInvalid choice.")

        except ValueError:
            print("\nPlease enter a valid number.")

# Function to drop items from  inventory
def drop(item):
    current_room = game_state["current_room"]
    item = item.lower()

    if item in [i.lower() for i in game_state["inventory"]]:
        item_to_drop = next(i for i in game_state["inventory"] if i.lower() == item)
        game_state["inventory"].remove(item_to_drop)
        game_state["rooms"][current_room]["items"].append(item_to_drop)
        log_move(f"Dropped {item_to_drop}")
        print(f"\nYou dropped the {item_to_drop}.")
    else:
        print(f"\nYou don't have {item} in your inventory.")

 # Function to show  inventory
def show_inventory():
    if game_state["inventory"]:
        print("\nYour inventory contains:")
        for item in game_state["inventory"]:
            print(f"- {item}")
    else:
        print("\nYour inventory is empty.")


#sp23-bai-003
import json

SAVE_FILE_PATH = "save_file.json"

# Move log file
move_log_file = "move_log.txt"

# Function to log each move to the save file
def log_move(move):
    try:
        with open(move_log_file, "a") as log_file:
            log_file.write(move + "\n")
    except Exception as e:
        print(f"\nError logging move: {e}")


# Function to show player's inventory
def show_inventory():
    if game_state["inventory"]:
        print("\nYour inventory contains:")
        for item in game_state["inventory"]:
            print(f"- {item}")
    else:
        print("\nYour inventory is empty.")


# Function to show help menu
def show_help():
    print("\n--- Help Menu ---")
    print("Available commands:")
    print("- 'move [direction]' to move in a direction (N, S, E, W)")
    print("- 'take' to pick up an item in the room")
    print("- 'drop [item]' to drop an item from your inventory")
    print("- 'inventory' to view your current inventory")
    print("- 'look' to look around the current room")
    print("- 'hint' to receive a hint (Max 2 per game)")
    print("- 'save' to save your game")
    print("- 'load' to load a previously saved game")
    print("- 'quit' to exit the game")

# Function to save the game
def save_game():
    try:
        with open(SAVE_FILE_PATH, 'w') as save_file:
            json.dump(game_state, save_file)
        print("\nGame saved successfully.")
    except Exception as e:
        print(f"Error saving game: {e}")

# Function to load the game
def load_game():
    global game_state
    try:
        with open(SAVE_FILE_PATH, 'r') as save_file:
            game_state = json.load(save_file)
        print("\nGame loaded successfully.")
        look()  # Display the current room after loading
    except FileNotFoundError:
        print("\nNo saved game found.")
    except Exception as e:
        print(f"Error loading game: {e}")

# Function to display the main menu
def main_menu():
    print("\n-- Main Menu --")
    print("1. Look around")
    print("2. Move to another room")
    print("3. Take an item")
    print("4. Drop an item")
    print("5. View inventory")
    print("6. Solve task")
    print("7. Save game")
    print("8. Load game")
    print("9. Get a hint")
    print("10. Help")
    print("11. Pause and Quit")




  # Main game loop
def play_game():
    print("Welcome to the Enchanted Labyrinth!")
    look()

    while True:
        main_menu()
        choice = input("\nChoose an option (1-11): ").strip()

        if choice == "1":
            look()
        elif choice == "2":
            while True:
                direction = input("Which direction do you want to move (N/n, S/s, E/e, W/w)? ").strip().lower()
                if move(direction):
                    break
        elif choice == "3":
            take()
        elif choice == "4":
            item = input("Which item do you want to drop? ").strip().lower()
            drop(item)
        elif choice == "5":
            show_inventory()
        elif choice == "6":
            solve_task()
        elif choice == "7":
            save_game()
        elif choice == "8":
            load_game()
        elif choice == "9":
            give_hint()
        elif choice == "10":
            show_help()
        elif choice == "11":  # Pause and Quit
            save_game()
            print("Game paused and saved. You can resume later!")
            break
        else:
            print("Invalid option. Please select a valid number (1-11).")

# Start the game
if _name_ == "_main_":
    play_game()
