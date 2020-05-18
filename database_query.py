import _sqlite3 as sql

# container class that contains constants used in program
class db_constants():
    list_to_index_converter = lambda my_list: {x: y - 1 for x, y in zip(my_list, range(len(my_list)))}

    ### CONSTANTS ###
    DAMAGE_TYPES = ["any", "cutting", "blunt"]
    DAM_TO_INDEX = list_to_index_converter(DAMAGE_TYPES)

    BALANCE_TYPES = ["any", "balanced", "melee", "boomerang"]
    BAL_TO_INDEX = list_to_index_converter(BALANCE_TYPES)

    ELEMENT_TYPES = ["any", "fire", "water", "thunder", "ice", "dragon", "poison", "sleep", "paralysis", "blastblight"]

    SHARPNESS_TYPES = ["any", "red", "orange", "yellow", "green", "blue", "white", "purple"]
    SHARPNESS_TO_RGB = {x:y for x,y in zip(SHARPNESS_TYPES, [[0,0,0], [200, 0, 0], [200,131, 0], [200, 200, 0], [0, 200, 0], [0, 0, 200], [200, 200, 200], [200, 0, 200]])}
    SHA_TO_INDEX = list_to_index_converter(SHARPNESS_TYPES)

    PHIAL_TYPES = ["any", "power", "dragon", "exhaust", "element", "poison", "paralysis", "impact"]
    # SHELLING_TYPES = ["any"] + [f"{x} {y}" for x in ["Normal", "Long", "Wide"] for y in ['', '1', '2', '3', '4', '5'] ]
    SHELLING_TYPES = ["any", "Normal", "Long", "Wide"]
    COATING_TYPES = ["Power 1", "Power 2", "Element 1", "Element 2", "Close Range", "Poison", "Paralysis", "Sleep", "Exhaust", "Blast"]

# wrapper class that filters and retrieves results from the Monster Hunter Generations Ultimate database
class WeaponDB:
    def __init__(self, db_location:str, weapon_table:str, columns_to_retrieve: list):
        self.db = sql.connect(db_location)
        self.weapon_table = weapon_table
        self.displayed_options = columns_to_retrieve
        self.additional_filters = ''
        self.results_order = 'order by items.name '

    # order results by specified column (name, rarity, attack (melee), attack (ranged), element, sharpness, affinity (melee), affinty (ranged), blunt, balance type)
    # ordered by name by default
    def order_results_by(self, type:str) -> None:
        if type == 'affinity':
            type = 'cast(affinity as integer)'
        self.results_order = f'order by {type} desc, name asc'

    def add_filter(self, filter:str):
        self.additional_filters += f'and {filter} '

    # gets results from database
    def _raw_execute(self, command) -> list:
        # execute and retrieve results from sql command
        cursor = self.db.execute(command)
        results = list(cursor.fetchall())

        # return results
        return results

    def execute(self) -> list:
        # adds selected options
        command = f"select {', '.join(self.displayed_options)} "
        command += f"from items, {self.weapon_table} where items._id = {self.weapon_table}._id  {self.additional_filters}"
        command += f" {self.results_order}"

        print(f"\n{command}")

        return self._raw_execute(command)



    # prints results into command line`
    def print_results(self, cursor:sql.Cursor) -> None:
        # temporary function that takes string and int and adds padding to the end
        print_formatted = lambda text, space: (print(f"{text.center(max(space, len(text)))}", end=" | "))

        padding = [22 for x in range(12)]

        header = ''
        for i in cursor.description:
            # print(f"'{i[0]}', ", end='')
            header += i[0].center(22) + ' | '
        print(header + '\n' + ''.join(['=' for x in range(len(header))]))

        # print out formatted table
        for row in cursor:

            for item in zip(row, padding):
                text = str(item[0])
                pad = item[1]
                print_formatted(text, pad)

            print()