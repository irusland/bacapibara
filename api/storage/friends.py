class FriendsStorage:
    def __init__(self):
        self._friends = set()

    def __len__(self) -> int:
        return len(self._friends)

    def add_friend(self, id_: int, other_id: int) -> set[tuple[int, int]]:
        relation = (id_, other_id)
        if relation in self._friends:
            raise Exception(f"Friendship {relation} already exists")
        self._friends.add(relation)
        return self._friends

    def get_friends(self) -> set[tuple[int, int]]:
        return self._friends
