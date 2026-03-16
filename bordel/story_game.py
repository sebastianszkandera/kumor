#!/usr/bin/env python3
"""
Comedic Horror Story Game
A choose-your-own-adventure game with numbered choices
"""

# Import the time module for the print_slow function
import time

def print_slow(text, delay=0.05):
    """Print text slowly for dramatic effect"""
    # Loop through each character in the text
    for char in text:
        # Print the character without a newline, with flush=True to show immediately
        print(char, end='', flush=True)
        # Wait for the specified delay between characters
        time.sleep(delay)
    # Print a newline at the end
    print()

def get_choice(max_choice):
    """Get a valid choice from the user"""
    # Start an infinite loop to keep asking until valid input
    while True:
        try:
            # Get user input and convert to integer
            choice = int(input("\nEnter your choice (1-" + str(max_choice) + "): "))
            # Check if the choice is within the valid range
            if 1 <= choice <= max_choice:
                # Return the valid choice
                return choice
            else:
                # Print error message for out-of-range choice
                print(f"Please enter a number between 1 and {max_choice}")
        except ValueError:
            # Print error message for non-numeric input
            print("Please enter a valid number")

def game_over(message):
    """Display game over message"""
    # Print a separator line
    print("\n" + "="*50)
    # Print the game over message slowly
    print_slow("GAME OVER: " + message)
    # Print another separator line
    print("="*50)
    # Ask if the player wants to play again
    play_again = input("\nPlay again? (y/n): ").lower()
    # Check if they want to play again
    if play_again == 'y':
        # Restart the game by calling main()
        main()
    else:
        # Print goodbye message
        print("Thanks for playing!")

def main():
    # Print the game title with decorative borders
    print("="*60)
    print("WELCOME TO THE HAUNTED HOUSE OF HORRIBLE HUMOR!")
    print("="*60)
    # Print the introduction story slowly
    print_slow("You are a brave (or foolish) adventurer who has decided to explore the infamous 'House of Eternal Chuckles' - a place where the dead tell dad jokes and ghosts go bump in the night... literally!")

    # Print the scene description
    print("\nYou stand before the creaky old mansion. The sign reads:")
    # Print the sign text slowly
    print_slow("'Welcome! Please wipe your feet on the welcome mat... of DOOM!'")

    # Print the first choice menu
    print("\nWhat do you do?")
    print("1. Knock on the door politely")
    print("2. Kick the door down like a action hero")
    print("3. Try to peek through the windows")
    print("4. Run away screaming (smart choice?)")

    # Get the player's choice (1-4)
    choice = get_choice(4)

    # Branch based on the player's choice
    if choice == 1:
        polite_entrance()
    elif choice == 2:
        action_hero_entrance()
    elif choice == 3:
        peek_windows()
    elif choice == 4:
        coward_ending()

def polite_entrance():
    # Print the scene description slowly
    print_slow("\nYou knock politely. The door creaks open by itself, revealing a butler who looks like he died of boredom.")

    # Print the butler's dialogue slowly
    print_slow("'Welcome, mortal! I am Jeeves, the eternally patient butler. Would you like some tea?'")

    # Print the choice menu for this scene
    print("\n1. Accept the tea (it might be poisoned... or just weak)")
    print("2. Ask about the house's history")
    print("3. Demand to see the owner")
    print("4. Run away (better late than never)")

    # Get the player's choice (1-4)
    choice = get_choice(4)

    # Branch to different story paths based on choice
    if choice == 1:
        tea_party()
    elif choice == 2:
        house_history()
    elif choice == 3:
        meet_owner()
    elif choice == 4:
        coward_ending()

def action_hero_entrance():
    # Print the dramatic entrance scene slowly
    print_slow("\nYou kick the door down with a dramatic 'HIII-YAH!' The door flies off its hinges and hits a ghost, who says 'Oof! That was my dramatic entrance!'")

    # Print the zombie encounter description slowly
    print_slow("Suddenly, zombie security guards shamble toward you. They look more confused than threatening.")

    # Print the choice menu for fighting zombies
    print("\n1. Fight them with your bare hands")
    print("2. Try to reason with them")
    print("3. Offer them pizza (zombies love pizza, right?)")
    print("4. Hide behind the door you just broke")

    # Get the player's choice (1-4)
    choice = get_choice(4)

    # Branch to different zombie encounter outcomes
    if choice == 1:
        fight_zombies()
    elif choice == 2:
        reason_zombies()
    elif choice == 3:
        pizza_zombies()
    elif choice == 4:
        hide_ending()

