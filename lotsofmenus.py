from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem, User

engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create first user
user1 = User(name="Admin", email="pixie.czar@gmail.com",
             picture='https://drive.google.com/open?id=1bmYCKAm8ez9gvVm-BdpXhqFboPzRpLmz')
session.add(user1)
session.commit()

# Restaurants
restaurant1 = Restaurant(user=user1, name="Scopa Caffe Cucina", address="141 Cuba Street, Te Aro, Wellington 6011")
session.add(restaurant1)
session.commit()

restaurant2 = Restaurant(user=user1, name="PappaRich", address="3b/1 Grey St, Wellington, 6011")
session.add(restaurant2)
session.commit()

restaurant3 = Restaurant(user=user1, name="Logan Brown Restaurant", address="192 Cuba Street, Te Aro, Wellington City")
session.add(restaurant3)
session.commit()

restaurant4 = Restaurant(user=user1, name="Ombra", address="199 Cuba Street, Te Aro, Wellington City")
session.add(restaurant4)
session.commit()

restaurant5 = Restaurant(user=user1, name="Saigon Van Grill Bar", address="201 Cuba Street, Te Aro, Wellington City")
session.add(restaurant5)
session.commit()

restaurant6 = Restaurant(user=user1, name="Restaurant 88", address="88 Tory Street, Te Aro, Wellington City")
session.add(restaurant6)
session.commit()

restaurant7 = Restaurant(user=user1, name="Five Boroughs", address="245 Cuba Sreet, Te Aro, Wellington City")
session.add(restaurant7)
session.commit()

restaurant8 = Restaurant(user=user1, name="Chow", address="45 Tory Street, Te Aro, Wellington City")
session.add(restaurant8)
session.commit()

restaurant9 = Restaurant(user=user1, name="Monsoon Poon", address="12 Blair Street, Te Aro, Wellington City")
session.add(restaurant9)
session.commit()

restaurant10 = Restaurant(user=user1, name="Floriditas", address="161 Cuba Street, Te Aro, Wellington City")
session.add(restaurant10)
session.commit()

# Menu for restaurant1 - Scopa Caffe Cucina
menuItem1 = MenuItem(user=user1, restaurant=restaurant1,
			name="Zuppa e scarpetta",
			description="White onion & watercress soup with crispy coppa & grilled Iyalian loaf",
                     	price="$14.00",
			course="Starters")
session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(user=user1, restaurant=restaurant1,
			name="Steamed mussels",
			description="White winem fregola, cream, chilli & garlic with grilled bread",
                     	price="$18.00",
			course="Starters")
session.add(menuItem2)
session.commit()

menuItem7 = MenuItem(user=user1, restaurant=restaurant1,
			name="Porcini Gnocchi",
			description="Oyster mushroom, baby spinach, gorgonzola fonduta",
                     	price="$26.00",
			course="Pasta")
session.add(menuItem7)
session.commit()

menuItem8 = MenuItem(user=user1, restaurant=restaurant1,
			name="Risotto Bianco",
			description="Roasted cauliflower, taleggio, pinenuts, micro herbs",
                     	price="$23.00",
			course="Pasta")
session.add(menuItem8)
session.commit()

menuItem9 = MenuItem(user=user1, restaurant=restaurant1,
			name="Saffron Capelli d'angelo",
			description="Prawns, crab, confit fennel, cream, bottarga",
                     	price="$29.00",
			course="Pasta")
session.add(menuItem9)
session.commit()

menuItem10 = MenuItem(user=user1, restaurant=restaurant1,
			name="Braised beef cheek Caramelle",
			description="Cavolo nero cioppino, Parmigiano Reggiano",
                     	price="$28.00",
			course="Pasta")
session.add(menuItem10)
session.commit()

menuItem3 = MenuItem(user=user1, restaurant=restaurant1,
			name="Lardo wrapped market fish",
			description="With put lentils & pancetta",
                     	price="$30.00",
			course="Mains")
session.add(menuItem3)
session.commit()

menuItem4 = MenuItem(user=user1, restaurant=restaurant1,
			name="Roast topside of wild Fiordland venison",
			description="Confit yams, shiitake mushrooms, cavolo nero",
                     	price="$35.00",
			course="Mains")
session.add(menuItem4)
session.commit()

menuItem5 = MenuItem(user=user1, restaurant=restaurant1,
			name="Gelato trio",
			description="With roasted white chocolate & macadamia nuts",
                     	price="$12.00",
			course="Dessert")
session.add(menuItem5)
session.commit()

