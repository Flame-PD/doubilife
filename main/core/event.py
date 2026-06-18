from dataclasses import dataclass
from typing import List,Optional

# effect 格式说明：effect是一个字典，记录某个选项会带来的影响
# {
#   "add_traits": ["特质1", "特质2"],   获得新特质
#   "remove_traits": ["特质3"],         失去某特质
#   "age_up": 3,            可选，增加年龄，但实际上我也没想好这玩意有什么用
#   "set_flags": {"key": True}, 可以作为某个全局flag的修改，暂未实现
#   "sub_event": "事件ID" 这个选项会指向的子事件id
# }

# branch 格式说明：branch是一个字典，用来判断某个选项根据不同的特质会引发不同的结果
# {
#   "need_traits": ["需要的特质"],
#   "no_need_traits": ["不能有的特质"],
#   "flag"
#   "result_str": "会返回的文本",
#   "effect": {effect参照上述格式}
# }

#condition 格式说明
#{
#   "age_limit_min" :年龄下限
#   "age_limit_max": 年龄上限
#   "need_traits": ["需要的特质"],
#   "no_need_traits": ["不能有的特质"],
#   "is_son": true or false 如果是子事件，就不能直接加入事件池
#}

@dataclass
class Result:
    branches: List[dict]
    def judge(self,player):
        for branch in self.branches:
            need = branch["need_traits"]
            if not all(player.has_trait(t) for t in need):
                continue
            no_need=branch["no_need_traits"]
            if any(player.has_trait(t) for t in no_need):
                continue

            return branch.get("result_str",""),branch.get("effect",{})
        return None,None



@dataclass
class Option: #选项类
    text: str #这个选项的文本
    result: Result #结果类，需要判定，判断方法在result内
    result_str: str
    effect: dict
    need_traits:List[str]=None
    no_need_traits:List[str]=None
    sub_event:Optional[str]=None
    def if_option(self,player) -> bool:
        if not all(player.has_trait(t) for t in self.need_traits):
            return False
        if any(player.has_trait(t) for t in self.no_need_traits):
            return False
        return True
    def get_result(self,player):
        self.result_str,self.effect = self.result.judge(player)

class Event:
    """事件类定义"""
    def __init__(self,
                 name: str,
                 title: str,
                 text: str,
                 options: List[Option],
                 effect: dict,
                 sub_event: str,
                 conditions: dict,
                 weight,
                 result_option: Option
                 ):
        self.name = name
        self.title = title
        self.text = text
        self.options = options
        self.effect = effect
        self.sub_event = sub_event
        self.conditions = conditions
        self.weight = weight
        self.result_option = result_option
    def choose_option(self,option,player):
        self.result_option = option
        self.result_option.get_result(player)
        self.effect = self.result_option.effect
    def apply_effect(self,player,events_queue):
        if "add_traits" in self.effect:
            player.add_traits(self.effect["add_traits"])
            print(f"获得特质:{self.effect["add_traits"]}")
        if "remove_traits" in self.effect:
            player.remove_traits(self.effect["remove_traits"])
            print(f"失去特质:{self.effect["remove_traits"]}")
        if "age_up" in self.effect:
            player.age_up(self.effect["age_up"])
            print(f"成长了: {self.effect["age_up"]} 岁")
        # if "set_flags" in self.effect:
        #     player.set_flags(self.effect["set_flags"])
        if "sub_event" in self.effect:
            events_queue.push_front(self.effect["sub_event"])
    def add_event(self,events_queue) -> bool:
        if self.sub_event is not None:
            events_queue.push_back(self.sub_event)
            return True
        return False