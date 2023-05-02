"""
Test all elements of the character class, which includes all model state
information for the game.
"""

from character import PlayerCharacter

DEFAULT_PLAYER_HEALTH = 10


def test_add_inventory():
    """
    Test that items are correctly added to a player's inventory.
    """
    # The sprite path is not used in this test, so it can be set to a null value
    player = PlayerCharacter("sprite_path", DEFAULT_PLAYER_HEALTH)

    player.update_inventory("item1")
    player.update_inventory("item2")

    assert player.inventory == ["item1", "item2"]


def test_remove_inventory():
    """
    Test that items are both added and removed from a player inventory
    correctly.
    """
    # The sprite path is not used in this test, so it can be set to a null value
    player = PlayerCharacter("sprite_path", DEFAULT_PLAYER_HEALTH)

    player.update_inventory("item1")
    player.update_inventory("item2")

    # Calling the update inventory method on a item already in the inventory
    # should remove it.
    player.update_inventory("item1")

    assert player.inventory == ["item2"]


def test_subtract_health():
    """
    Ensure that health is correctly removed from the player when the player is
    damaged by not killed.
    """

    # The sprite path is not used in this test, so it can be set to a null value
    player = PlayerCharacter("sprite_path", DEFAULT_PLAYER_HEALTH)

    # Remove only half of player health
    # The function additionally returns a boolean representing if the player is
    # still alive. Since we are only removing half the character's starting
    # health, this should still return true that the player is alive.
    assert player.update_health(DEFAULT_PLAYER_HEALTH // 2)

    # Assert that the health value is actually what it should be
    assert player.health == DEFAULT_PLAYER_HEALTH - (DEFAULT_PLAYER_HEALTH // 2)


def test_kill_player():
    """
    Assert that a player is correctly identified as dead (having less than zero
    health).
    """
    # The sprite path is not used in this test, so it can be set to a null value
    player = PlayerCharacter("sprite_path", DEFAULT_PLAYER_HEALTH)

    # Remove a number far greater than the initial player health to ensure the
    # player is dead. This should return false to represent the player being
    # dead.
    assert not player.update_health(DEFAULT_PLAYER_HEALTH * 10)


def test_add_health():
    """
    Assert that health can be added to the player by passing the update_health
    method a negative number.
    """
    # The sprite path is not used in this test, so it can be set to a null value
    player = PlayerCharacter("sprite_path", DEFAULT_PLAYER_HEALTH)

    # Remove only half of player health
    # The function additionally returns a boolean representing if the player is
    # still alive. Since we are only removing half the character's starting
    # health, this should still return true that the player is alive.
    assert player.update_health(-5)

    # Assert that the health value is actually what it should be
    assert player.health == DEFAULT_PLAYER_HEALTH + 5


def test_item_in_inventory():
    """
    Test that the method to check if something is in the player's inventory
    works correctly
    """
    # The sprite path is not used in this test, so it can be set to a null value
    player = PlayerCharacter("sprite_path", DEFAULT_PLAYER_HEALTH)

    test_items = ["item1", "item2", "item3"]

    for item in test_items:
        player.update_inventory(item)

    for item in test_items:
        assert player.in_inventory(item)

    assert not player.in_inventory("item4")
    assert not player.in_inventory(123)


def test_inventory_is_string():
    """
    Test that all objects added to the inventory get converted to strings.
    """

    # The sprite path is not used in this test, so it can be set to a null value
    player = PlayerCharacter("sprite_path", DEFAULT_PLAYER_HEALTH)

    test_items = ["item1", "item2", 123123, [12312, 123123]]

    for item in test_items:
        player.update_inventory(item)

    for item in player.inventory:
        assert isinstance(item, str)
