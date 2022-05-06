import pandas as pd
import requests
from thread_pokemon import Pokemon
from pokemon import non_thread_pokemon
import threading

#The data frame structure.
stats = {"Name": [], "ID": [], "Type 1": [], "Type 2": [], "HP": [], 
            "Att": [], "Def": [], "Sp A": [], "Sp D": [], "Spd": []}
data = pd.DataFrame(stats)
json_list = [] #list of received information from the API, to be later used in calculations.

def welcome():
    """
    Function displays a welcome title screen with a disclaimer for it's information.
    The program then generates a data frame containing the information for all relevant
    Pokemon to be used in the future calculations. This generation uses threads and
    the Pokemon API found in the README. These threads append a json object to a global
    list that is then converted to the information needed and added to the data frame.
    """
    print("-"*52)
    print("| Welcome to Doni's Pokemon API Program            |")
    print("| Please note: the current API is updated for the  |")
    print("| Sword/Shield DLC, but not for Legends: Arceus or |")
    print("| for Brilliant Diamond or Shinning Pearl.         |")
    print("-"*52)
    progress()
    
    #Generate threads to gather information quickly.
    print("Now gathering data, please wait.")
    threads = []
    pokemon_search = [x for x in range(1, 890)]
    full_search = append_with_extras(pokemon_search)
    for id in full_search: 
        url = "https://pokeapi.co/api/v2/pokemon/"
        url += str(id)
        t = Pokemon(json_list, url, id)
        threads.append(t)
        
    for t in threads:
        t.start()
    for t in threads:   
        t.join()
    print()
    progress()
    print("Converting data, please wait.")
    print()
    #convert the list of jsons to information added into the dataframe.
    for json in json_list:
        name = json["name"].capitalize()
        id = json["id"]
        type_1 = json["types"][0]["type"]["name"].capitalize()
        try: #some pokemon don't have a second type, skip if they don't have one.
            type_2 = json["types"][1]["type"]["name"].capitalize()
        except:
            type_2 = "---"
        hp =               json["stats"][0]["base_stat"]
        attack =           json["stats"][1]["base_stat"]
        defense =          json["stats"][2]["base_stat"]
        special_attack =   json["stats"][3]["base_stat"]
        special_defense =  json["stats"][4]["base_stat"]
        speed =            json["stats"][5]["base_stat"]
        new_data = [name, id, type_1, type_2, hp, attack, defense, special_attack, special_defense, speed]
        data.loc[len(data.index)] = new_data #adds the json information to the dataframe.
    
def progress():
    """a simple function to stop the print statements and allow the user to 
    control when they continue in the program."""
    input("Push enter to continue.")
    print()

def main_menu():
    choosing = True
    while choosing:
        menu_options = [1, 2, 3, 4, 5]
        print("Please Select an option:")
        print("")
        print("1 Compare Chosen Pokemon")
        print("2 Compare All Pokemon")
        print("3 Count By Type")
        print("4 Answer Assignment Questions")
        print("5 Quit")
        # print("6 ")
        menu_choice = input("> ")
        if int(menu_choice) in menu_options:
            choice = int(menu_choice)
            choosing = False
        else:
            print("I'm sorry that is an invalid input.")
            progress()
    """A director function that takes the user down a module according to their own choice.
    """
    if choice == 1:
        display_chosen_stats()
    if choice == 2:
        display_all_stats()
    if choice == 3:
        count_by_type()
    if choice == 4:
        answer_questions()
    if choice ==5:
        print("Thank you for using Doni's Pokemon API Program")
        print("Have a good day!")

def display_chosen_stats():
    """A function that will manually look up any number of Pokemon and what Pokemon the user 
    desires to look up."""
    number_of_pokemon = int(input("Compare how many Pokemon? ")) #max is 889, 10001-10194 have alt forms    
    new_data = pd.DataFrame(stats)
    for i in range(number_of_pokemon): 
        user_pokemon = user_selected_pokemon()
        new_data.loc[len(new_data.index)] = user_pokemon.data

    print(new_data)
    progress()
    main_menu()

