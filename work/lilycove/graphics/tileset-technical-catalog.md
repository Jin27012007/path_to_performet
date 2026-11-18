# Catálogo técnico completo dos tilesets — Lilycove e Rota 121

**Escopo:** os 26 mapas da área Lilycove / Rota 121 e os 10 tilesets referenciados pelos seus layouts.  
**Branch:** `work/lilycove-route121-workspace`  
**Estado:** estrutura dos 10 tilesets catalogada; foi adicionado um auditor reproduzível para cruzar mapas, metatiles, referências de tiles e atributos. O relatório ainda precisa ser executado no Codespaces. Nenhum PNG, metatile, paleta, atributo ou fonte executável foi editado.

## 1. Como a engine organiza os gráficos

Um layout aponta para dois tilesets: um **primário** e um **secundário**. O mapa não guarda imagens de metatiles; guarda IDs numéricos que apontam para essas duas coleções.

Estrutura confirmada no código:
- `include/fieldmap.h`: `NUM_METATILES_IN_PRIMARY = 512`, `NUM_METATILES_TOTAL = 1024` e `NUM_TILES_PER_METATILE = 8`.
- `include/global.fieldmap.h`: cada célula de `map.bin` é um valor de 16 bits com ID de metatile nos bits 0–9, colisão nos bits 10–11 e elevação nos bits 12–15.
- `include/global.fieldmap.h`: atributos de metatile guardam comportamento nos bits 0–7 e tipo de camada nos bits 12–15.
- `src/data/tilesets/headers.h`: associa cada tileset às suas imagens, paletas, metatiles, atributos e callback de animação.
- `src/data/tilesets/graphics.h`: indica como os PNGs e paletas são convertidos para os dados usados pela ROM.

Regra de endereçamento dos metatiles:
- IDs de 0 a 511 pertencem ao tileset primário.
- IDs de 512 a 1023 pertencem ao secundário.
- Para obter o índice local do secundário, subtrai-se 512 ao ID absoluto.
- Cada registro em `metatiles.bin` ocupa 16 bytes (oito referências de tile de 16 bits).
- Cada registro em `metatile_attributes.bin` ocupa 2 bytes (um atributo de 16 bits).

**Atenção:** os oito elementos armazenados por metatile não devem ser reorganizados. A ordem das referências, os bits de flip e os índices de paleta fazem parte da montagem visual. A imagem `tiles.png` é apenas a folha de tiles; não descreve sozinha como um metatile aparece no mapa.

## 2. Os 10 tilesets realmente usados

As dimensões foram lidas do cabeçalho PNG; as quantidades de metatiles e atributos foram calculadas pelos tamanhos dos respectivos arquivos binários. Os PNGs são folhas indexadas de 4 bits por pixel (4bpp), com tiles de 8×8 pixels.

| ID na engine | Papel | Folha PNG | Grade de tiles | Tiles na folha | Metatiles | Registros de atributos |
|---|---|---|---:|---:|---:|---:|
| `gTileset_General` | Primário | [tiles.png](../../../data/tilesets/primary/general/tiles.png) | 16 × 32 | 512 | 512 | 512 |
| `gTileset_Building` | Primário | [tiles.png](../../../data/tilesets/primary/building/tiles.png) | 16 × 32 | 512 | 8 | 8 |
| `gTileset_Lilycove` | Secundário | [tiles.png](../../../data/tilesets/secondary/lilycove/tiles.png) | 16 × 27 | 432 | 351 | 351 |
| `gTileset_GenericBuilding` | Secundário | [tiles.png](../../../data/tilesets/secondary/generic_building/tiles.png) | 16 × 32 | 512 | 512 | 512 |
| `gTileset_PokemonCenter` | Secundário | [tiles.png](../../../data/tilesets/secondary/pokemon_center/tiles.png) | 16 × 30 | 480 | 232 | 232 |
| `gTileset_Shop` | Secundário | [tiles.png](../../../data/tilesets/secondary/shop/tiles.png) | 16 × 32 | 512 | 289 | 289 |
| `gTileset_Facility` | Secundário | [tiles.png](../../../data/tilesets/secondary/facility/tiles.png) | 16 × 32 | 512 | 511 | 511 |
| `gTileset_LilycoveMuseum` | Secundário | [tiles.png](../../../data/tilesets/secondary/lilycove_museum/tiles.png) | 16 × 27 | 432 | 143 | 143 |
| `gTileset_Contest` | Secundário | [tiles.png](../../../data/tilesets/secondary/contest/tiles.png) | 16 × 27 | 432 | 233 | 233 |
| `gTileset_BattleFrontier` | Secundário | [tiles.png](../../../data/tilesets/secondary/battle_frontier/tiles.png) | 16 × 20 | 320 | 509 | 509 |

