# Abertura — implementação do roteiro v3

Sequência jogável, do "Novo Jogo" até o jogador ficar livre para ir ao Safari.

| Cena do roteiro | Onde está | Observações |
|---|---|---|
| 2 · Registro (gênero/nome) | `src/main_menu.c`, `data/text/birch_speech.inc` | Substitui a fala do Prof. Birch. Campo "Apresentação" (Ele/Ela) controla o sprite e os pronomes. Termina com "Inscrição recebida…" e o selo **INSCRIÇÃO CONCLUÍDA**. |
| 1 · Comercial | `LilycoveCity_ContestHall/scripts.inc`, `LilycoveCity/scripts.inc` | Tomada 1: palco do Centro de Concursos (MC, jurado, coordenadores, Skitty/Azurill/Pikachu se apresentando). Tomada 2: Lilycove decorada. Termina com o emblema da temporada. O jogador fica invisível. |
| 3 · Cabine | `data/maps/OpeningBoat_Cabin` | O comercial "termina" no monitor da cabine. Mala, foto, papéis, celular, monitor e janela com os monólogos opcionais. Nada altera afinidade. |
| 4 · Convés | `data/maps/OpeningBoat_Deck` | Aviso do tripulante ao entrar; passageiros opcionais; amurada. Falar com o tripulante → desembarque curto. |
| 5 · Porto | `LilycoveCity/scripts.inc` (`PortArrival`) | Pai no cais; 3 escolhas (viagem, bagagem, inscrição) com os Δ do roteiro. |
| 6 · Caminhada | idem | "Puxar conversa / Ficar em silêncio" + 3 perguntas. |
| 7 · Casa 4 | `data/maps/LilycoveCity_House4` | Ticket de Adoção e Vara de Pesca (uma única vez, por flag), escolhas com Δ, posição do pai, "Não vamos começar com isso agora…". |
| 8 · Quarto | `data/maps/LilycoveCity_House4_Room` | Quarto simples; uma interação com a mala organiza tudo (fade). O pai sai nesse momento. |
| 9 · Bilhete | `LilycoveCity_House4/scripts.inc` | Sala vazia, bilhete sobre a mesa, monólogo e **OBJETIVO**. A saída fica bloqueada até guardar as malas e ler o bilhete. Depois o pai fica na praia, perto dos barcos. |

**Ordem adotada:** Registro → Comercial → Cabine. O roteiro pede que o comercial
termine "revelando o monitor no salão do barco" e que o registro "transicione para a
cabine". Colocar o registro primeiro (como em qualquer Novo Jogo) permite cumprir as
duas coisas sem mostrar o protagonista antes de ele ter gênero e nome.

## Sistema de afinidade
* `src/affinity.c`: valor interno −100…+100, salvo em `VAR_AFFINITY_FATHER` como
  *delta* em relação ao valor inicial (pai = −10). Clamp em toda alteração.
* Barra no canto superior direito durante conversas: só a barra (sem número, rótulo
  ou cor de avaliação) e animação suave quando o valor muda.
* Macros de script: `affinity_show AFFINITY_FATHER`, `affinity_add AFFINITY_FATHER, ±n`,
  `affinity_hide`. Novos personagens: acrescente em `include/constants/affinity.h` e na
  tabela `sAffinityInfo`.
* Cada escolha é aplicada uma vez: as cenas rodam por `VAR_OPENING_STATE`, que avança
  antes de o jogador recuperar o controle.

## Dados persistentes (nomes do roteiro → implementação)
| Roteiro | Implementação |
|---|---|
| AFFINITY_FATHER | `VAR_AFFINITY_FATHER` (0x404E) |
| FLAG_OPENING_REGISTERED | `FLAG_OPENING_REGISTERED` (0x20) |
| FLAG_ADOPTION_TICKET_RECEIVED | `FLAG_ADOPTION_TICKET_RECEIVED` (0x21) |
| FLAG_FISHING_ROD_RECEIVED | `FLAG_FISHING_ROD_RECEIVED` (0x22) |
| FLAG_BAGS_STORED | `FLAG_BAGS_STORED` (0x23) |
| FLAG_FATHER_LEFT_FOR_WORK | `FLAG_FATHER_LEFT_FOR_WORK` (0x24) |
| FLAG_ADOPTION_TICKET_USED | `FLAG_ADOPTION_TICKET_USED` (0x25), ainda sem uso |
| VAR_ADOPTED_SPECIES | `VAR_ADOPTED_SPECIES` (0x408B), ainda sem uso |
| FLAG_FIRST_ADOPTION_COMPLETE | `FLAG_FIRST_ADOPTION_COMPLETE` (0x26), ainda sem uso |
| progresso da abertura | `VAR_OPENING_STATE` (0x4083), valores em `include/constants/lilycove_opening.h` |

Item novo: `ITEM_ADOPTION_TICKET` (Itens-chave). A Old Rod aparece como "Vara de Pesca".

## Proteções enquanto o jogador não tem Pokémon
Sem batalhas selvagens, sem treinadores (nem por visão, nem por conversa) e sem pesca
enquanto a equipe estiver vazia. Isso permite atravessar a Rota 121 até o Safari.

## Português
Glifos **ã õ Ã Õ** adicionados a todas as fontes latinas (`dev_scripts/pt_br/add_tilde_glyphs.py`).
Mensagens de item, nomes dos bolsos e SIM/NÃO traduzidos.

## Testes automatizados
`dev_scripts/headless/gbarun.c` roda a ROM sem tela (libmgba), aperta botões a partir
de um roteiro de comandos e tira screenshots. Foi usado para percorrer toda a abertura.
Veja `dev_scripts/headless/README.md`.

## Ainda não implementado
* Cenas 10–11 (atendente do Safari e interface de adoção), que dependem do catálogo de
  adoção.
* Interface visual de "formulário digital" própria (hoje usa o fundo da apresentação
  original com textos de formulário).
* Ilustração do "mapa gráfico" de participantes chegando de várias regiões no comercial.
