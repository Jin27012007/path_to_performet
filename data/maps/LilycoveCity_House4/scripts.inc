@ =============================================================================
@ Casa 4 — sala (Cena 7: presente antecipado e proposta de trabalho;
@                Cena 9: bilhete e liberdade)
@ =============================================================================

LilycoveCity_House4_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, LilycoveCity_House4_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, LilycoveCity_House4_OnFrame
	.byte 0

@ VAR_TEMP_1 = 1 bloqueia a saída enquanto o jogador ainda tem algo a fazer em casa.
LilycoveCity_House4_OnTransition:
	setrespawn HEAL_LOCATION_LILYCOVE_CITY       @ the house works as the player's Pokemon Center
	setvar VAR_TEMP_1, 0
	call_if_eq VAR_OPENING_STATE, OPENING_STATE_UNPACK, LilycoveCity_House4_EventScript_LockExit
	call_if_eq VAR_OPENING_STATE, OPENING_STATE_ROOM, LilycoveCity_House4_EventScript_LockExit
	call_if_eq VAR_OPENING_STATE, OPENING_STATE_FATHER_LEFT, LilycoveCity_House4_EventScript_LockExit
	call_if_eq VAR_OPENING_STATE, OPENING_STATE_NOTE, LilycoveCity_House4_EventScript_LockExit
	end

LilycoveCity_House4_EventScript_LockExit::
	setvar VAR_TEMP_1, 1
	return

LilycoveCity_House4_OnFrame:
	map_script_2 VAR_OPENING_STATE, OPENING_STATE_HOUSE, LilycoveCity_House4_EventScript_GiftsScene
	map_script_2 VAR_OPENING_STATE, OPENING_STATE_FATHER_LEFT, LilycoveCity_House4_EventScript_EmptyLivingRoom
	.2byte 0

@ ----------------------------------------------------------------- Cena 7
LilycoveCity_House4_EventScript_GiftsScene::
	lockall
	applymovement LOCALID_HOUSE4_FATHER, LilycoveCity_House4_Movement_FatherToTable
	waitmovement 0
	applymovement LOCALID_PLAYER, LilycoveCity_House4_Movement_PlayerToTable
	waitmovement 0
	affinity_show AFFINITY_FATHER
	msgbox LilycoveCity_House4_Text_FatherPutsObjects, MSGBOX_DEFAULT
	@ --- Ticket de Adoção (entregue uma única vez) ---
	goto_if_set FLAG_ADOPTION_TICKET_RECEIVED, LilycoveCity_House4_EventScript_TicketChoice
	msgbox LilycoveCity_House4_Text_FatherTicket, MSGBOX_DEFAULT
	giveitem ITEM_ADOPTION_TICKET
	setflag FLAG_ADOPTION_TICKET_RECEIVED
LilycoveCity_House4_EventScript_TicketChoice:
	msgbox LilycoveCity_House4_Text_WhatDoYouSay, MSGBOX_DEFAULT
	checkplayergender
	goto_if_eq VAR_RESULT, FEMALE, LilycoveCity_House4_EventScript_TicketChoiceFemale
	dynmultichoice 0, 7, TRUE, 3, 0, DYN_MULTICHOICE_CB_NONE, LilycoveCity_House4_Text_ChoiceTicketA_M, LilycoveCity_House4_Text_ChoiceTicketB, LilycoveCity_House4_Text_ChoiceTicketC
	goto LilycoveCity_House4_EventScript_TicketChoiceResult
LilycoveCity_House4_EventScript_TicketChoiceFemale:
	dynmultichoice 0, 7, TRUE, 3, 0, DYN_MULTICHOICE_CB_NONE, LilycoveCity_House4_Text_ChoiceTicketA_F, LilycoveCity_House4_Text_ChoiceTicketB, LilycoveCity_House4_Text_ChoiceTicketC
LilycoveCity_House4_EventScript_TicketChoiceResult:
	switch VAR_RESULT
	case 0, LilycoveCity_House4_EventScript_TicketA
	case 1, LilycoveCity_House4_EventScript_TicketB
	goto LilycoveCity_House4_EventScript_TicketC

