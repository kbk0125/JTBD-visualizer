"""Metric normalization, labels, totals, and shared bar scaling."""

from __future__ import annotations

from .constants import BAR_GAP, BAR_MAX_WIDTH, HOURS_PER_WEEK, LANES
from .model import JobMap, Stage


def format_number(value: int | float) -> str:
    number = float(value)
    return str(int(number)) if number.is_integer() else f"{number:g}"


def duration_value(stage: Stage) -> float:
    assert stage.duration is not None
    value = stage.duration.value
    return value * HOURS_PER_WEEK if stage.duration.unit == "weeks" else value


def duration_label(stage: Stage) -> str:
    assert stage.duration is not None
    value = stage.duration.value
    rendered = format_number(value)
    singular = "hour" if stage.duration.unit == "hours" else "week"
    unit = singular if value == 1 else stage.duration.unit
    return f"{rendered} {unit}"


def stage_bar_value(stage: Stage, representation: str) -> float:
    if representation == "time":
        return duration_value(stage)
    assert stage.dropoff_percent is not None
    return stage.dropoff_percent


def stage_metric_label(stage: Stage, representation: str) -> str:
    if representation == "time":
        return f"Time: {duration_label(stage)}"
    assert stage.dropoff_percent is not None
    return f"Drop-off: {format_number(stage.dropoff_percent)}%"


def total_metric_label(stages: tuple[Stage, ...], representation: str) -> str:
    if representation == "time":
        if all(stage.duration is not None and stage.duration.unit == "weeks" for stage in stages):
            total = sum(stage.duration.value for stage in stages if stage.duration is not None)
            unit = "week" if total == 1 else "weeks"
        else:
            total = sum(duration_value(stage) for stage in stages)
            unit = "hour" if total == 1 else "hours"
        return f"{format_number(total)} {unit}"

    completion = 100.0
    for stage in stages:
        assert stage.dropoff_percent is not None
        completion *= 1 - stage.dropoff_percent / 100
    return f"{format_number(round(completion, 2))}% reach the end"


def shared_bar_scale(maps: tuple[JobMap, ...], representation: str) -> float:
    candidates = []
    for job_map in maps:
        stage_lookup = {stage.id: stage for stage in job_map.stages}
        for lane in LANES.values():
            lane_total = sum(
                stage_bar_value(stage_lookup[stage_id], representation)
                for stage_id in lane["stages"]
            )
            if lane_total > 0:
                lane_gaps = BAR_GAP * (len(lane["stages"]) - 1)
                candidates.append((BAR_MAX_WIDTH - lane_gaps) / lane_total)
    return min(candidates) if candidates else 0
