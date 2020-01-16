import _sqlite3 as sql

# directory to database file
database = './Data/mhgu.db'

# open database file
conn = sql.connect(database)

# parameters for which weapon details to show
show_id = False
show_creation_cost = False
show_attack_melee = True
show_attack_ranged = True
show_element = True
show_element_melee = True
show_element_ranged = True
show_defense = True
show_sharpness = True
show_affinity_melee = True
show_affinity_ranged = True
show_blunt = True
show_balance = True

# generate command based on enabled parameters
show_string = 'items.name'
pw = 'palico_weapons.'
padding = [25]

# go through parameter and add to string
if show_id:
    show_string += f', {pw}_id'
    padding.append(8)
if show_creation_cost:
    show_string += f', {pw}creation_cost'
    padding.append(5)
if show_attack_melee:
    show_string += f', {pw}attack_melee'
    padding.append(3)
if show_attack_ranged:
    show_string += f', {pw}attack_ranged'
    padding.append(3)
if show_element:
    show_string += f', {pw}element'
    padding.append(11)
if show_element_melee:
    show_string += f', {pw}element_melee'
    padding.append(3)
if show_element_ranged:
    show_string += f', {pw}element_ranged'
    padding.append(3)
if show_defense:
    show_string += f', {pw}defense'
    padding.append(3)
if show_sharpness:
    show_string += f', {pw}sharpness'
    padding.append(3)
if show_affinity_melee:
    show_string += f', {pw}affinity_melee'
    padding.append(3)
if show_affinity_ranged:
    show_string += f', {pw}affinity_ranged'
    padding.append(3)
if show_blunt:
    show_string += f', {pw}blunt'
    padding.append(2)
if show_balance:
    show_string += f', {pw}balance'
    padding.append(2)

# generate entire command
command = f"select {show_string} from items, palico_weapons where items._id = palico_weapons._id and palico_weapons.element='Paralysis' order by palico_weapons.element_ranged desc"

# execute command and retrieve all weapons that meet parameter
cursor = conn.execute(command)

# print out formatted
for row in cursor:

    # temporary function that takes string and int and adds padding to the end
    print_formatted = lambda str, space: (print(f"{str:{space}}", end=" | "))

    for i in zip(row, padding):
        print_formatted(i[0], i[1])

    print()