quest acce begin
	state start begin
		when 60003.chat.locale_quest(20) begin
			say(locale_quest(21))
		end

		when 60003.chat.locale_quest(22) begin
			say(locale_quest(23))
			if select(locale_quest(4473), locale_quest(39)) == 1 then
				setskin(NOWINDOW)
				pc.open_sash(true)
			else return end
		end
		
		when 60003.chat.locale_quest(24) begin
			say(locale_quest(25))
			if select(locale_quest(4473), locale_quest(39)) == 1 then
				setskin(NOWINDOW)
				pc.open_sash(false)
			else return end
		end

		when 60003.chat.locale_quest(11829) begin
			setskin(NOWINDOW)
			pc.open_aura(true)
		end
		when 60003.chat.locale_quest(11825) begin
			setskin(NOWINDOW)
			pc.open_aura(false)
		end

	end
end