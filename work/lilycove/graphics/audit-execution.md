# Como executar a auditoria Lilycove

O workflow `.github/workflows/lilycove-tileset-audit.yml` foi adicionado à branch `work/lilycove-route121-workspace`.

## Execução manual

1. Abra o repositório no GitHub e selecione a branch `work/lilycove-route121-workspace`.
2. Abra a aba **Actions**.
3. Selecione **Lilycove tileset audit**.
4. Toque em **Run workflow**, mantenha a branch de trabalho selecionada e confirme.
5. Aguarde a execução terminar. Se falhar, abra o job e consulte a etapa **Run read-only Lilycove audit**.
6. Quando terminar com sucesso, baixe o artefato **lilycove-tileset-audit** na página da execução.

O artefato contém os CSVs e o `summary.json` produzidos pelo script. Envie esse ZIP nesta conversa para eu revisar os resultados e preparar a próxima etapa de folhas visuais numeradas.

## Segurança e escopo

- O workflow só lê o repositório e executa o auditor.
- Ele não compila nem modifica a ROM.
- Ele não altera mapas, tilesets, eventos ou sprites.
- O artefato é produzido somente se o script terminar sem erro.

## Limitação atual

A integração GitHub disponível nesta sessão permite gravar os arquivos na branch, mas não oferece uma ação de disparo manual do workflow. A primeira consulta à lista de execuções não retornou nenhuma execução. Portanto, o workflow está preparado, mas os relatórios ainda não foram gerados nem validados.
