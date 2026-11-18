# Auditoria de dependências gráficas — Lilycove e Centro de Concursos

**Estado:** levantamento estrutural inicial, sem edição de gráficos ou de código executável.  
**Base consultada:** branch `work/lilycove-route121-workspace`.

## 1. Fachada externa de Lilycove

O mapa externo `MAP_LILYCOVE_CITY` usa o layout `LAYOUT_LILYCOVE_CITY`. A combinação definida em `data/layouts/layouts.json` é:

- Primário: `gTileset_General` — `data/tilesets/primary/general/`
- Secundário: `gTileset_Lilycove` — `data/tilesets/secondary/lilycove/`

Portanto, a folha `secondary/lilycove/tiles.png` é relevante para o exterior da cidade, mas não é exclusiva do mapa de Lilycove.

### Uso compartilhado de `gTileset_Lilycove`

A tabela de layouts contém **10 layouts** com esse tileset secundário:

- `LAYOUT_LILYCOVE_CITY`
- `LAYOUT_ROUTE121`
- `LAYOUT_ROUTE122`
- `LAYOUT_ROUTE123`
- `LAYOUT_SAFARI_ZONE_NORTHWEST`
- `LAYOUT_SAFARI_ZONE_NORTH`
- `LAYOUT_SAFARI_ZONE_SOUTHWEST`
- `LAYOUT_SAFARI_ZONE_SOUTH`
- `LAYOUT_SAFARI_ZONE_NORTHEAST`
- `LAYOUT_SAFARI_ZONE_SOUTHEAST`

**Consequência:** editar `secondary/lilycove/tiles.png` pode alterar também as Rotas 121, 122 e 123 e as seis áreas da Safari Zone. Antes de modificar uma peça, é necessário saber se ela aparece em algum desses mapas.

## 2. Interior do Centro de Concursos de Lilycove

O mapa `MAP_LILYCOVE_CITY_CONTEST_HALL` usa `LAYOUT_LILYCOVE_CITY_CONTEST_HALL`, com **51 × 33** blocos. A combinação de tilesets é:

- Primário: `gTileset_Building` — `data/tilesets/primary/building/`
- Secundário: `gTileset_Contest` — `data/tilesets/secondary/contest/`

O lobby `MAP_LILYCOVE_CITY_CONTEST_LOBBY` usa a mesma combinação, com layout de **31 × 12**.

Arquivos gráficos e dados confirmados:

- `data/tilesets/primary/building/tiles.png`
- `data/tilesets/primary/building/metatiles.bin`
- `data/tilesets/primary/building/metatile_attributes.bin`
- `data/tilesets/secondary/contest/tiles.png`
- `data/tilesets/secondary/contest/metatiles.bin`
- `data/tilesets/secondary/contest/metatile_attributes.bin`

### Uso compartilhado de `gTileset_Contest`

A tabela de layouts contém **19 layouts** com o tileset secundário `gTileset_Contest`. Entre eles estão:

- Lilycove: `LAYOUT_LILYCOVE_CITY_CONTEST_LOBBY` e `LAYOUT_LILYCOVE_CITY_CONTEST_HALL`
- Salas de concurso: `LAYOUT_CONTEST_HALL`, `LAYOUT_CONTEST_HALL_BEAUTY`, `LAYOUT_CONTEST_HALL_TOUGH`, `LAYOUT_CONTEST_HALL_COOL`, `LAYOUT_CONTEST_HALL_SMART` e `LAYOUT_CONTEST_HALL_CUTE`
- Layouts nomeados como não utilizados e sobras: seis `LAYOUT_UNUSED_CONTEST_HALL*`, três `LAYOUT_UNUSED_CONTEST_ROOM*` e dois layouts `FALLARBOR_TOWN_LEFTOVER_RSCONTEST*`

O grupo de mapas também declara `ContestHall`, as cinco salas por categoria e `UnusedContestHall1` a `UnusedContestHall6`, além dos dois mapas de Lilycove.

**Consequência:** editar `secondary/contest/tiles.png` pode modificar outros ambientes de concurso, não apenas o Centro de Concursos de Lilycove.

## 3. O risco maior: `gTileset_Building`

O tileset primário `gTileset_Building` aparece em **179 layouts** da tabela. É um recurso amplamente compartilhado por interiores de várias cidades e instalações.

**Consequência:** não redesenhar `primary/building/tiles.png` globalmente para resolver um problema visual exclusivo de Lilycove. Isso pode mudar muitos edifícios fora da área de trabalho.

## 4. Decisão técnica recomendada

Para uma reformulação exclusiva de Lilycove:

1. Não editar ainda os PNGs compartilhados.
2. Identificar os metatiles e os índices realmente usados pelo mapa-alvo.
3. Marcar cada elemento como exclusivo, compartilhado localmente ou compartilhado globalmente.
4. Se a mudança precisar ser exclusiva, avaliar a criação de um tileset separado e a atualização do layout correspondente, mantendo intactos os tilesets compartilhados.
5. Testar mapas que compartilham os mesmos tilesets antes de integrar qualquer alteração.

## 5. O que ainda não foi concluído

Este levantamento identifica as dependências por layout e tileset, mas **ainda não identifica os índices exatos dos metatiles que formam cada parte da fachada ou do interior**. Isso exige cruzar os dados binários de cada layout com a tabela de metatiles. Não editar a folha de tiles com base apenas neste documento.

## Fontes do repositório

- [Mapa externo de Lilycove](../../../data/maps/LilycoveCity/map.json)
- [Mapa interno do Centro de Concursos](../../../data/maps/LilycoveCity_ContestHall/map.json)
- [Lobby do Centro de Concursos](../../../data/maps/LilycoveCity_ContestLobby/map.json)
- [Tabela central de layouts](../../../data/layouts/layouts.json)
- [Grupos de mapas](../../../data/maps/map_groups.json)
- [Tileset secundário de Lilycove](../../../data/tilesets/secondary/lilycove/tiles.png)
- [Tileset secundário de Concursos](../../../data/tilesets/secondary/contest/tiles.png)
- [Tileset primário de edifícios](../../../data/tilesets/primary/building/tiles.png)
