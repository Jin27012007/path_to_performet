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
