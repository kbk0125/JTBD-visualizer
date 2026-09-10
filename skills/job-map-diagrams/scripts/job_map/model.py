"""Normalized immutable data model for validated job-map specifications."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Source:
    id: str
    kind: str
    short_label: str
    label: str
    url: str | None


@dataclass(frozen=True)
class Activity:
    text: str
    evidence: tuple[str, ...]
    confidence: str


@dataclass(frozen=True)
class Duration:
    value: float
    unit: str


@dataclass(frozen=True)
class Stage:
    id: str
    activities: tuple[Activity, ...]
    duration: Duration | None = None
    dropoff_percent: float | None = None


@dataclass(frozen=True)
class JobMap:
    state: str
    stages: tuple[Stage, ...]


@dataclass(frozen=True)
class JobMapSpec:
    schema_version: int
    representation: str
    view: str
    title: str
    job_executor: str
    core_job: str
    sources: tuple[Source, ...]
    maps: tuple[JobMap, ...]

    @classmethod
    def from_dict(cls, data: dict) -> "JobMapSpec":
        sources = tuple(
            Source(
                id=source["id"],
                kind=source["kind"],
                short_label=source["short_label"],
                label=source["label"],
                url=source.get("url"),
            )
            for source in data["sources"]
        )
        maps = []
        for job_map in data["maps"]:
            stages = []
            for stage in job_map["stages"]:
                duration_data = stage.get("duration")
                duration = (
                    Duration(value=float(duration_data["value"]), unit=duration_data["unit"])
                    if duration_data is not None
                    else None
                )
                stages.append(
                    Stage(
                        id=stage["id"],
                        activities=tuple(
                            Activity(
                                text=activity["text"],
                                evidence=tuple(activity["evidence"]),
                                confidence=activity["confidence"],
                            )
                            for activity in stage["activities"]
                        ),
                        duration=duration,
                        dropoff_percent=(
                            float(stage["dropoff_percent"])
                            if "dropoff_percent" in stage
                            else None
                        ),
                    )
                )
            maps.append(JobMap(state=job_map["state"], stages=tuple(stages)))

        return cls(
            schema_version=data["schema_version"],
            representation=data["representation"],
            view=data["view"],
            title=data["title"],
            job_executor=data["job_executor"],
            core_job=data["core_job"],
            sources=sources,
            maps=tuple(maps),
        )
