# Gráficos, edifícios e texturas

Os layouts de Lilycove e Route 121 usam os tilesets abaixo. Os PNGs de tiles foram confirmados nos caminhos indicados. A estrutura original deve ser preservada; não substituir apenas `tiles.png` sem conferir metatiles, atributos, paletas e animações correspondentes.

## Área externa — cidade e rota

| ID do tileset | Arquivo visual |
|---|---|
| `gTileset_General` | [primary/general/tiles.png](../../../data/tilesets/primary/general/tiles.png) |
| `gTileset_Lilycove` | [secondary/lilycove/tiles.png](../../../data/tilesets/secondary/lilycove/tiles.png) |

Os dois mapas externos usam a mesma combinação. Isso significa que uma alteração no tileset de Lilycove pode afetar tanto a cidade quanto a Rota 121.

## Interiores

Tilesets primários:
- `gTileset_Building` — [primary/building/tiles.png](../../../data/tilesets/primary/building/tiles.png)

Tilesets secundários:
- `gTileset_GenericBuilding` — [secondary/generic_building/tiles.png](../../../data/tilesets/secondary/generic_building/tiles.png)
- `gTileset_PokemonCenter` — [secondary/pokemon_center/tiles.png](../../../data/tilesets/secondary/pokemon_center/tiles.png)
- `gTileset_Shop` — [secondary/shop/tiles.png](../../../data/tilesets/secondary/shop/tiles.png)
- `gTileset_Facility` — [secondary/facility/tiles.png](../../../data/tilesets/secondary/facility/tiles.png)
- `gTileset_LilycoveMuseum` — [secondary/lilycove_museum/tiles.png](../../../data/tilesets/secondary/lilycove_museum/tiles.png)
- `gTileset_Contest` — [secondary/contest/tiles.png](../../../data/tilesets/secondary/contest/tiles.png)
- `gTileset_BattleFrontier` — [secondary/battle_frontier/tiles.png](../../../data/tilesets/secondary/battle_frontier/tiles.png)

## Layouts que usam esses tilesets

A associação oficial está em [data/layouts/layouts.json](../../../data/layouts/layouts.json). Não deduzir o tileset apenas pelo nome do edifício: por exemplo, interiores diferentes compartilham `gTileset_GenericBuilding` ou `gTileset_Shop`.

## Cuidados de edição

1. Trabalhar com a imagem no tamanho original e manter a grade de tiles.
2. Respeitar o limite e a organização das paletas.
3. Verificar os arquivos associados de metatiles e atributos no mesmo diretório do tileset.
4. Não alterar os índices/ordem dos metatiles sem revisar os mapas que os usam.
5. Depois de editar, abrir Lilycove e Route 121 no jogo para conferir alinhamento, transparência, colisões e animações.

**Importante:** os diretórios de tilesets são recursos compartilhados da engine. O catálogo facilita encontrá-los, mas não significa que sejam exclusivos de Lilycove.
## Auditoria de dependências

Foi criado um levantamento do compartilhamento dos tilesets usados por Lilycove e pelo Centro de Concursos: [auditoria de dependências](contest-hall-dependencies.md). Ele registra que `gTileset_Lilycove`, `gTileset_Contest` e `gTileset_Building` são compartilhados por vários layouts e explica os cuidados antes de editar as folhas gráficas.
Inventário mapa a mapa: [mapas, layouts e tilesets](map-graphics-inventory.md). Use essa tabela antes de editar qualquer gráfico para conferir dependências e reutilização.

## Catálogo técnico dos tilesets

O [catálogo técnico completo dos 10 tilesets](tileset-technical-catalog.md) reúne dimensões reais das folhas, quantidade de tiles e metatiles, arquivos associados, paletas, animações, combinação primário/secundário por layout e limitações ainda pendentes na extração dos índices binários.


## Auditoria reproduzível de índices

Foi adicionado um script somente de leitura: [audit_tilesets.py](../tools/audit_tilesets.py). Execute a partir da raiz do repositório no terminal do Codespaces:

```bash
python3 work/lilycove/tools/audit_tilesets.py
```

Ele deriva automaticamente os 24 layouts únicos a partir das 26 entradas de `asset-index.json`, cruza cada `map.bin` com as dimensões declaradas e decodifica as células, separando metatile, colisão e elevação. Também separa IDs primários/secundários e decodifica as oito referências de tile de cada metatile usado, incluindo flips, slot de paleta, comportamento e camada. Os relatórios incluem índice de layouts, células, uso/composição de metatiles e distribuição de colisão/elevação. O script registra bytes excedentes após a grade ativa em vez de descartá-los.


A investigação do formato e a comparação de tamanho dos 24 arquivos estão em [auditoria do formato binário dos mapas](map-binary-audit.md). Ela documenta por que somente `width × height × 2` bytes formam a grade ativa, com referência às rotinas de carregamento do motor. O script revisado foi commitado, mas ainda precisa ser executado em um checkout completo do repositório; nenhum CSV gerado foi apresentado como resultado de execução.


## Integridade das referências de metatile

A inspeção direta dos mapas e dos binários encontrou referências fora do intervalo dos arquivos de metatiles em 19 dos 24 layouts auditados. São 204 combinações layout/índice e 1.574 células afetadas. O problema já está presente em `main`; não foi criado pela branch de trabalho. Consulte o [relatório de integridade](metatile-reference-integrity.md), o [JSON detalhado](../reports/tilesets/metatile-reference-integrity.json) e o [CSV das referências inválidas](../reports/tilesets/invalid-metatile-refs.csv). Não remapeie IDs nem substitua tilesets até a origem dessa divergência ser esclarecida.

O [catálogo das 1.006 composições válidas de metatiles](../reports/tilesets/valid-metatile-composition.json) lista os oito tiles usados por cada metatile, flips, paleta, comportamento e mapas onde aparece. As 204 referências fora dos arquivos ficam separadas no CSV de integridade; não foram inventadas composições para esses índices.
