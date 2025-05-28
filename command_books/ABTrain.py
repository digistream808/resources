"""A collection of all commands that Adele can use to interact with the game. 	"""

from src.common import config, settings, utils
import time
import math
from src.routine.components import Command
from src.common.vkeys import press, key_down, key_up


# List of key mappings
class Key:
    # Movement
    JUMP = 'alt'
    FLASH_JUMP = 'alt'
    ROPE = 'x'

    # Buffs
    SOULSEEK = '1'
    NOVA_WARRIOR = '2'
    OVERDRIVE = '3'
    PRETTT_EXALT = '4'
    TERMS = '5' 
    ROLL = '6'
    XP_30 = 'f5'
    LEGION_GOLD = 'f4'


    # Skills
    TRINITY = 'w'
    ROAR = 'q'
    SUPERNOVA = 'f'
    SPOTLIGHT = 'e'
    SPARKLE = 'r'
    RIBBON = 'a'
    Erda = 'j'
    Sol = 'h'
    Finale = '8'



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
    if abs(d_y) > settings.move_tolerance :
        if direction == 'down':
            press(Key.JUMP, 1)
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
                        press(Key.JUMP, 2, down_time=0.1)
                        key_up('down')
                        time.sleep(0.05)
                    counter -= 1
            error = utils.distance(config.player_pos, self.target)
            toggle = not toggle


class Buff(Command):

    def __init__(self):
        super().__init__(locals())
        self.cd60_buff_time = 0
        self.cd120_buff_time = 0
        self.cd300_buff_time = 0
        self.cd900_buff_time = 0
        self.decent_buff_time = 0

    def main(self):
        buffs = [Key.PRETTT_EXALT, Key.TERMS]
        Gains = [Key.LEGION_GOLD, Key.XP_30]

        now = time.time()

        if self.cd60_buff_time == 0 or now - self.cd60_buff_time > 60:
	        for key in buffs:
                    press(key, 1, up_time=0.5)
                    self.cd60_buff_time = now
        if self.cd120_buff_time == 0 or now - self.cd120_buff_time > 120:
            press(Key.ROLL,4)
            self.cd180_buff_time = now
        if self.cd300_buff_time == 0 or now - self.cd300_buff_time > 300:
            self.cd300_buff_time = now
        if self.decent_buff_time == 0 or now - self.decent_buff_time > 1820:
            self.decent_buff_time = now		

class Roar(Command):

    def __init__(self, direction, attacks=3, repetitions=1):
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
            press(Key.ROAR, self.attacks, up_time=0.1)
        key_up(self.direction)
        if self.attacks > 2:
            time.sleep(0.35)
        else:
            time.sleep(0.25)


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

class Trinity(Command):
    def main(self):
        press(Key.TRINITY, 2)

class SuperNova(Command):
    def main(self):
        press(Key.SUPERNOVA, 3)

class Sparkle(Command):
    def main(self):
        press(Key.SPARKLE, 3)

class ErdaShower(Command):
    def main(self):
        press(Key.Erda, 3)

class Spotlight(Command):
    def main(self):
        press(Key.SPOTLIGHT, 3)

class Rope(Command):
    def main(self):
        press(Key.ROPE, 3)

class ribbon(Command):
    def main(self):
        press(Key.RIBBON, 3)

class sol(Command):
    def main(self):
        press(Key.Sol, 3)

class finale(Command):
    def main(self):
        press(Key.Finale,3)

class holdcombo(Command):
    def main(self):
        press(Key.ROAR, 3, up_time=0.25)