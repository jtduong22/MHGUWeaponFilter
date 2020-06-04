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
                super().add_filter(f'palico_weapons.sharpness={type-1}')

    def order_results_by(self, type:int) -> None:
        if type > 0:
            super().order_results_by(self.WEAPON_PARAMETERS[type])
    # order results by column

# child class of WeaponDB
# all other weapons base off this one
class HunterWeapon(WeaponDB):
    HEADERS = ['name', 'attack', 'element',
               'elem atk', 'def', 'crit', 'slots']
    WEAPON_PARAMETERS = ['name', 'attack', 'element',
                         'element_attack', 'defense', 'affinity', 'num_slots']
    FILTERABLES = {'element':db_constants.ELEMENT_TYPES, 'num slots':['any', '1', '2', '3']}

    # initializes WeaponDB
    # indicates which weapon is being used with weapon_type
    def __init__(self, db_location:str, weapon_table:str, columns_to_retrieve: list, weapon_type):
        WeaponDB.__init__(self, db_location, weapon_table, columns_to_retrieve)
        super().add_filter(f'{weapon_table}.wtype == \"{weapon_type}\"')
        super().add_filter(f'{weapon_table}.final == 1')

    # filter results
    def add_filter(self, filter:str, type:int) -> None:
        if type > 0:
            if filter == 'element':
                elem = db_constants.ELEMENT_TYPES[type].capitalize()
                super().add_filter(f'weapons.element=\"{elem}\"')
            elif filter == 'num slots':
                super().add_filter(f'num_slots == \'{type}\'')
            # elif filter == 'sharpness':
            #     super().add_filter(f'weapons.sharpness={type}')

    def _add_filter(self, filter:str) -> None:
        super().add_filter(filter)

    # order results by column
    def order_results_by(self, type:int) -> None:
        if type > 0:
            super().order_results_by(self.WEAPON_PARAMETERS[type])

class BladeMaster(HunterWeapon):
    HEADERS = HunterWeapon.HEADERS + ['sharpness']
    WEAPON_PARAMETERS = HunterWeapon.WEAPON_PARAMETERS + ['sharpness']

    def __init__(self, db_location:str, weapon_table:str, columns_to_retrieve: list, weapon_type: str):
        HunterWeapon.__init__(self, db_location, weapon_table, columns_to_retrieve, weapon_type)

# definition of SwordAndShield class
class SwordAndShield(BladeMaster):
    # initialize parent class
    def __init__(self, db_location:str):
        BladeMaster.__init__(self, db_location, "weapons", self.WEAPON_PARAMETERS, 'Sword and Shield')

# definition of GreatSword class
class GreatSword(BladeMaster):
    # initialize parent class
    def __init__(self, db_location:str):
        BladeMaster.__init__(self, db_location, "weapons", self.WEAPON_PARAMETERS, 'Great Sword')

# definition of Hammer class
class Hammer(BladeMaster):
    # initialize parent class
    def __init__(self, db_location: str):
        BladeMaster.__init__(self, db_location, "weapons", self.WEAPON_PARAMETERS, 'Hammer')

# definition of Lance class
class Lance(BladeMaster):
    # initialize parent class
    def __init__(self, db_location: str):
        BladeMaster.__init__(self, db_location, "weapons", self.WEAPON_PARAMETERS, 'Lance')

# definition of LongSword class
class LongSword(BladeMaster):
    # initialize parent class
    def __init__(self, db_location: str):
        BladeMaster.__init__(self, db_location, "weapons", self.WEAPON_PARAMETERS, 'Long Sword')

# definition of SwitchAxe class
class ChargeBlade(BladeMaster):
    HEADERS = BladeMaster.HEADERS + ['phial types']
    WEAPON_PARAMETERS = BladeMaster.WEAPON_PARAMETERS + ['phial']
    FILTERABLES = {**BladeMaster.FILTERABLES, 'phial':['Impact', 'Element']}

    # initialize parent class
    def __init__(self, db_location: str):
        BladeMaster.__init__(self, db_location, "weapons", self.WEAPON_PARAMETERS, 'Charge Blade')

    # filter results
    def add_filter(self, filter: str, type: int) -> None:
        if type > 0:
            if filter == 'phial':
                phial = db_constants.PHIAL_TYPES[type].capitalize()
                self._add_filter(f'weapons.phial=\'{phial}\'')
            else:
                super().add_filter(filter, type)

