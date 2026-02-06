import pytest
import decimal
import os

from timeline.timeline import Timeline
from testdata import video_annotations_timeline_dicts

# Get the directory containing the tests
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(TEST_DIR)


def D(value) -> decimal.Decimal:
    return round(decimal.Decimal(value), 4)


def test_load_file_converts_timestamps_to_seconds():
    timeline = Timeline.load_file(os.path.join(PROJECT_ROOT, 'testdata/video_annotations_timeline.json'))
    assert timeline.value_dict[0.0] == {
        'RoomType': 'EntranceHall', 'Quality': 100}
    assert timeline.value_dict[D(1.69)] == {'InterestValue': 100}
    assert timeline.value_dict[D(4.47)] == {
        'RoomType': 'SittingArea', 'Quality': 100}
    assert timeline.value_dict[D(6.94)] == {'InterestValue': 100}
    assert timeline.value_dict[D(13.65)] == {
        'RoomType': 'Dining Area', 'Quality': 100}
    assert timeline.value_dict[D(14.92)] == {'InterestValue': 100}
    assert timeline.value_dict[D(26.59)] == {'InterestValue': 100}
    assert timeline.value_dict[D(31.2)] == {'InterestValue': 100}
    assert timeline.value_dict[D(36.31)] == {
        'RoomType': 'Kitchen', 'Quality': 100}
    assert timeline.value_dict[D(43.67)] == {'InterestValue': 100}
    assert timeline.value_dict[D(52.44)] == {
        'RoomType': 'LivingRoom', 'Quality': 100}
    assert timeline.value_dict[D(55.67)] == {'InterestValue': 100}
    assert timeline.value_dict[D(62.12)] == {
        'RoomType': 'EntranceHall2', 'Quality': 100}
    assert timeline.value_dict[D(66.89)] == {'RoomType': 'Hall', 'Quality': 100}
    assert timeline.value_dict[D(72.03)] == {'RoomType': 'Toilet', 'Quality': 100}
    assert timeline.value_dict[D(72.031)] == {'InterestValue': 100}
    assert timeline.value_dict[D(75.02)] == {'RoomType': 'Hall2', 'Quality': 100}
    assert timeline.value_dict[D(79.17)] == {
        'RoomType': 'Bedroom1', 'Quality': 100}
    assert timeline.value_dict[D(82.43)] == {'InterestValue': 100}
    assert timeline.value_dict[D(91.83)] == {
        'RoomType': 'Bedroom2', 'Quality': 100}
    assert timeline.value_dict[D(95.3)] == {'InterestValue': 100}
    assert timeline.value_dict[D(103.99)] == {
        'RoomType': 'Bathroom', 'Quality': 100}
    assert timeline.value_dict[D(107.88)] == {'InterestValue': 100}
    assert timeline.value_dict[D(115.46)] == {
        'RoomType': 'Bedroom3', 'Quality': 100}
    assert timeline.value_dict[D(118.91)] == {'InterestValue': 100}
    assert timeline.value_dict[D(124.86)] == {'InterestValue': 100}
    assert timeline.value_dict[D(129.6)] == {'RoomType': 'Hall3', 'Quality': 100}
    assert timeline.value_dict[D(136.25)] == {
        'RoomType': 'EntranceHall3', 'Quality': 100}
    assert timeline.value_dict[D(139.68)] == {'InterestValue': 100}
    assert timeline.value_dict[D(142.81)] == {
        'RoomType': 'Stairs', 'Quality': 100}
    assert timeline.value_dict[D(150.21)] == {
        'RoomType': 'NightHall', 'Quality': 100}
    assert timeline.value_dict[D(156.3)] == {'InterestValue': 100}
    assert timeline.value_dict[D(162.75)] == {
        'RoomType': 'Bedroom4', 'Quality': 100}
    assert timeline.value_dict[D(167.89)] == {'InterestValue': 100}
    assert timeline.value_dict[D(173.73)] == {
        'RoomType': 'NightHall2', 'Quality': 100}
    assert timeline.value_dict[D(178.59)] == {
        'RoomType': 'Dressing', 'Quality': 100}
    assert timeline.value_dict[D(183.85)] == {'InterestValue': 100}
    assert timeline.value_dict[D(193.24)] == {
        'RoomType': 'NightHall3', 'Quality': 100}
    assert timeline.value_dict[D(197.9)] == {'InterestValue': 100}
    assert timeline.value_dict[D(202.0)] == {'EOF': 'True'}


