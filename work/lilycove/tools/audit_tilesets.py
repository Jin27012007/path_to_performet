#!/usr/bin/env python3
"""Audit Lilycove / Route 121 map.bin data and metatile dependencies.

Run from the repository root:
    python3 work/lilycove/tools/audit_tilesets.py

The script is read-only with respect to source assets. It writes CSV/JSON
reports under work/lilycove/reports/tilesets/.
"""
from __future__ import annotations

import csv
import json
import struct
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ASSET_INDEX_FILE = ROOT / "work/lilycove/asset-index.json"
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


def read_u16(path: Path) -> list[int]:
    raw = path.read_bytes()
    if len(raw) % 2:
        raise ValueError(
            f"{path}: tamanho ímpar ({len(raw)} bytes); "
            "o arquivo deveria conter valores u16 little-endian completos"
        )
    count = len(raw) // 2
    return list(struct.unpack("<" + "H" * count, raw))


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise ValueError(f"Não há linhas para gravar em {path.name}")
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def load_target_layouts() -> tuple[list[dict], dict[str, list[str]], int]:
    asset = json.loads(ASSET_INDEX_FILE.read_text(encoding="utf-8"))
    map_entries = asset.get("maps", [])
    if not map_entries:
        raise ValueError(f"{ASSET_INDEX_FILE}: lista maps ausente ou vazia")

    declared_total = asset.get("scope", {}).get("totalMapEntries")
    if declared_total is not None and declared_total != len(map_entries):
        raise ValueError(
            f"asset-index declara {declared_total} mapas, mas contém "
            f"{len(map_entries)} entradas"
        )

    map_names_by_layout: dict[str, list[str]] = defaultdict(list)
    for entry in map_entries:
        map_name = entry.get("name")
        layout_id = entry.get("layout")
        if not map_name or not layout_id:
            raise ValueError(f"Entrada de mapa incompleta no asset-index: {entry}")
        map_names_by_layout[layout_id].append(map_name)

    source = json.loads(LAYOUTS_FILE.read_text(encoding="utf-8"))
    layouts_by_id = {
        entry["id"]: entry
        for entry in source.get("layouts", [])
        if "id" in entry
    }

    missing = sorted(set(map_names_by_layout) - set(layouts_by_id))
    if missing:
        raise ValueError(
            "Layouts do asset-index não encontrados em layouts.json: "
            + ", ".join(missing)
        )

    selected = [layouts_by_id[layout_id] for layout_id in map_names_by_layout]
    return selected, dict(map_names_by_layout), len(map_entries)