# definition of SwitchAxe class
class SwitchAxe(BladeMaster):
    HEADERS = BladeMaster.HEADERS + ['phial types']
    WEAPON_PARAMETERS = BladeMaster.WEAPON_PARAMETERS + ['phial']
    FILTERABLES = {**BladeMaster.FILTERABLES, 'phial':[x for x in db_constants.PHIAL_TYPES if x != 'impact']}

    # initialize parent class
    def __init__(self, db_location: str):
        BladeMaster.__init__(self, db_location, "weapons", self.WEAPON_PARAMETERS, 'Charge Blade')

    # filter results
    def add_filter(self, filter: str, type: int) -> None:
        if type > 0:
            if filter == 'phial':
                phial = db_constants.PHIAL_TYPES[type].capitalize()
                self._add_filter(f'weapons.phial=\'{phial}\'')
            else:
                super().add_filter(filter, type)


# definition of HuntingHorn class
class HuntingHorn(BladeMaster):
    CONTAINS = {"Songs":[]}

    # initialize parent class
    def __init__(self, db_location: str):
        BladeMaster.__init__(self, db_location, "weapons", self.WEAPON_PARAMETERS, 'Hunting Horn')

    def init_contains(self):
        song_names = self.get_song_names()
        HuntingHorn.CONTAINS["Songs"] = song_names

    # get list of all song names
    def get_song_names(self) -> list:
        command = 'select distinct name from horn_melodies'
        results = [x[0] for x in self._raw_execute(command)]

        return results

    # get notes associated with song name
    def get_notes(self, song_name: str) -> dict:
        command = f'select distinct notes from horn_melodies where name == \"{song_name}\" order by name'
        results = self._raw_execute(command)
        notes = [x[0] for x in results]

        return notes

    # filter results
    # checks if trying to filter for song, calls parent's add_filter otherwise
    def add_filter(self, filter: str, type: int) -> None:
        if filter == 'Songs':
            filtered_songs = []

            for i in reversed(range(len(self.CONTAINS['Songs']))):
                if type % 2 == 1:
                    filtered_songs.append(self.CONTAINS['Songs'][i])
                type = type >> 1

            formatted_songs = [f"select notes from horn_melodies where name == '{x}'" for x in filtered_songs]
            command = ' intersect '.join(formatted_songs)
            print(command)

            command = f"weapons.horn_notes in ({command})"

            super()._add_filter(command)
        else:
            super().add_filter(filter, type)

# definition of Gunlance class
class Gunlance(BladeMaster):
    HEADERS = BladeMaster.HEADERS + ['shelling type']
    WEAPON_PARAMETERS = BladeMaster.WEAPON_PARAMETERS + ['shelling_type']
    FILTERABLES = {**BladeMaster.FILTERABLES, 'shelling type':db_constants.SHELLING_TYPES}

    # initialize parent class
    def __init__(self, db_location: str):
        BladeMaster.__init__(self, db_location, "weapons", self.WEAPON_PARAMETERS, 'Gunlance')

    # filter results
    def add_filter(self, filter: str, type: int) -> None:
        if type > 0:
            if filter == 'shelling type':
                shell = db_constants.SHELLING_TYPES[type]
                self._add_filter(f'weapons.shelling_type like \'{shell}%\'')
            else:
                super().add_filter(filter, type)

# definition of DualBlades class
class DualBlades(BladeMaster):
    HEADERS = BladeMaster.HEADERS[0:4] + ['element 2', 'element 2 attack'] + BladeMaster.HEADERS[4:len(BladeMaster.HEADERS)]
    WEAPON_PARAMETERS = BladeMaster.WEAPON_PARAMETERS[0:4] + ['element_2', 'element_2_attack'] + BladeMaster.WEAPON_PARAMETERS[4:len(BladeMaster.WEAPON_PARAMETERS)]
    FILTERABLES = {**BladeMaster.FILTERABLES, 'element 2':db_constants.ELEMENT_TYPES}

    # initialize parent class
    def __init__(self, db_location: str):
        BladeMaster.__init__(self, db_location, "weapons", self.WEAPON_PARAMETERS, 'Dual Blades')

    # filter results
    def add_filter(self, filter: str, type: int) -> None:
        if type > 0:
            if filter == 'element 2':
                elem = db_constants.ELEMENT_TYPES[type].capitalize()
                self._add_filter(f'weapons.element_2=\"{elem}\"')
            else:
                super().add_filter(filter, type)