def test_load_dict():
    timeline = Timeline.load_dict(video_annotations_timeline_dicts.timeline_1)
    assert timeline.value_dict[0.0] == {
        'RoomType': 'LivingRoom', 'Quality': 100, 'InterestValue': 58}
    assert timeline.value_dict[1.0] == {'InterestValue': 72}
    assert timeline.value_dict[2.0] == {
        'InterestValue': 63, 'Quality': 50}
    assert timeline.value_dict[3.0] == {'InterestValue': 89}
    assert timeline.value_dict[4.0] == {'InterestValue': 94}
    assert timeline.value_dict[5.0] == {
        'RoomType': 'Kitchen', 'Quality': 100, 'InterestValue': 58}
    assert timeline.value_dict[6.0] == {'InterestValue': 72}
    assert timeline.value_dict[7.0] == {
        'InterestValue': 63, 'Quality': 50}
    assert timeline.value_dict[8.0] == {'InterestValue': 94}


def test_timeline_duration():
    timeline = Timeline.load_dict(video_annotations_timeline_dicts.timeline_1)
    assert timeline.duration() == 8


def test_iterate():
    timeline = Timeline.load_dict(video_annotations_timeline_dicts.timeline_1)
    index = 0
    for item in timeline:
        assert item == index
        index += 1


def test_ffill_values_carry_forward():
    timeline_value1 = {
        "RoomType": "LivingRoom",
        "Quality": 100,
        "InterestValue": 58
    }
    timeline_value2 = {
        "RoomType": "LivingRoom",
        "Quality": 100,
        "InterestValue": 72
    }

    timeline_data = {
        "00:00:00.000": timeline_value1,
        "00:00:01.000": timeline_value2
    }

    timeline = Timeline.load_dict(timeline_data)
    assert timeline[0.1] == timeline_value1
    assert timeline[0.2] == timeline_value1
    assert timeline[0.3] == timeline_value1
    assert timeline[0.4] == timeline_value1
    assert timeline[0.5] == timeline_value1
    assert timeline[0.6] == timeline_value1
    assert timeline[0.7] == timeline_value1
    assert timeline[0.8] == timeline_value1
    assert timeline[0.9] == timeline_value1
    assert timeline[0.99] == timeline_value1
    assert timeline[1.0] == timeline_value2
    assert timeline[1.1] == timeline_value2
    assert timeline[1000] == timeline_value2


def test_ffill_omitted_values_carry_forward():
    timeline_data = {
        "00:00:00.000": {
            "RoomType": "LivingRoom",
        },
        "00:00:01.000": {
            "Lighting": 72
        },
        "00:00:03.000": {
            "RoomType": "Kitchen",
        }
    }
    timeline = Timeline.load_dict(timeline_data)

    assert timeline[0]["RoomType"] == "LivingRoom"
    assert timeline[1]["RoomType"] == "LivingRoom"
    assert timeline[2]["RoomType"] == "LivingRoom"
    assert timeline[3]["RoomType"] == "Kitchen"


def test_ffill_starts_from_first_defined_value():
    timeline_data = {
        "00:00:00.000": {
            "RoomType": "LivingRoom",
        },
        "00:00:01.000": {
            "Lighting": 72
        },
        "00:00:03.000": {
            "RoomType": "Kitchen",
        }
    }
    timeline = Timeline.load_dict(timeline_data)
    assert "Lighting" not in timeline[0]
    for t in (1, 2, 3):
        assert timeline[t]["Lighting"] == 72


def test_timeline_equality():
    timeline1_data = {
        "00:00:00.000": {
            "RoomType": "LivingRoom",
        },
        "00:00:01.000": {
            "Lighting": 72
        },
        "00:00:03.000": {
            "Lighting": 75,
            "RoomType": "Kitchen",
        }
    }

    timeline2_data = {
        "00:00:03.000": {
            "RoomType": "Kitchen",
            "Lighting": 75,
        },
        "00:00:00.000": {
            "RoomType": "LivingRoom",
        },
        "00:00:01.000": {
            "Lighting": 72
        }
    }

    timeline1 = Timeline.load_dict(timeline1_data)
    timeline2 = Timeline.load_dict(timeline2_data)
    assert timeline1 == timeline2