menuItem6 = MenuItem(user=user1, restaurant=restaurant1,
			name="Salame al cioccolato",
			description="Chocolate - rum, orange & pistachio",
                     	price="$6.00",
			course="Dessert")
session.add(menuItem6)
session.commit()


# Menu for restaurant2 - PappaRich

menuItem1 = MenuItem(user=user1, restaurant=restaurant2,
			name="Roti Canai with Curry Chicken",
			description="An indian-influenced 'flying bread' that is soft and fluffy inside but crispy and flaky on the outside",
                     	price="$",
			course="Pappa Signature Dishes")
session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(user=user1, restaurant=restaurant2,
			name="Chicken Curry Laksa",
			description="Hokkien noodles in spicy coconut curry broth with chicken slices, tofu puffs, foo chok(beancurd skin), bean sprouts, eggplant and fish cake",
                     	price="$",
			course="Pappa Signature Dishes")
session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(user=user1, restaurant=restaurant2,
			name="Pappa Char Koay Teow",
			description="Our tasty Pappa Char Koay Teow is made with a burst of 'wok hei', a charcoal like flavour that has made the dish one of our all time favorites. This wok-fried flat noodle dish comes with prawns, fish cakes, egg, bean sprouts and chives.",
                     	price="$",
			course="Pappa Signature Dishes")
session.add(menuItem3)
session.commit()

menuItem4 = MenuItem(user=user1, restaurant=restaurant2,
			name="Pappa Chicken Rice with Steamed Chicken",
			description="A Malaysian favourite that comes with tender boiled chicken, fragrant chicken rice, chicken soup, bean sprouts and a combination of chilli, ginger and dark soya sauce for dipping.",
                     	price="$",
			course="Pappa Signature Dishes")
session.add(menuItem4)
session.commit()

menuItem5 = MenuItem(user=user1, restaurant=restaurant2,
			name="Pappa Special Nasi Lemak (2 Dishes) With Curry Chiken & Sambal Prawn",
			description="Also comes with fried anchovies, fried peanuts, hard boiled egg, cucumber slices, and daily made spicy sambal",
                     	price="$",
			course="Pappa Signature Dishes")
session.add(menuItem5)
session.commit()

menuItem6 = MenuItem(user=user1, restaurant=restaurant2,
			name="Pappa White Coffee",
			description="Hot",
                     	price="$",
			course="Pappa Special Drinks")
session.add(menuItem6)
session.commit()

menuItem7 = MenuItem(user=user1, restaurant=restaurant2,
			name="Pappa White Coffee + Coffee Jelly",
			description="Iced",
                     	price="$",
			course="Pappa Special Drinks")
session.add(menuItem7)
session.commit()

menuItem8 = MenuItem(user=user1, restaurant=restaurant2,
			name="Pappa White Coffee",
			description="Iced",
                     	price="$",
			course="Pappa Special Drinks")
session.add(menuItem8)
session.commit()

menuItem9 = MenuItem(user=user1, restaurant=restaurant2,
			name="Pappa Cham",
			description="Iced coffee + milk tea",
                     	price="$",
			course="Pappa Special Drinks")
session.add(menuItem9)
session.commit()

menuItem10 = MenuItem(user=user1, restaurant=restaurant2,
			name="Pappa Mocha + Ice Cream",
			description="",
                     	price="$",
			course="Pappa Special Drinks")
session.add(menuItem10)
session.commit()

menuItem11 = MenuItem(user=user1, restaurant=restaurant2,
			name="Longan Milk Honey",
			description="Iced",
                     	price="$",
			course="Pappa Special Drinks")
session.add(menuItem11)
session.commit()


# Menu for restaurant3 - Logan Brown Restaurant

menuItem1 = MenuItem(user=user1, restaurant=restaurant3,
			name="Rabbit & Pork Rillette",
			description="With Walnut Mustard, Cranberry Relish, Pickles & Watercress",
                     	price="$25.00",
			course="Entree")
session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(user=user1, restaurant=restaurant3,
			name="Apple Cured Ora King Salmon",
			description="With Rhubarb Kimchi, Wild Weeds Puree & Salmon Caviar",
                     	price="$26.00",
			course="Entree")
session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(user=user1, restaurant=restaurant3,
			name="Market Fish Oka",
			description="With Fresh Pressed Coconut Cream, Taro & Kawakawa Crisp",
                     	price="$28.00",
			course="Entree")
session.add(menuItem3)
session.commit()

menuItem4 = MenuItem(user=user1, restaurant=restaurant3,
			name="Pork Jowl, Moko Smoked Eel",
			description="With Horseradish & Green Apple",
                     	price="$26.00",
			course="Entree")
