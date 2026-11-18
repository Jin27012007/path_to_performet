# Inventário de NPCs, sprites e objetos de mapa — Lilycove e Rota 121

**Estado:** inventário de referências de eventos concluído para os 26 mapas catalogados. A identificação dos arquivos-fonte físicos de cada sprite ainda está pendente. Nenhum gráfico foi alterado.

**Método:** leitura dos campos `object_events`, `warp_events`, `coord_events` e `bg_events` nos arquivos `data/maps/<mapa>/map.json`. Os nomes abaixo são os identificadores `graphics_id` usados pelos eventos, não nomes de arquivos PNG confirmados.

## 1. Resumo por mapa

| Mapa | Object events | Warps | Coord events | BG events |
|---|---:|---:|---:|---:|
| LilycoveCity | 22 | 14 | 0 | 13 |
| Route121 | 29 | 1 | 4 | 10 |
| Cove Lily Motel 1F | 1 | 3 | 1 | 0 |
| Cove Lily Motel 2F | 7 | 1 | 0 | 0 |
| Lilycove Museum 1F | 10 | 3 | 0 | 16 |
| Lilycove Museum 2F | 4 | 1 | 0 | 12 |
| Contest Lobby | 25 | 4 | 0 | 12 |
| Contest Hall | 32 | 4 | 0 | 6 |
| Pokémon Center 1F | 5 | 3 | 0 | 0 |
| Pokémon Center 2F | 4 | 3 | 0 | 0 |
| Mart não utilizado | 0 | 2 | 0 | 0 |
| Pokémon Trainer Fan Club | 9 | 2 | 0 | 0 |
| Harbor | 5 | 2 | 0 | 0 |
| Move Deleter's House | 1 | 2 | 0 | 0 |
| House 1 | 2 | 2 | 0 | 0 |
| House 2 | 1 | 2 | 0 | 0 |
| House 3 | 6 | 2 | 0 | 0 |
| House 4 | 2 | 2 | 0 | 0 |
| Department Store 1F | 6 | 4 | 0 | 1 |
| Department Store 2F | 5 | 3 | 0 | 0 |
| Department Store 3F | 5 | 3 | 0 | 0 |
| Department Store 4F | 5 | 3 | 0 | 0 |
| Department Store 5F | 7 | 3 | 0 | 0 |
| Department Store Rooftop | 4 | 1 | 0 | 2 |
| Department Store Elevator | 1 | 2 | 0 | 0 |
| Safari Zone Entrance | 3 | 4 | 1 | 1 |

**Totais:** 201 eventos de objeto, 76 warps, 6 eventos de coordenada e 73 eventos de fundo nos 26 mapas.

## 2. Identificadores gráficos por mapa

Cada identificador representa um tipo de gráfico. A quantidade entre parênteses indica quantas instâncias daquele gráfico existem no mapa.

### Exteriores

**LilycoveCity** — `data/maps/LilycoveCity/map.json`
- `OBJ_EVENT_GFX_SAILOR` (2), `OBJ_EVENT_GFX_GIRL_1` (1), `OBJ_EVENT_GFX_MAN_1` (1), `OBJ_EVENT_GFX_RICH_BOY` (1), `OBJ_EVENT_GFX_MAN_2` (2), `OBJ_EVENT_GFX_WOMAN_2` (1), `OBJ_EVENT_GFX_EXPERT_M` (2), `OBJ_EVENT_GFX_EXPERT_F` (1), `OBJ_EVENT_GFX_AQUA_MEMBER_M` (5), `OBJ_EVENT_GFX_ITEM_BALL` (1), `OBJ_EVENT_GFX_GENTLEMAN` (1), `OBJ_EVENT_GFX_VAR_0` (1), `OBJ_EVENT_GFX_SCHOOL_KID_M` (1), `OBJ_EVENT_GFX_WOMAN_3` (1), `OBJ_EVENT_GFX_FAT_MAN` (1).