def test_timeline_equality_case_sensitive():
    timeline1_data = {
        "00:00:00.000": {
            "RoomType": "LivingRoom",
        },
        "00:00:01.000": {
            "Lighting": 72
        },
        "00:00:03.000": {
            "Lighting": 75,
            "RoomType": "kitchen",
        }
    }

    timeline2_data = {
        "00:00:03.000": {
            "RoomType": "Kitchen",
            "Lighting": 75,
        },
        "00:00:00.000": {
            "RoomType": "LivingRoom",
        },
        "00:00:01.000": {
            "Lighting": 72
        }
    }

    timeline1 = Timeline.load_dict(timeline1_data)
    timeline2 = Timeline.load_dict(timeline2_data)
    assert timeline1 != timeline2


def test_extract_rebases_to_zero():
    timeline_data = {
        "00:00:00.000": {
            "RoomType": "Hall",
            "Quality": 80,
            "InterestValue": 98
        },
        "00:00:02.000": {
            "RoomType": "LivingRoom",
            "Quality": 100,
            "InterestValue": 58
        },
        "00:00:03.000": {
            "RoomType": "Bedroom",
            "Quality": 99,
            "InterestValue": 90
        }
    }

    timeline = Timeline.load_dict(timeline_data)
    extracted_timeline = timeline.extract(2, 2.5)
    assert list(extracted_timeline.value_dict.keys()) == [0, 0.5]
    assert extracted_timeline.duration() == 0.5
    assert extracted_timeline[0] == {"RoomType": "LivingRoom", "Quality": 100, "InterestValue": 58}
    assert extracted_timeline[0.5] == {"RoomType": "LivingRoom", "Quality": 100, "InterestValue": 58}


def test_extract_no_rebase():
    timeline_data = {
        "00:00:00.000": {
            "RoomType": "Hall",
            "Quality": 80,
            "InterestValue": 98
        },
        "00:00:02.000": {
            "RoomType": "LivingRoom",
            "Quality": 100,
            "InterestValue": 58
        },
        "00:00:03.000": {
            "RoomType": "Bedroom",
            "Quality": 99,
            "InterestValue": 90
        }
    }

    timeline = Timeline.load_dict(timeline_data)
    extracted_timeline = timeline.extract(2, 2.5, rebase_zero=False)
    assert extracted_timeline.duration() == 2.5  # this is a bit counter intuitive - ToDo check
    assert extracted_timeline[0] == {}
    assert extracted_timeline[0.5] == {}
    assert extracted_timeline[2] == {"RoomType": "LivingRoom", "Quality": 100, "InterestValue": 58}
    assert extracted_timeline[2.5] == {"RoomType": "LivingRoom", "Quality": 100, "InterestValue": 58}


def test_rebase():
    timeline_data = {
        "00:00:02.000": {
            "RoomType": "LivingRoom",
            "Quality": 100,
            "InterestValue": 58
        },
        "00:00:03.000": {
            "RoomType": "Bedroom",
            "Quality": 99,
            "InterestValue": 90
        }
    }

    timeline = Timeline.load_dict(timeline_data)

    assert timeline.rebase(0) == Timeline.load_dict({
        "00:00:00.000": {
            "RoomType": "LivingRoom",
            "Quality": 100,
            "InterestValue": 58
        },
        "00:00:01.000": {
            "RoomType": "Bedroom",
            "Quality": 99,
            "InterestValue": 90
        }
    })

    assert timeline.rebase(1) == Timeline.load_dict({
        "00:00:01.000": {
            "RoomType": "LivingRoom",
            "Quality": 100,
            "InterestValue": 58
        },
        "00:00:02.000": {
            "RoomType": "Bedroom",
            "Quality": 99,
            "InterestValue": 90
        }
    })

    assert timeline.rebase(5) == Timeline.load_dict({
        "00:00:05.000": {
            "RoomType": "LivingRoom",
            "Quality": 100,
            "InterestValue": 58
        },
        "00:00:06.000": {
            "RoomType": "Bedroom",
            "Quality": 99,
            "InterestValue": 90
        }
    })