def main() -> None:
    selected, map_names_by_layout, map_entry_count = load_target_layouts()

    OUT.mkdir(parents=True, exist_ok=True)
    usage: dict[str, Counter] = defaultdict(Counter)
    collision_usage: dict[str, Counter] = defaultdict(Counter)
    elevation_usage: dict[str, Counter] = defaultdict(Counter)
    layout_rows: list[dict] = []
    cell_rows: list[dict] = []
    trailing_data: list[dict] = []

    for layout in selected:
        layout_id = layout["id"]
        map_path = ROOT / layout["blockdata_filepath"]
        raw = map_path.read_bytes()
        width = int(layout["width"])
        height = int(layout["height"])
        if width <= 0 or height <= 0:
            raise ValueError(f"{layout_id}: dimensões inválidas {width}x{height}")

        expected_size = width * height * 2
        if len(raw) < expected_size:
            raise ValueError(
                f"{map_path}: {len(raw)} bytes; são necessários pelo menos "
                f"{expected_size} bytes para {width}x{height} células u16"
            )

        # The engine copies exactly width * 2 bytes for each of height rows.
        # Therefore bytes after this range are not part of the active map grid.
        map_data = raw[:expected_size]
        tail = raw[expected_size:]
        if tail:
            trailing_data.append({
                "layout_id": layout_id,
                "map_file": layout["blockdata_filepath"],
                "map_bytes": len(raw),
                "consumed_bytes": expected_size,
                "trailing_bytes": len(tail),
                "trailing_hex_preview": tail[:32].hex(" "),
            })

        for index, (packed,) in enumerate(struct.iter_unpack("<H", map_data)):
            x = index % width
            y = index // width
            metatile_id = packed & 0x03FF
            collision = (packed & 0x0C00) >> 10
            elevation = (packed & 0xF000) >> 12
            usage[layout_id][metatile_id] += 1
            collision_usage[layout_id][collision] += 1
            elevation_usage[layout_id][elevation] += 1
            cell_rows.append({
                "layout_id": layout_id,
                "x": x,
                "y": y,
                "packed_hex": f"0x{packed:04X}",
                "metatile_id_absolute": metatile_id,
                "collision": collision,
                "elevation": elevation,
            })

        primary = layout.get("primary_tileset")
        secondary = layout.get("secondary_tileset")
        if primary not in TILESET_DIRS or secondary not in TILESET_DIRS:
            raise ValueError(
                f"{layout_id}: tileset não catalogado "
                f"(primary={primary}, secondary={secondary})"
            )

        layout_rows.append({
            "layout_id": layout_id,
            "map_names": ";".join(map_names_by_layout[layout_id]),
            "width": width,
            "height": height,
            "primary_tileset": primary,
            "secondary_tileset": secondary,
            "map_file": layout["blockdata_filepath"],
            "expected_map_bytes": expected_size,
            "actual_map_bytes": len(raw),
            "trailing_bytes": len(tail),
            "cells_audited": width * height,
        })

    rows: list[dict] = []
    used_metatiles: dict[str, set[int]] = defaultdict(set)
    layout_by_id = {layout["id"]: layout for layout in selected}

    for layout_id, counts in sorted(usage.items()):
        layout = layout_by_id[layout_id]
        for metatile_id, count in sorted(counts.items()):
            is_primary = metatile_id < 512
            tileset = (
                layout["primary_tileset"]
                if is_primary
                else layout["secondary_tileset"]
            )
            local_id = metatile_id if is_primary else metatile_id - 512
            used_metatiles[tileset].add(local_id)
            rows.append({
                "layout_id": layout_id,
                "map_names": ";".join(map_names_by_layout[layout_id]),
                "metatile_id_absolute": metatile_id,
                "tileset": tileset,
                "metatile_index_local": local_id,
                "tileset_side": "primary" if is_primary else "secondary",
                "occurrences": count,
            })

    composition_rows: list[dict] = []
    tileset_summary: dict[str, dict] = {}
    for tileset, local_ids in sorted(used_metatiles.items()):
        directory = ROOT / TILESET_DIRS[tileset]
        metatile_words = read_u16(directory / "metatiles.bin")
        attributes = read_u16(directory / "metatile_attributes.bin")
        if len(metatile_words) % 8:
            raise ValueError(
                f"{tileset}: metatiles.bin contém {len(metatile_words)} u16; "
                "o total não é divisível pelos 8 tiles de cada metatile"
            )
        metatile_count = len(metatile_words) // 8
        if len(attributes) != metatile_count:
            raise ValueError(
                f"{tileset}: {metatile_count} metatiles, mas "
                f"{len(attributes)} atributos"
            )

        tileset_summary[tileset] = {
            "metatile_count": metatile_count,
            "attribute_count": len(attributes),
            "used_local_metatiles": len(local_ids),
        }

        for local_id in sorted(local_ids):
            if local_id >= metatile_count:
                raise ValueError(
                    f"{tileset}: índice local {local_id} excede "
                    f"{metatile_count - 1}"
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
            for slot, word in enumerate(words):
                row[f"tile_{slot}_index"] = word & 0x03FF
                row[f"tile_{slot}_hflip"] = (word >> 10) & 1
                row[f"tile_{slot}_vflip"] = (word >> 11) & 1
                row[f"tile_{slot}_palette"] = (word >> 12) & 0x0F
            composition_rows.append(row)

    collision_rows = []
    elevation_rows = []
    for layout_id in sorted(collision_usage):
        for value, count in sorted(collision_usage[layout_id].items()):
            collision_rows.append({
                "layout_id": layout_id,
                "collision_value": value,
                "cells": count,
            })
        for value, count in sorted(elevation_usage[layout_id].items()):
            elevation_rows.append({
                "layout_id": layout_id,
                "elevation_value": value,
                "cells": count,
            })

    write_csv(OUT / "layout-index.csv", layout_rows)
    write_csv(OUT / "map-cells.csv", cell_rows)
    write_csv(OUT / "metatile-usage.csv", rows)
    write_csv(OUT / "metatile-composition.csv", composition_rows)
    write_csv(OUT / "collision-usage.csv", collision_rows)
    write_csv(OUT / "elevation-usage.csv", elevation_rows)

    summary = {
        "status": "success_with_warnings" if trailing_data else "success",
        "map_entries_in_asset_index": map_entry_count,
        "unique_layouts_audited": len(selected),
        "layout_cells_audited": sum(row["cells_audited"] for row in layout_rows),
        "distinct_layout_metatile_pairs": len(rows),
        "distinct_used_metatiles": len(composition_rows),
        "tilesets_used": tileset_summary,
        "trailing_data_files": trailing_data,
        "notes": [
            "Cada célula do mapa é um u16 little-endian: metatile bits 0-9, colisão bits 10-11 e elevação bits 12-15.",
            "O motor copia exatamente width * 2 bytes por linha durante height linhas; bytes posteriores ao bloco width * height não fazem parte da grade carregada.",
            "IDs 0-511 usam o tileset primário; IDs 512-1023 usam o secundário, com índice local igual ao ID absoluto menos 512.",
            "Cada metatile tem 8 referências u16; cada referência contém índice do tile, flips H/V e slot de paleta.",
            "Atributos de metatile Emerald: comportamento nos bits 0-7 e tipo de camada nos bits 12-15.",
            "Arquivos com bytes excedentes são reportados; os bytes extras não são apagados nem incluídos na análise da grade.",
        ],
    }
    (OUT / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"Relatórios gravados em: {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