**Route121** — `data/maps/Route121/map.json`
- `OBJ_EVENT_GFX_WOMAN_3` (1), `OBJ_EVENT_GFX_BERRY_TREE` (8), `OBJ_EVENT_GFX_LASS` (2), `OBJ_EVENT_GFX_AQUA_MEMBER_M` (3), `OBJ_EVENT_GFX_CUTTABLE_TREE` (3), `OBJ_EVENT_GFX_POKEFAN_F` (1), `OBJ_EVENT_GFX_GENTLEMAN` (1), `OBJ_EVENT_GFX_HEX_MANIAC` (1), `OBJ_EVENT_GFX_BEAUTY` (1), `OBJ_EVENT_GFX_ITEM_BALL` (3), `OBJ_EVENT_GFX_MANIAC` (1), `OBJ_EVENT_GFX_MAN_4` (1), `OBJ_EVENT_GFX_WOMAN_2` (1), `OBJ_EVENT_GFX_MAN_3` (1), `OBJ_EVENT_GFX_WOMAN_5` (1).

### Interiores de Lilycove

**Cove Lily Motel 1F:** `OBJ_EVENT_GFX_MAN_1` (1).

**Cove Lily Motel 2F:** `OBJ_EVENT_GFX_MAN_3` (1), `OBJ_EVENT_GFX_SCIENTIST_1` (1), `OBJ_EVENT_GFX_FAT_MAN` (1), `OBJ_EVENT_GFX_MAN_4` (1), `OBJ_EVENT_GFX_GAMEBOY_KID` (1), `OBJ_EVENT_GFX_WOMAN_2` (1), `OBJ_EVENT_GFX_SCOTT` (1).

**Lilycove Museum 1F:** `OBJ_EVENT_GFX_BEAUTY` (1), `OBJ_EVENT_GFX_GENTLEMAN` (1), `OBJ_EVENT_GFX_SCHOOL_KID_M` (1), `OBJ_EVENT_GFX_ARTIST` (2), `OBJ_EVENT_GFX_NINJA_BOY` (1), `OBJ_EVENT_GFX_WOMAN_4` (1), `OBJ_EVENT_GFX_WOMAN_2` (1), `OBJ_EVENT_GFX_FAT_MAN` (1), `OBJ_EVENT_GFX_PSYCHIC_M` (1).

**Lilycove Museum 2F:** `OBJ_EVENT_GFX_GENTLEMAN` (1), `OBJ_EVENT_GFX_GIRL_2` (1), `OBJ_EVENT_GFX_EXPERT_M` (1), `OBJ_EVENT_GFX_RICH_BOY` (1).

**Contest Lobby:** `OBJ_EVENT_GFX_TEALA` (2), `OBJ_EVENT_GFX_MAN_4` (1), `OBJ_EVENT_GFX_ARTIST` (3), `OBJ_EVENT_GFX_BLACK_BELT` (1), `OBJ_EVENT_GFX_GIRL_2` (1), `OBJ_EVENT_GFX_REPORTER_M` (1), `OBJ_EVENT_GFX_BOY_1` (1), `OBJ_EVENT_GFX_TWIN` (1), `OBJ_EVENT_GFX_FISHERMAN` (1), `OBJ_EVENT_GFX_FAT_MAN` (1), `OBJ_EVENT_GFX_NINJA_BOY` (2), `OBJ_EVENT_GFX_POKEFAN_F` (1), `OBJ_EVENT_GFX_EXPERT_M` (1), `OBJ_EVENT_GFX_GIRL_1` (1), `OBJ_EVENT_GFX_MAN_5` (1), `OBJ_EVENT_GFX_CAMPER` (1), `OBJ_EVENT_GFX_LITTLE_GIRL` (2), `OBJ_EVENT_GFX_SCIENTIST_2` (1), `OBJ_EVENT_GFX_WOMAN_1` (1), `OBJ_EVENT_GFX_OLD_MAN` (1).

