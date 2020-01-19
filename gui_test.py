import tkinter as tk
from database_query import *

list_to_index_converter = lambda my_list: {x:y-1 for x,y in zip(my_list, range(len(my_list)))}

### CONSTANTS ###
DAMAGE_TYPES = ["any", "cutting", "blunt"]
DAM_TO_INDEX = list_to_index_converter(DAMAGE_TYPES)

BALANCE_TYPES = ["any", "balanced", "melee", "boomerang"]
BAL_TO_INDEX = list_to_index_converter(BALANCE_TYPES)

ELEMENT_TYPES = ["any", "fire", "water", "thunder", "ice", "dragon", "poison", "sleep", "paralysis", "blastblight"]

SHARPNESS_TYPES = ["any", "red", "yellow", "green", "blue", "white", "purple"]
SHA_TO_INDEX = list_to_index_converter(SHARPNESS_TYPES)

ORDER_BY_TYPES = {'name':'name', 'attack (melee)':'attack_melee', 'attack (ranged)':'attack_ranged', 'element':'element', 'element (melee)':'element_melee', 'element (ranged)':'element_ranged', 'defense':'defense', 'sharpness':'sharpness', 'affinity melee':'affinity_melee', 'affinity ranged':'affinity_ranged', 'balance type':'balance', 'blunt':'blunt'}

# Begin with GUI

# start main program
m= tk.Tk()

# create main canvas to place gui elements on
canvas = tk.Canvas(m, bg='blue', width=600, height=400)
canvas.pack()

# create seperate canvas for filter options
filter_canvas = tk.Canvas(canvas, bg='green', width=560, height=360)
filter_canvas.pack()

# shortcut function for quickly creating dropdown with labels
def create_dropdown(parent: tk.Canvas, options: list, label_text: str, pack_side:str='top') -> tk.StringVar:
    container = tk.Canvas(parent, bg='purple', width=parent.winfo_width())
    container.pack(side=pack_side)

    label = tk.Label(container, text=label_text)
    label.grid(column=0, row=0)

    option_holder = tk.StringVar(container)
    option_holder.set(options[0])

    dropdown = tk.OptionMenu(container, option_holder, *options)
    dropdown.grid(column=1,row=0)
    return option_holder

# create filter dropdowns
damage_type_dropdown = create_dropdown(filter_canvas, DAMAGE_TYPES, 'damage type', pack_side='left')
balance_type_dropdown = create_dropdown(filter_canvas, BALANCE_TYPES, 'balance', pack_side='left')
element_type_dropdown = create_dropdown(filter_canvas, ELEMENT_TYPES, 'element', pack_side='left')
sharpness_type_dropdown = create_dropdown(filter_canvas, SHARPNESS_TYPES, 'sharpness', pack_side='left')

# create order by dropdown
order_by_dropdown = create_dropdown(canvas, list(ORDER_BY_TYPES.keys()), 'order by')

def test_read():
    d_type_selection = damage_type_dropdown.get()
    b_type_selection = balance_type_dropdown.get()
    e_type_selection = element_type_dropdown.get()
    s_type_selection = sharpness_type_dropdown.get()
    o_type_selection = order_by_dropdown.get()

    # directory to database file
    database = './Data/mhgu.db'
    db = weapon_db(database)
    db.add_damage_type_filter(DAM_TO_INDEX[d_type_selection])
    db.add_balance_type_filter(BAL_TO_INDEX[b_type_selection])
    db.add_element_type_filter(e_type_selection.capitalize())
    db.add_sharpness_filter(SHA_TO_INDEX[s_type_selection])
    db.order_results_by(ORDER_BY_TYPES[o_type_selection])
    db.execute()


tk.Button(m, text="Read Options", width=10, command=test_read).pack()

button = tk.Button(m, text='Exit', width=10, command=m.destroy)
button.pack()

m.mainloop()

print('done')