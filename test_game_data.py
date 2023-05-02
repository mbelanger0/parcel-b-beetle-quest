"""
Test that all game data is correctly implemented such that events don't
reference other events that don't exist.

IMPORTANT_NOTE: these tests are mostly checking that we have correctly input and
formatted all of our data, rather than testing our actual implementation of the
code.

NOTE ON PYLINT: Multiple pylint disable pointless-statements are used
throughout this file. This is since many checks are simply preforming whether
a given dictionary access results in an KeyError - the actual value isn't
being test and is irrelevant, it is just the fact that the key exists that is
being checked.
"""
from json import load
from ast import literal_eval
import pytest
from scene import MAP_SCENES_FILEPATH, EVENT_SCENES_FILEPATH


def test_map_event_references():
    """
    Test that map scenes don't references events that don't exist.
    """

    with open(MAP_SCENES_FILEPATH, "r", encoding="utf-8") as file:
        map_data = load(file)

    with open(EVENT_SCENES_FILEPATH, "r", encoding="utf-8") as file:
        event_data = load(file)

    for map_event in map_data:
        event_id = map_event["SpecialEvent"]

        # -100 is used in the datafile to signify a special event does not occur
        # at a given map point.
        if event_id != -100:
            # If there isn't an event that corresponds to the ID that the map
            # is supposed to invoke, this will result in a KeyError
            event_data[event_id]  # pylint: disable=pointless-statement


def test_map_direction_references():
    """
    Test that the map scenes don't try to move to map points that don't exist.
    """
    # Load the external map data file
    with open(MAP_SCENES_FILEPATH, "r", encoding="utf-8") as file:
        map_data = load(file)

    # Loop though each point on the map
    for map_event in map_data:
        # JSON data doesn't support tuples, so literal_eval converts from the
        # string that is stored in the JSON data back into a tuple.
        directions = literal_eval(map_event["DirectionsToMove"])

        for direction in directions:
            # Not every index in the tuple is going to have a value, with None
            # being used to represent directions that the player isn't allowed
            # to move.
            if direction is not None:
                # If the map scene is trying to call another scene that doesn't
                # exist, this will result in a key error.
                map_data[direction]  # pylint: disable=pointless-statement


def test_next_event_references():
    """
    Test that nested events (events that lead to other events) don't call on
    events that don't exist.
    """

    # Load external event data
    with open(EVENT_SCENES_FILEPATH, "r", encoding="utf-8") as file:
        event_data = load(file)

    # Loop through to test each event
    for event in event_data:
        # literal eval to make sure everything is correctly formatted from JSON
        # to Python
        next_events = literal_eval(event["OptionResultID"])

        for index, next_event in enumerate(next_events):
            # -100 is used to signify that the end of an event tree is reached,
            # and should throw an exception that is handled in the code to exit
            # back to the main map.
            if next_event == -100:
                with pytest.raises(IndexError):
                    event_data[  # pylint: disable=pointless-statement
                        next_event
                    ]
            # None is used as a seperate event tree end to signify that the
            # player has either won or lost the game. As such, there should
            # be something in the GameEnd variable to display as a death/win
            # message
            elif next_event is None:
                with pytest.raises(TypeError):
                    event_data[  # pylint: disable=pointless-statement
                        next_event
                    ]
                assert literal_eval(event["GameEnd"])[index] is not None

            else:
                # If the value isn't None (meaning it should continue on to
                # another event), this statement should execute without error.
                event_data[next_event]  # pylint: disable=pointless-statement