def test_append():
    timeline1 = Timeline.load_dict({
        "00:00:00.000": {
            "RoomType": "LivingRoom",
            "Quality": 100,
            "InterestValue": 58
        },
        "00:00:01.000": {
            "InterestValue": 72
        },
    })
    timeline2 = Timeline.load_dict({
        "00:00:00.000": {
            "RoomType": "Hallway",
            "Quality": 99,
            "InterestValue": 20
        },
        "00:00:01.000": {
            "InterestValue": 75
        },
    })

    timeline = Timeline.append([timeline1, timeline2])

    assert timeline.duration() == 2

    assert timeline[0] == {
        "RoomType": "LivingRoom",
        "Quality": 100,
        "InterestValue": 58
    }

    assert timeline[1] == {
        "RoomType": "Hallway",
        "Quality": 99,
        "InterestValue": 20 #ToDo clearly work at the specs. This is not correct as a default.
    }

    assert timeline[2] == {
        "RoomType": "Hallway",
        "Quality": 99,
        "InterestValue": 75
    }


def test_split():
    timeline_data = {
        "00:00:00.000": {
            "RoomType": "LivingRoom",
            "Quality": 100,
            "InterestValue": 58
        },
        "00:00:01.000": {
            "InterestValue": 72
        },
        "00:00:02.000": {
            "InterestValue": 63,
            "Quality": 50,
        },
        "00:00:03.000": {
            "InterestValue": 89
        },
        "00:00:04.000": {
            "InterestValue": 94
        },
        "00:00:05.000": {
            "RoomType": "Kitchen",
            "Quality": 100,
            "InterestValue": 58
        },
        "00:00:06.000": {
            "InterestValue": 72
        },
        "00:00:07.000": {
            "InterestValue": 63,
            "Quality": 50,
        },
        "00:00:08.000": {
            "InterestValue": 94
        }
    }

    timeline = Timeline.load_dict(timeline_data)
    parts = timeline.split(8)
    for start, end, part in parts:
        assert isinstance(part, Timeline)
        assert part.duration() == 1
        assert end - start == 1
        assert part[0] == timeline[start]
        assert part[1] == timeline[end]


def test_split():
    timeline_data = {
        "00:00:00.000": {
            "RoomType": "LivingRoom",
            "Quality": 100,
            "InterestValue": 58
        },
        "00:00:01.000": {
            "InterestValue": 72
        }
    }

    parts = Timeline.load_dict(timeline_data).split(10)

    start, end, timeline = parts[0]
    start1, end1, timeline1 = parts[1]
    start2, end2, timeline2 = parts[2]
    start3, end3, timeline3 = parts[3]
    start4, end4, timeline4 = parts[4]
    start5, end5, timeline5 = parts[5]
    start6, end6, timeline6 = parts[6]
    start7, end7, timeline7 = parts[7]
    start8, end8, timeline8 = parts[8]
    start9, end9, timeline9 = parts[9]

    first_value = {
        "00:00:00.000": {
            "RoomType": "LivingRoom",
            "Quality": 100,
            "InterestValue": 58
        },
        "00:00:00.100": {
            "RoomType": "LivingRoom",
            "Quality": 100,
            "InterestValue": 58
        }
    }

    last_value = {
        '00:00:00.000': {
            'RoomType': 'LivingRoom',
            'Quality': 100,
            'InterestValue': 58
        },
        '00:00:00.100': {
            'RoomType': 'LivingRoom',
            'Quality': 100,
            'InterestValue': 72
        }
    }

    assert start == D(0)
    assert end == D(0.1)
    assert timeline == Timeline.load_dict(first_value)

    assert start1 == D(0.1)
    assert end1 == D(0.2)
    assert timeline1 == Timeline.load_dict(first_value)

    assert start2 == D(0.2)
    assert end2 == D(0.3)
    assert timeline2 == Timeline.load_dict(first_value)

    assert start3 == D(0.3)
    assert end3 == D(0.4)
    assert timeline3 == Timeline.load_dict(first_value)

    assert start4 == D(0.4)
    assert end4 == D(0.5)
    assert timeline4 == Timeline.load_dict(first_value)

    assert start5 == D(0.5)
    assert end5 == D(0.6)
    assert timeline5 == Timeline.load_dict(first_value)

    assert start6 == D(0.6)
    assert end6 == D(0.7)
    assert timeline6 == Timeline.load_dict(first_value)

    assert start7 == D(0.7)
    assert end7 == D(0.8)
    assert timeline7 == Timeline.load_dict(first_value)

    assert start8 == D(0.8)
    assert end8 == D(0.9)
    assert timeline8 == Timeline.load_dict(first_value)

    assert start9 == D(0.9)
    assert end9 == D(1.0)
    assert timeline9 == Timeline.load_dict(last_value)



