from core.event import *
from core.event_container import *
from core.player import *
from blessed import Terminal
term = Terminal()

class Game:
    def __init__(self):
        self.player = GamePlayer("玩家1", ["活着", "没死"], {}, 0)
        self.event_container = EventContainer()
        self.window_width = term.width
        self.window_height = term.height
    def main_menu(self):
        while True:
            print(term.green("我的逗比人生"))
            print("1>开始游戏")
            print("2>待扩展")
            num_input=input(term.green(">"))
            match int(num_input):
                case 1:
                    self.game_init()
                    self.game_loop(input(term.green("请输入你的名字>")))
                case _:
                    continue
    def game_init(self):
        self.event_container.clear_all()

    def game_loop(self,player_name):
        player = GamePlayer(player_name,[],{},0)
        while True:
            self.event_container.update(player)
            ce = self.event_container.event()#ce = current_event

            print("+"+"-"*(self.window_width-2)+"+")
            print(term.bold_yellow(ce.title))
            print(ce.text)
            available_options = []
            option_id = 0
            for option in ce.options:
                if not option.if_option(player):
                    continue
                available_options.append(option)
                text = option.text
                option_id += 1
                match option_id % 4:
                    case 1:
                        print(f"{option_id}. {term.green(text)}")
                    case 2:
                        print(f"{option_id}. {term.yellow(text)}")
                    case 3:
                        print(f"{option_id}. {term.cyan(text)}")
                    case _:
                        print(f"{option_id}. {term.magenta(text)}")
            print("%" + "="*(self.window_width-2) + "%")
            print(term.green("名字: ")+player_name+term.yellow("年龄: ")+player.age)
            for trait in player.traits:
                print("["+term.bold_cyan(trait)+"]",end=(" "*(5-len(trait))))
            while True:
                choice = input(term.green(">"))
                if choice.isdigit() and 0 < int(choice) <= option_id:
                    break
            choice_option = available_options[int(choice)-1]
            ce.choose_option(choice_option,player)
            print(ce.result_option.result_str)
            ce.apply_effect(player,self.event_container.event_queue)
            ce.add_event(self.event_container.event_queue)
            term.inkey()
            if self.event_container.event_queue.empty():
                player.age_up(1)







    def start(self):
        print(term.green("我的逗比人生")+ term.yellow("personal-remake")+ term.cyan("v0.0.1"))
        print("请按任意键继续...>")
        with term.cbreak():
            term.inkey()
        self.main_menu()

