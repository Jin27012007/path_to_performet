@ =============================================================================
@ Casa 4 — quarto extra (Cena 8: quarto e malas)
@ =============================================================================

LilycoveCity_House4_Room_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, LilycoveCity_House4_Room_OnFrame
	.byte 0

LilycoveCity_House4_Room_OnFrame:
	map_script_2 VAR_OPENING_STATE, OPENING_STATE_UNPACK, LilycoveCity_House4_Room_EventScript_FirstEnter
	.2byte 0

LilycoveCity_House4_Room_EventScript_FirstEnter::
	lockall
	delay 16
	msgbox LilycoveCity_House4_Room_Text_ThisIsMyRoom, MSGBOX_DEFAULT
	closemessage
	setvar VAR_OPENING_STATE, OPENING_STATE_ROOM
	releaseall
	end

@ Uma única interação organiza tudo (fade simples).
LilycoveCity_House4_Room_EventScript_Bags::
	lockall
	msgbox LilycoveCity_House4_Room_Text_Bags, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	playse SE_CLICK
	delay 30
	playse SE_CLICK
	delay 30
	removeobject LOCALID_HOUSE4_ROOM_BAGS
	setflag FLAG_BAGS_STORED
	@ Enquanto o protagonista arruma o quarto, o pai sai para trabalhar.
	setflag FLAG_FATHER_LEFT_FOR_WORK
	setflag FLAG_HIDE_HOUSE4_FATHER
	clearflag FLAG_HIDE_LILYCOVE_FATHER_BEACH
	setvar VAR_OPENING_STATE, OPENING_STATE_FATHER_LEFT
	delay 20
	fadescreen FADE_FROM_BLACK
	msgbox LilycoveCity_House4_Room_Text_Done, MSGBOX_DEFAULT
	releaseall
	end

LilycoveCity_House4_Room_EventScript_Bed::
	msgbox LilycoveCity_House4_Room_Text_Bed, MSGBOX_SIGN
	end

LilycoveCity_House4_Room_EventScript_Window::
	msgbox LilycoveCity_House4_Room_Text_Window, MSGBOX_SIGN
	end

LilycoveCity_House4_Room_EventScript_Desk::
	goto_if_set FLAG_BAGS_STORED, LilycoveCity_House4_Room_EventScript_DeskAfter
	msgbox LilycoveCity_House4_Room_Text_Desk, MSGBOX_SIGN
	end
LilycoveCity_House4_Room_EventScript_DeskAfter:
	msgbox LilycoveCity_House4_Room_Text_DeskAfter, MSGBOX_SIGN
	end

LilycoveCity_House4_Room_Text_ThisIsMyRoom:
	.string "Então… este é meu quarto.\p"
	.string "Pelo menos agora tenho um lugar\n"
	.string "para ficar. Vou ter que arrumar tudo.$"

LilycoveCity_House4_Room_Text_Bags:
	.string "Suas malas. Hora de arrumar as\n"
	.string "coisas.$"

LilycoveCity_House4_Room_Text_Done:
	.string "Pronto. Não é muito, mas é meu\n"
	.string "espaço por enquanto.$"

LilycoveCity_House4_Room_Text_Bed:
	.string "O colchão é antigo, mas parece\n"
	.string "confortável o bastante.$"

LilycoveCity_House4_Room_Text_Window:
	.string "Dá para ver uma parte de Lilycove.$"

LilycoveCity_House4_Room_Text_Desk:
	.string "Está vazia. Talvez eu possa colocar\n"
	.string "minhas coisas aqui.$"

LilycoveCity_House4_Room_Text_DeskAfter:
	.string "Seus documentos e a foto com sua mãe\n"
	.string "agora estão sobre a escrivaninha.$"
