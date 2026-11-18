# Folhas de tiles numeradas

Cada arquivo mostra o PNG original do tileset com a numeração do índice de tile sobre cada célula. Os números são **índices de tile 8×8**, contados da esquerda para a direita e de cima para baixo, começando em zero.

Isso é diferente do índice de metatile. Um metatile é composto por oito referências de tile, e as referências de cada metatile estão em metatiles.bin. Use valid-metatile-composition.json para converter um metatile em oito índices de tile.

| Tileset | Folha | Grade | Total de tiles |
|---|---|---:|---:|
| General | [Abrir folha numerada](gtileset_general-numbered.svg) | 16×32 | 512 |
| Building | [Abrir folha numerada](gtileset_building-numbered.svg) | 16×32 | 512 |
| Lilycove | [Abrir folha numerada](gtileset_lilycove-numbered.svg) | 16×27 | 432 |
| Generic Building | [Abrir folha numerada](gtileset_genericbuilding-numbered.svg) | 16×32 | 512 |
| Pokémon Center | [Abrir folha numerada](gtileset_pokemoncenter-numbered.svg) | 16×30 | 480 |
| Shop | [Abrir folha numerada](gtileset_shop-numbered.svg) | 16×32 | 512 |
| Facility | [Abrir folha numerada](gtileset_facility-numbered.svg) | 16×32 | 512 |
| Lilycove Museum | [Abrir folha numerada](gtileset_lilycovemuseum-numbered.svg) | 16×27 | 432 |
| Contest | [Abrir folha numerada](gtileset_contest-numbered.svg) | 16×27 | 432 |
| Battle Frontier | [Abrir folha numerada](gtileset_battlefrontier-numbered.svg) | 16×20 | 320 |

As folhas SVG referenciam os PNGs originais no mesmo branch do repositório; não duplicam nem alteram os arquivos gráficos. Os índices numéricos permitem localizar rapidamente o tile citado em cada referência de metatile.

**Limite atual:** os SVGs identificam os tiles gráficos, mas não aplicam as 16 paletas individuais. A aparência final em jogo depende do slot de paleta indicado na referência do metatile e da paleta carregada pelo tileset. Ainda não existe uma folha numerada de metatiles montados com as paletas corretas.
