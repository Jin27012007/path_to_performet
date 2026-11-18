# Área de trabalho — Lilycove e Rota 121

Esta pasta organiza o desenvolvimento da ROM em torno de **Lilycove** e da **Rota 121**.

## Regra principal

Os arquivos originais permanecem nos caminhos usados pela engine. Esta área contém índices, documentação e atalhos relativos para os recursos originais. Não mover nem duplicar mapas, tilesets, scripts ou binários sem atualizar e validar todas as referências.

## Estrutura

- [maps/](maps/README.md) — mapas externos, interiores, layouts e conexões.
- [graphics/](graphics/README.md) — edifícios, terrenos, tilesets e paletas.
- [events/](events/README.md) — scripts, eventos, objetos e diálogos.
- [characters/](characters/README.md) — NPCs, sprites e objetos de mapa.
- [systems/](systems/README.md) — concursos, encontros, batalhas e menus.
- [tests/](tests/README.md) — compilação, validação e testes no emulador.

## Escopo mapeado

- 2 mapas externos principais: Lilycove City e Route 121.
- 23 mapas internos no grupo de Lilycove.
- 1 entrada interna da Safari Zone associada ao grupo de Route 121.
- 24 layouts exclusivos ou compartilhados identificados no catálogo.
- 10 tilesets referenciados pelos layouts desse conjunto.

## Fontes de verdade

- [Grupos de mapas](../../data/maps/map_groups.json)
- [Definição dos layouts](../../data/layouts/layouts.json)
- [Mapa externo de Lilycove](../../data/maps/LilycoveCity/map.json)
- [Mapa externo da Rota 121](../../data/maps/Route121/map.json)

## Estado atual

**Etapa 1 — catalogação estrutural concluída.** Esta organização não altera o comportamento do jogo nem substitui os arquivos originais. As alterações visuais e funcionais serão feitas nos arquivos-fonte canônicos, em etapas pequenas e testáveis.

## Fluxo seguro

1. Escolher um mapa, edifício ou tileset neste catálogo.
2. Abrir o arquivo-fonte original indicado.
3. Guardar a versão anterior e alterar somente o recurso selecionado.
4. Verificar paletas, metatiles, colisões, eventos e referências.
5. Compilar e testar no emulador antes de integrar outras mudanças.
