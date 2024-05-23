"""A collection of all commands that Adele can use to interact with the game. 	"""

from src.common import config, settings, utils
import time
import math
from src.routine.components import Command
from src.common.vkeys import press, key_down, key_up


# List of key mappings
class Key:
    # Movement
    JUMP = 'space'
    FLASH_JUMP = 'space'
    SWEEP = 'q'

    # Buffs
    NATURES_PROVIDENCE = '1'
    MAPLE_WARRIOR = '2'
    MOTHERS_NATURE = '3'
    AURA_OF_DESTINY = '4'
    HEAL ='5'
    MP_POT = 'r'


    # Buffs Toggle
    PECK = '7'
    SNEAK_ATTACK = '8'

    # Skills
    STRIKE = 'a'
    EARTH_PULVERIZATION = 'w'
    ROAR = 'e'
    PREDATORS_BLOW = 'd'


#########################
#       Commands        #
#########################
def step(direction, target):
    """
    Performs one movement step in the given DIRECTION towards TARGET.
    Should not press any arrow keys, as those are handled by Auto Maple.
    """

    num_presses = 2
    if direction == 'up' or direction == 'down':
        num_presses = 1
    if config.stage_fright and direction != 'up' and utils.bernoulli(0.75):
        time.sleep(utils.rand_float(0.1, 0.3))
    d_y = target[1] - config.player_pos[1]
    if abs(d_y) > settings.move_tolerance * 1.5:
        if direction == 'down':
            press(Key.JUMP, 3)
        elif direction == 'up':
            press(Key.JUMP, 1)
    press(Key.FLASH_JUMP, num_presses)


class Adjust(Command):
    """Fine-tunes player position using small movements."""

    def __init__(self, x, y, max_steps=5):
        super().__init__(locals())
        self.target = (float(x), float(y))
        self.max_steps = settings.validate_nonnegative_int(max_steps)

    def main(self):
        counter = self.max_steps
        toggle = True
        error = utils.distance(config.player_pos, self.target)
        while config.enabled and counter > 0 and error > settings.adjust_tolerance:
            if toggle:
                d_x = self.target[0] - config.player_pos[0]
                threshold = settings.adjust_tolerance / math.sqrt(2)
                if abs(d_x) > threshold:
                    walk_counter = 0
                    if d_x < 0:
                        key_down('left')
                        while config.enabled and d_x < -1 * threshold and walk_counter < 60:
                            time.sleep(0.05)
                            walk_counter += 1
                            d_x = self.target[0] - config.player_pos[0]
                        key_up('left')
                    else:
                        key_down('right')
                        while config.enabled and d_x > threshold and walk_counter < 60:
                            time.sleep(0.05)
                            walk_counter += 1
                            d_x = self.target[0] - config.player_pos[0]
                        key_up('right')
                    counter -= 1
            else:
                d_y = self.target[1] - config.player_pos[1]
                if abs(d_y) > settings.adjust_tolerance / math.sqrt(2):
                    if d_y < 0:
                        FlashJump('up').main()
                    else:
                        key_down('down')
                        time.sleep(0.05)
                        press(Key.JUMP, 3, down_time=0.1)
                        key_up('down')
                        time.sleep(0.05)
                    counter -= 1
            error = utils.distance(config.player_pos, self.target)
            toggle = not toggle

class Buff(Command):
    """Uses each buff once."""

    def __init__(self):
        super().__init__(locals())
        self.cd120_buff_time = 0
        self.cd60a_buff_time = 0
        self.cd60b_buff_time = 0
        self.cdpot_buff_time = 0
        self.cd900_buff_time = 0
        self.decent_buff_time = 0

    def main(self):
        buffs = []
        now = time.time()

        if self.cd120_buff_time == 0 or now - self.cd120_buff_time > 120:
            press(Key.NATURES_PROVIDENCE, 3)
            self.cd120_buff_time = now

        if self.heal_active:
            if self.cd60a_buff_time == 0 or now - self.cd60a_buff_time > 60:
                press(Key.HEAL, 3)
                self.cd60a_buff_time = now
                self.heal_active = False  # Switch to MOTHERS_NATURE next
        else:
            if self.cd60b_buff_time == 0 or now - self.cd60b_buff_time > 60:
                press(Key.MOTHERS_NATURE, 3)
                self.cd60b_buff_time = now
                self.heal_active = True  # Switch to HEAL next

        if self.cdpot_buff_time == 0 or now - self.cdpot_buff_time > 30:
            press(Key.MP_POT, 2)
            self.cdpot_buff_time = now

        if self.cd900_buff_time == 0 or now - self.cd900_buff_time > 900:
            press(Key.MAPLE_WARRIOR, 3)
            self.cd900_buff_time = now

        if self.decent_buff_time == 0 or now - self.decent_buff_time > 270:
            for key in buffs:
                press(key, 1, up_time=0.3)
            self.decent_buff_time = now


class Strike(Command):
    """Attacks using 'Solar Slash' in a given direction."""

    def __init__(self, direction, attacks=2, repetitions=1):
        super().__init__(locals())
        self.direction = settings.validate_horizontal_arrows(direction)
        self.attacks = int(attacks)
        self.repetitions = int(repetitions)

    def main(self):
        time.sleep(0.05)
        key_down(self.direction)
        time.sleep(0.05)
        if config.stage_fright and utils.bernoulli(0.7):
            time.sleep(utils.rand_float(0.1, 0.3))
        for _ in range(self.repetitions):
            press(Key.STRIKE, self.attacks, up_time=0.05)
        key_up(self.direction)
        if self.attacks > 2:
            time.sleep(0.3)
        else:
            time.sleep(0.2)


class FlashJump(Command):
    """Performs a flash jump in the given direction."""

    def __init__(self, direction):
        super().__init__(locals())
        self.direction = settings.validate_arrows(direction)

    def main(self):
        key_down(self.direction)
        time.sleep(0.1)
        press(Key.FLASH_JUMP, 1)
        if self.direction == 'up':
            press(Key.FLASH_JUMP, 1)
        else:
            press(Key.FLASH_JUMP, 1)
        key_up(self.direction)
        time.sleep(0.5)

class EarthPulverization(Command):
    """Uses Earth Pulverization once."""

    def main(self):
        press(Key.EARTH_PULVERIZATION, 3)

class Roar(Command):
    """Uses Roar once."""

    def main(self):
        press(Key.ROAR, 3)

class SneakAttack(Command):
    """Uses Earth Pulverization once."""

    def main(self):
        press(Key.SNEAK_ATTACK, 3)
