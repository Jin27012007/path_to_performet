# Eventos, scripts e diálogos

Os eventos de cada mapa são definidos principalmente em seus arquivos `map.json` e, quando aplicável, `scripts.inc`.

Fontes principais:
- [Lilycove City — map.json](../../../data/maps/LilycoveCity/map.json)
- [Lilycove City — scripts.inc](../../../data/maps/LilycoveCity/scripts.inc)
- [Route 121 — map.json](../../../data/maps/Route121/map.json)

Os mapas internos seguem o mesmo padrão de diretório em `data/maps/`. A lista completa está em [../maps/README.md](../maps/README.md).

## O que catalogar ao alterar um mapa

- `object_events`: NPCs, objetos e seus identificadores gráficos.
- `warp_events`: entradas/saídas e destinos dos edifícios.
- `coord_events`: gatilhos por coordenada.
- `bg_events`: placas, itens ocultos e interações de cenário.
- scripts chamados pelos eventos e textos associados.
- flags, variáveis e scripts comuns usados por mais de um mapa.

## Regra de segurança

Não remover scripts, flags, variáveis, warps ou eventos só porque um edifício foi redesenhado. Mudanças de aparência devem ser independentes das alterações de comportamento sempre que possível. Scripts compartilhados devem ser tratados como dependências, não como arquivos locais de Lilycove.