def test_extract_by_attribute():
    timeline_data = {
        "00:00:00.000": {
            "RoomType": "Hall",
            "Quality": 100,
            "InterestValue": 58
        },
        "00:00:01.000": {
            "RoomType": "LivingRoom",
            "InterestValue": 30
        },
        "00:00:02.000": {
            "RoomType": "LivingRoom",
            "Quality": 100,
            "InterestValue": 58
        },
        "00:00:03.000": {
            "Quality": 95,
            "InterestValue": 70
        },
        "00:00:04.000": {
            "RoomType": "Bedroom",
        },
        "00:00:05.000": {
            "RoomType": "Bedroom",
        }
    }

    timeline = Timeline.load_dict(timeline_data)
    timelines = timeline.extract_by_attribute("RoomType", "LivingRoom")
    assert timelines[0][0] == {'RoomType': 'LivingRoom', 'Quality': 100, 'InterestValue': 30}
    assert timelines[0][1] == {'RoomType': 'LivingRoom', 'Quality': 100, 'InterestValue': 58}
    assert timelines[0][2] == {'RoomType': 'LivingRoom', 'Quality': 95, 'InterestValue': 70}

    timelines = timeline.extract_by_attribute("RoomType", "LivingRoom", rebase_zero=False)
    assert timelines[0][1] == {'RoomType': 'LivingRoom', 'Quality': 100, 'InterestValue': 30}
    assert timelines[0][2] == {'RoomType': 'LivingRoom', 'Quality': 100, 'InterestValue': 58}
    assert timelines[0][3] == {'RoomType': 'LivingRoom', 'Quality': 95, 'InterestValue': 70}


def test_extract_by_attribute_returns_many():
    timeline_data = {
        "00:00:00.000": {
            "RoomType": "Hall",
            "Quality": 100,
            "InterestValue": 58
        },
        "00:00:01.000": {
            "RoomType": "LivingRoom",
            "InterestValue": 30
        },
        "00:00:02.000": {
            "RoomType": "LivingRoom",
            "Quality": 100,
            "InterestValue": 58
        },
        "00:00:03.000": {
            "Quality": 95,
            "InterestValue": 70
        },
        "00:00:04.000": {
            "InterestValue": 50,
            "RoomType": "Bedroom",
        },
        "00:00:05.000": {
            "InterestValue": 70,
            "RoomType": "Bedroom",
        },
        "00:00:06.000": {
            "InterestValue": 70,
            "RoomType": "Terras",
        }
    }

    timeline = Timeline.load_dict(timeline_data)

    timelines = timeline.extract_by_attribute("InterestValue", 70)
    assert len(timelines) == 2
    assert timelines[0][0] == {"RoomType": "LivingRoom", "Quality": 95, "InterestValue": 70}
    assert timelines[1][0] == {"InterestValue": 70, "RoomType": "Bedroom", "Quality": 95}
    assert timelines[1][1] == {"InterestValue": 70, "RoomType": "Terras", "Quality": 95}

    timelines = timeline.extract_by_attribute("InterestValue", 70, rebase_zero=False)
    assert len(timelines) == 2
    assert timelines[0][3] == {"RoomType": "LivingRoom", "Quality": 95, "InterestValue": 70}
    assert timelines[1][5] == {"InterestValue": 70, "RoomType": "Bedroom", "Quality": 95}
    assert timelines[1][6] == {"InterestValue": 70, "RoomType": "Terras", "Quality": 95}


