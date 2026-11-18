# Map binary format audit — Lilycove / Route 121

## Findings

The workspace index contains **26 map entries**. Those entries resolve to **24 unique layouts**, because House1 and House4 share `LAYOUT_HOUSE1`, while Move Deleter's House and House3 share `LAYOUT_HOUSE2`.

The map grid format is confirmed by the source:
- `include/global.fieldmap.h` defines each map-grid cell as a 16-bit value: 10-bit metatile ID, 2-bit collision, and 4-bit elevation.
- `include/global.fieldmap.h` defines `struct MapLayout` with explicit width, height, and a `const u16 *map`.
- `src/fieldmap.c`, in `InitMapLayoutData` and `InitBackupMapLayoutData`, copies exactly `width * 2` bytes for each of `height` rows. Therefore the active map grid consumes exactly `width * height * 2` bytes from the beginning of its map data.

## File-size comparison

The byte counts below were calculated from the GitHub Base64 file contents after removing line breaks and decoding the Base64 payload. “Expected” is the layout's declared width × height × 2.

| Layout | Declared size | Expected bytes | File bytes | Bytes after active grid |
|---|---:|---:|---:|---:|
| LAYOUT_LILYCOVE_CITY | 80×40 | 6,400 | 6,400 | 0 |
| LAYOUT_ROUTE121 | 80×20 | 3,200 | 4,385 | 1,185 |
| LAYOUT_LILYCOVE_CITY_COVE_LILY_MOTEL_1F | 12×9 | 216 | 230 | 14 |
| LAYOUT_LILYCOVE_CITY_COVE_LILY_MOTEL_2F | 12×9 | 216 | 231 | 15 |
| LAYOUT_LILYCOVE_CITY_LILYCOVE_MUSEUM_1F | 21×14 | 588 | 590 | 2 |
| LAYOUT_LILYCOVE_CITY_LILYCOVE_MUSEUM_2F | 22×13 | 572 | 656 | 84 |
| LAYOUT_LILYCOVE_CITY_CONTEST_LOBBY | 31×12 | 744 | 798 | 54 |
| LAYOUT_LILYCOVE_CITY_CONTEST_HALL | 51×33 | 3,366 | 3,423 | 57 |
| LAYOUT_POKEMON_CENTER_1F | 14×9 | 252 | 261 | 9 |
| LAYOUT_POKEMON_CENTER_2F | 14×10 | 280 | 328 | 48 |
| LAYOUT_MART | 11×8 | 176 | 176 | 0 |
| LAYOUT_LILYCOVE_CITY_POKEMON_TRAINER_FAN_CLUB | 12×14 | 336 | 353 | 17 |
| LAYOUT_HARBOR | 24×15 | 720 | 785 | 65 |
| LAYOUT_HOUSE2 | 11×8 | 176 | 193 | 17 |
| LAYOUT_HOUSE1 | 10×9 | 180 | 202 | 22 |
| LAYOUT_LILYCOVE_CITY_HOUSE2 | 8×8 | 128 | 146 | 18 |
| LAYOUT_LILYCOVE_CITY_DEPARTMENT_STORE_1F | 18×8 | 288 | 431 | 143 |
| LAYOUT_LILYCOVE_CITY_DEPARTMENT_STORE_2F | 18×8 | 288 | 332 | 44 |
| LAYOUT_LILYCOVE_CITY_DEPARTMENT_STORE_3F | 18×8 | 288 | 368 | 80 |
| LAYOUT_LILYCOVE_CITY_DEPARTMENT_STORE_4F | 18×8 | 288 | 330 | 42 |
| LAYOUT_LILYCOVE_CITY_DEPARTMENT_STORE_5F | 18×8 | 288 | 288 | 0 |
| LAYOUT_LILYCOVE_CITY_DEPARTMENT_STORE_ROOFTOP | 18×12 | 432 | 531 | 99 |
| LAYOUT_LILYCOVE_CITY_DEPARTMENT_STORE_ELEVATOR | 5×6 | 60 | 60 | 0 |
| LAYOUT_ROUTE121_SAFARI_ZONE_ENTRANCE | 18×14 | 504 | 659 | 155 |

## Auditor behavior

The auditor now derives its target layouts from `work/lilycove/asset-index.json`; it no longer maintains a hard-coded layout list. It validates that all referenced layout IDs exist in `data/layouts/layouts.json`.

For each `map.bin`, it:
1. Requires at least `width * height * 2` bytes.
2. Decodes only the active grid prefix, matching the runtime copy loop.
3. Records any bytes after that prefix in the layout report and `summary.json`; it does not delete or silently discard them.
4. Exports one row per active grid cell, with coordinates, metatile ID, collision, and elevation.

Generated reports:
- `layout-index.csv`
- `map-cells.csv`
- `metatile-usage.csv`
- `metatile-composition.csv`
- `collision-usage.csv`
- `elevation-usage.csv`
- `summary.json`

**Execution status:** the corrected script has been committed, but it has not yet been run in a complete repository checkout. The file-size comparison above is a direct inspection of the 24 indexed map binaries, not output from the script.