# definition of InsectGlaive class
class InsectGlaive(BladeMaster):
    # initialize parent class
    def __init__(self, db_location: str):
        BladeMaster.__init__(self, db_location, "weapons", self.WEAPON_PARAMETERS, 'Insect Glaive')

# definition of Bow class
class Bow(HunterWeapon):
    HEADERS = HunterWeapon.HEADERS + ['charges']
    WEAPON_PARAMETERS = HunterWeapon.WEAPON_PARAMETERS + ['charges']
    FILTERABLES = {**HunterWeapon.FILTERABLES, 'charges':db_constants.CHARGE_TYPES}
    CONTAINS = {'Coatings':[]}

    # initialize parent class
    def __init__(self, db_location: str):
        HunterWeapon.__init__(self, db_location, "weapons", self.WEAPON_PARAMETERS, 'Bow')

    def init_contains(self):
        Bow.CONTAINS['Coatings'] = db_constants.COATING_TYPES

    # filter results
    # checks if trying to filter for coating, calls parent's add_filter otherwise
    def add_filter(self, filter: str, type: int) -> None:
        if type > 0:
            # add coating
            if filter == 'Coatings':
                # get possible coatings
                selected_coatings = type
                possible_coats = self.get_all_other_coatings(len(db_constants.COATING_TYPES), 0, selected_coatings)

                # create command
                command = ', '.join(possible_coats)
                command = f"weapons.coatings in ({command})"
                print(command)
                super()._add_filter(command)
            elif filter == 'charges':
                charge = db_constants.CHARGE_TYPES[type]
                command = f"weapons.charges like \"%{charge}%\""
                super()._add_filter(command)
            else:
                super().add_filter(filter, type)

    # calculates all other coatings code
    # database stores coats in bitcode (whereever there's a 1, the weapon has that coating)
        # e.g nerscylla bow has power 1, poison, and sleep coatings
        # has the code 1065 or 1000010100 1
        # leftmost 1 is power 1, 6th 1 is poison, 8th 1 is sleep (adds up to 532)
        # database multiplies by 2 and adds 1 (hence 1065)
    def get_all_other_coatings(self, index, sum, coating_code) -> list:
        potential_coating = []

        # keep going
        if index > 0:
            # coating was not explicitly selected. add scenario where coating doesn't exist
            if (coating_code >> (index - 1)) % 2 == 0:
                potential_coating += self.get_all_other_coatings(index - 1, sum << 1, coating_code)

            potential_coating += self.get_all_other_coatings(index - 1, (sum << 1) + 1, coating_code)
        # done with recursion, return list
        else:
            potential_coating += [str((sum << 1) + 1)]

        return potential_coating

class Gunner(HunterWeapon):
    HEADERS = HunterWeapon.HEADERS[0:1] + HunterWeapon.HEADERS[4:] + ['recoil', 'reload speed', 'deviation', 'ammo', 'special ammo']
    WEAPON_PARAMETERS = HunterWeapon.WEAPON_PARAMETERS[0:1] + HunterWeapon.WEAPON_PARAMETERS[4:] + ['recoil', 'reload_speed', 'deviation', 'ammo', 'special_ammo']
    FILTERABLES = {x:HunterWeapon.FILTERABLES[x] for x in HunterWeapon.FILTERABLES.keys() if x != 'element' and x != 'element_attack'}
    CONTAINS = {'Shot Types':[], 'Special Ammo':[]}

    def __init__(self, db_location: str, weapon_table: str, columns_to_retrieve: list, weapon_type: str):
        HunterWeapon.__init__(self, db_location, weapon_table, columns_to_retrieve, weapon_type)

    def init_contains(self):
        self.CONTAINS['Shot Types'] = db_constants.SHOT_TYPES
        self.CONTAINS['Special Ammo'] = self.get_special_shots()

    def filter_special_rapid_shots(self, filter_string:str, bit_selected:int) -> list:
        selected_shots = []

        # cycle through each shot type
        for i in reversed(range(len(self.CONTAINS[filter_string]))):
            # check if shot is selected
            if bit_selected % 2 == 1:
                shot = self.CONTAINS[filter_string][i]
                selected_shots.append(shot)

            # shift bit over by one
            bit_selected = bit_selected >> 1
        return selected_shots

    # filter results
    def add_filter(self, filter: str, type: int) -> None:
        if type > 0:
            if filter == 'Shot Types':
                selected_shots = []

                # filter through each shot type to see what's selected
                for i in range(len(self.CONTAINS['Shot Types'])):
                    # left most bit is 1 (i.e shot is selected)
                    if type % 2 == 1:
                        selected_shots += ['_*']
                    else:
                        selected_shots += ['%']
                    type = type >> 1

                command = f"weapons.ammo like \"{'|'.join(reversed(selected_shots))}|%|%|\""
                print(command)
                super()._add_filter(command)

            # filter through each shot type to see what's selected
            elif filter == 'Special Ammo':
                selected_shots = self.filter_special_rapid_shots(filter, type)
                for shot in selected_shots:
                    command = f"weapons.special_ammo like '%{shot}%'"
                    self._add_filter(command)

            else:
                super().add_filter(filter, type)