LilycoveCity_House4_EventScript_TicketA:
	checkplayergender
	call_if_eq VAR_RESULT, MALE, LilycoveCity_House4_EventScript_SayTicketA_M
	call_if_eq VAR_RESULT, FEMALE, LilycoveCity_House4_EventScript_SayTicketA_F
	affinity_add AFFINITY_FATHER, 3
	msgbox LilycoveCity_House4_Text_FatherGoodPartner, MSGBOX_DEFAULT
	goto LilycoveCity_House4_EventScript_Rod
LilycoveCity_House4_EventScript_SayTicketA_M:
	msgbox LilycoveCity_House4_Text_SayTicketA_M, MSGBOX_DEFAULT
	return
LilycoveCity_House4_EventScript_SayTicketA_F:
	msgbox LilycoveCity_House4_Text_SayTicketA_F, MSGBOX_DEFAULT
	return
LilycoveCity_House4_EventScript_TicketB:
	msgbox LilycoveCity_House4_Text_SayTicketB, MSGBOX_DEFAULT
	affinity_add AFFINITY_FATHER, 1
	msgbox LilycoveCity_House4_Text_FatherAlreadyDone, MSGBOX_DEFAULT
	goto LilycoveCity_House4_EventScript_Rod
LilycoveCity_House4_EventScript_TicketC:
	msgbox LilycoveCity_House4_Text_SayTicketC, MSGBOX_DEFAULT
	affinity_add AFFINITY_FATHER, -3
	msgbox LilycoveCity_House4_Text_FatherItsYourBirthday, MSGBOX_DEFAULT
	goto LilycoveCity_House4_EventScript_Rod

	@ --- Vara de Pesca (entregue uma única vez) ---
LilycoveCity_House4_EventScript_Rod:
	msgbox LilycoveCity_House4_Text_FatherSomethingUseful, MSGBOX_DEFAULT
	goto_if_set FLAG_FISHING_ROD_RECEIVED, LilycoveCity_House4_EventScript_RodChoice
	giveitem ITEM_OLD_ROD
	setflag FLAG_FISHING_ROD_RECEIVED
LilycoveCity_House4_EventScript_RodChoice:
	msgbox LilycoveCity_House4_Text_RodIsAProposal, MSGBOX_DEFAULT
	dynmultichoice 0, 5, TRUE, 4, 0, DYN_MULTICHOICE_CB_NONE, LilycoveCity_House4_Text_ChoiceRodA, LilycoveCity_House4_Text_ChoiceRodB, LilycoveCity_House4_Text_ChoiceRodC, LilycoveCity_House4_Text_ChoiceRodD
	switch VAR_RESULT
	case 0, LilycoveCity_House4_EventScript_RodA
	case 1, LilycoveCity_House4_EventScript_RodB
	case 2, LilycoveCity_House4_EventScript_RodC
	goto LilycoveCity_House4_EventScript_RodD

LilycoveCity_House4_EventScript_RodA:
	msgbox LilycoveCity_House4_Text_SayRodA, MSGBOX_DEFAULT
	affinity_add AFFINITY_FATHER, 2
	msgbox LilycoveCity_House4_Text_FatherWillingToTalk, MSGBOX_DEFAULT
	goto LilycoveCity_House4_EventScript_FatherPosition
LilycoveCity_House4_EventScript_RodB:
	msgbox LilycoveCity_House4_Text_SayRodB, MSGBOX_DEFAULT
	affinity_add AFFINITY_FATHER, -2
	msgbox LilycoveCity_House4_Text_FatherIgnoringRisk, MSGBOX_DEFAULT
	goto LilycoveCity_House4_EventScript_FatherPosition
LilycoveCity_House4_EventScript_RodC:
	msgbox LilycoveCity_House4_Text_SayRodC, MSGBOX_DEFAULT
	affinity_add AFFINITY_FATHER, -1
	msgbox LilycoveCity_House4_Text_FatherStableLife, MSGBOX_DEFAULT
	msgbox LilycoveCity_House4_Text_FatherPosition, MSGBOX_DEFAULT
	@ O protagonista confronta o pai sobre o passado; ele interrompe.
	msgbox LilycoveCity_House4_Text_PlayerConfronts, MSGBOX_DEFAULT
	goto LilycoveCity_House4_EventScript_EndGifts
