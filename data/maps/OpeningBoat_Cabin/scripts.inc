@ =============================================================================
@ Barco — cabine (fim do comercial + Cena 3: exploração)
@ Nenhum objeto da cabine altera afinidade: o pai não está presente.
@ =============================================================================

OpeningBoat_Cabin_MapScripts::
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, OpeningBoat_Cabin_OnWarp
	map_script MAP_SCRIPT_ON_FRAME_TABLE, OpeningBoat_Cabin_OnFrame
	.byte 0

OpeningBoat_Cabin_OnWarp:
	map_script_2 VAR_OPENING_STATE, OPENING_STATE_CABIN, OpeningBoat_Cabin_EventScript_FaceLuggage
	.2byte 0

OpeningBoat_Cabin_EventScript_FaceLuggage::
	turnobject LOCALID_PLAYER, DIR_EAST
	end

OpeningBoat_Cabin_OnFrame:
	map_script_2 VAR_OPENING_STATE, OPENING_STATE_CABIN, OpeningBoat_Cabin_EventScript_CommercialEnds
	.2byte 0

@ O comercial termina; a câmera "recua" e revela o monitor da cabine.
OpeningBoat_Cabin_EventScript_CommercialEnds::
	lockall
	setvar VAR_OPENING_STATE, OPENING_STATE_CABIN_FREE
	delay 30
	msgbox OpeningBoat_Cabin_Text_CommercialEnds, MSGBOX_DEFAULT
	closemessage
	fadedefaultbgm
	releaseall
	end

OpeningBoat_Cabin_EventScript_Luggage::
	msgbox OpeningBoat_Cabin_Text_Luggage, MSGBOX_SIGN
	end

OpeningBoat_Cabin_EventScript_Photo::
	lockall
	msgbox OpeningBoat_Cabin_Text_Photo, MSGBOX_DEFAULT
	msgbox OpeningBoat_Cabin_Text_PhotoThought, MSGBOX_DEFAULT
	releaseall
	end

OpeningBoat_Cabin_EventScript_Papers::
	lockall
	msgbox OpeningBoat_Cabin_Text_Papers, MSGBOX_DEFAULT
	msgbox OpeningBoat_Cabin_Text_PapersThought, MSGBOX_DEFAULT
	releaseall
	end

OpeningBoat_Cabin_EventScript_Phone::
	lockall
	msgbox OpeningBoat_Cabin_Text_Phone, MSGBOX_DEFAULT
	msgbox OpeningBoat_Cabin_Text_PhoneThought, MSGBOX_DEFAULT
	releaseall
	end

OpeningBoat_Cabin_EventScript_Monitor::
	msgbox OpeningBoat_Cabin_Text_Monitor, MSGBOX_SIGN
	end

OpeningBoat_Cabin_EventScript_Window::
	lockall
	msgbox OpeningBoat_Cabin_Text_Window, MSGBOX_DEFAULT
	msgbox OpeningBoat_Cabin_Text_WindowThought, MSGBOX_DEFAULT
	releaseall
	end

OpeningBoat_Cabin_Text_CommercialEnds:
	.string "O comercial termina com o emblema\n"
	.string "da temporada, no pequeno monitor\l"
	.string "da cabine.\p"
	.string "Você está perto da bagagem.\n"
	.string "O barco balança devagar.$"

OpeningBoat_Cabin_Text_Luggage:
	.string "Algumas roupas, documentos e seus\n"
	.string "pertences.\p"
	.string "O restante da sua vida ficou\n"
	.string "em Kalos.$"

OpeningBoat_Cabin_Text_Photo:
	.string "Uma foto sua com sua mãe.\p"
	.string "Ela parece cansada, mas está\n"
	.string "sorrindo.$"

OpeningBoat_Cabin_Text_PhotoThought:
	.string "Mãe… eu consegui chegar até aqui.\n"
	.string "Você teria achado essa cidade bonita.$"

OpeningBoat_Cabin_Text_Papers:
	.string "Recibos e papéis antigos.\p"
	.string "Você prefere não reler aquilo agora.$"

OpeningBoat_Cabin_Text_PapersThought:
	.string "Eu ainda lembro das ligações.\p"
	.string "Sempre diziam que a gente precisava\n"
	.string "de mais tempo… e de mais dinheiro.$"

OpeningBoat_Cabin_Text_Phone:
	.string "A última mensagem do seu pai:\p"
	.string "“Estarei no porto quando chegar.”$"

OpeningBoat_Cabin_Text_PhoneThought:
	.string "Ele disse que vai estar esperando.\p"
	.string "Faz tanto tempo que a gente não\n"
	.string "fica no mesmo lugar…$"

OpeningBoat_Cabin_Text_Monitor:
	.string "A Temporada Mundial de Concursos\n"
	.string "será realizada em Lilycove…$"

OpeningBoat_Cabin_Text_Window:
	.string "O mar se estende até o horizonte.\p"
	.string "Você está deixando Kalos para trás.$"

OpeningBoat_Cabin_Text_WindowThought:
	.string "Se eu conseguir competir de verdade,\n"
	.string "talvez consiga me sustentar.\p"
	.string "Não posso depender de alguém para\n"
	.string "decidir o que acontece comigo.$"
