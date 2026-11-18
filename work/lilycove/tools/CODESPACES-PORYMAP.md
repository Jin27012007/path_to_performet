# Porymap no GitHub Codespaces

Esta configuração prepara um desktop Linux remoto dentro do Codespaces para abrir a interface gráfica do Porymap no navegador, inclusive em um celular. O Porymap continua sendo um aplicativo desktop; o navegador acessa a sessão remota por noVNC.

## Abrir o Codespace

1. Abra o repositório: https://github.com/Jin27012007/path_to_performet
2. Selecione a branch `work/lilycove-route121-workspace`.
3. Toque em **Code** → **Codespaces** → **Create codespace on work/lilycove-route121-workspace**.
4. Se o Codespaces perguntar qual configuração usar, aceite `.devcontainer/devcontainer.json`.
5. Aguarde a criação do container. Na primeira inicialização, o script clona e compila o Porymap upstream; isso pode demorar alguns minutos.
6. A porta `6080` deve ser encaminhada como **Porymap Desktop (noVNC)**. Abra a URL encaminhada no navegador.

## Abrir Porymap

Na área de trabalho remota, abra o terminal XFCE e execute:

```bash
bash .devcontainer/launch-porymap.sh
```

O Porymap abrirá apontando para a raiz do repositório. Se a janela de seleção de projeto aparecer, selecione a pasta raiz do checkout, que contém `data/`, `include/`, `src/` e `pokeemerald.gba` (quando compilado).

Se preferir iniciar pelo terminal integrado do VS Code, execute:

```bash
DISPLAY=:1 QT_X11_NO_MITSHM=1 "$HOME/.local/opt/porymap/porymap" "$PWD"
```

## Recompilar o Porymap

```bash
bash .devcontainer/setup-porymap.sh
```

A configuração fixa o código upstream em `26b919d7ff4b54152de010abd5bf344af2ebe116` para que a versão usada seja reproduzível. O código do Porymap não é copiado para dentro do repositório do jogo; fica em `$HOME/.local/src/porymap`.

## Segurança e limites

- A porta noVNC é configurada como **private** no Codespaces. Não altere para public.
- A sessão VNC não usa senha porque o acesso é protegido pelo encaminhamento privado/autenticado do Codespaces. Não exponha a porta 5900 diretamente.
- O Codespace é um ambiente remoto Linux. Alterações feitas no projeto são alterações reais no checkout da branch e devem ser revisadas no Git antes de commit.
- Faça commits pequenos e mantenha a branch de trabalho; não edite `main`.
- O Porymap não substitui a edição de PNGs de tilesets/sprites nem nossa auditoria de colisões e dependências.
- A primeira compilação pode falhar caso pacotes Qt necessários tenham mudado no Ubuntu base. Nesse caso, consulte o log de `postCreateCommand` e não tente editar os mapas até corrigir a instalação.
- O arquivo de configuração foi preparado, mas ainda precisa ser validado por uma criação real do Codespace. Não declarar Porymap funcional até a janela abrir e carregar Lilycove/Route 121 sem erros.

## Arquivos da configuração

- `.devcontainer/Dockerfile`: dependências Qt e desktop remoto.
- `.devcontainer/devcontainer.json`: configuração do Codespaces e encaminhamento privado da porta.
- `.devcontainer/setup-porymap.sh`: clone fixado e compilação do Porymap.
- `.devcontainer/start-desktop.sh`: inicia XFCE, Xvfb, VNC e noVNC.
- `.devcontainer/launch-porymap.sh`: abre o editor no projeto atual.

## Verificação obrigatória depois da abertura

1. Confirmar que Porymap inicia sem erro.
2. Abrir Lilycove City e Route121.
3. Verificar se os tilesets primário e secundário aparecem corretamente.
4. Verificar se object events, warps e conexões são carregados.
5. Não salvar alterações até essa validação terminar.