LilycoveCity_House4_EventScript_RodD:
	msgbox LilycoveCity_House4_Text_SayRodD, MSGBOX_DEFAULT
	affinity_add AFFINITY_FATHER, 3
	msgbox LilycoveCity_House4_Text_FatherAllIAsk, MSGBOX_DEFAULT
	goto LilycoveCity_House4_EventScript_FatherPosition

LilycoveCity_House4_EventScript_FatherPosition:
	msgbox LilycoveCity_House4_Text_FatherPosition, MSGBOX_DEFAULT
LilycoveCity_House4_EventScript_EndGifts:
	msgbox LilycoveCity_House4_Text_FatherNotNow, MSGBOX_DEFAULT
	closemessage
	affinity_hide
	setflag FLAG_HOUSE4_GIFTS_DONE
	setobjectxyperm LOCALID_HOUSE4_FATHER, 8, 4
	setvar VAR_OPENING_STATE, OPENING_STATE_UNPACK
	setvar VAR_TEMP_1, 1
	releaseall
	end

@ Pai na sala enquanto o protagonista ainda não guardou as malas.
LilycoveCity_House4_EventScript_Father::
	lock
	faceplayer
	affinity_show AFFINITY_FATHER
	msgbox LilycoveCity_House4_Text_FatherRoomAtEnd, MSGBOX_DEFAULT
	closemessage
	affinity_hide
	applymovement VAR_LAST_TALKED, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

@ ----------------------------------------------------------------- Cena 9
@ ON_FRAME: precisa mudar VAR_OPENING_STATE, senão rodaria a cada frame.
LilycoveCity_House4_EventScript_EmptyLivingRoom::
	lockall
	setflag FLAG_SAW_EMPTY_LIVING_ROOM
	setvar VAR_OPENING_STATE, OPENING_STATE_NOTE
	delay 20
	msgbox LilycoveCity_House4_Text_FatherIsGone, MSGBOX_DEFAULT
	closemessage
	releaseall
	end

LilycoveCity_House4_EventScript_Table::
	lockall
	goto_if_ge VAR_OPENING_STATE, OPENING_STATE_FATHER_LEFT, LilycoveCity_House4_EventScript_Note
	msgbox LilycoveCity_House4_Text_Table, MSGBOX_DEFAULT
	releaseall
	end

LilycoveCity_House4_EventScript_Note:
	msgbox LilycoveCity_House4_Text_Note, MSGBOX_DEFAULT
	goto_if_set FLAG_READ_FATHER_NOTE, LilycoveCity_House4_EventScript_NoteEnd
	msgbox LilycoveCity_House4_Text_HeIsGone, MSGBOX_DEFAULT
	setflag FLAG_READ_FATHER_NOTE
	setvar VAR_OPENING_STATE, OPENING_STATE_FREE
	setvar VAR_TEMP_1, 0
	playfanfare MUS_OBTAIN_ITEM
	message LilycoveCity_House4_Text_Objective
	waitfanfare
	waitmessage
	waitbuttonpress
LilycoveCity_House4_EventScript_NoteEnd:
	closemessage
	releaseall
	end

LilycoveCity_House4_EventScript_Calendar::
	msgbox LilycoveCity_House4_Text_Calendar, MSGBOX_SIGN
	end

LilycoveCity_House4_EventScript_Kitchen::
	msgbox LilycoveCity_House4_Text_Kitchen, MSGBOX_SIGN
	end

@ Impede sair de casa antes de guardar as malas / ler o bilhete.
LilycoveCity_House4_EventScript_BlockExit::
	lockall
	goto_if_ge VAR_OPENING_STATE, OPENING_STATE_FATHER_LEFT, LilycoveCity_House4_EventScript_BlockExitNote
	msgbox LilycoveCity_House4_Text_FatherStoreBagsFirst, MSGBOX_DEFAULT
	goto LilycoveCity_House4_EventScript_BlockExitEnd
LilycoveCity_House4_EventScript_BlockExitNote:
	msgbox LilycoveCity_House4_Text_ReadNoteFirst, MSGBOX_DEFAULT
