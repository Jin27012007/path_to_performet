# Validação do carregamento de map.bin — Lilycove / Route 121

## Objetivo

Registrar o que foi confirmado no código do motor antes de interpretar os arquivos binários dos mapas no auditor de tilesets.

## Regra de carregamento confirmada

Arquivo-fonte: `src/fieldmap.c`, função `InitBackupMapLayoutData`.

A função recebe o ponteiro para os dados do mapa e as dimensões `width` e `height`. Para cada linha:

1. copia `width * 2` bytes com `CpuCopy16(map, dest, width * 2)`;
2. avança o destino por `width + MAP_OFFSET_W` células;
3. avança a origem por `width` células.

Consequência: a grade ativa consome exatamente `width * height` valores u16 little-endian, em ordem contínua. Bytes que apareçam depois desses valores no arquivo não são lidos por essa função como células do mapa.

Referência de código:
- [src/fieldmap.c — carregamento da grade](https://github.com/Jin27012007/path_to_performet/blob/work/lilycove-route121-workspace/src/fieldmap.c#L180-L192)

## Caso Lilycove City

O layout `LAYOUT_LILYCOVE_CITY` declara 80 × 40 células e aponta para `data/layouts/LilycoveCity/map.bin`.

- Células esperadas: 3.200.
- Bytes consumidos pela grade: 6.400.
- A resposta base64 do GitHub para esse arquivo tinha 8.679 caracteres. Esse tamanho codificado, isoladamente, não deve ser confundido com o tamanho binário; é necessário decodificar antes de calcular o excedente exato.
- O auditor deve preservar e reportar qualquer excedente, sem incluí-lo na grade nem removê-lo do repositório.

Referência do layout:
- [layouts.json — LAYOUT_LILYCOVE_CITY](https://github.com/Jin27012007/path_to_performet/blob/work/lilycove-route121-workspace/data/layouts/layouts.json)

## Estado do auditor

O arquivo `work/lilycove/tools/audit_tilesets.py` atualmente:
- lê os 26 mapas do `asset-index.json`;
- deduplica os layouts compartilhados;
- resolve os layouts pelo `data/layouts/layouts.json`;
- calcula o tamanho esperado a partir de largura × altura × 2;
- rejeita arquivos menores que a grade necessária;
- analisa somente os bytes da grade;
- registra bytes excedentes em `summary.json`;
- separa referências de metatile fora do limite em `invalid-metatile-refs.csv`.

Referência:
- [auditor de tilesets](https://github.com/Jin27012007/path_to_performet/blob/work/lilycove-route121-workspace/work/lilycove/tools/audit_tilesets.py)

## O que ainda não está validado

- O auditor ainda não foi executado em um checkout completo do repositório.
- Não há relatórios CSV/JSON gerados e revisados.
- O tamanho binário decodificado de todos os mapas ainda precisa ser confrontado com suas dimensões.
- Referências de metatiles, paletas, colisões e composições ainda precisam dos resultados de execução.
- Nenhum PNG, tileset, mapa ou evento foi alterado nesta etapa.

## Próxima etapa

Executar o auditor em Codespaces a partir da raiz do repositório e revisar primeiro `summary.json`, `layout-index.csv` e `invalid-metatile-refs.csv`. Só depois disso gerar folhas visuais numeradas e propor alterações gráficas.