def test_extract_by_attribute_range():
    timeline_data = {
        "00:00:00.000": {
            "RoomType": "Hall",
            "Quality": 100,
            "InterestValue": 58
        },
        "00:00:01.000": {
            "RoomType": "LivingRoom",
            "InterestValue": 30
        },
        "00:00:02.000": {
            "RoomType": "LivingRoom",
            "Quality": 100,
            "InterestValue": 58
        },
        "00:00:03.000": {
            "Quality": 95,
            "InterestValue": 70
        },
        "00:00:04.000": {
            "InterestValue": 50,
            "RoomType": "Bedroom",
        },
        "00:00:05.000": {
            "InterestValue": 70,
            "RoomType": "Bedroom",
        },
        "00:00:06.000": {
            "InterestValue": 70,
            "RoomType": "Terras",
        }
    }

    timeline = Timeline.load_dict(timeline_data)

    timelines = timeline.extract_by_attribute_exp("InterestValue", comparison_func=lambda x: x > 50)
    assert len(timelines) == 3
    assert timelines[0][0] == {'RoomType': 'Hall', 'Quality': 100, 'InterestValue': 58}
    assert timelines[1][0] == {
        "RoomType": "LivingRoom",
        "Quality": 100,
        "InterestValue": 58
    }
    assert timelines[1][1] == {
        "RoomType": "LivingRoom",
        "Quality": 95,
        "InterestValue": 70
    }

    assert timelines[2][0] == {
        "RoomType": "Bedroom",
        "Quality": 95,
        "InterestValue": 70,
    }

    assert timelines[2][1] == {
        "RoomType": "Terras",
        "Quality": 95,
        "InterestValue": 70,
    }


def test_groupby():
    timeline = Timeline.load_dict(
        {
            "00:00:00.000": {
                "RoomType": "Hall",
                "Quality": 100,
                "InterestValue": 58
            },
            "00:00:01.000": {
                "RoomType": "LivingRoom",
                "InterestValue": 30
            },
            "00:00:02.000": {
                "RoomType": "LivingRoom",
                "Quality": 100,
                "InterestValue": 58
            },
            "00:00:03.000": {
                "Quality": 95,
                "InterestValue": 70
            },
            "00:00:04.000": {
                "InterestValue": 50,
                "RoomType": "Bedroom",
            },
            "00:00:05.000": {
                "InterestValue": 70,
                "RoomType": "Bedroom",
            },
            "00:00:06.000": {
                "InterestValue": 70,
                "RoomType": "Terras",
            }
        }
    )

    result = timeline.group_by(attribute="RoomType")

    assert len(result) == 4
    assert result[0].attribute == "RoomType"
    assert result[0].attribute_value == "Hall"
    assert result[1].attribute_value == "LivingRoom"
    assert result[2].attribute_value == "Bedroom"
    assert result[3].attribute_value == "Terras"


# ============================================================================
# New tests for bug fixes and improvements
# ============================================================================

def test_insert_marker_preserves_existing_data():
    """Test that insert_marker doesn't overwrite existing data at the timestamp."""
    timeline = Timeline.load_dict({
        "00:00:01.000": {
            "RoomType": "LivingRoom",
            "Quality": 100,
        }
    })

    # Insert a marker at an existing timestamp
    timeline.insert_marker("highlight", True, D(1))

    # Both the original data and marker should exist
    assert timeline.value_dict[D(1)]["RoomType"] == "LivingRoom"
    assert timeline.value_dict[D(1)]["Quality"] == 100
    assert timeline.value_dict[D(1)]["marker_highlight"] is True


def test_insert_marker_at_nonexistent_timestamp_raises():
    """Test that inserting a marker at a nonexistent timestamp raises KeyError."""
    timeline = Timeline.load_dict({
        "00:00:00.000": {"RoomType": "Hall"}
    })

    with pytest.raises(KeyError) as exc_info:
        timeline.insert_marker("cut", "start", D(0.5))

    assert "0.5" in str(exc_info.value)


def test_insert_marker_updates_existing_marker():
    """Test that inserting a marker with the same name updates its value."""
    timeline = Timeline.load_dict({
        "00:00:01.000": {"RoomType": "Hall"}
    })

    timeline.insert_marker("score", 50, D(1))
    assert timeline.value_dict[D(1)]["marker_score"] == 50

    timeline.insert_marker("score", 75, D(1))
    assert timeline.value_dict[D(1)]["marker_score"] == 75


def test_duration_with_unordered_insertion():
    """Test that duration() returns correct value regardless of insertion order."""
    # Insert in reverse order
    timeline_data = {
        "00:00:05.000": {"Event": "End"},
        "00:00:00.000": {"Event": "Start"},
        "00:00:02.500": {"Event": "Middle"},
    }
    timeline = Timeline.load_dict(timeline_data)

    assert timeline.duration() == D(5)


