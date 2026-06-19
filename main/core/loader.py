import json
import yaml
import os
from typing import List, Dict, Any
from core.event import Event, Option, Result

class PackageLoader:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.packages_dir = os.path.join(data_dir, "packages")
        self.config_path = os.path.join(data_dir, "config.yml")

    def load_all(self) -> List[Event]:
        # 1. 读 config.yml，拿到要加载的包名列表
        package_ids = self._read_config()
        all_events = []

        for pid in package_ids:
            # 2. 读每个包的 packages.yml，拿到事件文件路径
            meta = self._read_package_meta(pid)
            if meta is None:
                continue

            events_file = meta.get("events_file", "events.json")
            events_path = os.path.join(self.packages_dir, pid, events_file)

            # 3. 读事件的 JSON 文件，解析成 Event 对象
            events = self._parse_events_file(events_path)
            all_events.extend(events)

        return all_events

    def _read_config(self) -> List[str]:
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config.get("packages", [])

    def _read_package_meta(self, package_id: str) -> Dict:
        path = os.path.join(self.packages_dir, package_id, "package.yml")
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def _parse_events_file(self, path: str) -> List[Event]:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        events = []
        for event_id, raw in data.items():
            events.append(self._parse_event(event_id, raw))
        return events

    def _parse_event(self, event_id: str, raw: Dict) -> Event:
        options = []
        for opt_raw in raw.get("options", []):
            result_raw = opt_raw.get("result", {})
            result = Result(branches=result_raw.get("branches", []))
            option = Option(
                text=opt_raw["text"],
                result=result,
                conditions=opt_raw.get("conditions", {})
            )
            options.append(option)

        return Event(
            name=raw.get("name", event_id),
            title=raw.get("title", ""),
            text=raw.get("text", ""),
            options=options,
            conditions=raw.get("conditions", {}),
            weight=raw.get("weight", 1)
        )