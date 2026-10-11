quest status_reset begin
	state start begin
		when 71002.use begin
			say_title(locale_quest(8004))
			say(locale_quest(8015))
			local s = select(locale_quest(2625), locale_quest(39))
			if 2 == s then
				return
			end

			item.remove()
			pc.reset_point()
		end
	end
end
