from core.event import *
from core.condition import *
from core.loader import *
from core.event_container import *
from core.player import *
from blessed import Terminal
term = Terminal()

class Game:
    def __init__(self):
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
                    self.game_loop(input(term.green("请输入你的名字>")),(1 if input(term.green("请输入性别,0为男，1为女>")).strip()=="1" else 0))
                case _:
                    continue
    def game_init(self):
        self.event_container.clear_all()
        # result0_0=Result([
        #     {
        #         "conditions":{},
        #         "result_str":"你健康而响亮的哭声让大家都松了口气，产婆预言你将是个活泼好动的孩子。",
        #         "effect":{
        #             "add_traits":["活泼"]
        #         }
        #     }
        # ])
        # result0_1=Result([
        #     {
        #         "conditions":{},
        #         "result_str":"你的哭声很快安静下来，在大人们惊吓之余，你早已经睡得安详，不需要惊天动地，你安安静静地进入了你的角色。",
        #         "effect":{
        #             "add_traits":["安静"]
        #         }
        #     }
        # ])
        # option0_0=Option("大声哭闹",result0_0,{})
        # option0_1=Option("安稳睡觉",result0_1,{})
        # event0=Event("birth","你出生了","在一个风和日丽的雨天，随着一声清晰的啼哭划破雨夜，你出生在这个世界上",[option0_0,option0_1],{
        #     "age_limit_min":0,
        #     "age_limit_max":0,
        # },256)
        # event1=Event(
        #     name="urGood",
        #     title="你很活泼！",
        #     text="你现在拥有了活泼特质！你看到这条信息，说明事件的条件在正常运作！",
        #     conditions={
        #         "age_limit_min":1,
        #         "need_traits":["活泼"]
        #     },
        #     options=[
        #         Option(
        #             text="继续",
        #             result=Result(branches=[{
        #                 "conditions":{},
        #                 "result_str":"那么接下来会是一个子事件",
        #                 "effect":{
        #                     "sub_event":"urGood_sub",
        #                 }
        #             }]),
        #             conditions={}
        #         )
        #     ],
        #     weight=256
        # )
        # event2=Event(
        #     name="urGood_sub",
        #     title="活泼子事件！",
        #     text="如果你看到这条信息而不是死亡，说明子事件在正常运作！检查你的年龄是不是没有增长？这就对了！",
        #     conditions={"is_son":True},
        #     options=[
        #         Option(
        #             text="继续",
        #             result=Result(branches=[{
        #                 "conditions": {},
        #                 "result_str": "子事件测试结束！",
        #                 "effect": {}
        #             }]),
        #             conditions={}
        #         )
        #     ],
        #     weight=256
        # )
        # self.event_container.add_event([event0,event1,event2])
        loader = PackageLoader()
        events = loader.load_all()
        self.event_container.add_event(events)
        print(f"加载了 {len(events)} 个事件")
    def game_loop(self,player_name,player_sx):
        player = GamePlayer(player_name,player_sx,[],{},0)
        while True:
            if player.has_trait("死亡"):
                print(term.red("你的故事到此结束……"))
                break
            self.event_container.update(player)
            #ce = self.event_container.event()#ce = current_event
            print("库中事件：", list(self.event_container.event_library.library.keys()))
            self.event_container.update(player)
            print("池中事件：", self.event_container.event_pool.pool)
            ce = self.event_container.event()
            print("获取到的事件：", ce.name)
            print("%"+"="*(self.window_width-2)+"+")
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
            print(term.green("名字: ")+player_name+term.yellow("  年龄: ")+f"{player.age}"+term.cyan("  性别: ")+("女" if player.sx else "男"))
            for trait in player.traits:
                print("["+term.bold_cyan(trait)+"]",end=(" "*(9-len(trait))))
            print("")
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

