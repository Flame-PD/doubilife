from core.event import *
from core.player import *
from collections import deque
from typing import Dict, List, Optional
import random

class EventQueue:
    def __init__(self):
        self.queue = deque()

    def clear(self) -> None:
        self.queue.clear()

    def push_front(self,event:str) -> None:
        self.queue.appendleft(event)

    def push_back(self,event:str) -> None:
        self.queue.append(event)

    def pop(self) -> Optional[str]:
        return self.queue.popleft()

    def empty(self) -> bool:
        return len(self.queue) == 0

class EventLibrary:
    def __init__(self):
        self.library : Dict[str, Event] = {}

    def get_event(self,event_name:str) -> Optional[Event]:
        return self.library.get(event_name)

    def add_event(self,events:List[Event]) -> None:
        for event in events:
            self.library[event.name] = event

    def clear(self) -> None:
        self.library.clear()


def judge_condition(conditions:dict, player:GamePlayer) -> bool:
    is_son = conditions["is_son"]
    if is_son:
        return False
    if player.age < conditions["age_limit_min"] or player.age > conditions["age_limit_max"]:
        return False
    need = conditions["need_traits"]
    if not all(player.has_trait(t) for t in need):
        return False
    no_need = conditions["no_need_traits"]
    if any(player.has_trait(t) for t in no_need):
        return False
    return True


class EventPool:
    def __init__(self) -> None:
        self.pool : List[(str, int)] = []

    def clear(self) -> None:
        self.pool = []

    def add_event(self,events:List[(str, int)]) -> None:
        for event in events:
            if event not in self.pool:
                self.pool.append(event)

    def remove_event(self,events:List[(str, int)]) -> None:
        for event in events:
            if event in self.pool:
                self.pool.remove(event)

    def get_event(self) -> Optional[str]:
        if not self.pool:
            return None
        _, weights = zip(self.pool)
        random_result = random.choices(self.pool,weights=weights,k=1)[0]
        self.remove_event([random_result])
        return  random_result

    def update(self,event_library:EventLibrary,player:GamePlayer) -> None:
        for name, event in event_library.library.items():
            conditions = event.conditions
            if not judge_condition(conditions, player):
                self.remove_event([(name,event.weight)])
            else:
                self.add_event([(name,event.weight)])

class EventContainer:
    def __init__(self):
        self.event_pool = EventPool()
        self.event_library = EventLibrary()
        self.event_queue = EventQueue()

    def get_event_name(self) -> Optional[str]:
        if self.event_queue.empty():
            return self.event_pool.get_event()
        return self.event_queue.pop()

    def get_event(self,event_name:str) -> Optional[Event]:
        return self.event_library.get_event(event_name)
    def event(self) -> Event:
        return self.get_event(self.get_event_name())
    def clear_queue(self) -> None:
        self.event_queue.clear()
    def clear_library(self) -> None:
        self.event_library.clear()
    def clear_pool(self) -> None:
        self.event_pool.clear()
    def clear_all(self) -> None:
        self.clear_queue()
        self.clear_library()
        self.clear_pool()
    def update(self,player:GamePlayer) -> None:
        self.event_pool.update(self.event_library,player)