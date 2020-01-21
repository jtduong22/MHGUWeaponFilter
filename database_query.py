import _sqlite3 as sql

class db_constants():
    list_to_index_converter = lambda my_list: {x: y - 1 for x, y in zip(my_list, range(len(my_list)))}

    ### CONSTANTS ###
    DAMAGE_TYPES = ["any", "cutting", "blunt"]
    DAM_TO_INDEX = list_to_index_converter(DAMAGE_TYPES)

    BALANCE_TYPES = ["any", "balanced", "melee", "boomerang"]
    BAL_TO_INDEX = list_to_index_converter(BALANCE_TYPES)

    ELEMENT_TYPES = ["any", "fire", "water", "thunder", "ice", "dragon", "poison", "sleep", "paralysis", "blastblight"]

    SHARPNESS_TYPES = ["any", "red", "yellow", "green", "blue", "white", "purple"]
    SHA_TO_INDEX = list_to_index_converter(SHARPNESS_TYPES)

    ORDER_BY_TYPES = {'name': 'name', 'attack (melee)': 'attack_melee', 'attack (ranged)': 'attack_ranged',
                      'element': 'element', 'element (melee)': 'element_melee', 'element (ranged)': 'element_ranged',
                      'defense': 'defense', 'sharpness': 'sharpness', 'affinity melee': 'affinity_melee',
                      'affinity ranged': 'affinity_ranged', 'balance type': 'balance', 'blunt': 'blunt'}

class weapon_db:
    def __init__(self, db_location:str):
        self.db = sql.connect(db_location)
        self.displayed_options = ', palico_weapons.attack_melee, palico_weapons.attack_ranged, palico_weapons.element, palico_weapons.element_melee, palico_weapons.element_ranged, palico_weapons.defense, palico_weapons.sharpness, palico_weapons.affinity_melee, palico_weapons.affinity_ranged, palico_weapons.blunt, palico_weapons.balance'
        self.additional_filters = ''
        self.results_order = 'order by items.name '
        self.headers = ['attack_melee', 'attack_ranged', 'element', 'element_melee', 'element_ranged', 'defense', 'sharpness', 'affinity_melee', 'affinity_ranged', 'blunt', 'balance']

    def add_damage_type_filter(self, type:int) -> None:
        if type > 0:
            self.additional_filters += f'and palico_weapons.blunt={type} '

    def add_balance_type_filter(self, type:int) -> None:
        if type > 0:
            self.additional_filters += f'and palico_weapons.balance={type} '

    def add_element_type_filter(self, type:int) -> None:
        if type > 0:
            self.additional_filters += f'and palico_weapons.balance={db_constants.ELEMENT_TYPES[type]} '
        # if type.lower() != 'any':
        #     self.additional_filters += f"and palico_weapons.element='{type}'"

    def add_sharpness_filter(self, type:int):
        if type > 0:
            self.additional_filters += f"and palico_weapons.sharpness={type} "

    def order_results_by(self, type:int) -> None:
        if type > 0:
            key = list(db_constants.ORDER_BY_TYPES.keys())[type]
            self.results_order = f'order by {db_constants.ORDER_BY_TYPES[key]} desc, name asc'
        # if type in self.headers:
        #     self.results_order = f'order by {type} desc, name asc'

    def execute(self, is_print_enabled=True) -> None:
        command = f"select items.name{self.displayed_options} "
        command += f"from items, palico_weapons where items._id = palico_weapons._id  {self.additional_filters}"
        command += f" {self.results_order}"

        print(f"\n{command}")

        cursor = self.db.execute(command)

        self.print_results(cursor)

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

if __name__ == '__main__':
    print(db_constants.ORDER_BY_TYPES)