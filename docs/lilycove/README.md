# Nova Lilycove — reformulação do mapa

![Nova Lilycove](lilycove_nova_legenda.png)

Mapa `LAYOUT_LILYCOVE_CITY` refeito do zero (64×52 tiles, antes 80×40), inspirado na
imagem de referência: centro de concursos no eixo central, praça com fontes, bairro
residencial ao norte, orla com cais ao sul e praia a leste.

## Zonas

| Zona | Posição (x,y da porta) | Observação |
|---|---|---|
| Museu | (7,7) e (8,7) | Platô com escadaria, canto noroeste |
| Bairro residencial | Move Deleter (18,5), Casa 1 (24,5), Casa 2 (30,5) | Fileira norte |
| **Casa 4 (casa do pai)** | (18,10) | Residência do protagonista no roteiro |
| Fã-clube | (25,10) | |
| Loja de Departamentos | (44,8) | Prédio alto no canto nordeste |
| Centro Pokémon | (4,17) | Perto da entrada da Rota 121 |
| Casa 3 | (10,17) | |
| **Centro de Concursos** | (27,19) | No eixo central, com jardins e postes |
| Motel Cove Lily + piscina | (42,17) | Acima da praia |
| Porto (SS Tidal) | (7,31) | Com píer próprio |
| Praça das Fontes | y 23–35 | Três fontes, canteiros floridos |
| Orla / píer central | y 36–47 | Muro de contenção, píeres, navio e barcos (objetos decorativos) |
| Praia | x 42–51, y 19–41 | Areia → água rasa → mar. Barcos de pesca do pai |
| Caverna (Aqua) | (58,5) | Ilhota no mar, só por Surf (mantém o warp original) |

## Conexões
* **Rota 121** a oeste: avenida principal nas linhas y 20–23 (offset 15 / −15).
* A conexão com a **Rota 124** foi removida (o jogo usa só Lilycove + Rota 121).

## Compatibilidade preservada
* A ordem dos 14 warps foi mantida, portanto todos os interiores continuam voltando
  para a porta certa sem alterações.
* Ponto de cura (`heal_locations.json`) e `setescapewarp` do Porto foram atualizados.
* Todos os NPCs, placas e itens escondidos originais foram reposicionados em tiles
  válidos (os scripts antigos continuam funcionando até serem reescritos).

## Como editar
```
python3 dev_scripts/lilycove_redesign/build_lilycove.py --preview /tmp/lilycove.png
```
Edite `dev_scripts/lilycove_redesign/layout.py` (funções `house`, `contest`, `pond`,
`path`, `trees`, `lamp`…) e rode de novo; o script regrava `map.bin` e gera a prévia.
Se mover prédios, atualize as coordenadas em `data/maps/LilycoveCity/map.json`.

## Atmosfera da Temporada Mundial de Concursos
Tiles novos no tileset secundário de Lilycove (gerados por
`dev_scripts/lilycove_redesign/festival_tiles.py`, usando as paletas 6 e 12, que
estavam vazias):

| Elemento | Onde aparece |
|---|---|
| Piso de tijolo vermelho | Praça das Fontes, orla e frente do Porto |
| Tapete vermelho | Da porta do Centro de Concursos até a fonte central |
| Bandeirolas (vermelho/azul) | Avenida, rua norte, borda da praça e orla |
| Estandartes da temporada | Ao lado do Centro de Concursos e nos cantos da praça |
| Guarda-sóis (vermelho/azul) e palmeiras | Praia; palmeiras também na orla |

Uso: 475/512 tiles e 399/512 metatiles do tileset secundário.

`vivid_palettes.py` aumenta a saturação (+22%) e o brilho (+4%) das paletas externas
(General 0–5 e Lilycove 7–11). Os originais ficam em `base_tileset/`, e os dois
scripts podem ser rodados de novo sem acumular o efeito.

Ordem para regenerar tudo:
```
python3 dev_scripts/lilycove_redesign/festival_tiles.py
python3 dev_scripts/lilycove_redesign/vivid_palettes.py
python3 dev_scripts/lilycove_redesign/build_lilycove.py --preview /tmp/lilycove.png
```

## Próximos passos
* Interior da Casa 4 (sala, cozinha, quarto extra) conforme o roteiro.
* Abertura: comercial, formulário de inscrição, cabine e chegada ao porto.