**Diferença entre capacidade e uso:** a quantidade de tiles que cabe na folha PNG não é a mesma coisa que a quantidade de metatiles definidos. Por exemplo, o tileset primário Building possui uma folha de 512 tiles, mas só 8 registros de metatile. Não se deve interpretar isso como 512 metatiles disponíveis.

## 3. Arquivos que compõem cada tileset

Todos os dez diretórios seguem o mesmo padrão básico:

| Arquivo / diretório | Função |
|---|---|
| `tiles.png` | Folha gráfica indexada, formada por tiles de 8×8 pixels |
| `palettes/00.pal` a `palettes/15.pal` | 16 paletas individuais; cada arquivo contém 16 cores |
| `metatiles.bin` | Conjunto de metatiles; oito referências de tile por registro |
| `metatile_attributes.bin` | Comportamento e tipo de camada de cada metatile |
| `anim/` (quando presente) | Quadros gráficos que substituem tiles em animações |

Diretórios canônicos:
- [General — primário](../../../data/tilesets/primary/general/)
- [Building — primário](../../../data/tilesets/primary/building/)
- [Lilycove — secundário](../../../data/tilesets/secondary/lilycove/)
- [Generic Building — secundário](../../../data/tilesets/secondary/generic_building/)
- [Pokémon Center — secundário](../../../data/tilesets/secondary/pokemon_center/)
- [Shop — secundário](../../../data/tilesets/secondary/shop/)
- [Facility — secundário](../../../data/tilesets/secondary/facility/)
- [Lilycove Museum — secundário](../../../data/tilesets/secondary/lilycove_museum/)
- [Contest — secundário](../../../data/tilesets/secondary/contest/)
- [Battle Frontier — secundário](../../../data/tilesets/secondary/battle_frontier/)

Os 16 arquivos de paleta foram confirmados na estrutura de cada um desses diretórios. A folha usa indexação 4bpp; ao editar, mantenha os índices das cores e as referências de paleta usadas pelos tiles. Trocar a ordem das cores sem atualizar os dados relacionados altera a aparência de todos os tiles que apontam para aquela posição.

## 4. Animações que afetam a área

As animações ativas são controladas por callbacks registrados no cabeçalho dos tilesets, e não apenas pela existência de uma pasta `anim`.

### Primário General

Callback: `InitTilesetAnim_General`.

| Animação | Diretório | Quadros |
|---|---|---:|
| Flores | `primary/general/anim/flower/` | 3 (0–2) |
| Água | `primary/general/anim/water/` | 8 (0–7) |
| Borda areia/água | `primary/general/anim/sand_water_edge/` | 7 (0–6) |
| Cachoeira | `primary/general/anim/waterfall/` | 4 (0–3) |
| Borda terra/água | `primary/general/anim/land_water_edge/` | 4 (0–3) |

O callback distribui as atualizações em intervalos do contador de animação. Não renomear ou remover quadros sem atualizar o código de animação.

### Primário Building

Callback: `InitTilesetAnim_Building`.

| Animação | Diretório | Quadros |
|---|---|---:|
| TV ligada | `primary/building/anim/tv_turned_on/` | 2 (0–1) |

### Secundário Lilycove

