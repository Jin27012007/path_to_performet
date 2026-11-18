# Porymap — edição visual de mapas

## O que é

[Porymap](https://github.com/huderlem/porymap) é um editor gráfico para projetos de descompilação da terceira geração de Pokémon, incluindo pokeemerald. Ele permite editar mapas visualmente, trabalhar com metatiles/tilesets e configurar eventos de mapa sem editar manualmente cada arquivo JSON/binário.

## Compatibilidade com este projeto

Este projeto usa uma base pokeemerald-expansion. Porymap é destinado a projetos pokeemerald e deve ser apontado para a raiz do repositório, onde estão diretórios como `data/maps`, `data/layouts`, `data/tilesets` e os arquivos de configuração do projeto.

A compatibilidade exata com esta versão de pokeemerald-expansion precisa ser validada abrindo uma cópia da branch de trabalho e verificando se o Porymap carrega os mapas e tilesets sem avisos. Não considere a compatibilidade comprovada apenas porque o programa abre.

## Instalação

Página oficial e downloads:
- https://github.com/huderlem/porymap
- Guia oficial: https://huderlem.github.io/porymap/
- Releases: https://github.com/huderlem/porymap/releases

O README oficial disponibiliza pacotes prontos para Windows e macOS. Em Linux, o caminho documentado é compilar a partir do código-fonte ou usar um pacote de terceiros, que pode estar desatualizado.

Porymap é um aplicativo desktop. A interface web do GitHub e o Codespaces no navegador não o transformam automaticamente em uma ferramenta Android. Não há, neste repositório, uma versão Android oficial integrada.

## Fluxo seguro para Lilycove / Route 121

1. Faça clone ou baixe uma cópia do repositório e selecione a branch `work/lilycove-route121-workspace`.
2. Mantenha uma cópia de segurança antes da primeira abertura no editor.
3. Inicie Porymap e abra a raiz do projeto (não a pasta `work/lilycove`).
4. Verifique se Lilycove City, Route 121 e os interiores aparecem na lista de mapas.
5. Abra um mapa simples primeiro e confirme que os tilesets primário e secundário carregam corretamente.
6. Faça uma alteração pequena em uma cópia/branch de teste, salve e confira no Git quais arquivos foram modificados.
7. Revise especialmente `data/maps/**/map.json`, `data/layouts/**/map.bin`, `data/layouts/**/border.bin` e referências de tilesets antes de aceitar alterações.
8. Compile e teste a ROM depois de cada conjunto pequeno de mudanças.

## Cuidados importantes

- Não edite diretamente `main`; use a branch de trabalho.
- Não aceite atualizações em massa sem revisar o diff.
- Porymap facilita a edição de mapas, mas não substitui o editor de imagens para redesenhar os PNGs dos tilesets e sprites.
- Alterações em metatiles podem afetar colisão, comportamento, elevação, camadas e animações. Confira esses atributos, não apenas a aparência.
- O auditor `work/lilycove/tools/audit_tilesets.py` continua útil como verificação complementar; Porymap não substitui essa auditoria.
- Antes de editar os 26 mapas, confirme compatibilidade com a versão exata do projeto.

## Limitação para uso pelo celular

O Porymap oficial é desktop (Windows/macOS; Linux via build/pacote). Não é possível adicioná-lo como uma aba nativa do GitHub Mobile ou executá-lo diretamente dentro do editor web do GitHub. No Android, o usuário pode consultar o repositório e revisar commits, mas a edição visual com Porymap exige um computador ou uma solução remota de desktop configurada separadamente.

## Estado

- Ferramenta identificada e documentação de integração adicionada.
- Nenhum binário do Porymap foi incorporado ao repositório.
- Nenhum mapa foi aberto ou salvo no Porymap nesta etapa.
- Compatibilidade real com a versão atual do projeto ainda precisa de teste.

## Execução pelo GitHub Codespaces

Foi preparada uma configuração de desktop remoto Linux com Qt, XFCE e noVNC para permitir abrir o aplicativo no navegador:
- [Guia de Codespaces + Porymap](CODESPACES-PORYMAP.md)
- Arquivos de ambiente: [`.devcontainer/`](../../../.devcontainer/)

A configuração ainda precisa ser testada criando um Codespace real. Não considerar a instalação validada até o Porymap abrir e carregar Lilycove e Route121.
