"""Compose validated job-map specifications into Eraser Diagrams JSON."""

from __future__ import annotations

from .constants import (
    BAR_GAP,
    BAR_HEIGHT,
    HEADER_HEIGHT,
    HEADER_Y,
    HATCH_SPACING,
    LANES,
    LEGEND_Y,
    CONNECTOR_COLOR,
    CONNECTOR_WIDTH,
    PHASE_TITLE_FONT_SIZE,
    PHASE_TITLE_X,
    OUTSIDE_PRODUCT_THRESHOLD,
    STAGE_ICONS,
    STAGE_TITLES,
    STATE_TITLE_FONT_SIZE,
)
from .layout import plan_layout
from .metrics import shared_bar_scale, stage_bar_value, stage_metric_label, total_metric_label
from .model import JobMapSpec, Source, Stage


def _source_footer(source_ids: list[str], sources: dict[str, Source], markdown: bool) -> str:
    rendered = []
    for source_id in source_ids:
        source = sources[source_id]
        if markdown and source.url:
            rendered.append(f"[{source.short_label}]({source.url})")
        else:
            rendered.append(source.short_label)
    return " · ".join(rendered) if rendered else "No direct evidence — inferred"


def _card_content(stage: Stage, sources: dict[str, Source]) -> tuple[str, str, str]:
    bullets = []
    evidence_ids = []
    for activity in stage.activities:
        suffix = " — inferred" if activity.confidence == "inferred" else ""
        bullets.append(f"• {activity.text}{suffix}")
        for source_id in activity.evidence:
            if source_id not in evidence_ids:
                evidence_ids.append(source_id)

    card_body = "\n\n".join(bullets)
    visible_sources = f"Sources: {_source_footer(evidence_ids, sources, markdown=True)}"
    sizing_sources = f"Sources: {_source_footer(evidence_ids, sources, markdown=False)}"
    overlay = "\n".join(bullets) + "\n\n" + visible_sources
    return card_body, sizing_sources, overlay


def _header_entity(spec: JobMapSpec) -> dict:
    return {
        "tag": "Shape",
        "id": "map-title",
        "shape": "rectangle",
        "x": 40,
        "y": HEADER_Y,
        "width": 1400,
        "height": HEADER_HEIGHT,
        "bgColor": "#FBFCFE",
        "borderColor": "#D7DEE8",
        "styleMode": "plain",
        "cornerRadius": "round",
        "vAlign": "middle",
        "texts": [
            {"text": spec.title, "fontSize": 26, "hAlign": "left", "typeface": "rough"},
            {"text": f"Executor: {spec.job_executor}", "fontSize": 18, "hAlign": "left", "typeface": "clean"},
            {"text": f"Core job: {spec.core_job}", "fontSize": 18, "hAlign": "left", "typeface": "clean"},
        ],
    }


def _format_percent(value: float) -> str:
    return f"{value:g}%"


def _hatch_path(width: int, height: int) -> str:
    """Return clipped diagonal line segments for a custom Eraser geoPath."""
    segments = []
    for offset in range(-height + HATCH_SPACING, width, HATCH_SPACING):
        start_x = max(0, offset)
        start_y = max(0, -offset)
        end_x = min(width, offset + height)
        end_y = end_x - offset
        if start_x < end_x:
            segments.append(f"M {start_x},{start_y} L {end_x},{end_y}")
    return " ".join(segments)


def _hatch_entity(entity_id: str, x: int, y: int, width: int, height: int, color: str) -> dict:
    return {
        "tag": "Shape",
        "id": entity_id,
        "shape": "parallelogram",
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "geoPath": _hatch_path(width, height),
        "geoW": width,
        "geoH": height,
        "color": color,
        "bgColor": "#00000000",
        "borderColor": color,
        "styleMode": "plain",
        "texts": [],
    }


