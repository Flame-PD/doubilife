from core.event import *
from core.player import GamePlayer
from core.condition import *
from collections import deque
from typing import Dict, List, Optional
import random

death = Event(
    name = "death",
    title = "意料之外的结局",
    text = """恭喜你，你触摸到了这个游戏的边界，出于各种各样的原因，你已经没办法再继续游戏了，这通常是因为没有合法的事件了。
为了这个世界，天意的大手发力了，一辆面包车停在你家门口，车上跳下来十个大汉，你被一群自称游戏管理员的蒙面大汉乱棍打死了。死得很惨。
如果你正在测试你的事件，这个事件是因为返回事件时出错，例如当前事件池内没有任何可以执行的事件了，请检查你的事件池是否为空，检查事件的条件是否有误（比如说永远无法实现，例如最小年龄大于最大年龄），也有可能是你指向了一个不存在的事件""",
    conditions={

    },
    options =[
        Option("回到主菜单",
            result = Result(
                branches = [
                {
                    "conditions" : {},
                    "effect" : {
                        "add_traits" : ["死亡"]
                    }
                }
            ]),
            conditions = {}
        )
    ],
    weight = 9999
)

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
            if event.name not in self.library:
                self.library[event.name] = event
    def remove_event(self,event_name:str) -> None:
        self.library.pop(event_name)
    def clear(self) -> None:
        self.library.clear()





class EventPool:
    def __init__(self) -> None:
        self.pool : List[tuple[str, int]] = []

    def clear(self) -> None:
        self.pool = []

    def add_event(self,events:List[tuple[str, int]]) -> None:
        for event in events:
            if event not in self.pool:
                self.pool.append(event)

    def remove_event(self,events:List[tuple[str, int]]) -> None:
        for event in events:
            if event in self.pool:
                self.pool.remove(event)

    def get_event(self) -> Optional[str]:
        if not self.pool:
            return None
        _, weights = zip(*self.pool)
        random_result = random.choices(self.pool,weights=weights,k=1)[0]
        self.remove_event([random_result])
        return  random_result[0]

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
    def remove_event(self,event_name:str) -> None:
        self.event_library.remove_event(event_name)
    def event(self) -> Event:
        return_event = self.get_event(self.get_event_name())
        if return_event is None:
            return_event = self.get_event(self.get_event_name())
            if return_event is None:
                return death
            return return_event
        return return_event
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
    def add_event(self,events:List[Event]) -> None:
        self.event_library.add_event(events)