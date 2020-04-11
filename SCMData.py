import bs4
from urllib import request
import DataBaseMngr


def choose_new_data():
    # default link for data retrieval
    link = "https://steamcommunity.com/market/search?"

    print()
    print("Choose game: ")
    game_choice = input("DEFAULT: 1, CSGO: 2, TF2: 3, Steam: 4, Rust: 5, PUBG: 6")

    # appid changes to a game-specific page
    if game_choice == "2":
        link = link + "appid=730"
    elif game_choice == "3":
        link = link + "appid=440"
    elif game_choice == "4":
        link = link + "appid=753"
    elif game_choice == "5":
        link = link + "appid=252490"
    elif game_choice == "6":
        link = link + "appid=578080"

    return link


def grab_data(link):
    # temp list to be filled with the data if user wants to add to db
    data_list = []

    # request to open page
    r = request.urlopen(link)

    # open a BS html parser, with the requested URL
    soup = bs4.BeautifulSoup(r, "html.parser")

    i = 0
    while i < 8:
        # retrieve data points from market, use soup.find_all to get specific data
        item_name = soup.find_all('span', {'class': 'market_listing_item_name'})[i].text
        item_price = soup.find_all('span', {'class': 'normal_price', 'data-currency': '1'})[i].text
        item_quantity = soup.find_all('span', {'class': 'market_listing_num_listings_qty'})[i].text

        # adding to data_list
        data_list.insert(0, [item_name, item_price, item_quantity])

        # display current results
        print(item_name)
        print(item_quantity)
        print(item_price)
        print()

        i = i + 1

    # either disregard data after view and move on, or add it to the database
    print()
    add_db_choice = input("CONTINUE: 1, ADD DATA TO DB: 2")

    if add_db_choice == "2":
        add_data_to_DB(data_list)


def display_DB():
    # display every line from the database
    item_list = DataBaseMngr.retrieveDB()
    print("Updated DB: ")


    for item in item_list:
        print(item[1], " - ", item[2], " - ", item[3])
        print()



def add_data_to_DB(item_list):
    # add the new data to the current database
    i = 0
    while i < 8:
        DataBaseMngr.addDB(item_list[i][0], item_list[i][1], item_list[i][2])
        i = i + 1


def search_by_name():
    # get a keyword and search the database for matching entries
    keyword = input("Enter search term: ")
    item_list = DataBaseMngr.searchNames(keyword)

    for item in item_list:
        print(item[1], " - ", item[2], " - ", item[3])
        print()


# ----- program execution ----- #

# try to create DB if not already created
DataBaseMngr.createDB()

# main loop
while True:
    print()
    print("-- Steam Community Market Data --")
    print()

    print("What would you like to do?")
    task = input("Get new data: 1, Search data by keyword: 2, Display all data: 3, Clean out database: 4")

    if task == "1":
        the_link = choose_new_data()
        print("RESULTS: ")
        grab_data(the_link)

    elif task == "2":
        search_by_name()

    elif task == "4":
        choice = input("Are you sure? (Y/N)")

        if (choice == "Y") or (choice == "y") or (choice == "yes") or (choice == "Yes"):
            DataBaseMngr.clearDB()
    else:
        display_DB()
