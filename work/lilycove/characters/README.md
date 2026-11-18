# Personagens, NPCs e objetos

Esta área será usada para catalogar os recursos gráficos referenciados pelos mapas de Lilycove e Route 121.

O campo `graphics_id` em cada `map.json` identifica o gráfico usado por um evento. Antes de substituir um sprite, localizar sua definição e os arquivos de imagem correspondentes no projeto.

Escopo:
- NPCs e treinadores posicionados nos mapas.
- Objetos de cenário e objetos interativos.
- Árvores, itens no chão e elementos animados.
- Sprites, paletas, animações e dimensões.

Não alterar identificadores gráficos nem suas tabelas de definição durante uma simples reformulação visual. Manter a correspondência com os eventos de mapa.

## Inventário atual

- [Inventário de NPCs, sprites e objetos de mapa](object-event-inventory.md): referências `graphics_id`, quantidade de eventos por mapa, eventos de fundo e próximos passos para localizar os arquivos gráficos físicos.
