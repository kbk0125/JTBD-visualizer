"""Content-aware vertical and horizontal placement for job-map diagrams."""

from __future__ import annotations

import math
from dataclasses import dataclass

from .constants import (
    BAR_CARD_GAP,
    BAR_HEIGHT,
    CANVAS_LEFT,
    CANVAS_RIGHT,
    CARD_GAP,
    COMPARISON_FIRST_STATE_HEADING_Y,
    LANE_CLEARANCE,
    LANES,
    PHASE_TITLE_FONT_SIZE,
    PHASE_TITLE_TO_BAR,
    SINGLE_FIRST_PHASE_TITLE_Y,
    STATE_CLEARANCE,
    STATE_TO_PHASE_GAP,
    TOTAL_CLEARANCE,
)
from .model import JobMapSpec, Source, Stage


@dataclass(frozen=True)
class LaneLayout:
    name: str
    title_y: int
    bar_y: int
    card_y: int
    card_xs: tuple[int, ...]
    estimated_card_height: int


@dataclass(frozen=True)
class MapLayout:
    state: str
    heading_y: int | None
    lanes: tuple[LaneLayout, ...]
    total_y: int


def _even_positions(count: int) -> list[int]:
    if count == 1:
        return [(CANVAS_LEFT + CANVAS_RIGHT) // 2]
    span = CANVAS_RIGHT - CANVAS_LEFT
    return [round(CANVAS_LEFT + span * index / (count - 1)) for index in range(count)]


def _card_xs(lane_name: str, count: int, card_width: int) -> tuple[int, ...]:
    if lane_name == "Plan":
        return tuple(x - card_width // 2 for x in _even_positions(count))
    first_x = CANVAS_LEFT - LANES["Plan"]["card_width"] // 2
    return tuple(first_x + index * (card_width + CARD_GAP) for index in range(count))


def _wrapped_lines(text: str, width: int, average_character_width: float = 8.0) -> int:
    characters_per_line = max(12, int(width / average_character_width))
    return max(1, math.ceil(len(text) / characters_per_line))


def estimate_card_height(
    stage: Stage,
    card_width: int,
    sources: dict[str, Source],
) -> int:
    body_width = card_width - 24 - round(card_width * 0.075)
    activity_lines = 0
    evidence_ids = []
    for activity in stage.activities:
        suffix = " — inferred" if activity.confidence == "inferred" else ""
        activity_lines += _wrapped_lines(f"• {activity.text}{suffix}", body_width)
        for source_id in activity.evidence:
            if source_id not in evidence_ids:
                evidence_ids.append(source_id)

    if evidence_ids:
        source_text = "Sources: " + " · ".join(sources[source_id].short_label for source_id in evidence_ids)
    else:
        source_text = "Sources: No direct evidence — inferred"
    source_lines = _wrapped_lines(source_text, body_width)

    body_start = 61
    text_line_height = 18
    source_separation = 18
    bottom_clearance = 18
    return (
        body_start
        + activity_lines * text_line_height
        + source_separation
        + source_lines * text_line_height
        + bottom_clearance
    )


def plan_layout(spec: JobMapSpec) -> tuple[MapLayout, ...]:
    sources = {source.id: source for source in spec.sources}
    is_comparison = spec.view == "compare"
    next_state_heading_y = COMPARISON_FIRST_STATE_HEADING_Y
    layouts = []

    for job_map in spec.maps:
        heading_y = next_state_heading_y if is_comparison else None
        phase_title_y = (
            heading_y + STATE_TO_PHASE_GAP
            if heading_y is not None
            else SINGLE_FIRST_PHASE_TITLE_Y
        )
        stage_lookup = {stage.id: stage for stage in job_map.stages}
        lane_layouts = []

        for lane_name, lane in LANES.items():
            bar_y = phase_title_y + PHASE_TITLE_TO_BAR
            card_y = bar_y + BAR_HEIGHT // 2 + BAR_CARD_GAP
            card_width = lane["card_width"]
            tallest_card = max(
                estimate_card_height(stage_lookup[stage_id], card_width, sources)
                for stage_id in lane["stages"]
            )
            lane_layouts.append(
                LaneLayout(
                    name=lane_name,
                    title_y=phase_title_y,
                    bar_y=bar_y,
                    card_y=card_y,
                    card_xs=_card_xs(lane_name, len(lane["stages"]), card_width),
                    estimated_card_height=tallest_card,
                )
            )
            phase_title_y = card_y + tallest_card + LANE_CLEARANCE

        last_lane = lane_layouts[-1]
        total_y = last_lane.card_y + last_lane.estimated_card_height + TOTAL_CLEARANCE
        layouts.append(
            MapLayout(
                state=job_map.state,
                heading_y=heading_y,
                lanes=tuple(lane_layouts),
                total_y=total_y,
            )
        )
        next_state_heading_y = total_y + PHASE_TITLE_FONT_SIZE + STATE_CLEARANCE

    return tuple(layouts)