def user_selected_pokemon():
    """Allows the user to specify a specific Pokemon they wish to look up."""
    url = "https://pokeapi.co/api/v2/pokemon/"
    user_input= input("Please insert the ID of the desired Pokemon. ")
    url += str(user_input)
    return non_thread_pokemon(url)

def display_all_stats():
    """This function uses the global dataframe that was generated to format and use data
    from the API and display a sorted dataframe and how many pokemon they'd like to see.
    The can also choose to sort the dataframe by ascending or decending value."""
    #max is 889, 10001-10194 have alt forms
    #sorting    
    sort_option = input("Do you wish to sort? (y/n)")
    if sort_option.lower() == "y":
        sort_by = sort_options()
        sort_ascending =input("Sort by ascending? (y/n)")
        if sort_ascending == "y":
            sort_ascending = True
        else:
            sort_ascending = False
        data.sort_values(by=[sort_by], inplace=True, ascending=sort_ascending)
    
    #how many they wish to display
    display_amount = int(input("Display how many? "))
    
    #display data
    final_data = data.head(display_amount)
    print(final_data)
    progress()
    main_menu()

def append_with_extras(poke_list):
    """These extras are extra forms or pokemon that aren't in the pokedex per se
    but should be included in the searches as they increase the type counts and
    stats for specific pokemon. IE the pokemon Rotom is an Electric/Ghost, but it's
    alt forms can be Electric/Fire, Electric/Grass, Electric/Water, Electric/Ice, etc
    and should be counted as a fire, grass, ect Pokemon.
    Another example is Deoxys. Deoxy has different forms that drastically change its
    stats, including making it the fastest pokemon in speed form"""
    
    #for full seach, for the 10001-10228 range, don't include:
    #10016, 10024-25, 10061, 10080-85, 10093-99, 10116-19, 
    #10121-22, 10127-51, 10153-60, 10182-84, 10187, 10192
    #include 10001-15, 10017-23, 10026-10060, 10062-10079, 10086-10092, 10100-10115, 
    #10120, 10123-26, 10152, 10161-10181, 10185-86, 10188-10191, 10193-10194
    for i in range(10001, 10016):
        poke_list.append(i)
    for i in range(10017, 10024):
        poke_list.append(i)
    for i in range(10026, 10061):
        poke_list.append(i)
    for i in range(10062, 10080):
        poke_list.append(i)
    for i in range(10086, 10090):
        poke_list.append(i)
    for i in range(10091, 10093):
        poke_list.append(i)
    for i in range(10100, 10116):
        poke_list.append(i)
    poke_list.append(10120)
    for i in range(10123, 10127):
        poke_list.append(i)
    poke_list.append(10152)
    for i in range(10161, 10182):
        poke_list.append(i)
    for i in range(10185, 10187):
        poke_list.append(i)
    for i in range(10188, 10190):
        poke_list.append(i)
    poke_list.append(10191)
    for i in range(10193, 10195):
        poke_list.append(i)
    return poke_list
    
def sort_options():
    """Allows the user to sort the data frame by one of the values in the dictionary."""
    #stats = {"Name": [], "ID": [], "Type 1": [], "Type 2": [], "HP": [], 
    #        "Att": [], "Def": [], "Sp A": [], "Sp D": [], "Spd": []}
    print("Please Select a sort option")
    print("Name = name")
    print("ID = pokedex number")
    print("Type 1 = First type")
    print("Type 2 = Second type")
    print("HP = HP")
    print("Att = Attack")
    print("Def = Defense")
    print("Sp A = Special Attack")
    print("Sp D = Special Defense")
    print("Spd = Speed")
    user_sort_option = input()
    if user_sort_option in stats:
        return user_sort_option
    else:
        sort_options()

