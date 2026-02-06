from bisect import bisect_right, insort_left
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Callable, Dict, List, Optional, Iterator
import json

try:
    from . import helper
except ImportError:
    import helper  # fallback for running standalone


@dataclass
class GroupByResult:
    attribute: str = ""
    attribute_value: Any = ""
    value: 'Timeline' = field(default_factory=lambda: Timeline())


class Timeline:
    """
    A timeline data structure for time-based structured data with forward-fill semantics.

    Internally maintains sorted keys for O(log n) lookups and insertions.
    Values at any point in time are computed by forward-filling from all
    previous timestamps.
    """

    def __init__(self):
        self._data: Dict[Decimal, Dict[str, Any]] = {}
        self._sorted_keys: List[Decimal] = []

    @property
    def value_dict(self) -> Dict[Decimal, Any]:
        """Expose internal data for backwards compatibility."""
        return self._data

    @value_dict.setter
    def value_dict(self, value: Dict[Decimal, Any]):
        """Set internal data and rebuild sorted keys."""
        self._data = value
        self._sorted_keys = sorted(self._data.keys())

    def _insert_key(self, key: Decimal) -> None:
        """Insert a key maintaining sorted order. O(log n) search + O(n) insert."""
        if key not in self._data:
            insort_left(self._sorted_keys, key)

    def _remove_key(self, key: Decimal) -> None:
        """Remove a key from sorted keys list."""
        if key in self._data:
            idx = bisect_right(self._sorted_keys, key) - 1
            if idx >= 0 and self._sorted_keys[idx] == key:
                self._sorted_keys.pop(idx)

    @classmethod
    def load_file(cls, path: str) -> 'Timeline':
        with open(path, 'r') as f:
            timeline_dict = json.loads(f.read())
        return cls.load_dict(timeline_dict)

    @classmethod
    def load_dict(cls, data: Dict[str, Any]) -> 'Timeline':
        timeline = cls.from_json(data)
        timeline._validate()
        return timeline

    @classmethod
    def from_json(cls, json_data: Dict[str, Any]) -> 'Timeline':
        timeline = cls()
        for timestamp, data in json_data.items():
            second = helper.timestamp_to_second(timestamp)
            timeline._data[second] = data
        timeline._sorted_keys = sorted(timeline._data.keys())
        return timeline

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Timeline):
            return self._data == other._data
        return False

    def __len__(self) -> int:
        return len(self._data)

    def __contains__(self, key: Decimal) -> bool:
        return key in self._data

    def _validate(self) -> None:
        """Validate timeline data. Override in subclasses for custom validation."""
        pass

    def __iter__(self) -> Iterator[Decimal]:
        """Iterate over timestamps in sorted order."""
        return iter(self._sorted_keys)

    def __getitem__(self, timestamp) -> Dict[str, Any]:
        """
        Get the cumulative state at a given timestamp using forward-fill.

        Uses binary search for O(log n) key lookup, then O(k) to merge
        k entries up to that point.
        """
        if not self._sorted_keys:
            return {}

        # Convert to Decimal for consistent comparison
        if not isinstance(timestamp, Decimal):
            timestamp = Decimal(str(timestamp))

        # Find the rightmost key <= timestamp
        idx = bisect_right(self._sorted_keys, timestamp)

        # Merge all values from start up to idx
        ffill_data: Dict[str, Any] = {}
        for i in range(idx):
            key = self._sorted_keys[i]
            ffill_data.update(self._data[key])

        return ffill_data

    def __repr__(self) -> str:
        if not self._data:
            return "Timeline(empty)"
        return f"Timeline(entries={len(self._data)}, duration={self.duration()})"

    def to_dict(self) -> Dict[str, Dict[str, Any]]:
        """Convert timeline to a dictionary with timestamp strings as keys."""
        result = {}
        for second in self._sorted_keys:
            timestamp = helper.second_to_timestamp(second)
            result[timestamp] = self[second]
        return result

    def duration(self) -> Decimal:
        """Return the timestamp of the last entry, or 0 if empty."""
        if not self._sorted_keys:
            return Decimal(0)
        return self._sorted_keys[-1]

    def skip(self, percentage: float) -> tuple[Decimal, Decimal, 'Timeline']:
        """
        Skip a percentage of the timeline from the beginning.

        Returns a tuple of (start_second, end_second, extracted_timeline).
        """
        dur = self.duration()
        start_second = round(Decimal(dur * Decimal(percentage) / 100), 4)
        end_second = dur
        return (start_second, end_second,
                self.extract(start_second, end_second,
                             _force_edges=True,
                             rebase_zero=True))

    def split(self, parts: int) -> List[tuple[Decimal, Decimal, 'Timeline']]:
        """
        Split the timeline into equal parts.

        Returns a list of tuples (start_second, end_second, timeline_part).
        """
        dur = self.duration()
        part_duration = round(dur / parts, 4)
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

    def extract_by_attribute(
        self,
        attribute: str,
        value: Any,
        force_edges: bool = True,
        rebase_zero: bool = True
    ) -> List['Timeline']:
        """Extract segments where an attribute equals a specific value."""
        return self.extract_by_attribute_exp(
            attribute=attribute,
            comparison_func=lambda x: x == value,
            force_edges=force_edges,
            rebase_zero=rebase_zero
        )

    def extract_by_attribute_exp(
        self,
        attribute: str,
        comparison_func: Callable[[Any], bool],
        force_edges: bool = True,
        rebase_zero: bool = True
    ) -> List['Timeline']:
        """
        Extract segments where an attribute satisfies a comparison function.

        Returns a list of Timeline objects for each contiguous segment
        where the comparison function returns True.
        """
        result: List[Timeline] = []
        start_second: Optional[Decimal] = None
        end_second: Optional[Decimal] = None

        for second in self._sorted_keys:
            cumulative = self[second]
            if attribute in cumulative:
                v = cumulative[attribute]
                if comparison_func(v):
                    if start_second is None:
                        start_second = second
                    end_second = second
                else:
                    if start_second is not None and end_second is not None:
                        result.append(
                            self.extract(start_second, end_second,
                                        _force_edges=force_edges,
                                        rebase_zero=rebase_zero))
                        start_second = None
                        end_second = None

        if start_second is not None and end_second is not None:
            result.append(
                self.extract(start_second, end_second,
                            _force_edges=force_edges,
                            rebase_zero=rebase_zero))

        return result

    def set(self, second: Decimal, data: Dict[str, Any]) -> None:
        """
        Set or update data at a specific timestamp.

        If the timestamp already exists, the data is merged with existing data.
        """
        if second in self._data:
            self._data[second].update(data)
        else:
            self._insert_key(second)
            self._data[second] = data.copy()

    def insert_marker(self, name: str, value: Any, second: Decimal) -> None:
        """
        Insert a marker at an existing timestamp.

        Markers are stored with a 'marker_' prefix and added to the existing
        data at the timestamp.

        Args:
            name: Marker name (will be prefixed with 'marker_')
            value: Marker value
            second: Timestamp that must already exist in the timeline

        Raises:
            KeyError: If the timestamp does not exist in the timeline
        """
        # Convert to Decimal for consistent comparison
        if not isinstance(second, Decimal):
            second = Decimal(str(second))

        if second not in self._data:
            raise KeyError(f"Timestamp {second} does not exist in timeline")

        marker_key = f'marker_{name}'
        self._data[second][marker_key] = value

    @classmethod
    def append(cls, timelines: List['Timeline']) -> 'Timeline':
        """
        Concatenate multiple timelines sequentially.

        Each timeline is rebased to start after the previous one ends.
        """
        result = cls()
        cumulative_duration = Decimal(0)

        for i, timeline in enumerate(timelines):
            if i == 0:
                for second in timeline._sorted_keys:
                    result._data[second] = timeline[second]
                cumulative_duration = timeline.duration()
            else:
                rebased_timeline = timeline.rebase(cumulative_duration)
                for second in rebased_timeline._sorted_keys:
                    result._data[second] = rebased_timeline[second]
                cumulative_duration += timeline.duration()

        result._sorted_keys = sorted(result._data.keys())
        return result

    def rebase(self, base: Decimal) -> 'Timeline':
        """
        Shift all timestamps so the minimum timestamp becomes the given base.

        Returns a new Timeline with rebased timestamps.
        """
        result = Timeline()
        if not self._sorted_keys:
            return result

        min_second = self._sorted_keys[0]
        delta = min_second - base

        for second in self._sorted_keys:
            rebased_second = second - delta
            result._data[rebased_second] = self[second]

        result._sorted_keys = sorted(result._data.keys())
        return result

    def extract(
        self,
        start,
        end,
        *,
        _force_edges: bool = True,
        rebase_zero: bool = True
    ) -> 'Timeline':
        """
        Extract a portion of the timeline between start and end timestamps.

        Args:
            start: Start timestamp (inclusive) - will be converted to Decimal
            end: End timestamp (inclusive) - will be converted to Decimal
            _force_edges: If True, ensure data exists at start and end points
            rebase_zero: If True and start != 0, shift timestamps so start becomes 0

        Returns:
            A new Timeline containing the extracted portion.
        """
        # Convert to Decimal for consistent handling
        start = Decimal(str(start)) if not isinstance(start, Decimal) else start
        end = Decimal(str(end)) if not isinstance(end, Decimal) else end

        result = Timeline()

        if _force_edges:
            # Ensure we have data at the start edge
            key_before_start = self._get_key_before(start)
            if key_before_start is not None:
                result._data[start] = self[key_before_start]
                result._sorted_keys.append(start)

        # Copy all entries within the range
        for second in self._sorted_keys:
            if start <= second <= end:
                if second not in result._data:  # Don't overwrite forced edge
                    result._data[second] = self[second]
                    if second not in result._sorted_keys:
                        insort_left(result._sorted_keys, second)

        if _force_edges:
            # Ensure we have data at the end edge
            if end not in result._data:
                key_before_end = self._get_key_before(end)
                if key_before_end is not None:
                    result._data[end] = self[key_before_end]
                    insort_left(result._sorted_keys, end)

        if start != 0 and rebase_zero:
            result = result.rebase(Decimal(0))

        return result

    def group_by(self, attribute: str) -> List[GroupByResult]:
        """
        Group timeline entries by changes in an attribute value.

        Returns a list of GroupByResult objects, each containing entries
        where the attribute has the same value.
        """
        result: List[GroupByResult] = []
        prev_value = None

        for second in self._sorted_keys:
            if attribute in self._data[second]:
                current_value = self._data[second][attribute]
                if current_value != prev_value:
                    result_item = GroupByResult(
                        attribute=attribute,
                        attribute_value=current_value,
                        value=Timeline()
                    )
                    result.append(result_item)
                    prev_value = current_value
                result[-1].value._data[second] = self._data[second]
                insort_left(result[-1].value._sorted_keys, second)

        return result

    def _get_key_before(self, second) -> Optional[Decimal]:
        """
        Get the largest key that is less than or equal to the given second.

        Returns None if no such key exists.
        """
        if not self._sorted_keys:
            return None

        # Convert to Decimal for consistent comparison
        if not isinstance(second, Decimal):
            second = Decimal(str(second))

        if second in self._data:
            return second

        idx = bisect_right(self._sorted_keys, second)
        if idx > 0:
            return self._sorted_keys[idx - 1]

        return None
