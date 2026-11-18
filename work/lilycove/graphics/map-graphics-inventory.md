# Inventário gráfico — Lilycove e Rota 121

**Estado:** inventário estrutural dos mapas, layouts e tilesets. Nenhum gráfico ou fonte executável foi alterado.  
**Fontes:** `data/maps/map_groups.json`, `data/maps/*/map.json` e `data/layouts/layouts.json`.

## 1. Mapas externos

| Mapa | Layout | Dimensões | Tileset primário | Tileset secundário |
|---|---|---:|---|---|
| Lilycove City | `LAYOUT_LILYCOVE_CITY` | 80 × 40 | `gTileset_General` | `gTileset_Lilycove` |
| Route 121 | `LAYOUT_ROUTE121` | 80 × 20 | `gTileset_General` | `gTileset_Lilycove` |

## 2. Interiores de Lilycove

| Mapa | Layout | Dimensões | Tileset primário | Tileset secundário |
|---|---|---:|---|---|
| Cove Lily Motel 1F | `LAYOUT_LILYCOVE_CITY_COVE_LILY_MOTEL_1F` | 12 × 9 | `gTileset_Building` | `gTileset_GenericBuilding` |
| Cove Lily Motel 2F | `LAYOUT_LILYCOVE_CITY_COVE_LILY_MOTEL_2F` | 12 × 9 | `gTileset_Building` | `gTileset_GenericBuilding` |
| Lilycove Museum 1F | `LAYOUT_LILYCOVE_CITY_LILYCOVE_MUSEUM_1F` | 21 × 14 | `gTileset_Building` | `gTileset_LilycoveMuseum` |
| Lilycove Museum 2F | `LAYOUT_LILYCOVE_CITY_LILYCOVE_MUSEUM_2F` | 22 × 13 | `gTileset_Building` | `gTileset_LilycoveMuseum` |
| Contest Lobby | `LAYOUT_LILYCOVE_CITY_CONTEST_LOBBY` | 31 × 12 | `gTileset_Building` | `gTileset_Contest` |
| Contest Hall | `LAYOUT_LILYCOVE_CITY_CONTEST_HALL` | 51 × 33 | `gTileset_Building` | `gTileset_Contest` |
| Pokémon Center 1F | `LAYOUT_POKEMON_CENTER_1F` | 14 × 9 | `gTileset_Building` | `gTileset_PokemonCenter` |
| Pokémon Center 2F | `LAYOUT_POKEMON_CENTER_2F` | 14 × 10 | `gTileset_Building` | `gTileset_PokemonCenter` |
| Mart não utilizado | `LAYOUT_MART` | 11 × 8 | `gTileset_Building` | `gTileset_Shop` |
| Pokémon Trainer Fan Club | `LAYOUT_LILYCOVE_CITY_POKEMON_TRAINER_FAN_CLUB` | 12 × 14 | `gTileset_Building` | `gTileset_GenericBuilding` |
| Harbor | `LAYOUT_HARBOR` | 24 × 15 | `gTileset_General` | `gTileset_Facility` |
| Move Deleter's House | `LAYOUT_HOUSE2` | 11 × 8 | `gTileset_Building` | `gTileset_GenericBuilding` |
| House 1 | `LAYOUT_HOUSE1` | 10 × 9 | `gTileset_Building` | `gTileset_GenericBuilding` |
| House 2 | `LAYOUT_LILYCOVE_CITY_HOUSE2` | 8 × 8 | `gTileset_Building` | `gTileset_GenericBuilding` |
| House 3 | `LAYOUT_HOUSE2` | 11 × 8 | `gTileset_Building` | `gTileset_GenericBuilding` |
| House 4 | `LAYOUT_HOUSE1` | 10 × 9 | `gTileset_Building` | `gTileset_GenericBuilding` |
| Department Store 1F | `LAYOUT_LILYCOVE_CITY_DEPARTMENT_STORE_1F` | 18 × 8 | `gTileset_Building` | `gTileset_Shop` |
| Department Store 2F | `LAYOUT_LILYCOVE_CITY_DEPARTMENT_STORE_2F` | 18 × 8 | `gTileset_Building` | `gTileset_Shop` |
| Department Store 3F | `LAYOUT_LILYCOVE_CITY_DEPARTMENT_STORE_3F` | 18 × 8 | `gTileset_Building` | `gTileset_Shop` |
| Department Store 4F | `LAYOUT_LILYCOVE_CITY_DEPARTMENT_STORE_4F` | 18 × 8 | `gTileset_Building` | `gTileset_Shop` |
| Department Store 5F | `LAYOUT_LILYCOVE_CITY_DEPARTMENT_STORE_5F` | 18 × 8 | `gTileset_Building` | `gTileset_Shop` |
| Department Store Rooftop | `LAYOUT_LILYCOVE_CITY_DEPARTMENT_STORE_ROOFTOP` | 18 × 12 | `gTileset_Building` | `gTileset_Shop` |
| Department Store Elevator | `LAYOUT_LILYCOVE_CITY_DEPARTMENT_STORE_ELEVATOR` | 5 × 6 | `gTileset_Building` | `gTileset_BattleFrontier` |

## 3. Interior associado à Rota 121

| Mapa | Layout | Dimensões | Tileset primário | Tileset secundário |
|---|---|---:|---|---|
| Safari Zone Entrance | `LAYOUT_ROUTE121_SAFARI_ZONE_ENTRANCE` | 18 × 14 | `gTileset_Building` | `gTileset_Shop` |

## 4. Quantidade de layouts que referenciam cada tileset

Os números abaixo contam **definições de layout** em `data/layouts/layouts.json`, não mapas ativos. A lista contém também layouts não utilizados, protótipos e sobras.

| Tileset | Papel | Layouts que o referenciam |
|---|---|---:|
| `gTileset_General` | Primário | 238 |
| `gTileset_Building` | Primário | 179 |
| `gTileset_Lilycove` | Secundário | 10 |
| `gTileset_GenericBuilding` | Secundário | 38 |
| `gTileset_PokemonCenter` | Secundário | 4 |
| `gTileset_Shop` | Secundário | 10 |
| `gTileset_Facility` | Secundário | 26 |
| `gTileset_LilycoveMuseum` | Secundário | 2 |
| `gTileset_Contest` | Secundário | 19 |
| `gTileset_BattleFrontier` | Secundário | 12 |

## 5. Reutilização confirmada

- `LAYOUT_HOUSE1` é usado por House 1 e House 4 de Lilycove.
- `LAYOUT_HOUSE2` é usado por Move Deleter's House e House 3 de Lilycove.
- `gTileset_Lilycove` também aparece em seis setores da Safari Zone, além das Rotas 122 e 123.
- `gTileset_Contest` também aparece em salas de concurso e layouts não utilizados/protótipos.
- `gTileset_Building` é um tileset primário amplo, referenciado por 179 definições de layout no projeto.

## 6. Como usar este inventário

Este documento indica **quais arquivos investigar**, não quais pixels devem ser alterados. Antes de editar um prédio:

1. Confirmar o mapa e seu layout nesta tabela.
2. Abrir os dois tilesets correspondentes.
3. Rastrear os metatiles usados pelo layout e seus atributos.
4. Verificar se o tileset ou layout é reutilizado fora do mapa-alvo.
5. Escolher entre manter a alteração compartilhada ou separar o recurso em um tileset/layout próprio.

A auditoria de dependências específicas do Centro de Concursos está em [contest-hall-dependencies.md](contest-hall-dependencies.md).
