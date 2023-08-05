import collections.abc as abc
import copy
from typing import Any
from typing import Dict
from typing import List


def are_lists_identical(hub, list1: List, list2: List) -> bool:
    """
    Compare two lists and logs the difference.
    :param list1: first list.
    :param list2: second list.
    :return: true if there is no difference between both lists.
    :raises exception if one of the list  is not of type list
    """
    if (list1 is None or len(list1) == 0) and (list2 is None or len(list2) == 0):
        return True
    if list1 is None or len(list1) == 0 or list2 is None or len(list2) == 0:
        return False

    for l in [list1, list2]:
        if not isinstance(l, List):
            raise TypeError(
                f"Expecting lists to compare. This is expected to be of type List: '{l}'"
            )

    diff = [i for i in list1 + list2 if i not in list1 or i not in list2]
    result = len(diff) == 0
    if not result:
        hub.log.debug(f"There are {len(diff)} differences:\n{diff[:5]}")
    return result


def deep_diff(
    hub, current_state: Dict, desire_state: Dict, ignore: List = None
) -> Dict[str, Any]:
    """
    Recursively compare two dictionaries(current_state and desire_state) and find the differences.
    """
    ignore = ignore or []
    res = {}
    current_state = copy.deepcopy(current_state) or {}
    desire_state = copy.deepcopy(desire_state) or {}

    stack = [(current_state, desire_state, False)]

    while len(stack) > 0:
        tmps = []
        tmp_current_state, tmp_desire_state, reentrant = stack.pop()
        for key in set(list(tmp_current_state) + list(tmp_desire_state)):
            if (
                key in tmp_current_state
                and key in tmp_desire_state
                and isinstance(tmp_current_state[key], List)
                and hub.tool.spotinst.state_comparison_utils.are_lists_identical(
                    tmp_current_state[key], tmp_desire_state[key]
                )
            ):
                del tmp_current_state[key]
                del tmp_desire_state[key]
                continue
            elif (
                key in tmp_current_state
                and key in tmp_desire_state
                and tmp_current_state[key] == tmp_desire_state[key]
            ):
                del tmp_current_state[key]
                del tmp_desire_state[key]
                continue
            if not reentrant:
                if key in tmp_current_state and key in ignore:
                    del tmp_current_state[key]
                if key in tmp_desire_state and key in ignore:
                    del tmp_desire_state[key]
                if isinstance(tmp_current_state.get(key), abc.Mapping) and isinstance(
                    tmp_desire_state.get(key), abc.Mapping
                ):
                    tmps.append((tmp_current_state[key], tmp_desire_state[key], False))
        if tmps:
            stack.extend([(tmp_current_state, tmp_desire_state, True)] + tmps)
    if current_state:
        res["current_state"] = current_state
    if desire_state:
        res["desire_state"] = desire_state
    return res
