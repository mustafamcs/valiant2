quest fisher begin
	state start begin
		when 9009.chat.locale_quest(1301) begin
			npc.open_shop()
			setskin(NOWINDOW)
		end
	end
end
