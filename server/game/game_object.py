from __future__ import annotations

import datetime
import enum
import serial
from typing import Optional, Final

__all__ = (
    'PanelItem',
    'Player'
)


class PanelItem(enum.Enum):
    """
    Game Item Enum :
    this enum represents items which are displayed on mole (Panel which player hits).
    """
    # 0~4 : Positive items (for player self)
    BLANK = 0               # Transparent   : 아무런 아이템도 없는 빈 칸입니다.
    HEAL_SELF = 1           # Green         : 자신을 회복하는 칸입니다.
    OPPONENT_BLOCK = 2      # Purple        : 상대방이 일시적으로 자신을 공격하지 못하게 합니다.
    ATTACK_OPPONENT = 3     # Red           : 상대방을 공격하는 칸입니다.

    # 5~9 : Negative items (for player self)
    HEAL_OPPONENT = 4       # Pink          : 상대방을 회복하는 칸입니다.

    @classmethod
    def from_value(cls, value: int) -> Optional[PanelItem]:
        """
        Get PanelItem Enum using value.
        :param value: value of the enum.
        :return: PanelItem Enum if value is valid. Else, `None` is returned.
        """
        return next(filter(
            lambda e: e.value == value,
            cls.__members__.values()
        ), None)

    def __int__(self):
        """
        Override how int(self) works.
        :return: value of this enum.
        """
        return self.value

    def __repr__(self) -> str:
        """
        Override how repr(self) works.
        :return: debug information of this enum.
        """
        return f'PanelItem.{self.name}({self.value})'

    def __str__(self) -> str:
        """
        Override how str(self) works.
        :return:
        """
        return f'PanelItem.{self.name}'


"""
Player object
"""
# Constants
MAX_HP: Final[int] = 0          # Currently On Discussion.  # TODO : Fix value after the discussion.
MIN_HP: Final[int] = 0
ATTACK_DAMAGE: Final[int] = 10
HEAL_AMOUNT: Final[int] = 0     # Currently On Discussion.  # TODO : Fix value after the discussion.


class Player:
    """
    Player object which indicates player who plays the game.
    """

    serial_port: serial.Serial
    name: str
    session: GameSession

    def __init__(
            self,
            serial_port: serial.Serial,
            name: str,
            session: GameSession
    ):
        """

        :param serial_port: Serial port connected to this player.
        :param name: Name of the player. ex) Player1, Player2, ...
        """
        self.serial_port = serial_port
        self.name = name
        self.session = session
        self.hp = MAX_HP

    def heal(self):
        self.hp += HEAL_AMOUNT
        if self.hp > MAX_HP:
            # Fix player's health in health range (0 ~ MAX_HEALTH)
            self.hp = MAX_HP

    def damage(self):
        self.hp -= ATTACK_DAMAGE
        if self.hp < MIN_HP:
            self.session.onPlayerDeath(self)


class GameSession:
    """
    Game Session Object.
    """

    startedAt: datetime.datetime

    def __init__(
            self,
            startedAt: datetime.datetime
    ):
        self.startedAt = startedAt
        self.players = []

    def onPlayerDeath(self, player: Player):
        """
        Player Death Event Handler
        :param player: player instance who died.
        """
        pass