def peek_windows():
    # Print the window peeking scene slowly
    print_slow("\nYou sneak up to a window and peek inside. You see a vampire trying to bite his own neck because he forgot where his fangs go.")

    # Print the vampire's confused dialogue slowly
    print_slow("'Curse this eternal life! I can never remember if I'm supposed to sparkle or burn in sunlight!'")

    # Print the choice menu for vampire encounter
    print("\n1. Throw a garlic bulb through the window")
    print("2. Knock on the window to get his attention")
    print("3. Join him in his confusion")
    print("4. Back away slowly")

    # Get the player's choice (1-4)
    choice = get_choice(4)

    # Branch to different vampire interaction outcomes
    if choice == 1:
        garlic_attack()
    elif choice == 2:
        vampire_chat()
    elif choice == 3:
        confusion_party()
    elif choice == 4:
        safe_ending()

def coward_ending():
    # Call the game_over function with a coward message
    game_over("You ran away before anything scary could happen. Congratulations, you're alive... and a coward!")

def tea_party():
    # Print the tea party scene description slowly
    print_slow("\nYou accept the tea. It's surprisingly good, but Jeeves keeps trying to serve you 'finger sandwiches' - literally fingers!")

    # Print Jeeves' creepy explanation slowly
    print_slow("'These are my grandmother's recipe! She was a witch, you know.'")

    # Print the choice menu for the tea party
    print("\n1. Eat the finger sandwiches (you're starving)")
    print("2. Ask for regular sandwiches instead")
    print("3. Accuse him of being a cannibal butler")
    print("4. Spit out the tea and run")

    # Get the player's choice (1-4)
    choice = get_choice(4)

    # Branch to different outcomes based on choice
    if choice == 1:
        game_over("You ate the finger sandwiches and became undead. Now you're Jeeves' new apprentice butler!")
    elif choice == 2:
        print_slow("\nJeeves looks offended. 'Regular sandwiches? How pedestrian!' He snaps his fingers and turns you into a sandwich.")
        game_over("You are now a ham sandwich. The horror... the bread!")
    elif choice == 3:
        print_slow("\nJeeves gasps. 'Cannibal? I prefer the term 'recycling enthusiast'! He turns you into a teapot.")
        game_over("You're now a teapot. At least you get to hold tea forever.")
    elif choice == 4:
        coward_ending()

def house_history():
    # Print the house history explanation slowly
    print_slow("\nJeeves tells you the house was built by a mad scientist who wanted to create the perfect comedian. Instead, he created ghosts who tell terrible puns.")

    # Print the ghost's pun slowly
    print_slow("Suddenly, a ghost appears: 'Why did the skeleton go to the party alone? Because he had no body to go with!'")

    # Print the choice menu for responding to the pun
    print("\n1. Laugh at the pun (be polite)")
    print("2. Tell a better pun")
    print("3. Ask the ghost to leave")
    print("4. Run away from the bad jokes")

    # Get the player's choice (1-4)
    choice = get_choice(4)

    # Branch to different pun-related outcomes
    if choice == 1:
        print_slow("\nThe ghost is delighted! 'You have a good sense of humor... for a mortal!' He gives you a treasure.")
        game_over("You won a chest full of dad jokes. You're rich in puns!")
    elif choice == 2:
        print_slow("\nYou tell a pun so bad that the ghost dies of laughter... again. The other ghosts applaud.")
        game_over("You killed a ghost with comedy. You're the ultimate comedian!")
    elif choice == 3:
        print_slow("\nThe ghost gets offended and possesses you. Now you tell puns involuntarily.")
        game_over("You're now a pun-possessed human. Help... I'm punning!")
    elif choice == 4:
        coward_ending()

