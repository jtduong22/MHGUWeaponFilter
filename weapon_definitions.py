from database_query import *

class PalicoWeapon(WeaponDB):
    headers = ['name', 'rarity', 'attack (melee)', 'attack (ranged)', 'element', 'element (melee)', 'element (ranged)', 'defense', 'sharpness', 'affinity (melee)', 'affinity (ranged)', 'blunt', 'balance type']
    weapon_parameters = ['name', 'rarity', 'attack_melee', 'attack_ranged', 'element', 'element_melee', 'element_ranged', 'defense', 'sharpness', 'affinity_melee', 'affinity_ranged', 'blunt', 'balance']

    def __init__(self, db_location:str):
        WeaponDB.__init__(self, db_location, 'palico_weapons', self.weapon_parameters)

    # adds filter for damage type (cutting, blunt)
    def add_damage_type_filter(self, type:int) -> None:
        if type > 0:
            self.add_filter(f"palico_weapons.blunt={type-1}")

    # adds filter for balance type (balanced, melee, boomerang)
    def add_balance_type_filter(self, type:int) -> None:
        if type > 0:
            self.add_filter(f'palico_weapons.balance={type-1}')

    # adds filter for element type (fire, water, thunder, ice, dragon, poison, sleep, paralysis, blastblight)
    def add_element_type_filter(self, type:int) -> None:
        if type > 0:
            elem = db_constants.ELEMENT_TYPES[type].capitalize()
            self.add_filter(f'palico_weapons.element=\"{elem}\"')

    # adds filter for sharpness type (red, yellow, green, blue, white, purple)
    def add_sharpness_filter(self, type:int):
        if type > 0:
            self.add_filter(f'palico_weapons.sharpness={type}')

class HunterWeapon(WeaponDB):
    def __init__(self, db_location:str, weapon_table:str, columns_to_retrieve: list, weapon_type):
        WeaponDB.__init__(self, db_location, weapon_table, columns_to_retrieve)
        self.add_filter(f'{weapon_table}.wtype == {weapon_type}')

class SwordAndShield(HunterWeapon):
    def __init__(self, db_location:str):
        weapon_parameters = ['name', 'attack', 'max_attack', 'element',
         'element_attack', 'awaken', 'awaken_attack', 'defense', 'sharpness', 'affinity', 'num_slots']

        HunterWeapon.__init__(self, db_location, "weapons", weapon_parameters, 'Sword and Shield')