def count_by_type():
    """needs to be adjusted to use data frame"""
    types_list = [] #list to store types
    url = "https://pokeapi.co/api/v2/type"
    r = requests.get(url)
    json = r.json()
    type_amount = int(json["count"]) - 2 #this -2 is necessary as we don't care about "shadow" type or "???" type which are exclusive to very specific games.
    #add all types to the 2 lists.
    for i in range(0, type_amount):
        types_list.append(json["results"][i]["name"])  
    print("Types:", ", ".join(types_list))
    selected_type = input("Select a type to count: ").capitalize()
    count = 0
    for i in range(1020):
        type_1 = str(data.at[i, "Type 1"]).capitalize() #search type 1
        type_2 = str(data.at[i, "Type 2"]).capitalize() #the secondary type might match if the first doesn't.
        if type_1 == selected_type or type_2 == selected_type: #if either type matches, we found the right pokemon.
            count +=1
    print(f"There are {count} {selected_type} types.")
    progress()
    main_menu()
    
def question_1():
    """This function answer's question 1 from the README. It does this by 
    using the global data frame and sorting it by Speed, and then 
    displaying the top 10 items of the dataframe.
    """
    print("Question 1: What are the 10 fastest Pokémon in terms of speed stat?")

    #Sorting Panda's dataframe by Speed Stat
    sort_by = "Spd"
    data.sort_values(by=[sort_by], inplace=True, ascending=False, ignore_index=True)
    
    #Filtering data via only the top 10
    display_amount = 10
    final_data = data.head(display_amount)
    progress()
    print("These are the top 10 fastest Pokemon:")
    print(final_data)
    progress()
    return data

def question_2(data):
    """This function answers question 2 from the README. It does this by
    using the globat dataframe that is already sorted and comparing the
    found Pokemon to the types found from the API. This function finds
    the first Pokemon with the matching type and creates a list of Pokemon
    that correspond with the searched type.
    """
    print("Question 2: What are the fastest Pokémon, in terms of speed, for each type?")
    progress()
    #grab the types from the API
    types_list = [] #list to store types
    pokemon_for_type = [] #list to store types then replace them with the fastest Pokemon of that type.
    url = "https://pokeapi.co/api/v2/type"
    r = requests.get(url)
    json = r.json()
    type_amount = int(json["count"]) - 2 #this -2 is necessary as we don't care about "shadow" type or "???" type which are exclusive to very specific games.
    #add all types to the 2 lists.
    for i in range(0, type_amount):
        types_list.append(json["results"][i]["name"])
        pokemon_for_type.append(json["results"][i]["name"])
    type_index = 0 #to allow replacing of type in pokemon_for_type list, where the type will be replaced with fastest Pokemon.
    #Will search the dataframe for the first Pokemon with the specific type, and therefore, the fastest pokemon as the dataframe is sorted by speed.
    for single_type in types_list:
        searching = True
        i = 0
        while searching:
            type_1 = str(data.at[i, "Type 1"]).capitalize() #search type 1
            type_2 = str(data.at[i, "Type 2"]).capitalize() #the secondary type might match if the first doesn't.
            if type_1 == single_type.capitalize() or type_2 == single_type.capitalize(): #if either type matches, we found the right pokemon.
                pokemon_for_type[type_index] = data.at[i, "Name"]
                i += 1
                searching = False #we found what we are looking for, finish search for specific type.
            else:
                i += 1
        type_index +=1
    print("The fastest pokemon for each type are: ")
    second_column = int((len(pokemon_for_type))/2) #split the found list to two columns.
    for i in range(second_column):
        print(f"{types_list[i].capitalize():10}- {pokemon_for_type[i].capitalize():15} {types_list[i+second_column].capitalize():10}- {pokemon_for_type[i+second_column].capitalize()} ")
    print()
    progress()

