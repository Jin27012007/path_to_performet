@ Lilycove contest hack — scripts compartilhados da abertura

@ Usado por trainerbattle quando o jogador ainda não tem Pokémon.
EventScript_TrainerNoPartner::
	lock
	faceplayer
	msgbox Text_TrainerNoPartner, MSGBOX_DEFAULT
	release
	end

Text_TrainerNoPartner:
	.string "Você ainda não tem um Pokémon.\n"
	.string "Que tal voltar depois de encontrar\l"
	.string "um parceiro?$"

@ Mantém o jogador invisível durante as "tomadas" do comercial.
Opening_EventScript_HidePlayer::
	hideplayer
	end

Opening_Movement_PerformerJump:
	jump_in_place_down
	jump_in_place_down
	face_down
	step_end

Opening_Movement_PerformerSpin:
	face_left
	delay_4
	face_up
	delay_4
	face_right
	delay_4
	face_down
	jump_in_place_down
	step_end