O tileset `gTileset_Lilycove` tem callback `InitTilesetAnim_Lilycove`, mas esse callback configura o callback secundário como `NULL`. Portanto, não há animação secundária específica de Lilycove ativa nesse código, embora o tileset compartilhe a animação do primário General nos mapas externos.

Os outros sete tilesets secundários listados neste catálogo possuem callback `NULL` em seus cabeçalhos; não foi encontrada animação específica ativa para eles.

## 5. Mapa de layouts e combinação de tilesets

A associação abaixo vem de `data/layouts/layouts.json` e do inventário dos mapas. Os mapas podem compartilhar um mesmo layout.

| Layout | Mapa / sala | Primário | Secundário |
|---|---|---|---|
| `LAYOUT_LILYCOVE_CITY` | Lilycove City (exterior) | General | Lilycove |
| `LAYOUT_ROUTE121` | Route 121 (exterior) | General | Lilycove |
| `LAYOUT_LILYCOVE_CITY_COVE_LILY_MOTEL_1F` | Cove Lily Motel 1F | Building | GenericBuilding |
| `LAYOUT_LILYCOVE_CITY_COVE_LILY_MOTEL_2F` | Cove Lily Motel 2F | Building | GenericBuilding |
| `LAYOUT_LILYCOVE_CITY_LILYCOVE_MUSEUM_1F` | Lilycove Museum 1F | Building | LilycoveMuseum |
| `LAYOUT_LILYCOVE_CITY_LILYCOVE_MUSEUM_2F` | Lilycove Museum 2F | Building | LilycoveMuseum |
| `LAYOUT_LILYCOVE_CITY_CONTEST_LOBBY` | Contest Lobby | Building | Contest |
| `LAYOUT_LILYCOVE_CITY_CONTEST_HALL` | Contest Hall | Building | Contest |
| `LAYOUT_POKEMON_CENTER_1F` | Pokémon Center 1F | Building | PokemonCenter |
| `LAYOUT_POKEMON_CENTER_2F` | Pokémon Center 2F | Building | PokemonCenter |
| `LAYOUT_MART` | Mart não utilizado | Building | Shop |
| `LAYOUT_LILYCOVE_CITY_POKEMON_TRAINER_FAN_CLUB` | Pokémon Trainer Fan Club | Building | GenericBuilding |
| `LAYOUT_HARBOR` | Harbor | General | Facility |
| `LAYOUT_HOUSE2` | Move Deleter's House e House 3 | Building | GenericBuilding |
| `LAYOUT_HOUSE1` | House 1 e House 4 | Building | GenericBuilding |
| `LAYOUT_LILYCOVE_CITY_HOUSE2` | House 2 | Building | GenericBuilding |
| `LAYOUT_LILYCOVE_CITY_DEPARTMENT_STORE_1F` | Department Store 1F | Building | Shop |
| `LAYOUT_LILYCOVE_CITY_DEPARTMENT_STORE_2F` | Department Store 2F | Building | Shop |
| `LAYOUT_LILYCOVE_CITY_DEPARTMENT_STORE_3F` | Department Store 3F | Building | Shop |
| `LAYOUT_LILYCOVE_CITY_DEPARTMENT_STORE_4F` | Department Store 4F | Building | Shop |
| `LAYOUT_LILYCOVE_CITY_DEPARTMENT_STORE_5F` | Department Store 5F | Building | Shop |
| `LAYOUT_LILYCOVE_CITY_DEPARTMENT_STORE_ROOFTOP` | Department Store Rooftop | Building | Shop |
| `LAYOUT_LILYCOVE_CITY_DEPARTMENT_STORE_ELEVATOR` | Department Store Elevator | Building | BattleFrontier |
| `LAYOUT_ROUTE121_SAFARI_ZONE_ENTRANCE` | Safari Zone Entrance | Building | Shop |

## 6. Consequências para a edição visual

