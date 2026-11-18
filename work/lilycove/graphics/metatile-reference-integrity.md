# Integridade das referências de metatile — Lilycove / Route 121

## Resultado principal

A leitura direta dos 24 layouts únicos apontou **204 combinações layout/metatile fora do intervalo real dos arquivos de metatiles**, distribuídas por **19 layouts**. Essas combinações correspondem a **1.574 células de mapa** que apontam para registros que não existem nos arquivos binários dos tilesets atualmente associados aos layouts.

Isso não é uma previsão de falha visual: é uma incompatibilidade objetiva entre os valores presentes em `map.bin`, a atribuição de tilesets em `data/layouts/layouts.json` e a quantidade de registros presente nos arquivos `metatiles.bin` / `metatile_attributes.bin`.

## Resumo por tileset

| Tileset | Metatiles presentes | Índices únicos usados | Índices fora do arquivo | Combinações layout/índice inválidas | Células afetadas |
|---|---:|---:|---:|---:|---:|
| `gTileset_Building` | 8 | 49 | 45 | 141 | 1.246 |
| `gTileset_Contest` | 233 | 124 | 6 | 8 | 74 |
| `gTileset_Shop` | 289 | 169 | 13 | 20 | 68 |
| `gTileset_LilycoveMuseum` | 143 | 115 | 14 | 14 | 39 |
| `gTileset_PokemonCenter` | 232 | 99 | 4 | 5 | 12 |
| `gTileset_Lilycove` | 351 | 224 | 16 | 16 | 135 |
| `gTileset_General` | 512 | 174 | 0 | 0 | 0 |
| `gTileset_GenericBuilding` | 512 | 104 | 0 | 0 | 0 |
| `gTileset_Facility` | 511 | 30 | 0 | 0 | 0 |
| `gTileset_BattleFrontier` | 509 | 16 | 0 | 0 | 0 |

**Observação importante sobre a leitura:** o total de 49 índices usados em `gTileset_Building`, por exemplo, inclui os índices de metatile lidos da grade primária dos mapas. O arquivo primário Building contém só 8 registros, embora os mapas usem IDs primários até 482. Não foi aplicado deslocamento alternativo para tentar fazê-los caber.

## Evidência no código-fonte

- `include/global.fieldmap.h` define a célula do mapa: ID de metatile nos bits 0–9, colisão nos bits 10–11 e elevação nos bits 12–15.
- `include/fieldmap.h` define 512 metatiles primários e 1.024 IDs totais no formato Emerald.
- `src/fieldmap.c`, em `GetAttributeByMetatileIdAndMapLayout`, seleciona o tileset primário para IDs abaixo de 512 e o secundário para IDs a partir de 512, usando o índice secundário como ID absoluto menos 512.
- `src/data/tilesets/headers.h` associa `gTileset_Building` a `gMetatiles_InsideBuilding`.
- `src/data/tilesets/metatiles.h` associa `gMetatiles_InsideBuilding` diretamente a `data/tilesets/primary/building/metatiles.bin`.

Essas regras não permitem concluir que os índices excedentes devam ser deslocados, reinterpretados ou atribuídos a outro tileset. Fazer isso sem recuperar a estrutura pretendida pode quebrar mapas e colisões.

## Verificação contra a branch main

Comparei hashes de arquivos em `main` e `work/lilycove-route121-workspace`. Os seguintes pares estavam idênticos entre as duas branches:
- `data/layouts/layouts.json`
- `data/layouts/Route121/map.bin`
- `data/layouts/House1/map.bin`
- `data/layouts/LilycoveCity_ContestHall/map.bin`
- `data/maps/Route121/map.json`
- `include/fieldmap.h`
- `src/fieldmap.c`
- binários de metatiles e atributos de Building, Contest, Shop, Lilycove, Lilycove Museum e Pokémon Center.

Logo, a incompatibilidade observada já existe em `main` e não foi introduzida pelos commits de documentação/auditoria desta branch. Essa comparação não identifica ainda qual revisão upstream ou conjunto de assets deveria substituir os dados atuais.

## Arquivos de auditoria

- `../reports/tilesets/map-grid-audit.json`: leitura das 9.993 células de grade nos 24 layouts, com contagem de metatile, colisão e elevação.
- `../reports/tilesets/metatile-reference-integrity.json`: contagens por tileset e lista detalhada das referências inválidas.
- `../reports/tilesets/invalid-metatile-refs.csv`: 204 combinações inválidas, com layout, ID absoluto, índice local, quantidade de ocorrências e limite real.

## Como o auditor foi ajustado

`tools/audit_tilesets.py` não interrompe mais toda a auditoria quando encontra um ID fora do arquivo de metatiles. Ele deve exportar:
- `metatile-composition.csv` somente para registros que existem;
- `invalid-metatile-refs.csv` para as referências fora do intervalo;
- `summary.json` com contagens por tileset.

O script foi atualizado no GitHub, mas ainda não foi executado em um checkout integral do Codespaces. Os relatórios JSON/CSV acima foram montados por inspeção direta dos arquivos da branch através da API do GitHub; não são apresentados como saída de uma execução do script.

## Próxima ação técnica necessária

Antes de desenhar ou substituir tiles, é necessário reconciliar a versão dos mapas/layouts com os binários dos tilesets. O melhor próximo passo é obter uma cópia integral do repositório em Codespaces e verificar o histórico/origem dos diretórios `data/layouts` e `data/tilesets`, além de gerar uma ROM de controle da própria `main`. Até essa comparação, não alterar índices de metatile, tilesets primários/secundários, paletas ou atributos de colisão.
