@ =============================================================================
@ Barco — convés (Cena 4: aproximação de Lilycove e desembarque)
@ =============================================================================

OpeningBoat_Deck_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, OpeningBoat_Deck_OnFrame
	.byte 0

OpeningBoat_Deck_OnFrame:
	map_script_2 VAR_OPENING_STATE, OPENING_STATE_CABIN_FREE, OpeningBoat_Deck_EventScript_Announcement
	.2byte 0

@ Primeira vez no convés: o tripulante anuncia a aproximação.
OpeningBoat_Deck_EventScript_Announcement::
	lockall
	setvar VAR_OPENING_STATE, OPENING_STATE_DECK_FREE
	delay 30
	playse SE_DING_DONG
	waitse
	msgbox OpeningBoat_Deck_Text_Announcement, MSGBOX_DEFAULT
	closemessage
	releaseall
	end

OpeningBoat_Deck_EventScript_Crew::
	lock
	faceplayer
	msgbox OpeningBoat_Deck_Text_ReadyToDisembark, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, OpeningBoat_Deck_EventScript_NotYet
	@ --- cutscene curta de chegada ---
	msgbox OpeningBoat_Deck_Text_LetsGo, MSGBOX_DEFAULT
	closemessage
	applymovement VAR_LAST_TALKED, Common_Movement_FaceOriginalDirection
	waitmovement 0
	playse SE_SHIP
	msgbox OpeningBoat_Deck_Text_ShipSlowsDown, MSGBOX_DEFAULT
	closemessage
	waitse
	setvar VAR_OPENING_STATE, OPENING_STATE_ARRIVING
	warp MAP_LILYCOVE_CITY, 27, 43
	waitstate
	release
	end

OpeningBoat_Deck_EventScript_NotYet::
	msgbox OpeningBoat_Deck_Text_TakeYourTime, MSGBOX_DEFAULT
	release
	end

OpeningBoat_Deck_EventScript_Passenger::
	msgbox OpeningBoat_Deck_Text_Passenger, MSGBOX_NPC
	end

OpeningBoat_Deck_EventScript_Passenger2::
	msgbox OpeningBoat_Deck_Text_Passenger2, MSGBOX_NPC
	end

OpeningBoat_Deck_EventScript_Railing::
	msgbox OpeningBoat_Deck_Text_Railing, MSGBOX_SIGN
	end

OpeningBoat_Deck_Text_Announcement:
	.string "TRIPULANTE: Estamos nos aproximando\n"
	.string "do porto de Lilycove.\p"
	.string "Recolham seus pertences e aguardem\n"
	.string "o desembarque.$"

OpeningBoat_Deck_Text_ReadyToDisembark:
	.string "TRIPULANTE: Já estamos chegando.\n"
	.string "Quer desembarcar agora?$"

OpeningBoat_Deck_Text_LetsGo:
	.string "TRIPULANTE: Certo. Por aqui.$"

OpeningBoat_Deck_Text_TakeYourTime:
	.string "TRIPULANTE: Sem pressa. Ainda dá\n"
	.string "para aproveitar a vista.$"

OpeningBoat_Deck_Text_ShipSlowsDown:
	.string "O barco reduz a velocidade.\n"
	.string "Lilycove surge logo à frente…$"

OpeningBoat_Deck_Text_Passenger:
	.string "Lilycove está cheia nesta época.\p"
	.string "Dizem que coordenadores de várias\n"
	.string "regiões já chegaram.$"

OpeningBoat_Deck_Text_Passenger2:
	.string "Vim só para assistir às apresentações.\n"
	.string "Dizem que os palcos estão enormes!$"

OpeningBoat_Deck_Text_Railing:
	.string "O vento do mar é mais forte aqui.\p"
	.string "Ao longe, a costa de Hoenn começa\n"
	.string "a tomar forma.$"