def meet_owner():
    # Print the meeting with the werewolf owner slowly
    print_slow("\nJeeves leads you to the owner - a werewolf who's allergic to the full moon!")

    # Print the werewolf's sneezy dialogue slowly
    print_slow("'Ah-choo! Excuse me, the moonlight is making my fur itch!'")

    # Print the choice menu for interacting with the werewolf
    print("\n1. Offer him allergy medicine")
    print("2. Ask why he's a werewolf if he's allergic")
    print("3. Try to pet him")
    print("4. Run from the itchy werewolf")

    # Get the player's choice (1-4)
    choice = get_choice(4)

    # Branch to different werewolf interaction outcomes
    if choice == 1:
        print_slow("\nThe werewolf takes the medicine and transforms into a cute puppy. 'Thank you! I've been human for 300 years!'")
        game_over("You cured the werewolf! Now he's your loyal dog companion.")
    elif choice == 2:
        print_slow("\n'It was a curse from my ex-wife, the witch. She thought it would be funny!'")
        game_over("You learned the werewolf's tragic backstory. He offers you a job as his therapist.")
    elif choice == 3:
        print_slow("\nYou pet the werewolf. He sneezes and accidentally bites you. Now you're a werewolf too!")
        game_over("You're now allergic to the moon. The horror of itchy transformations!")
    elif choice == 4:
        coward_ending()

def fight_zombies():
    # Print the zombie fight scene slowly
    print_slow("\nYou fight the zombies! But they're so slow and clumsy that you easily defeat them. One zombie says 'Good fight! Wanna go bowling?'")

    # Print the treasure discovery slowly
    print_slow("You find a treasure room filled with zombie bowling trophies.")

    # End the game with a zombie victory message
    game_over("You defeated the zombies and won the bowling championship! Zombie apocalypse averted... for now.")

def reason_zombies():
    # Print the reasoning with zombies scene slowly
    print_slow("\nYou try to reason with them. 'Guys, violence isn't the answer!' The zombies agree and invite you to their support group.")

    # Print the zombies' backstory slowly
    print_slow("'We're zombies because we ate bad fast food. Now we just want hugs.'")

    # End the game with a friendship message
    game_over("You made friends with zombies! They promise not to eat your brains... much.")

def pizza_zombies():
    # Print the pizza offering scene slowly
    print_slow("\nYou offer pizza. The zombies cheer! 'Pizza! Our one weakness!' They devour the pizza and become friendly.")

    # Print the zombie's thank you slowly
    print_slow("One zombie says 'Thanks! Wanna join our pizza delivery service?'")

    # End the game with a pizza friendship message
    game_over("You befriended zombies with pizza! Now you have undead delivery drivers.")

def hide_ending():
    # Print the hiding scene slowly
    print_slow("\nYou hide behind the broken door. The zombies can't find you and eventually give up.")

    # Print the trapped revelation slowly
    print_slow("But now you're trapped in the haunted house with no way out...")

    # End the game with a trapped message
    game_over("You're stuck forever. At least the ghosts tell good jokes!")

def garlic_attack():
    # Print the garlic throwing scene slowly
    print_slow("\nYou throw garlic through the window. The vampire screams 'My Italian weakness!' and turns into a pile of glitter.")

    # Print the vampire's reformation slowly
    print_slow("But wait... he's not a Twilight vampire. He reforms and says 'That tickled!'")

    # End the game with a vampire comedian message
    game_over("You 'killed' the vampire, but he comes back as a comedian. Now he tells vampire jokes forever!")

def vampire_chat():
    # Print the vampire conversation scene slowly
    print_slow("\nYou knock on the window. The vampire opens it. 'Hello! Want to come in? I promise not to bite... much.'")

    # Print the poetry slam invitation slowly
    print_slow("He invites you to his poetry slam about eternal life.")

    # End the game with a poetry slam message
    game_over("You attended a vampire poetry slam. The poems were to die for!")

def confusion_party():
    # Print the joining confusion scene slowly
    print_slow("\nYou join the vampire in confusion. Together you try to figure out vampire rules.")

    # Print the vampire rule questions slowly
    print_slow("'Do we fly or just dramatically cape-sweep?' 'Is blood type a preference or requirement?'")

    # End the game with a support group message
    game_over("You and the vampire start a support group for confused immortals. Therapy sessions are eternal!")

def safe_ending():
    # Print the backing away scene slowly
    print_slow("\nYou back away slowly. The vampire waves goodbye. 'Come back when you figure out immortality!'")

    # End the game with a safe escape message
    game_over("You escaped safely! But now you're curious about vampire life. Maybe next time...")

# This block checks if the script is being run directly (not imported)
if __name__ == "__main__":
    # Call the main function to start the game
    main()
