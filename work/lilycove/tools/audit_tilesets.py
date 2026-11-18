#!/usr/bin/env python3
"""Audit map.bin -> metatile usage for Lilycove / Route 121 layouts.

Run from the repository root:
    python3 work/lilycove/tools/audit_tilesets.py

The script is read-only. It validates binary lengths and writes CSV/JSON reports
under work/lilycove/reports/tilesets/.
"""
from __future__ import annotations

import csv
import json
import struct
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LAYOUTS_FILE = ROOT / "data/layouts/layouts.json"
OUT = ROOT / "work/lilycove/reports/tilesets"

TILESET_DIRS = {
    "gTileset_General": "data/tilesets/primary/general",
    "gTileset_Building": "data/tilesets/primary/building",
    "gTileset_Lilycove": "data/tilesets/secondary/lilycove",
    "gTileset_GenericBuilding": "data/tilesets/secondary/generic_building",
    "gTileset_PokemonCenter": "data/tilesets/secondary/pokemon_center",
    "gTileset_Shop": "data/tilesets/secondary/shop",
    "gTileset_Facility": "data/tilesets/secondary/facility",
    "gTileset_LilycoveMuseum": "data/tilesets/secondary/lilycove_museum",
    "gTileset_Contest": "data/tilesets/secondary/contest",
    "gTileset_BattleFrontier": "data/tilesets/secondary/battle_frontier",
}

TARGET_IDS = {
    "LAYOUT_LILYCOVE_CITY",
    "LAYOUT_ROUTE121",
    "LAYOUT_LILYCOVE_CITY_COVE_LILY_MOTEL_1F",
    "LAYOUT_LILYCOVE_CITY_COVE_LILY_MOTEL_2F",
    "LAYOUT_LILYCOVE_CITY_LILYCOVE_MUSEUM_1F",
    "LAYOUT_LILYCOVE_CITY_LILYCOVE_MUSEUM_2F",
    "LAYOUT_LILYCOVE_CITY_CONTEST_LOBBY",
    "LAYOUT_LILYCOVE_CITY_CONTEST_HALL",
    "LAYOUT_POKEMON_CENTER_1F",
    "LAYOUT_POKEMON_CENTER_2F",
    "LAYOUT_MART",
    "LAYOUT_LILYCOVE_CITY_POKEMON_TRAINER_FAN_CLUB",
    "LAYOUT_HARBOR",
    "LAYOUT_HOUSE1",
    "LAYOUT_HOUSE2",
    "LAYOUT_LILYCOVE_CITY_HOUSE2",
    "LAYOUT_LILYCOVE_CITY_DEPARTMENT_STORE_1F",
    "LAYOUT_LILYCOVE_CITY_DEPARTMENT_STORE_2F",
    "LAYOUT_LILYCOVE_CITY_DEPARTMENT_STORE_3F",
    "LAYOUT_LILYCOVE_CITY_DEPARTMENT_STORE_4F",
    "LAYOUT_LILYCOVE_CITY_DEPARTMENT_STORE_5F",
    "LAYOUT_LILYCOVE_CITY_DEPARTMENT_STORE_ROOFTOP",
    "LAYOUT_LILYCOVE_CITY_DEPARTMENT_STORE_ELEVATOR",
    "LAYOUT_ROUTE121_SAFARI_ZONE_ENTRANCE",
}

