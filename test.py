import _sqlite3 as sql

# directory to database file
database = './Data/mhgu.db'

# open database file
conn = sql.connect(database)

# settings for which settings to show + padding for each
parameters = {
    "_id":[False, 8],
    "creation_cost":[False, 5],
    "attack_melee":[True,3],
    "attack_ranged":[True,3],
    "element":[True,11],
    "element_melee":[True,3],
    "element_ranged":[True,3],
    "defense":[True,3],
    "sharpness":[True,3],
    "affinity_melee":[True,3],
    "affinity_ranged":[True,3],
    "blunt":[True,3],
    "balance":[True,3]
}
padding = [("name", 25)]

# generate command based on enabled parameters
show_string = 'items.name'.center(25)

# go through parameter and add to string
for key in parameters.keys():
    if parameters[key][0] == True:
        show_string += f', palico_weapons.{key}'
        padding.append((key, parameters[key][1]))

is_order = True
is_desc = True
order_by = 'element'
order_string = ''

if is_order:
    order_string = f"order by {order_by}"
    if is_desc:
        order_string += " desc"


# generate entire command
command = f"select {show_string} from items, palico_weapons where items._id = palico_weapons._id and palico_weapons.element <> '' {order_string}"
print(command)
# execute command and retrieve all weapons that meet parameter
cursor = conn.execute(command)

# temporary function that takes string and int and adds padding to the end
print_formatted = lambda text, space: (print(f"{text.center(max(space, len(text)))}", end=" | "))

# print out header
for item in padding:
    print_formatted(item[0], item[1])
print()

# print out formatted table
for row in cursor:
    for item in zip(row, padding):
        text = str(item[0])
        pad = max(item[1][1], len(item[1][0]))
        print_formatted(text, pad)

    print()