def test_duration_empty_timeline():
    """Test that duration() returns 0 for empty timeline."""
    timeline = Timeline()
    assert timeline.duration() == D(0)


def test_get_key_before_returns_none_for_early_timestamp():
    """Test _get_key_before returns None when no key exists before timestamp."""
    timeline = Timeline.load_dict({
        "00:00:05.000": {"Event": "Start"}
    })

    # Ask for key before any data exists
    result = timeline._get_key_before(D(2))
    assert result is None


def test_get_key_before_returns_exact_match():
    """Test _get_key_before returns the key itself if it exists."""
    timeline = Timeline.load_dict({
        "00:00:05.000": {"Event": "Start"}
    })

    result = timeline._get_key_before(D(5))
    assert result == D(5)


def test_get_key_before_returns_previous_key():
    """Test _get_key_before returns the largest key before the timestamp."""
    timeline = Timeline.load_dict({
        "00:00:01.000": {"Event": "A"},
        "00:00:03.000": {"Event": "B"},
        "00:00:05.000": {"Event": "C"},
    })

    result = timeline._get_key_before(D(4))
    assert result == D(3)


def test_get_key_before_empty_timeline():
    """Test _get_key_before returns None for empty timeline."""
    timeline = Timeline()
    assert timeline._get_key_before(D(1)) is None


def test_repr_empty():
    """Test __repr__ for empty timeline."""
    timeline = Timeline()
    assert repr(timeline) == "Timeline(empty)"


def test_repr_with_data():
    """Test __repr__ for timeline with data."""
    timeline = Timeline.load_dict({
        "00:00:00.000": {"A": 1},
        "00:00:01.000": {"B": 2},
        "00:00:02.000": {"C": 3},
    })
    assert "Timeline(entries=3, duration=" in repr(timeline)
    assert "2" in repr(timeline)


def test_contains():
    """Test __contains__ for checking if timestamp exists."""
    timeline = Timeline.load_dict({
        "00:00:01.000": {"A": 1},
        "00:00:02.000": {"B": 2},
    })

    assert D(1) in timeline
    assert D(2) in timeline
    assert D(1.5) not in timeline
    assert D(0) not in timeline


def test_set_new_timestamp():
    """Test set() method for adding data at new timestamp."""
    timeline = Timeline()
    timeline.set(D(1), {"RoomType": "Kitchen"})

    assert D(1) in timeline
    assert timeline.value_dict[D(1)] == {"RoomType": "Kitchen"}


def test_set_existing_timestamp_merges_data():
    """Test set() method merges data at existing timestamp."""
    timeline = Timeline.load_dict({
        "00:00:01.000": {"RoomType": "Kitchen", "Quality": 80}
    })

    timeline.set(D(1), {"Quality": 100, "Lighting": 50})

    assert timeline.value_dict[D(1)] == {
        "RoomType": "Kitchen",
        "Quality": 100,
        "Lighting": 50
    }


def test_iteration_is_sorted():
    """Test that iteration yields timestamps in sorted order."""
    # Insert in random order
    timeline_data = {
        "00:00:03.000": {"C": 3},
        "00:00:01.000": {"A": 1},
        "00:00:05.000": {"E": 5},
        "00:00:02.000": {"B": 2},
        "00:00:04.000": {"D": 4},
    }
    timeline = Timeline.load_dict(timeline_data)

    timestamps = list(timeline)
    expected = [D(1), D(2), D(3), D(4), D(5)]
    assert timestamps == expected


def test_getitem_before_any_data():
    """Test that __getitem__ returns empty dict for timestamp before any data."""
    timeline = Timeline.load_dict({
        "00:00:05.000": {"Event": "Start"}
    })

    # Query before first entry
    assert timeline[D(2)] == {}


def test_getitem_empty_timeline():
    """Test that __getitem__ returns empty dict for empty timeline."""
    timeline = Timeline()
    assert timeline[D(1)] == {}


def test_value_dict_setter_rebuilds_sorted_keys():
    """Test that setting value_dict rebuilds the sorted keys."""
    timeline = Timeline()

    # Directly set value_dict (backwards compatibility)
    timeline.value_dict = {
        D(3): {"C": 3},
        D(1): {"A": 1},
        D(2): {"B": 2},
    }

    # Iteration should still be sorted
    assert list(timeline) == [D(1), D(2), D(3)]
    assert timeline.duration() == D(3)