def _legend_entities() -> list[dict]:
    swatch_width = 64
    swatch_height = 14
    first_x = PHASE_TITLE_X
    second_x = first_x + 300
    entities = [
        {
            "tag": "Shape",
            "id": "legend-in-product",
            "shape": "rectangle",
            "x": first_x,
            "y": LEGEND_Y,
            "width": swatch_width,
            "height": swatch_height,
            "color": LANES["Plan"]["line_color"],
            "bgColor": LANES["Plan"]["line_color"],
            "borderColor": LANES["Plan"]["line_color"],
            "styleMode": "plain",
            "cornerRadius": "round",
            "texts": [],
        },
        {
            "tag": "Textbox",
            "id": "legend-in-product-label",
            "x": first_x + swatch_width + 12,
            "y": LEGEND_Y - 5,
            "width": 210,
            "text": "Mostly in product",
            "color": "#4B5563",
            "fontSize": 16,
            "hAlign": "left",
            "typeface": "clean",
        },
        {
            "tag": "Shape",
            "id": "legend-outside-product",
            "shape": "rectangle",
            "x": second_x,
            "y": LEGEND_Y,
            "width": swatch_width,
            "height": swatch_height,
            "color": LANES["Plan"]["line_color"],
            "bgColor": LANES["Plan"]["line_color"],
            "borderColor": LANES["Plan"]["line_color"],
            "styleMode": "plain",
            "cornerRadius": "round",
            "texts": [],
        },
        _hatch_entity(
            "legend-outside-product-hatch",
            second_x,
            LEGEND_Y,
            swatch_width,
            swatch_height,
            LANES["Plan"]["hatch_color"],
        ),
        {
            "tag": "Textbox",
            "id": "legend-outside-product-label",
            "x": second_x + swatch_width + 12,
            "y": LEGEND_Y - 5,
            "width": 360,
            "text": "Mostly outside product (>50%)",
            "color": "#4B5563",
            "fontSize": 16,
            "hAlign": "left",
            "typeface": "clean",
        },
    ]
    return entities


def _card_entities(
    stage: Stage,
    state_id: str,
    card_x: int,
    card_y: int,
    card_width: int,
    line_color: str,
    fill_color: str,
    representation: str,
    sources: dict[str, Source],
) -> list[dict]:
    stage_id = stage.id
    card_body, card_sources_sizing, card_body_overlay = _card_content(stage, sources)
    card_metric = stage_metric_label(stage, representation)
    product_boundary = f"Outside product: {_format_percent(stage.outside_product_percent)}"
    prefix = f"{state_id}-"

    return [
        {
            "tag": "Shape",
            "id": f"{prefix}card-{stage_id}",
            "shape": "rectangle",
            "x": card_x,
            "y": card_y,
            "width": card_width,
            "color": line_color,
            "bgColor": fill_color,
            "borderColor": line_color,
            "styleMode": "watercolor",
            "cornerRadius": "round",
            "textAspectRatio": 10,
            "vAlign": "top",
            "vMargin": 10,
            "texts": [
                {
                    "text": "\u00a0",
                    "fontSize": 18,
                    "color": "#00000000",
                    "hAlign": "left",
                    "typeface": "rough",
                },
                {
                    "text": card_body,
                    "fontSize": 16,
                    "color": "#00000000",
                    "hAlign": "left",
                    "typeface": "clean",
                },
                {
                    "text": card_metric,
                    "fontSize": 14,
                    "color": "#00000000",
                    "hAlign": "left",
                    "typeface": "clean",
                },
                {
                    "text": product_boundary,
                    "fontSize": 14,
                    "color": "#00000000",
                    "hAlign": "left",
                    "typeface": "clean",
                },
                {
                    "text": "\u00a0",
                    "fontSize": 6,
                    "color": "#00000000",
                    "hAlign": "left",
                    "typeface": "rough",
                },
                {
                    "text": card_sources_sizing,
                    "fontSize": 16,
                    "color": "#00000000",
                    "hAlign": "left",
                    "typeface": "clean",
                },
                {
                    "text": "\u00a0",
                    "fontSize": 12,
                    "color": "#00000000",
                    "hAlign": "left",
                    "typeface": "rough",
                },
            ],
        },
        {
            "tag": "Icon",
            "id": f"{prefix}icon-{stage_id}",
            "icon": STAGE_ICONS[stage_id],
            "x": card_x + 12,
            "y": card_y + 6,
            "width": 18,
            "height": 18,
            "color": "#111827",
        },
        {
            "tag": "Textbox",
            "id": f"{prefix}card-title-{stage_id}",
            "x": card_x + 34,
            "y": card_y + 8,
            "width": card_width - 46,
            "text": STAGE_TITLES[stage_id],
            "color": "#111827",
            "fontSize": 18,
            "hAlign": "left",
            "typeface": "rough",
        },
        {
            "tag": "Textbox",
            "id": f"{prefix}card-metric-{stage_id}",
            "x": card_x + 24,
            "y": card_y + 36,
            "width": card_width - 48,
            "text": card_metric,
            "color": line_color,
            "fontSize": 14,
            "hAlign": "left",
            "typeface": "clean",
        },
        {
            "tag": "Textbox",
            "id": f"{prefix}card-body-{stage_id}",
            "x": card_x + 24,
            "y": card_y + 86,
            "width": card_width - 24 - round(card_width * 0.075),
            "text": card_body_overlay,
            "color": "#4B5563",
            "fontSize": 16,
            "hAlign": "left",
            "typeface": "clean",
        },
        {
            "tag": "Textbox",
            "id": f"{prefix}card-product-boundary-{stage_id}",
            "x": card_x + 24,
            "y": card_y + 57,
            "width": card_width - 48,
            "text": product_boundary,
            "color": "#4B5563",
            "fontSize": 14,
            "hAlign": "left",
            "typeface": "clean",
        },
    ]


