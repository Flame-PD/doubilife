from typing import List,Optional,Dict
from dataclasses import dataclass

@dataclass
class MacroPlayer:
    name: str
    achievements: List[str]

@dataclass
class GamePlayer:
    name: str
    traits: List[str]
    flags: dict
    age: int
    def age_up(self,num) -> None:
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
    def has_trait(self,trait) -> bool:
        return trait in self.traits