# get list of all special shots
    def get_special_shots(self):
        # get all special shots combinations
        command = "select distinct special_ammo from weapons where final == '1' and special_ammo <> ''"
        s_shots = self._raw_execute(command)

        # get only unique shots
        parsed_shots = set()

        # cycle through all loadouts to get
        for shots in s_shots:
            for shot in shots[0].split('*'):
                shot = shot.split(':')[0]
                parsed_shots.add(shot)

        return sorted(parsed_shots)

    # get all rapid_fire_shots
    def get_rapid_fire_shots(self, weapon_type):
        command = f"select distinct rapid_fire from weapons where final == '1' and wtype == '{weapon_type}'"
        r_shots = self._raw_execute(command)

        parsed_shots = set()

        # retrieve all shot rapid fire shot types
        for shots in r_shots:
            for shot in shots[0].split('*'):
                shot = shot.split(':')[0]
                parsed_shots.add(shot)

        # return list in alphabetical order
        return sorted(parsed_shots)

class LightBowgun(Gunner):
    HEADERS = Gunner.HEADERS + ['rapid fire']
    WEAPON_PARAMETERS = Gunner.WEAPON_PARAMETERS + ['rapid_fire']
    CONTAINS = {**Gunner.CONTAINS, 'Rapid Fire':[]}

    # initialize parent class
    def __init__(self, db_location:str):
        Gunner.__init__(self, db_location, 'weapons', self.WEAPON_PARAMETERS, 'Light Bowgun')

    def init_contains(self):
        super().init_contains()
        self.CONTAINS['Rapid Fire'] = self.get_rapid_fire_shots('Light Bowgun')


    def add_filter(self, filter: str, type: int) -> None:
        if type > 0:
            if filter == 'Rapid Fire':
                selected_shots = self.filter_special_rapid_shots('Rapid Fire', type)

                for shot in selected_shots:
                    command = f"weapons.rapid_fire like '%{shot}%'"
                    self._add_filter(command)
            else:
                super().add_filter(filter, type)

class HeavyBowgun(Gunner):
    HEADERS = Gunner.HEADERS + ['siege fire']
    WEAPON_PARAMETERS = Gunner.WEAPON_PARAMETERS + ['rapid_fire']
    CONTAINS = {**Gunner.CONTAINS, 'Siege Fire':[]}

    # initialize parent class
    def __init__(self, db_location:str):
        Gunner.__init__(self, db_location, 'weapons', self.WEAPON_PARAMETERS, 'Heavy Bowgun')

    def init_contains(self):
        super().init_contains()
        self.CONTAINS["Siege Fire"] = self.get_rapid_fire_shots('Heavy Bowgun')

    def add_filter(self, filter: str, type: int) -> None:
        if type > 0:
            if filter ==  'Siege Fire':
                selected_shots = self.filter_special_rapid_shots('Siege Fire', type)

                for shot in selected_shots:
                    command = f"weapons.rapid_fire like '%{shot}%'"
                    self._add_filter(command)
            else:
                super().add_filter(filter, type)

