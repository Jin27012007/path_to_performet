# Mapas e layouts

## Mapas externos principais

| Mapa | Fonte |
|---|---|
| Lilycove City | [map.json](../../../data/maps/LilycoveCity/map.json) · [scripts.inc](../../../data/maps/LilycoveCity/scripts.inc) |
| Route 121 | [map.json](../../../data/maps/Route121/map.json) · scripts em `data/maps/Route121/` quando existentes |

Os mapas externos estão conectados entre si. Lilycove também aponta para Route 124. Route 121 aponta para Route 120 e Route 122. Essas conexões são dependências de transição; não apagar os mapas vizinhos nem remover os destinos sem decidir como serão tratados na ROM.

## Interiores de Lilycove

Todos os nomes abaixo vêm do grupo `gMapGroup_IndoorLilycove` em [map_groups.json](../../../data/maps/map_groups.json). Cada mapa tem seu diretório próprio em `data/maps/<nome>/`, com `map.json` e scripts quando definidos.

- `LilycoveCity_CoveLilyMotel_1F`
- `LilycoveCity_CoveLilyMotel_2F`
- `LilycoveCity_LilycoveMuseum_1F`
- `LilycoveCity_LilycoveMuseum_2F`
- `LilycoveCity_ContestLobby`
- `LilycoveCity_ContestHall`
- `LilycoveCity_PokemonCenter_1F`
- `LilycoveCity_PokemonCenter_2F`
- `LilycoveCity_UnusedMart` — mapa listado no grupo; confirmar se continua inacessível antes de alterar.
- `LilycoveCity_PokemonTrainerFanClub`
- `LilycoveCity_Harbor`
- `LilycoveCity_MoveDeletersHouse`
- `LilycoveCity_House1`
- `LilycoveCity_House2`
- `LilycoveCity_House3`
- `LilycoveCity_House4`
- `LilycoveCity_DepartmentStore_1F`
- `LilycoveCity_DepartmentStore_2F`
- `LilycoveCity_DepartmentStore_3F`
- `LilycoveCity_DepartmentStore_4F`
- `LilycoveCity_DepartmentStore_5F`
- `LilycoveCity_DepartmentStoreRooftop`
- `LilycoveCity_DepartmentStoreElevator`

## Interior da Rota 121

- `Route121_SafariZoneEntrance`

## Layouts e arquivos de mapa

A tabela central é [data/layouts/layouts.json](../../../data/layouts/layouts.json). Ela associa cada layout à largura, altura, tileset primário/secundário e aos arquivos binários de borda e blocos.

Layouts externos confirmados:
- Lilycove: `data/layouts/LilycoveCity/map.bin` e `border.bin` (80 × 40).
- Route 121: `data/layouts/Route121/map.bin` e `border.bin` (80 × 20).

Layouts genéricos são compartilhados. Exemplos: `LAYOUT_HOUSE1` é usado por House1 e House4; `LAYOUT_HOUSE2` é usado pelo Move Deleter e House3. Pokémon Centers, Mart e Harbor também usam layouts genéricos. Alterar um desses layouts pode afetar outros mapas além de Lilycove.

## Regras

- Não mudar largura/altura sem atualizar e validar o layout.
- Não apagar conexões para Route 120, 122 ou 124 por engano.
- Mudanças de cenário devem considerar bordas, blocos, metatiles e colisões.
- Confirmar os mapas internos usados por warps antes de modificar edifícios.
