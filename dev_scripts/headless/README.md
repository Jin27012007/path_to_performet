# gbarun — runner headless para testar cenas

```
sudo apt-get install libmgba-dev
gcc -O2 -o dev_scripts/headless/gbarun dev_scripts/headless/gbarun.c -lmgba
dev_scripts/headless/gbarun pokeemerald.gba roteiro.txt pasta_saida/
```

O relógio do jogo é fixado ao meio-dia (sem tinta noturna e com execuções reproduzíveis).

Comandos do roteiro (um por linha):

| comando | efeito |
|---|---|
| `wait N` | roda N frames sem teclas |
| `press TECLAS N` | segura as teclas (ex.: `A`, `UP`, `A+B`) por N frames |
| `tap TECLAS [vezes]` | toque curto (4 frames + 12 de pausa) |
| `shot NOME` | salva `NOME.ppm` |
| `savestate NOME` / `loadstate NOME` | estados salvos na pasta de saída |

Dica: o texto avança devagar. Use `savestate` em pontos-chave e continue a partir
deles, conferindo os screenshots a cada etapa.