def question_3(data, bool_ascending):
    """This function allows for the answering of both questions 3 
    and 4 found in the README, as they are pretty much the same 
    question except in reverse. There are several Pokemon that tie for
    the same lowest/highest stat so they had to be included as well. 
    """
    #by default this will answer question 4, but if bool_ascending is False, then the function will
    #reroute to do question 3.
    high_low = "lowest "
    if bool_ascending != True:
        print("Question 3: What are the Pokémon with the highest of each stat?")
        high_low = "highest"
        progress()

    #the values are sorted by the given stat. All the if statements are to check if there are any stat ties
    data.sort_values(by=["HP" ], inplace=True, ascending=bool_ascending, ignore_index=True)
    print(f"The Pokemon with the {high_low} HP              - {data.iloc[0,0]}")
    if data.iloc[1,4] == data.iloc[0,4]:
        print(f"                                           and {data.iloc[1,0]}")
    if data.iloc[2,4] == data.iloc[0,4]:
        print(f"                                           and {data.iloc[2,0]}")
    data.sort_values(by=["Att"], inplace=True, ascending=bool_ascending, ignore_index=True)
    print(f"The Pokemon with the {high_low} attack          - {data.iloc[0,0]}")
    if data.iloc[1,5] == data.iloc[0,5]:
        print(f"                                           and {data.iloc[1,0]}")
    if data.iloc[2,5] == data.iloc[0,5]:
        print(f"                                           and {data.iloc[2,0]}")
    data.sort_values(by=["Def"], inplace=True, ascending=bool_ascending, ignore_index=True)
    print(f"The Pokemon with the {high_low} defense         - {data.iloc[0,0]}")
    if data.iloc[1,6] == data.iloc[0,6]:
        print(f"                                           and {data.iloc[1,0]}")
    if data.iloc[2,6] == data.iloc[0,6]:
        print(f"                                           and {data.iloc[2,0]}")
    data.sort_values(by=["Sp A"], inplace=True, ascending=bool_ascending, ignore_index=True)
    print(f"The Pokemon with the {high_low} special attack  - {data.iloc[0,0]}")
    if data.iloc[1,7] == data.iloc[0,7]:
        print(f"                                           and {data.iloc[1,0]}")
    if data.iloc[2,7] == data.iloc[0,7]:
        print(f"                                           and {data.iloc[2,0]}")
    if data.iloc[3,7] == data.iloc[0,7]:
        print(f"                                           and {data.iloc[3,0]}")
    data.sort_values(by=["Sp D"], inplace=True, ascending=bool_ascending, ignore_index=True)
    print(f"The Pokemon with the {high_low} special defense - {data.iloc[0,0]}")
    if data.iloc[1,8] == data.iloc[0,8]:
        print(f"                                           and {data.iloc[1,0]}")
    if data.iloc[2,8] == data.iloc[0,8]:
        print(f"                                           and {data.iloc[2,0]}")
    if data.iloc[3,8] == data.iloc[0,8]:
        print(f"                                           and {data.iloc[3,0]}")
    if data.iloc[4,8] == data.iloc[0,8]:
        print(f"                                           and {data.iloc[4,0]}")
    if data.iloc[5,8] == data.iloc[0,8]:
        print(f"                                           and {data.iloc[5,0]}")
    if data.iloc[6,8] == data.iloc[0,8]:
        print(f"                                           and {data.iloc[6,0]}")
    if data.iloc[7,8] == data.iloc[0,8]:
        print(f"                                           and {data.iloc[7,0]}")
    data.sort_values(by=["Spd"], inplace=True, ascending=bool_ascending, ignore_index=True)
    print(f"The Pokemon with the {high_low} speed is        - {data.iloc[0,0]}")
    if data.iloc[1,9] == data.iloc[0,9]:
        print(f"                                           and {data.iloc[1,0]}")
    if data.iloc[2,9] == data.iloc[0,9]:
        print(f"                                           and {data.iloc[2,0]}")
    progress()

def question_4(data):
    """This function is to run question 3 but with the inverse, causing 
    ascending in the sorting and therefore, finding the lowest of each stat."""
    print("Question 4: What are the Pokémon with the lowest of each stat?")
    progress()
    question_3(data, True)   

def answer_questions():
    """This function runs through the four questions as found in the README file.
    """
    print("The four challenge questions are as follows: ")
    print("Question 1: What are the 10 fastest Pokémon in terms of speed stat?")
    print("Question 2: What are the fastest Pokémon, in terms of speed, for each type?")
    print("Question 3: What are the Pokémon with the highest of each stat?")
    print("Question 4: What are the Pokémon with the lowest of each stat?")
    progress()
    data = question_1()
    question_2(data)
    question_3(data, False)
    question_4(data)
    print("The questions are therefore answered.")
    progress()
    main_menu()

def main():
    """The main function, it runs through the welcome and through the menu."""
    welcome()
    main_menu()

if __name__ == "__main__":
    main()
    