def build_diagram(spec: JobMapSpec) -> dict:
    representation = spec.representation
    sources = {source.id: source for source in spec.sources}
    scale = shared_bar_scale(spec.maps, representation)
    layouts = plan_layout(spec)
    entities = [_header_entity(spec), *_legend_entities()]
    connections = []

    for job_map, map_layout in zip(spec.maps, layouts):
        state_id = job_map.state.replace("_", "-")
        stage_lookup = {stage.id: stage for stage in job_map.stages}

        if map_layout.heading_y is not None:
            state_label = "Status Quo" if job_map.state == "status_quo" else "After"
            entities.append(
                {
                    "tag": "Textbox",
                    "id": f"state-heading-{state_id}",
                    "x": PHASE_TITLE_X,
                    "y": map_layout.heading_y,
                    "width": 360,
                    "text": state_label,
                    "color": "#111827",
                    "fontSize": STATE_TITLE_FONT_SIZE,
                    "hAlign": "left",
                    "typeface": "rough",
                }
            )

        for lane_layout in map_layout.lanes:
            lane = LANES[lane_layout.name]
            line_color = lane["line_color"]
            fill_color = lane["fill_color"]
            entities.append(
                {
                    "tag": "Textbox",
                    "id": f"{state_id}-lane-{lane_layout.name.lower()}",
                    "x": PHASE_TITLE_X,
                    "y": lane_layout.title_y,
                    "width": 180,
                    "text": lane_layout.name,
                    "color": "#111827",
                    "fontSize": PHASE_TITLE_FONT_SIZE,
                    "hAlign": "left",
                    "typeface": "rough",
                }
            )

            bar_x = PHASE_TITLE_X
            for stage_id, card_x in zip(lane["stages"], lane_layout.card_xs):
                stage = stage_lookup[stage_id]
                bar_width = max(8, round(stage_bar_value(stage, representation) * scale))
                bar_id = f"{state_id}-metric-bar-{stage_id}"
                card_id = f"{state_id}-card-{stage_id}"
                entities.append(
                    {
                        "tag": "Shape",
                        "id": bar_id,
                        "shape": "rectangle",
                        "x": bar_x,
                        "y": lane_layout.bar_y - BAR_HEIGHT // 2,
                        "width": bar_width,
                        "height": BAR_HEIGHT,
                        "color": line_color,
                        "bgColor": line_color,
                        "borderColor": line_color,
                        "styleMode": "plain",
                        "cornerRadius": "round",
                        "texts": [],
                    }
                )
                if stage.outside_product_percent > OUTSIDE_PRODUCT_THRESHOLD:
                    entities.append(
                        _hatch_entity(
                            f"{bar_id}-hatch",
                            bar_x,
                            lane_layout.bar_y - BAR_HEIGHT // 2,
                            bar_width,
                            BAR_HEIGHT,
                            lane["hatch_color"],
                        )
                    )
                connections.append(
                    {
                        "tag": "Relationship",
                        "id": f"{state_id}-bar-card-connector-{stage_id}",
                        "from": bar_id,
                        "fromPort": "bottom",
                        "to": card_id,
                        "toPort": "top",
                        "endArrowhead": None,
                        "connectorStyle": "straight",
                        "cornerStyle": "straight",
                        "lineStyle": "solid",
                        "color": CONNECTOR_COLOR,
                        "lineWidth": CONNECTOR_WIDTH,
                    }
                )
                bar_x += bar_width + BAR_GAP
                entities.extend(
                    _card_entities(
                        stage,
                        state_id,
                        card_x,
                        lane_layout.card_y,
                        lane["card_width"],
                        line_color,
                        fill_color,
                        representation,
                        sources,
                    )
                )

        entities.append(
            {
                "tag": "Textbox",
                "id": f"{state_id}-map-total",
                "x": PHASE_TITLE_X,
                "y": map_layout.total_y,
                "width": 480,
                "text": f"Total: {total_metric_label(job_map.stages, representation)}",
                "color": "#111827",
                "fontSize": PHASE_TITLE_FONT_SIZE,
                "hAlign": "left",
                "typeface": "rough",
            }
        )

    return {"entities": entities, "connections": connections}