LilycoveCity_House4_EventScript_BlockExitEnd:
	closemessage
	applymovement LOCALID_PLAYER, Common_Movement_WalkUp
	waitmovement 0
	releaseall
	end

LilycoveCity_House4_Movement_FatherToTable:
	walk_right
	walk_up
	walk_up
	walk_up
	walk_up
	walk_right
	face_left
	step_end

LilycoveCity_House4_Movement_PlayerToTable:
	walk_right
	walk_right
	walk_right
	walk_up
	walk_up
	walk_up
	walk_up
	face_right
	step_end

@ ----------------------------------------------------------------- textos
LilycoveCity_House4_Text_FatherPutsObjects:
	.string "Seu pai coloca dois objetos sobre\n"
	.string "a mesa.\p"
	.string "PAI: Seu aniversário é na semana\n"
	.string "que vem.\p"
	.string "Não sabia bem o que comprar,\n"
	.string "então consegui isto.$"

LilycoveCity_House4_Text_FatherTicket:
	.string "PAI: Um Ticket de Adoção. Dá direito\n"
	.string "a escolher um Pokémon no Safari.\p"
	.string "Achei que seria bom você ter um\n"
	.string "parceiro por aqui.$"

LilycoveCity_House4_Text_WhatDoYouSay:
	.string "O que você responde?$"

LilycoveCity_House4_Text_ChoiceTicketA_M:
	.string "Obrigado. Eu queria muito isso.$"
LilycoveCity_House4_Text_ChoiceTicketA_F:
	.string "Obrigada. Eu queria muito isso.$"
LilycoveCity_House4_Text_ChoiceTicketB:
	.string "Não precisava gastar com isso.$"
LilycoveCity_House4_Text_ChoiceTicketC:
	.string "Pelo menos nisso você pensou.$"

LilycoveCity_House4_Text_SayTicketA_M:
	.string "{PLAYER}: Obrigado. Eu queria muito\n"
	.string "ter meu próprio Pokémon.$"
LilycoveCity_House4_Text_SayTicketA_F:
	.string "{PLAYER}: Obrigada. Eu queria muito\n"
	.string "ter meu próprio Pokémon.$"
LilycoveCity_House4_Text_SayTicketB:
	.string "{PLAYER}: Você não precisava gastar\n"
	.string "com isso.$"
LilycoveCity_House4_Text_SayTicketC:
	.string "{PLAYER}: Pelo menos nisso você\n"
	.string "pensou.$"

LilycoveCity_House4_Text_FatherGoodPartner:
	.string "PAI: Então espero que encontre um\n"
	.string "bom parceiro.$"
LilycoveCity_House4_Text_FatherAlreadyDone:
	.string "PAI: Já estava resolvido.\n"
	.string "É seu presente.$"
LilycoveCity_House4_Text_FatherItsYourBirthday:
	.string "Seu pai fica em silêncio por um\n"
	.string "instante.\p"
	.string "PAI: …É seu aniversário.$"

LilycoveCity_House4_Text_FatherSomethingUseful:
	.string "PAI: E também trouxe uma coisa que\n"
	.string "pode ser útil.\p"
	.string "Uma Vara de Pesca. O pessoal da\n"
	.string "praia está precisando de ajuda.\p"
	.string "Você pode começar com a pesca e\n"
	.string "receber por isso.\p"
	.string "É um trabalho honesto.$"

LilycoveCity_House4_Text_RodIsAProposal:
	.string "A vara não é só um presente.\n"
	.string "É a proposta de trabalho dele.$"

LilycoveCity_House4_Text_ChoiceRodA:
	.string "Ajudar às vezes, mas competir$"
LilycoveCity_House4_Text_ChoiceRodB:
	.string "Vim pelos Concursos$"
LilycoveCity_House4_Text_ChoiceRodC:
	.string "Questionar o caminho dele$"
LilycoveCity_House4_Text_ChoiceRodD:
	.string "Ajudar até me organizar$"

LilycoveCity_House4_Text_SayRodA:
	.string "{PLAYER}: Posso ajudar às vezes,\n"
	.string "mas quero competir.$"
