quest guild_war_join begin
	state start begin
		when letter  begin
			local e = guild.get_any_war()

			if e != 0 and pc.get_war_map() == 0 then
				setskin(NOWINDOW)
				send_letter(locale_quest(2617))
				--makequestbutton(locale_quest(2617))
			end
		end

		when button begin
			local e = guild.get_any_war()

			if e == 0 then
				say(locale_quest(2621))
			else
				say(string.format(locale_quest(1911), guild.name(e)))

				local s = select(locale_quest(2625), locale_quest(39))

				if s == 1 then
					guild.war_enter(e)
				else
					setskin(NOWINDOW)
					send_letter(locale_quest(2617))
					--makequestbutton(locale_quest(2617))
				end
			end
		end
	end
end
