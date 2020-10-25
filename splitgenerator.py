game_name = input("Game: ")
category_name = input("Category: ")

split_names = []

print("Leave input empty when all the splits have been entered.")
while True:
    new_split_name = input(f"Split #{len(split_names)}: ")
    
    if new_split_name:
        split_names.append(new_split_name)
    else:
        break

print()
print("Generating file...")
data = {"game": game_name, "category": category_name, "splits": [{"name": name, "best": 3600000000000, "personal_best": 3600000000000} for name in split_names], "personal_best": 3600000000000, "attempts": 0}

with open(f"{game_name.replace(' ', '').lower()}{category_name.replace(' ', '').lower()}.split", "w+") as file:
    file.write(str(data))

print("Done.")
