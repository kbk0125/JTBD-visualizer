"""Validation for versioned job-map specifications."""

from __future__ import annotations

import math
from urllib.parse import urlparse

from .constants import SCHEMA_VERSION, STAGE_IDS
from .model import JobMapSpec


def fail(message: str) -> None:
    raise ValueError(message)


def required_text(value: object, field: str, max_length: int) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(f"{field} must be a non-empty string")
    text = value.strip()
    if len(text) > max_length:
        fail(f"{field} must be {max_length} characters or fewer")
    return text


def _validate_sources(sources: object) -> dict[str, str]:
    if not isinstance(sources, list):
        fail("sources must be an array")

    source_kinds = {}
    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            fail(f"sources[{index}] must be an object")
        source_id = required_text(source.get("id"), f"sources[{index}].id", 12)
        if source_id in source_kinds:
            fail(f"duplicate source id: {source_id}")
        source_kind = source.get("kind")
        if source_kind not in {"customer_evidence", "proposal_evidence", "method"}:
            fail(f"sources[{index}].kind must be customer_evidence, proposal_evidence, or method")
        source_kinds[source_id] = source_kind
        required_text(source.get("label"), f"sources[{index}].label", 160)
        required_text(source.get("short_label"), f"sources[{index}].short_label", 40)
        url = source.get("url")
        if url is not None:
            url = required_text(url, f"sources[{index}].url", 500)
            if urlparse(url).scheme not in {"http", "https"}:
                fail(f"sources[{index}].url must use http or https")
    return source_kinds


def _validate_metric(stage: dict, stage_path: str, representation: str) -> None:
    if representation == "time":
        duration = stage.get("duration")
        if not isinstance(duration, dict):
            fail(f"{stage_path}.duration must be an object in time mode")
        value = duration.get("value")
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not math.isfinite(value)
            or value <= 0
        ):
            fail(f"{stage_path}.duration.value must be a positive finite number")
        if duration.get("unit") not in {"hours", "weeks"}:
            fail(f"{stage_path}.duration.unit must be hours or weeks")
        if "dropoff_percent" in stage:
            fail(f"{stage_path} must not include dropoff_percent in time mode")
        return

    dropoff = stage.get("dropoff_percent")
    if (
        isinstance(dropoff, bool)
        or not isinstance(dropoff, (int, float))
        or not math.isfinite(dropoff)
        or not 0 <= dropoff <= 100
    ):
        fail(f"{stage_path}.dropoff_percent must be a finite number from 0 to 100")
    if "duration" in stage:
        fail(f"{stage_path} must not include duration in funnel mode")


def _validate_activities(
    stage: dict,
    stage_path: str,
    state: str,
    source_kinds: dict[str, str],
) -> None:
    activities = stage.get("activities")
    if not isinstance(activities, list) or not 1 <= len(activities) <= 5:
        fail(f"{stage_path}.activities must contain 1 to 5 items")

    allowed_evidence_kinds = {"customer_evidence"}
    if state == "after":
        allowed_evidence_kinds.add("proposal_evidence")

    for activity_index, activity in enumerate(activities):
        prefix = f"{stage_path}.activities[{activity_index}]"
        if not isinstance(activity, dict):
            fail(f"{prefix} must be an object")
        required_text(activity.get("text"), f"{prefix}.text", 120)
        if activity.get("confidence") not in {"explicit", "inferred"}:
            fail(f"{prefix}.confidence must be explicit or inferred")
        evidence = activity.get("evidence")
        if not isinstance(evidence, list):
            fail(f"{prefix}.evidence must be an array")
        unknown = [item for item in evidence if item not in source_kinds]
        if unknown:
            fail(f"{prefix}.evidence contains unknown source ids: {unknown}")
        disallowed = [item for item in evidence if source_kinds[item] not in allowed_evidence_kinds]
        if disallowed:
            fail(f"{prefix}.evidence uses source kinds not allowed for {state}: {disallowed}")


def _validate_maps(
    maps: object,
    view: str,
    representation: str,
    source_kinds: dict[str, str],
) -> None:
    if not isinstance(maps, list):
        fail("maps must be an array")
    expected_states = {
        "status_quo": ["status_quo"],
        "after": ["after"],
        "compare": ["status_quo", "after"],
    }[view]
    actual_states = [item.get("state") if isinstance(item, dict) else None for item in maps]
    if actual_states != expected_states:
        fail(f"maps must contain states in this order: {', '.join(expected_states)}")

    for map_index, job_map in enumerate(maps):
        stages = job_map.get("stages")
        if not isinstance(stages, list):
            fail(f"maps[{map_index}].stages must be an array")
        actual_ids = [stage.get("id") if isinstance(stage, dict) else None for stage in stages]
        if actual_ids != list(STAGE_IDS):
            fail(f"maps[{map_index}].stages must appear exactly once in this order: {', '.join(STAGE_IDS)}")

        state = job_map["state"]
        for stage_index, stage in enumerate(stages):
            stage_path = f"maps[{map_index}].stages[{stage_index}]"
            if not isinstance(stage, dict):
                fail(f"{stage_path} must be an object")
            _validate_metric(stage, stage_path, representation)
            _validate_activities(stage, stage_path, state, source_kinds)


def validate_spec(spec: object) -> JobMapSpec:
    if not isinstance(spec, dict):
        fail("top-level input must be an object")
    schema_version = spec.get("schema_version")
    if isinstance(schema_version, bool) or schema_version != SCHEMA_VERSION:
        fail(f"schema_version must be {SCHEMA_VERSION}")

    representation = spec.get("representation")
    if representation not in {"time", "funnel"}:
        fail("representation must be time or funnel")
    view = spec.get("view")
    if view not in {"status_quo", "after", "compare"}:
        fail("view must be status_quo, after, or compare")

    for field, limit in (("title", 90), ("job_executor", 80), ("core_job", 180)):
        required_text(spec.get(field), field, limit)
    required_title_prefix = {
        "status_quo": "status quo:",
        "after": "after:",
        "compare": "comparison:",
    }[view]
    if not spec["title"].strip().lower().startswith(required_title_prefix):
        fail(f"title must begin with '{required_title_prefix.title()}' in {view} view")

    source_kinds = _validate_sources(spec.get("sources"))
    _validate_maps(spec.get("maps"), view, representation, source_kinds)
    return JobMapSpec.from_dict(spec)