LilycoveCity_House4_Text_SayRodB:
	.string "{PLAYER}: Eu não vim para trabalhar\n"
	.string "na praia. Vim pelos Concursos.$"
LilycoveCity_House4_Text_SayRodC:
	.string "{PLAYER}: Você quer que eu siga o\n"
	.string "mesmo caminho que você escolheu\l"
	.string "para mim?$"
LilycoveCity_House4_Text_SayRodD:
	.string "{PLAYER}: Talvez eu possa começar\n"
	.string "ajudando até me organizar.$"

LilycoveCity_House4_Text_FatherWillingToTalk:
	.string "PAI: Pelo menos está disposto a\n"
	.string "conversar.$"
LilycoveCity_House4_Text_FatherIgnoringRisk:
	.string "PAI: Você está ignorando o risco.$"
LilycoveCity_House4_Text_FatherStableLife:
	.string "PAI: Quero que tenha uma vida\n"
	.string "estável.$"
LilycoveCity_House4_Text_FatherAllIAsk:
	.string "PAI: É tudo o que estou pedindo\n"
	.string "por enquanto.$"

LilycoveCity_House4_Text_FatherPosition:
	.string "PAI: Eu não vou bancar uma carreira\n"
	.string "incerta.\p"
	.string "A pesca é um caminho seguro.\n"
	.string "É o que eu posso te oferecer.$"

LilycoveCity_House4_Text_PlayerConfronts:
	.string "{PLAYER}: Seguro? Você passou anos\n"
	.string "longe, tentando as Ligas, e a mãe…$"

LilycoveCity_House4_Text_FatherNotNow:
	.string "PAI: Não vamos começar com isso agora.\p"
	.string "Guarde suas malas. O quarto está no\n"
	.string "fim do corredor.$"

LilycoveCity_House4_Text_FatherRoomAtEnd:
	.string "PAI: O quarto está no fim do\n"
	.string "corredor.$"

LilycoveCity_House4_Text_FatherStoreBagsFirst:
	.string "PAI: Guarde suas malas primeiro.\n"
	.string "O quarto está no fim do corredor.$"

LilycoveCity_House4_Text_ReadNoteFirst:
	.string "Tem um bilhete em cima da mesa.\n"
	.string "Melhor ler antes de sair.$"

LilycoveCity_House4_Text_FatherIsGone:
	.string "Seu pai não está mais em casa.\p"
	.string "Tem um bilhete sobre a mesa.$"

LilycoveCity_House4_Text_Table:
	.string "Uma mesa simples. Ainda tem a marca\n"
	.string "de onde seu pai deixou os presentes.$"

LilycoveCity_House4_Text_Note:
	.string "BILHETE: Fui para a praia. Se precisar\n"
	.string "de mim, estarei perto dos barcos\l"
	.string "de pesca.\p"
	.string "Não esqueça de levar o ticket\n"
	.string "ao Safari.$"

LilycoveCity_House4_Text_HeIsGone:
	.string "Ele já foi…\p"
	.string "Pelo menos agora posso decidir\n"
	.string "por mim.$"

LilycoveCity_House4_Text_Objective:
	.string "OBJETIVO: Vá ao Safari e escolha seu\n"
	.string "primeiro Pokémon usando o Ticket\l"
	.string "de Adoção.$"

LilycoveCity_House4_Text_Calendar:
	.string "Um calendário. Seu aniversário está\n"
	.string "marcado daqui a sete dias.\p"
	.string "Não há nenhuma decoração de festa.$"

LilycoveCity_House4_Text_Kitchen:
	.string "Uma cozinha compacta. Panelas\n"
	.string "lavadas e uma garrafa de café.$"

@ Depois de perder: o jogador volta para casa, descansa e o time se recupera.
LilycoveCity_House4_EventScript_WhiteoutRest::
	lockall
	msgbox LilycoveCity_House4_Text_RestedAtHome, MSGBOX_DEFAULT
	call Common_EventScript_OutOfCenterPartyHeal
	fadedefaultbgm
	releaseall
	end

LilycoveCity_House4_Text_RestedAtHome:
	.string "Você voltou para casa e descansou\n"
	.string "um pouco.\p"
	.string "Seus POKéMON estão recuperados!$"
