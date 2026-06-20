from core.player import *
import random

# condition 格式说明
# {
#   "age_limit_min":int 年龄下限
#   "age_limit_max": int 年龄上限
#   "need_traits": List[str] ["需要的特质"],
#   "no_need_traits": List[str] ["不能有的特质"],
#   "need_sx": bool 性别
#   "is_son": true or false 如果是子事件，就不能直接加入事件池
# }


def judge_condition(conditions:dict, player:GamePlayer) -> bool:
    if "is_son" in conditions:
        is_son = conditions["is_son"]
        if is_son:
            return False
    if "need_sx" in conditions:
        if conditions["need_sx"] != player.sx:
            return False
    if "age_limit_min" in conditions:
        if player.age < conditions["age_limit_min"]:
            return False
    if "age_limit_max" in conditions:
        if player.age > conditions["age_limit_max"]:
            return False
    if "need_traits" in conditions:
        need = conditions["need_traits"]
        if not all(player.has_trait(t) for t in need):
            return False
    if "no_need_traits" in conditions:
        no_need = conditions["no_need_traits"]
        if any(player.has_trait(t) for t in no_need):
            return False
    if "probability" in conditions:
        x_prob = random.randint(0,100)
        if x_prob > conditions["probability"]:
            return False
    return True
