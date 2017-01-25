# coding=utf-8
from app.models import *

session = db.session
print("session init ...")

pending_status = OrderStatus(name="Pending")
confirmed_status = OrderStatus(name="Confirmed")
shipped_status = OrderStatus(name="Shipped")
delivered_status = OrderStatus(name="Delivered")

session.add(pending_status)
session.add(confirmed_status)
session.add(shipped_status)
session.add(delivered_status)
session.commit()
# agentRoleSells = models.AgentsRole(name="Sells Man", description="Responsible for all the sales")
# agentRoleManager = models.AgentsRole(name="Manager", description="Responsible for all the sales")
#
# session.add(agentRoleSells)
# session.add(agentRoleManager)
#
# session.commit()
#
# agnet1 = models.Agents(first_name="Ahmed", last_name="Mansour", email="ahmed.20@gmail.com", passwd="ahmed123",
#                        role=agentRoleSells)
# agnet2 = models.Agents(first_name="Mohamed", last_name="Kasem", email="kasem@gmail.com", passwd="kasem123",
#                        role=agentRoleManager)
#
# session.add(agnet1)
# session.add(agnet2)
#
# session.commit()

# agent_ahmed = session.query(Agents).filter_by(first_name="Ahmed").first()
# print("Agent " + agent_ahmed.first_name + ": Loaded")

