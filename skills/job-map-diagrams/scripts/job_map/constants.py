"""Shared semantic and visual constants for job-map diagrams."""

from __future__ import annotations

SCHEMA_VERSION = 1

STAGES = (
    ("define", "Define", "Plan"),
    ("locate", "Locate", "Plan"),
    ("prepare", "Prepare", "Plan"),
    ("confirm", "Confirm", "Plan"),
    ("execute", "Execute", "Do"),
    ("monitor", "Monitor", "Do"),
    ("modify", "Modify", "Review"),
    ("conclude", "Conclude", "Review"),
)

STAGE_TITLES = {stage_id: title for stage_id, title, _ in STAGES}
STAGE_IDS = tuple(stage_id for stage_id, _, _ in STAGES)

STAGE_ICONS = {
    "define": "target",
    "locate": "search",
    "prepare": "settings",
    "confirm": "check-circle",
    "execute": "play",
    "monitor": "activity",
    "modify": "edit",
    "conclude": "flag",
}

LANES = {
    "Plan": {
        "line_color": "#4F76A8",
        "fill_color": "#E4EDF7",
        "stages": ("define", "locate", "prepare", "confirm"),
        "card_width": 320,
    },
    "Do": {
        "line_color": "#8A5B9E",
        "fill_color": "#F1E4F4",
        "stages": ("execute", "monitor"),
        "card_width": 480,
    },
    "Review": {
        "line_color": "#A9752A",
        "fill_color": "#F7E9CF",
        "stages": ("modify", "conclude"),
        "card_width": 480,
    },
}

CANVAS_LEFT = 300
CANVAS_RIGHT = 1440
PHASE_TITLE_X = CANVAS_LEFT - LANES["Plan"]["card_width"] // 2
BAR_MAX_WIDTH = CANVAS_RIGHT - CANVAS_LEFT
BAR_HEIGHT = 18
BAR_CARD_GAP = 28
BAR_GAP = 10
CONNECTOR_COLOR = "#C7CDD6"
CONNECTOR_WIDTH = 1
CARD_GAP = 40

HEADER_Y = 30
HEADER_HEIGHT = 110
SINGLE_FIRST_PHASE_TITLE_Y = 192
COMPARISON_FIRST_STATE_HEADING_Y = 155
STATE_TO_PHASE_GAP = 82
PHASE_TITLE_TO_BAR = 58
LANE_CLEARANCE = 80
TOTAL_CLEARANCE = 65
STATE_CLEARANCE = 70

PHASE_TITLE_FONT_SIZE = 29
STATE_TITLE_FONT_SIZE = 34
HOURS_PER_WEEK = 168
