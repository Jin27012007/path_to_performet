# Testes e validação

Executar validação em etapas pequenas, mantendo uma build estável antes de cada grupo de alterações.

## Checklist por mudança gráfica

- [ ] PNG mantém dimensões e transparência esperadas.
- [ ] Paletas e cores permanecem válidas.
- [ ] Metatiles continuam apontando para os tiles corretos.
- [ ] Atributos e colisões permanecem corretos.
- [ ] Não há tiles desalinhados, paredes invisíveis ou passagens bloqueadas.
- [ ] Nenhum warp ou evento foi deslocado.
- [ ] Lilycove e Route 121 foram testadas no emulador.

## Checklist por mapa

- [ ] Conexões de mapa continuam válidas.
- [ ] Entradas e saídas de edifícios funcionam.
- [ ] NPCs e objetos aparecem nas coordenadas corretas.
- [ ] Scripts e diálogos continuam acionáveis.
- [ ] Eventos diários e flags não foram quebrados.

## Build

Usar o fluxo de compilação já configurado no repositório. Não marcar uma mudança como concluída apenas porque o arquivo foi enviado: exigir build concluída e teste no emulador. Guardar o commit da última versão estável para reversão rápida.