# Cooker = Category(name="Cooker")
# TV = Category(name="TV")
# Refrigerators = Category(name="Refrigerators")
# Washing = Category(name="Washing")
#
# session.add(Cooker)
# session.add(TV)
# session.add(Refrigerators)
# session.add(Washing)
# session.commit()
#
# # Menu for UrbanBurger
# Products2 = Products(name="Rose NG8210 Electrical Twin Cooker, Silver",
#                      description="Electric Double Burner Color: Silver 2 Switches to Control Each Burner’s Temperature Power: 1500 Watt for the Larger Burner, 1000 Watt for the Smaller One Can be used to cook and warming food Equipped with Safety Rubber Feet Length * width * height:49*29*7Cm ",
#                      price=1350.99, category=Cooker, quantity=10)
#
# session.add(Products2)
# session.commit()
#
# Products1 = Products(name="Unionaire T5555SS-128 Stainless Table Gas Stove - 55×55 cm",
#                      description=" Stainless Run by Gas Size: 55 x 55 cm Weight: 22 kg ",
#                      price=1299.95, category=Cooker, quantity=10)
#
# session.add(Products1)
# session.commit()
#
# Products2 = Products(name="Kiriazi -9601 King-Cooker 5 Burners - Stainless Steel",
#                      description="Curved Horizontally Double Glass Door Timer Self-ignition for Top Burners High Capability Burner consists of 3 parts  to have 3 sources of fire The ability to switch grill and oven at the same time while the oven’s door is close. The ability to slip the oven’s shelf outside the oven ... ",
#                      price=3500.00, category=Cooker, quantity=10)
#
# session.add(Products2)
# session.commit()
#
# Products3 = Products(name="Kiriazi Cooker 4 Burners - Stainless Steel- 6600",
#                      description="Bombay Surface Double Glass Door Timer Self-ignition Electrical Rotary Grill with Rods Dimensions:  60 -  60  Oven Dimensions: Width 45 – Depth 49 – Height 35 ",
#                      price=2399, category=Cooker, quantity=10)
#
# session.add(Products3)
# session.commit()
#
# Products4 = Products(name="Natural Sky One-Eye Gas Cooker",
#                      description="Single stainless steel burner Gas operated Hot Plate Powerful stainless steel body Autoignition ",
#                      price=3799, category=Cooker, quantity=10)
#
# session.add(Products4)
# session.commit()
#
# Products5 = Products(name="Kiriazi Cooker 4 Burners - Stainless Steel- 6600",
#                      description="Bombay Surface Double Glass Door Timer Self-ignition Electrical Rotary Grill with Rods Dimensions:  60 -  60  Oven Dimensions: Width 45 – Depth 49 – Height 35 ",
#                      price=1199, category=Cooker, quantity=10)
#
# session.add(Products5)
# session.commit()
#
# Products6 = Products(name="portable stove 1in1", description="",
#                      price=899, category=Cooker, quantity=10)
#
# session.add(Products6)
# session.commit()
#
# Products7 = Products(name="Kiriazi - 8600 M -Cooker 5 Burners - Stainless Steel",
#                      description="Bombay Surface Double Glass Door Timer Self-ignition High Capability Burner The ability to switch grill and oven at the same time while the oven’s door is close. Electrical Rotary Grill with Rods Dimensions:  Width 80 – Depth 60 Oven Dimensions: Width 66 – Depth 50 – Height ... ",
#                      price=2349, category=Cooker, quantity=10)
#
# session.add(Products7)
# session.commit()
#
# Products8 = Products(name="Kiriazi -8900- Cooker 5 burners - Stainless Steel",
#                      description="Burners: 5 Rounded Gas Burner Double Glass Door Timer Self-ignition for Top Burners Electrical Rotary Grill with Rods High Capability Burner with internal and external Holes   Dimensions:   Width 90 – Depth 60 Oven Dimensions: Width 76 – Depth 49 – Height 38 ",
#                      price=2599, category=Cooker, quantity=10)
#
# session.add(Products8)
# session.commit()
#
#
# # Menu for Super Stir Fry
# Products1 = Products(name="Grouhy", description="39 Inch Full HD LED TV - EH-G39-9999",
#                      price=2550, category=TV, quantity=10)
#
# session.add(Products1)
# session.commit()
#
# Products2 = Products(name="JAC 39AS", description="39 Inch FullHD LED TV", price=2899, category=TV, quantity=10)
#
# session.add(Products2)
# session.commit()
#
# Products3 = Products(name="Tornado 32M1350", description="32 Inch HD LED TV", price=1215, category=TV, quantity=10)
#
# session.add(Products3)
# session.commit()
#
# Products4 = Products(name="UnionAir M-LD-43UN-SM801-ASD", description="43 Inch HD LED Smart TV+",
#                      price=1256, category=TV, quantity=10)
#
# session.add(Products4)
# session.commit()
#
# Products5 = Products(name="JAC 42AS1", description="42 Inch FullHD LED TV", price=1400, category=TV, quantity=10)
#
# session.add(Products5)
# session.commit()
#
# Products6 = Products(name="JAC 142ASS", description="42 Inch FullHD LED Smart Android TV", price=1250, category=TV,
#                      quantity=10)
#
# session.add(Products6)
# session.commit()
#
#
# # Menu for Panda Garden
# Products1 = Products(name="Kiriazi K 315/2",
#                      description="Total capacity in litres 315. Freezer capacity in litres 50 Defrost Refrigerator body made of steel anti rust according to the standard specifications.",
#                      price=2156, category=Refrigerators, quantity=10)
#
# session.add(Products1)
# session.commit()
#
# Products2 = Products(name="kiriazi KH145 CF",
#                      description="Width 55 - 67 Depth - High 85 Capicity: 140 liter The possibility of fast freezing, if necessary Digital Screen Energy savings due to the thickness of the insulation (6-8 cm) Monthly consumption of electric power 29 kWh Color: white Chest deep freezer one door.",
#                      price=3699, category=Refrigerators, quantity=10)
#
# session.add(Products2)
# session.commit()
#
# Products3 = Products(name="Kiriazi E220",
#                      description="Chest deep freezer one door Freezer Capacity in litres 220 Defrost Energy saving is conserved due to the insulation thickness which is 6:8 cm. Freezer body made of steel anti rust according to the standard specifications.",
#                      price=2995, category=Refrigerators, quantity=10)
#
# session.add(Products3)
# session.commit()
#
# Products4 = Products(name="Kiriazi K 325/2",
#                      description="Total capacity in litres 325 Freezer capacity in litres 50 Defrost Refrigerator body made of steel anti rust according to the standard specifications.",
#                      price=2699, category=Refrigerators, quantity=10)
#
# session.add(Products4)
# session.commit()
#
# Products2 = Products(name="Kiriazi E210N",
#                      description="Total capacity in liters 210 Consists of 4 drawers Class (B) Freezing rate: NO frost Fan Stops on opening the freezer door to keep cooling temperature inside and save energy Indicator for each drawer Information System to identify contents in each drawer",
#                      price=4950, category=Refrigerators, quantity=10)
#
# session.add(Products2)
# session.commit()
#
#
# # Menu for Thyme for that
#
# Products1 = Products(name="Kiriazi KW 1209 Front Load Washing Machine - 9 Kg, White",
#                      description="Washing capacity: 9 Kg.  Digital panel with Special design showing washing process, elapsed time to finish the washing cycle, Water temperature.  Electronic program to show troubles or faults accompanying the washing process.  Choosing water level automatically.",
#                      price=7950, category=Washing, quantity=10)
#
# session.add(Products1)
# session.commit()
#
# Products2 = Products(name="Kiriazi KW 1210 Front Load Washing Machine - 10 Kg, Silver",
#                      description="Washing capacity: 10 Kg. Possibility of spin speed controlling up till 1200 r.p.m. Digital panel with Special design showing washing process, elapsed time to finish the washing cycle, water temperature. Electronic program to show troubles or faults accompanying the washing process.",
#                      price=8545, category=Washing, quantity=10)
#
# session.add(Products2)
# session.commit()
#
# Products3 = Products(name="Samsung WA13J5730SS Washing Machine-13kg Silver Top Loader ",
#                      description="Samsung WA13J5730SS 13KG Top Loader Washing Machine Easy pre-treatment The activ dualwash system includes a sink for a convenient place to hand-wash delicate items and pre-treat heavily soiled clothes. A water jet starts and stops at the push of a button.",
#                      price=6777, category=Washing, quantity=10)
#
# session.add(Products3)
# session.commit()
#
# Products4 = Products(name="Cauliflower Manchurian",
#                      description="Golden fried cauliflower florets in a midly spiced soya,garlic sauce cooked with fresh cilantro, celery, chilies,ginger & green onions",
#                      price=6894, category=Washing, quantity=10)
#
# session.add(Products4)
# session.commit()
#
# Products5 = Products(name="Kiriazi KW 1209 Front Load Washing Machine - 9 Kg, Silver",
#                      description="Washing capacity: 9 Kg.  Digital panel with Special design showing washing process, elapsed time to finish the washing cycle, Water temperature.  Electronic program to show troubles or faults accompanying the washing process. ",
#                      price=4899, category=Washing, quantity=10)
#
# session.add(Products5)
# session.commit()
#
# Products2 = Products(name="Kiriazi KW 1210 Front Load Washing Machine - 10 Kg, White",
#                      description="Washing capacity: 10 Kg. Possibility of spin speed controlling up till 1200 r.p.m. Digital panel with Special design showing washing process, elapsed time to finish the washing cycle, water temperature. Electronic program to show troubles or faults accompanying the washing process. ",
#                      price=3522, category=Washing, quantity=10)
#
# session.add(Products2)
# session.commit()
#
#
# # Menu for Tony's Bistro
# Products1 = Products(name="Kiriazi -9600 M-Cooker 5 Burners - Stainless Steel",
#                      description="Bombay Surface Double Glass Door Timer Self-ignition for burners High capability burner The ability to switch the grill and oven at the same time when the oven’s door is close Electrical Rotary Grill with Rods Dimensions: Width 90 – Depth 60 Oven Dimensions: Width 45 – Depth 49",
#                      price=1395, category=Cooker, quantity=10)
#
# session.add(Products1)
# session.commit()
#
# Products2 = Products(name="Rose NG3008 Gas Cooker with Integrated Single Hot Plate, White",
#                      description="Single Gas Burner With Single Electric Burner Equipped With Switches to Control Ignition and Temperature Electric Burner’s Power: 1000 Watt Electric Burner Can be used to cook and warming food Equipped With Dedicated Gas Port Color: White Comes With Metal Pan Support Equipped",
#                      price=2495, category=Cooker, quantity=10)
#
# session.add(Products2)
# session.commit()
#
# Products3 = Products(name="Kiriazi -6400- Cooker 4 Burners - Stainless Steel ",
#                      description="Right Angle Surface Double Glass Door Timer Self-ignition for Top Burners, oven and grill Electrical Rotary Grill with Rods Dimensions:   60  - 60 Oven Dimensions: Width 45 – Depth 45 – Height 35 ",
#                      price=3695, category=Cooker, quantity=10)
#
# session.add(Products3)
# session.commit()
#
# Products4 = Products(name="Kiriazi -6400 Safety- Cooker 4 Burners - Stainless Steel",
#                      description="Right Angle Surface Double Glass Door Timer Self-ignition for Top Burners, oven and grill Safety Sensors when switch off burners or oven for gas anti-leakage Electrical Rotary Grill with Rods Dimensions:   60  - 60 Oven Dimensions: Width 45 – Depth 45 – Height 35 ",
#                      price=2395, category=Cooker,
#                      quantity=10)
#
# session.add(Products4)
# session.commit()
#
# # Menu for Andala's
# Products1 = Products(name="UnionAir 43 Inch HD LED Smart TV- M-LD-43UN-SM801-ASD",
#                      description="Specifications‎:‎ Display size ‎‎(‎‎diagonal‎‎)‎‎‎‎:‎‎ 43 Inch Resolution‎‎:‎‎ 1366 x 768 Back light unit‎‎:‎‎ ELED Brightness‎‎:‎‎ 300 cd/m² Contrast Ratio‎‎:‎‎ 3000 Response Time‎‎:‎‎ 6.5ms Smart Features: Android Free Share Web Browser Applications‎‎:‎‎ YouTube / Facebook",
#                      price=1578, category=TV, quantity=10)
#
# session.add(Products1)
# session.commit()
#
# Products2 = Products(name="UnionAir 39 Inch HD LED Smart TV - M-LD-39UN-SM628-EXD",
#                      description="Bring high resolution entertainment to your homes with the UnionAir 39inch HD LED Smart TV. One of the most important and conspicuous features of this television include its huge 39inch Edge LED backlit panel that generates fantastic 1366 x 768 pixel resolution images. The TV comes fitted ",
#                      price=1754, category=TV, quantity=10)
#
# session.add(Products2)
# session.commit()
#
# Products3 = Products(name="UnionAir 55 Inch Smart FullHD LED TV - M-LD-55UN-SM628-EXD",
#                      description="Online Audio& Video: Four smart advantages making your Monitor the home entertainment centre‎:‎ Massive resources view on demand‎;‎ intelligent program memory‎;‎ Real‎-time recommendation‎;‎ Multi‎-screen synchronously broadcast‎.‎Built‎-in Wi‎-Fi: Built‎-in Wi‎-Fi module",
#                      price=1423, category=TV, quantity=10)
#
# session.add(Products3)
# session.commit()
#
# Products4 = Products(name="Philips 32 Inch HD LED TV - 32PHA4100 ",
#                      description="Picture/Display: Display: LED HD TV Diagonal screen size: 32 inch / 80 cm Panel resolution: 1366 x 768p Aspect ratio: 16:9 Picture enhancement: Digital Crystal Clear, 100 Hz Perfect Motion Rate Brightness: 200 cd/m² Smart Interaction: Ease of Use: One-stop Home button Firmware ",
#                      price=1864, category=TV, quantity=10)
#
# session.add(Products4)
# session.commit()
#
# Products2 = Products(name="Samsung 49 Inch Curved Full HD Smart LED TV - 49K6500",
#                      description="With the Samsung 49K6500 49inch Curved Full HD Smart LED TV, you can enjoy watching your favorite TV shows or movies with your family. This Samsung LED TV features Auto Depth Enhancer that adds greater depth to the scenes for a more lifelike viewing experience",
#                      price=1299, category=TV, quantity=10)
#
# session.add(Products2)
# session.commit()
