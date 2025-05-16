from dataclasses import dataclass
from decimal import Decimal
import json
import helper
from typing import *


@dataclass
class GroupByResult:
    attribute: str
    attribute_value: str
    value: 'Timeline'


class Timeline:
    def __init__(self):
        self.value_dict: dict[Decimal, Any] = {}

    @classmethod
    def load_file(cls, path):
        with open(path, 'r') as f:
            timeline_dict = json.loads(f.read())
        return Timeline.load_dict(timeline_dict)

    @classmethod
    def load_dict(cls, data: dict):
        timeline = Timeline.from_json(data)
        timeline.__validate()
        return timeline

    @classmethod
    def from_json(cls, json_data: Dict):
        timeline = cls()
        for timestamp, data in json_data.items():
            second = helper.timestamp_to_second(timestamp)
            timeline.value_dict[second] = data
        return timeline

    # @classmethod
    # def load(cls, json_data: str):
    #     timeline = cls.from_json(json.loads(json_data))
    #     timeline.__validate()
    #     return timeline

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Timeline):
            return self.value_dict == other.value_dict
        return False

    def __len__(self):
        return len(self.value_dict)

    def __validate(self):
        pass

    def __iter__(self):
        return iter(self.value_dict)

    def __getitem__(self, item):
        ffill_data = {}
        for second in sorted(self.value_dict.keys()):
            if second <= item:
                ffill_data.update(self.value_dict[second])

        return ffill_data

    def to_dict(self) -> dict:
        result = {}
        for second in self:
            timestamp = helper.second_to_timestamp(second)
            result[timestamp] = self[second]
        return result

    def duration(self) -> Decimal:
        if not self.value_dict:
            return 0
        return list(self.value_dict.keys())[-1]  # TODO sort

    def skip(self, percentage):
        duration = self.duration()
        start_second = round(Decimal(duration * (percentage / 100)), 4)
        end_second = duration
        return (start_second, end_second,
                self.extract(start_second, end_second,
                             _force_edges=True,
                             rebase_zero=True))

    def split(self, parts: int):
        duration = self.duration()
        part_duration = round(duration / parts, 4)
        results = []
        for i in range(parts):
            start_second = i * part_duration
            end_second = (i + 1) * part_duration
            results.append(
                (start_second, end_second,
                 self.extract(start_second, end_second,
                              _force_edges=True,
                              rebase_zero=True)))
        return results

    def split_by_attribute(self, attribute: str, value, force_edges=True, rebase_zero=True):
        self.extract_by_attribute(attribute, value, force_edges, rebase_zero)
        pass

    def extract_by_attribute(self, attribute: str, value, force_edges=True, rebase_zero=True):
        return self.extract_by_attribute_exp(
            attribute=attribute,
            comparison_func=lambda x: x == value,
            force_edges=force_edges,
            rebase_zero=rebase_zero
        )

    def extract_by_attribute_exp(self, attribute: str, comparison_func, force_edges=True, rebase_zero=True):
        result = []
        start_second = None
        end_second = None
        for second in self.value_dict:
            if attribute in self[second]:
                v = self[second][attribute]
                if comparison_func(v):
                    if not start_second:
                        start_second = second
                    end_second = second
                else:
                    if start_second is not None:
                        result.append(
                            self.extract(start_second, end_second, _force_edges=force_edges, rebase_zero=rebase_zero))
                        start_second = None
                        end_second = None

        if start_second and end_second:
            result.append(self.extract(start_second, end_second, _force_edges=force_edges, rebase_zero=rebase_zero))

        return result

    def insert_marker(self, name, value, second):
        if second in self.value_dict:
            if f'marker_{name}' in self.value_dict[second]:
                self.value_dict[second][f'marker_{name}'] = value
            self.value_dict[second] = {f'marker_{name}': value}
        else:
            self.value_dict[second] = {f'marker_{name}': value}

    @classmethod
    def append(cls, timelines):
        result = cls()
        index = 0
        for timeline in timelines:
            if index == 0:
                for second in timeline:
                    result.value_dict[second] = timeline[second]
            else:
                rebased_timeline = timeline.rebase(timelines[index - 1].duration())
                for second in rebased_timeline:
                    result.value_dict[second] = rebased_timeline[second]
            index += 1
        return result

    def rebase(self, base):
        result = Timeline()
        min_second = min(self.value_dict.keys())
        delta = min_second - base
        for second in self.value_dict:
            rebased_second = second - delta
            result.value_dict[rebased_second] = self[second]
        return result

    def extract(self, start, end, *, _force_edges=True, rebase_zero=True):
        result = Timeline()
        if _force_edges:
            if not result[start]:
                result.value_dict[start] = self[self._get_key_before(start)]
        for second in self.value_dict:
            if start <= second <= end:
                result.value_dict[second] = self[second]
        if _force_edges:
            if end not in result:
                result.value_dict[end] = self[self._get_key_before(end)]

        if start != 0 and rebase_zero:
            result = result.rebase(0)

        return result

    def group_by(self, attribute: str) -> List[GroupByResult]:
        result: List[GroupByResult] = []
        prev_value = None
        for second in self.value_dict:
            if attribute in self.value_dict[second]:
                if self.value_dict[second][attribute] != prev_value:
                    result_item = GroupByResult()
                    result_item.attribute = attribute
                    result_item.attribute_value = self.value_dict[second][attribute]
                    result_item.value = Timeline()
                    result.append(result_item)
                    prev_value = self.value_dict[second][attribute]
                result[-1].value.value_dict[second] = self.value_dict[second]
        return result

    def _get_key_before(self, second):
        if second in self.value_dict:
            return second
        else:
            for _ in reversed(self.value_dict):
                if _ < second:
                    return _