**Contest Hall:** `OBJ_EVENT_GFX_BOY_1` (2), `OBJ_EVENT_GFX_BOY_3` (2), `OBJ_EVENT_GFX_GIRL_3` (1), `OBJ_EVENT_GFX_WOMAN_3` (3), `OBJ_EVENT_GFX_CONTEST_JUDGE` (3), `OBJ_EVENT_GFX_BLACK_BELT` (1), `OBJ_EVENT_GFX_EXPERT_M` (1), `OBJ_EVENT_GFX_MANIAC` (1), `OBJ_EVENT_GFX_LINK_RECEPTIONIST` (1), `OBJ_EVENT_GFX_EXPERT_F` (2), `OBJ_EVENT_GFX_WOMAN_5` (1), `OBJ_EVENT_GFX_WOMAN_4` (1), `OBJ_EVENT_GFX_TWIN` (1), `OBJ_EVENT_GFX_PSYCHIC_M` (1), `OBJ_EVENT_GFX_POKEFAN_F` (1), `OBJ_EVENT_GFX_WOMAN_2` (2), `OBJ_EVENT_GFX_WOMAN_1` (1), `OBJ_EVENT_GFX_MAN_1` (2), `OBJ_EVENT_GFX_CAMPER` (1), `OBJ_EVENT_GFX_BOY_2` (1), `OBJ_EVENT_GFX_GIRL_2` (1), `OBJ_EVENT_GFX_LITTLE_GIRL` (1), `OBJ_EVENT_GFX_SAILOR` (1).

**Pokémon Center 1F:** `OBJ_EVENT_GFX_NURSE` (1), `OBJ_EVENT_GFX_BOY_1` (1), `OBJ_EVENT_GFX_MANIAC` (1), `OBJ_EVENT_GFX_VAR_0` (1), `OBJ_EVENT_GFX_VAR_1` (1).

**Pokémon Center 2F:** `OBJ_EVENT_GFX_TEALA` (3), `OBJ_EVENT_GFX_MYSTERY_GIFT_MAN` (1).

**Mart não utilizado:** nenhum evento de objeto.

**Pokémon Trainer Fan Club:** `OBJ_EVENT_GFX_LASS` (1), `OBJ_EVENT_GFX_MAN_4` (1), `OBJ_EVENT_GFX_POKEFAN_M` (1), `OBJ_EVENT_GFX_LITTLE_GIRL` (1), `OBJ_EVENT_GFX_NINJA_BOY` (1), `OBJ_EVENT_GFX_BOY_2` (1), `OBJ_EVENT_GFX_WOMAN_3` (1), `OBJ_EVENT_GFX_EXPERT_F` (1), `OBJ_EVENT_GFX_BOY_1` (1).

**Harbor:** `OBJ_EVENT_GFX_BEAUTY` (1), `OBJ_EVENT_GFX_SS_TIDAL` (1), `OBJ_EVENT_GFX_SAILOR` (2), `OBJ_EVENT_GFX_EXPERT_M` (1).

**Move Deleter's House:** `OBJ_EVENT_GFX_EXPERT_M` (1).

**House 1:** `OBJ_EVENT_GFX_EXPERT_M` (1), `OBJ_EVENT_GFX_KECLEON` (1).

**House 2:** `OBJ_EVENT_GFX_FAT_MAN` (1).

**House 3:** `OBJ_EVENT_GFX_GAMEBOY_KID` (4), `OBJ_EVENT_GFX_POKEFAN_F` (1), `OBJ_EVENT_GFX_MAN_1` (1).

**House 4:** `OBJ_EVENT_GFX_MAN_4` (1), `OBJ_EVENT_GFX_MAN_1` (1).

**Department Store 1F:** `OBJ_EVENT_GFX_BEAUTY` (2), `OBJ_EVENT_GFX_POKEFAN_F` (1), `OBJ_EVENT_GFX_LITTLE_GIRL` (1), `OBJ_EVENT_GFX_POKEFAN_M` (1), `OBJ_EVENT_GFX_AZUMARILL` (1).

**Department Store 2F:** `OBJ_EVENT_GFX_COOK` (1), `OBJ_EVENT_GFX_POKEFAN_F` (1), `OBJ_EVENT_GFX_SAILOR` (1), `OBJ_EVENT_GFX_WOMAN_3` (2).

