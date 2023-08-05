from typing import List


def is_update_required(hub, old_tags_list: List, new_tags_list: List) -> bool:
    old_tags_list = old_tags_list if old_tags_list is not None else []
    new_tags_list = new_tags_list if new_tags_list is not None else []

    tags_to_add = {}
    tags_to_remove = {}
    new_tags = {}
    for tag in new_tags_list:
        new_tags[tag["tagKey"]] = tag.get("tagValue")

    old_tags = {}
    for tag in old_tags_list:
        old_tags[tag["tagKey"]] = tag.get("tagValue")

    for key, value in old_tags.items():
        if key in new_tags:
            if old_tags[key] != new_tags[key]:
                tags_to_remove.update({key: old_tags[key]})
                tags_to_add.update({key: new_tags[key]})
            new_tags.pop(key)
        else:
            tags_to_remove.update({key: old_tags[key]})
    tags_to_add.update(new_tags)

    return tags_to_add or tags_to_remove