def read_u16(path: Path) -> list[int]:
    raw = path.read_bytes()
    if len(raw) % 2:
        raise ValueError(f"{path}: tamanho ímpar ({len(raw)} bytes), esperado u16 little-endian")
    return list(struct.unpack("<" + "H" * (len(raw) // 2), raw))

def main() -> None:
    layouts = json.loads(LAYOUTS_FILE.read_text(encoding="utf-8"))["layouts"]
    selected = [x for x in layouts if x["id"] in TARGET_IDS]
    found = {x["id"] for x in selected}
    missing = sorted(TARGET_IDS - found)
    if missing:
        raise SystemExit("Layouts não encontrados em layouts.json: " + ", ".join(missing))

    OUT.mkdir(parents=True, exist_ok=True)
    usage = defaultdict(Counter)
    layout_rows = []
    for layout in selected:
        map_path = ROOT / layout["blockdata_filepath"]
        raw = map_path.read_bytes()
        expected = layout["width"] * layout["height"] * 2
        if len(raw) < expected:
            raise ValueError(
                f"{map_path}: {len(raw)} bytes; esperado pelo menos {expected} "
                f"para {layout['width']}x{layout['height']} células"
            )
        if len(raw) != expected:
            raise ValueError(
                f"{map_path}: tamanho {len(raw)} difere dos {expected} bytes "
                "calculados. Não vou ignorar bytes extras sem identificar o formato."
            )
        cells = struct.unpack("<" + "H" * (len(raw) // 2), raw)
        for packed in cells:
            metatile_id = packed & 0x03FF
            collision = (packed & 0x0C00) >> 10
            elevation = (packed & 0xF000) >> 12
            usage[layout["id"]][metatile_id] += 1
        layout_rows.append({
            "layout_id": layout["id"],
            "width": layout["width"],
            "height": layout["height"],
            "primary_tileset": layout["primary_tileset"],
            "secondary_tileset": layout["secondary_tileset"],
            "map_file": layout["blockdata_filepath"],
            "cells": len(cells),
        })

    with (OUT / "layout-index.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(layout_rows[0]))
        writer.writeheader()
        writer.writerows(layout_rows)

    rows = []
    used_metatiles = defaultdict(set)
    for layout_id, counts in sorted(usage.items()):
        layout = next(x for x in selected if x["id"] == layout_id)
        for metatile_id, count in sorted(counts.items()):
            is_primary = metatile_id < 512
            tileset = layout["primary_tileset"] if is_primary else layout["secondary_tileset"]
            used_metatiles[tileset].add(metatile_id - (0 if is_primary else 512))
            rows.append({
                "layout_id": layout_id,
                "metatile_id_absolute": metatile_id,
                "tileset": tileset,
                "metatile_index_local": metatile_id if is_primary else metatile_id - 512,
                "tileset_side": "primary" if is_primary else "secondary",
                "occurrences": count,
            })

    with (OUT / "metatile-usage.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    composition_rows = []
    for tileset, local_ids in sorted(used_metatiles.items()):
        directory = ROOT / TILESET_DIRS[tileset]
        metatile_words = read_u16(directory / "metatiles.bin")
        attributes = read_u16(directory / "metatile_attributes.bin")
        if len(metatile_words) % 8:
            raise ValueError(f"{tileset}: metatiles.bin não contém registros completos de 8 u16")
        metatile_count = len(metatile_words) // 8
        if len(attributes) != metatile_count:
            raise ValueError(
                f"{tileset}: {metatile_count} metatiles, mas {len(attributes)} atributos"
            )
        for local_id in sorted(local_ids):
            if local_id >= metatile_count:
                raise ValueError(
                    f"{tileset}: índice {local_id} excede {metatile_count - 1}"
                )
            attr = attributes[local_id]
            words = metatile_words[local_id * 8:(local_id + 1) * 8]
            row = {
                "tileset": tileset,
                "metatile_index_local": local_id,
                "attribute_hex": f"0x{attr:04X}",
                "behavior_id": attr & 0x00FF,
                "layer_type": (attr >> 12) & 0x0F,
            }
            for i, word in enumerate(words):
                row[f"tile_{i}_index"] = word & 0x03FF
                row[f"tile_{i}_hflip"] = (word >> 10) & 1
                row[f"tile_{i}_vflip"] = (word >> 11) & 1
                row[f"tile_{i}_palette"] = (word >> 12) & 0x0F
            composition_rows.append(row)

    with (OUT / "metatile-composition.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(composition_rows[0]))
        writer.writeheader()
        writer.writerows(composition_rows)

    summary = {
        "status": "success",
        "layouts_audited": len(selected),
        "layout_cells": sum(x["cells"] for x in layout_rows),
        "distinct_layout_metatile_pairs": len(rows),\n        "distinct_used_metatiles": len(composition_rows),
        "unique_absolute_metatile_ids": sorted({
            int(row["metatile_id_absolute"]) for row in rows
        }),
        "notes": [
            "Metatile ID: bits 0-9; collision: bits 10-11; elevation: bits 12-15.",
            "IDs 0-511 are primary; IDs 512-1023 are secondary (local ID = absolute ID - 512).",
            "Metatile composition includes 8 tile references per metatile: tile index, H/V flip, and palette slot.\",\n            "Attributes expose behavior bits 0-7 and layer type bits 12-15; interpret behavior IDs against the engine constants.");
        ],
    }
    (OUT / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"Relatórios gravados em: {OUT.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