**Department Store 3F:** `OBJ_EVENT_GFX_RUNNING_TRIATHLETE_M` (1), `OBJ_EVENT_GFX_POKEFAN_M` (1), `OBJ_EVENT_GFX_WOMAN_5` (1), `OBJ_EVENT_GFX_WOMAN_3` (2).

**Department Store 4F:** `OBJ_EVENT_GFX_GENTLEMAN` (1), `OBJ_EVENT_GFX_WOMAN_2` (1), `OBJ_EVENT_GFX_YOUNGSTER` (1), `OBJ_EVENT_GFX_WOMAN_3` (2).

**Department Store 5F:** `OBJ_EVENT_GFX_LITTLE_GIRL` (1), `OBJ_EVENT_GFX_POKEFAN_F` (1), `OBJ_EVENT_GFX_WOMAN_3` (4), `OBJ_EVENT_GFX_WOMAN_2` (1).

**Department Store Rooftop:** `OBJ_EVENT_GFX_MAN_2` (1), `OBJ_EVENT_GFX_MAN_3` (1), `OBJ_EVENT_GFX_ROOFTOP_SALE_WOMAN` (1), `OBJ_EVENT_GFX_WOMAN_3` (1).

**Department Store Elevator:** `OBJ_EVENT_GFX_TEALA` (1).

### Interior associado à Rota 121

**Safari Zone Entrance:** `OBJ_EVENT_GFX_PICNICKER` (1), `OBJ_EVENT_GFX_CAMPER` (2).

## 3. Classes de recursos encontradas

Os identificadores confirmam que os mapas usam uma mistura de:
- NPCs civis, treinadores, funcionários e personagens especiais.
- Personagens de evento: membros da Equipe Aqua, Teala, Scott, juízes de concurso e recepcionista de Link.
- Objetos animados/interativos: árvores de berries, árvores cortáveis, item balls.
- Criaturas/objetos especiais: Kecleon, Azumarill e navio SS Tidal.
- Gráficos variáveis: `OBJ_EVENT_GFX_VAR_0` e `OBJ_EVENT_GFX_VAR_1`; a aparência final pode depender de estado/dados de execução.

A classificação acima é baseada no nome do identificador. A função exata de cada sprite deve ser confirmada na definição da tabela de gráficos e nos arquivos de origem.

## 4. Dependências e riscos de edição

1. Um mesmo `graphics_id` aparece em vários mapas. Editar o recurso original pode alterar todos os mapas que usam aquele identificador.
2. NPCs que compartilham um mesmo gráfico não necessariamente compartilham scripts, movimento, coordenadas ou comportamento.
3. Não confundir `object_events` com `bg_events`: os eventos de fundo podem representar placas, portas, itens ou interações que não usam sprites de personagem.
4. A contagem de `bg_events` não equivale à quantidade de sprites.
5. Os 74 warps, 6 coord events e 60 bg events precisam ser preservados ao reformular layouts e colisões.
6. Não substituir um gráfico variável sem descobrir como a engine escolhe sua aparência.

## 5. Próxima etapa: localizar os arquivos gráficos reais

Para cada identificador, ainda precisamos registrar:
- arquivo de definição do `graphics_id`;
- caminho do sprite-sheet/imagem de origem;
- dimensões e número de frames;
- paleta associada;
- animações e tabela de animação;
- offsets, tamanho do objeto e comportamento de sombra;
- outros mapas que reutilizam o mesmo identificador;
- possibilidade de criar uma cópia exclusiva para Lilycove/Rota 121.

Até essa etapa ser concluída, este inventário permite localizar quais mapas usam cada identificador, mas não autoriza editar diretamente um PNG específico.

## 6. Fontes

- `data/maps/<mapa>/map.json` para cada mapa listado.
- `work/lilycove/asset-index.json` para o escopo dos 26 mapas.
- `include/constants/event_objects.h` e arquivos de definição de gráficos de objetos: localizar e validar na próxima etapa; caminhos ainda não confirmados neste inventário.