session.add(menuItem4)
session.commit()

menuItem5 = MenuItem(user=user1, restaurant=restaurant3,
			name="Jerusalem Artichoke & Goats Cheese Tart",
			description="With Macadamia, Perigord Truffle & Pink Oyster Mushrooms",
                     	price="$21.00",
			course="Entree")
session.add(menuItem5)
session.commit()

menuItem6 = MenuItem(user=user1, restaurant=restaurant3,
			name="Spinach & Ricotta Gnocchi",
			description="With Salt Baked Beets,  Arugula & Roast Hazelnuts ",
                     	price="$19.00",
			course="Entree")
session.add(menuItem6)
session.commit()

menuItem7 = MenuItem(user=user1, restaurant=restaurant3,
			name="Line Caught Market Fish",
			description="Kapiti Crab Nage, Pickled Eggplant & Mandarin",
                     	price="$39.00",
			course="Main Course")
session.add(menuItem7)
session.commit()

menuItem8 = MenuItem(user=user1, restaurant=restaurant3,
			name="Chestnut Flour Pappardelle",
			description="Truffle Cream, Shiitake & Gorgonzola",
                     	price="$38.00",
			course="Main Course")
session.add(menuItem8)
session.commit()

menuItem9 = MenuItem(user=user1, restaurant=restaurant3,
			name="Wild Fiordland Venison",
			description="Beetroot & Bush Herb Gratin, Puffed Grains & Baby Leeks",
                     	price="$43.00",
			course="Main Course")
session.add(menuItem9)
session.commit()

menuItem10 = MenuItem(user=user1, restaurant=restaurant3,
			name="Origin South Lamb Loin",
			description="Sweetbreads, Hay Smoked Celeriac Puree, Brussels Sprouts & Cassoulet",
                     	price="$42.00",
			course="Main Course")
session.add(menuItem10)
session.commit()


# Menu for restaurant10 - Floriditas

menuItem10 = MenuItem(user=user1, restaurant=restaurant10,
			name="Asparagus, kale, parmesan soup",
			description="With Salty bread sticks",
                     	price="$14.00",
			course="Entree")
session.add(menuItem10)
session.commit()

menuItem3 = MenuItem(user=user1, restaurant=restaurant10,
			name="Harmony, free range pan-roasted chicken breast",
			description="With roasted caultiflower & cos leaves with sorrel dressing",
                     	price="$29.5",
			course="Main Plates")
session.add(menuItem3)
session.commit()

menuItem4 = MenuItem(user=user1, restaurant=restaurant10,
			name="Pan fried John Dory",
			description="With brocolli, white & watermelon radish, parsley & caper salad",
                     	price="$29.50",
			course="Main Plates")
session.add(menuItem4)
session.commit()

menuItem5 = MenuItem(user=user1, restaurant=restaurant10,
			name="Lamb skewers",
			description="With Jerusalem artichoke, red onion, spring greens & sherry vinegar dressing",
                     	price="$29.50",
			course="Main Plates")
session.add(menuItem5)
session.commit()

menuItem6 = MenuItem(user=user1, restaurant=restaurant10,
			name="Crispy skin duck leg",
			description="With beetroot, baby kale leaves & mint salad",
                     	price="$34.50",
			course="Main Plates")
session.add(menuItem6)
session.commit()

menuItem8 = MenuItem(user=user1, restaurant=restaurant10,
			name="Chargrilled Wakanui sirloin steak",
			description="With roasted yams, mint, parsley & lemon (180g)",
                     	price="$30.5",
			course="Main Plates")
session.add(menuItem8)
session.commit()

menuItem9 = MenuItem(user=user1, restaurant=restaurant10,
			name="Chargrilled Black Angus filet steak",
			description="With roasted yams, mint, parsley & lemon (200g)",
                     	price="$39.00",
			course="Main Plates")
session.add(menuItem9)
session.commit()

menuItem7 = MenuItem(user=user1, restaurant=restaurant10,
			name="Affrogato, vanilla bean ice cream",
			description="With shot of Amaretto & espresso",
                     	price="$15.00",
			course="Desserts")
session.add(menuItem7)
session.commit()

menuItem1 = MenuItem(user=user1, restaurant=restaurant10,
			name="Karma Cola",
			description="Softdrink",
                     	price="$5.50",
			course="Beverage")
session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(user=user1, restaurant=restaurant10,
			name="Lemmy Lemonade",
			description="Lemonade",
                     	price="$5.50",
			course="Beverage")
session.add(menuItem2)
session.commit()

print("added Wellington restaurant and menu items")