- **Exterior de Lilycove e Route 121:** os dois usam a mesma combinação General + Lilycove. A folha Lilycove contém a parte específica da região; General fornece o conjunto primário compartilhado, inclusive terrenos e animações gerais.
- **Fachadas e elementos exteriores:** não presumir que cada prédio seja um sprite único. O layout é uma grade de IDs de metatile, montados a partir dos dois tilesets.
- **Interiores:** Building é o primário comum de vários interiores. A identidade visual especializada vem principalmente do tileset secundário correspondente.
- **Centro de Concursos:** os dois interiores usam Building + Contest. O exterior da cidade usa General + Lilycove, portanto a fachada externa e o salão interno pertencem a conjuntos gráficos diferentes.
- **Porto:** é a única sala listada usando General + Facility.
- **Elevador da loja:** usa Building + BattleFrontier, não Shop.
- **Colisões e camadas:** alterar apenas o desenho pode deixar o metatile com colisão errada, comportamento de terreno errado ou camada de renderização inadequada. Os arquivos de atributos devem ser auditados junto com os gráficos.
- **Compartilhamento:** apesar de o escopo de jogo priorizar Lilycove e Route 121, os tilesets e layouts são recursos canônicos da engine. Algumas alterações podem atingir outros mapas que usem a mesma combinação. A prioridade será validar o conjunto-alvo, sem duplicar assets desnecessariamente.

## 7. O que ainda falta para o mapeamento visual ficar realmente fechado

O catálogo estrutural dos dez tilesets está confirmado. Ainda não vou declarar o mapeamento de índices como concluído, pois falta uma extração binária sem perda para cruzar:
1. Cada célula de cada `map.bin` com o ID absoluto do metatile e seu índice local no tileset primário/secundário.
2. Cada índice de metatile com os oito tiles que o compõem, incluindo flip horizontal/vertical e paleta selecionada em cada referência.
3. Cada metatile com seu registro em `metatile_attributes.bin`: comportamento, tipo de camada e implicações de colisão.
4. Uma folha de referência visual numerada (tiles, metatiles e paletas) que permita ao editor identificar o que está vendo sem adivinhar coordenadas.
5. Um índice de animações com o tile de destino na VRAM e o ciclo aplicado pelo callback.

**Limitação encontrada:** a leitura dos arquivos binários `.bin` pelo conector GitHub não é adequada para decodificar os valores de 16 bits com segurança. Por isso, não vou publicar índices de uso presumidos. Foi adicionado `work/lilycove/tools/audit_tilesets.py`, que lê os bytes diretamente no checkout do repositório e valida os tamanhos antes de gerar os relatórios. O script ainda não foi executado nesta etapa.

## 8. Referências-fonte

- [Definição dos layouts](../../../data/layouts/layouts.json)
- [Definições dos tilesets](../../../src/data/tilesets/headers.h)
- [Importação de folhas e paletas](../../../src/data/tilesets/graphics.h)
- [Referências de metatiles](../../../src/data/tilesets/metatiles.h)
- [Estruturas e contagens de tilesets](../../../include/fieldmap.h)
- [Formato dos IDs, colisões, elevação e atributos](../../../include/global.fieldmap.h)
- [Callbacks e ciclos de animação](../../../src/tileset_anims.c)

## 9. Próximo passo técnico

Execute no terminal do Codespaces, a partir da raiz do repositório:\n\n```bash\npython3 work/lilycove/tools/audit_tilesets.py\n```\n\nO script valida os 24 layouts-alvo e gera `layout-index.csv`, `metatile-usage.csv`, `metatile-composition.csv` e `summary.json` em `work/lilycove/reports/tilesets/`. A composição registra os oito tiles de cada metatile, índice de tile, flips horizontal/vertical, paleta, comportamento e camada. Se a validação interromper o processo, não force a geração: o erro indicará qual arquivo ou hipótese de formato precisa ser investigado.\n\nDepois dessa auditoria, ainda será necessário gerar folhas visuais numeradas dos tiles e metatiles, relacionar os IDs de comportamento aos nomes da engine e auditar os destinos de animação na VRAM. Esses são os passos que transformam o catálogo estrutural em um mapa visual realmente completo.
