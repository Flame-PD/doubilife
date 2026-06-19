from typing import List,Optional,Dict
from dataclasses import dataclass

@dataclass
class MacroPlayer:
    name: str
    achievements: List[str]

@dataclass
class GamePlayer:
    name: str #本局游戏的名字
    sx: bool #性别，0为男，1为女
    traits: List[str] #特质列表
    flags: dict # 待实现的flag列表
    age: int #年龄
    def age_up(self,num) -> None: #年龄增长
        self.age += num
    def add_traits(self,traits_list: List[str]) -> None:
        """批量添加特质（自动去重，忽略已存在的）"""
        for t in traits_list:
            if t not in self.traits:
                self.traits.append(t)
    def remove_traits(self, traits_to_remove: List[str]) -> None:
        """批量移除特质（如果不存在则忽略）"""
        for t in traits_to_remove:
            if t in self.traits:
                self.traits.remove(t)
    def has_trait(self,trait) -> bool: #判断是否拥有某特质
        return trait in self.traits