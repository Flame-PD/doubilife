from dataclasses import dataclass,field
from typing import List,Optional

from core.condition import judge_condition


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
#   "conditions": {condition字典}
#   "result_str": "会返回的文本",
#   "effect": {effect参照上述格式}
# }

#condition 格式说明
#{
#   "age_limit_min" :年龄下限
#   "age_limit_max": 年龄上限
#   "need_traits": ["需要的特质"],
#   "no_need_traits": ["不能有的特质"],
#   "need_sx": bool 性别
#   "is_son": true or false 如果是子事件，就不能直接加入事件池，只用在事件管理
#}

@dataclass
class Result:
    branches: List[dict]
    def judge(self,player) -> tuple[str,dict]:
        for branch in self.branches:
            conditions = branch["conditions"]
            if judge_condition(conditions, player):
                return branch.get("result_str",""),branch.get("effect",{})
        return "", {}



@dataclass
class Option: #选项类
    text: str #这个选项的文本
    result: Result #结果类，需要判定，判断方法在result内
    conditions: dict = None
    sub_event:Optional[str]=None
    result_str: str=""
    effect: dict= field(default_factory=dict)
    def if_option(self,player) -> bool:
        if not judge_condition(self.conditions, player):
            return False
        return True
    def get_result(self,player) -> None:
        self.result_str,self.effect = self.result.judge(player)

class Event:
    """事件类定义"""
    def __init__(self,
                 name: str, #事件名，类id性质，用于在事件集中以名字作为唯一对应
                 title: str, #事件标题
                 text: str, #事件内容
                 options: List[Option], #是一个选项集，选项构成参照以上
                 conditions: dict, #条件字典，格式参考如上
                 weight, #
                 sub_event: str = None, #子事件，默认为无，你可以在这里添加子事件的事件名
                 result_option: Option = None, #选择的选项
                 effect: dict = None, #效果
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
            has_add=player.add_traits(self.effect["add_traits"])
            print(f"获得特质:{has_add}")
        if "remove_traits" in self.effect:
            has_remove=player.remove_traits(self.effect["remove_traits"])
            print(f"失去特质:{has_remove}")
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