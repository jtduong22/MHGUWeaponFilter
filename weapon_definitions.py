from database_query import *

# definition for PalicoWeapon class
# child of WeaponDB
class PalicoWeapon(WeaponDB):
#### Class Constants ####
    HEADERS = ['name', 'rarity', 'attack (melee)', 'attack (ranged)', 'element', 'element (melee)', 'element (ranged)', 'defense', 'sharpness', 'affinity (melee)', 'affinity (ranged)', 'damage type', 'balance type']
    WEAPON_PARAMETERS = ['name', 'rarity', 'attack_melee', 'attack_ranged', 'element', 'element_melee', 'element_ranged', 'defense', 'sharpness', 'affinity_melee', 'affinity_ranged', 'blunt', 'balance']
    FILTERABLES = {'damage type':db_constants.DAMAGE_TYPES, 'balance type':db_constants.BALANCE_TYPES, 'element type':db_constants.ELEMENT_TYPES, 'sharpness':db_constants.SHARPNESS_TYPES}

#### Class Methods ####
    def __init__(self, db_location:str):
        # initialize parent
        WeaponDB.__init__(self, db_location, 'palico_weapons', self.WEAPON_PARAMETERS)

    # filter results
    def add_filter(self, filter:str, type:int):
        if type > 0:
            if filter == 'damage type':
                super().add_filter(f"palico_weapons.blunt={type-1}")
            elif filter == 'balance type':
                super().add_filter(f'palico_weapons.balance={type-1}')
            elif filter == 'element type':
                elem = db_constants.ELEMENT_TYPES[type].capitalize()
                super().add_filter(f'palico_weapons.element=\"{elem}\"')
            elif filter == 'sharpness':
                super().add_filter(f'palico_weapons.sharpness={type}')

    # order results by column
    def order_results_by(self, type:int) -> None:
        if type > 0:
            super().order_results_by(self.WEAPON_PARAMETERS[type])

# child class of WeaponDB
# all other weapons base off this one
class HunterWeapon(WeaponDB):
    # initializes WeaponDB
    # indicates which weapon is being used with weapon_type
    def __init__(self, db_location:str, weapon_table:str, columns_to_retrieve: list, weapon_type):
        WeaponDB.__init__(self, db_location, weapon_table, columns_to_retrieve)
        super().add_filter(f'{weapon_table}.wtype == \"{weapon_type}\"')

# definition of SwordAndShield class
class SwordAndShield(HunterWeapon):
    HEADERS = ['name', 'attack', 'element',
               'element attack', 'defense', 'sharpness', 'affinity', 'num slots']
    WEAPON_PARAMETERS = ['name', 'attack', 'element',
                         'element_attack', 'defense', 'sharpness', 'affinity', 'num_slots']
    FILTERABLES = {'element':db_constants.ELEMENT_TYPES, 'sharpness':db_constants.SHARPNESS_TYPES}

    # initialize parent class
    def __init__(self, db_location:str):
        HunterWeapon.__init__(self, db_location, "weapons", self.WEAPON_PARAMETERS, 'Sword and Shield')

    # filter results
    def add_filter(self, filter:str, type:int) -> None:
        if type > 0:
            if filter == 'element':
                elem = db_constants.ELEMENT_TYPES[type].capitalize()
                super().add_filter(f'weapons.element=\"{elem}\"')
            if filter == 'sharpness':
                super().add_filter(f'weapons.sharpness={type}')

    # order results by column
    def order_results_by(self, type:int) -> None:
        if type > 0:
            super().order_results_by(self.WEAPON_PARAMETERS[type])