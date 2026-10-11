quest change_empire begin
	state start begin
		when 71054.use begin
			say_title(locale_quest(125))
			say(locale_quest(147))
			if get_time() < pc.getqf("next_use_time") then
				say_title(locale_quest(148))
				say_reward(locale_quest(149))

				if pc.is_gm() then
					say(locale_quest(150))
					local s = select(locale_quest(4473), locale_quest(3418))
					if s == 1 then
						say(locale_quest(151))
						pc.setqf("next_use_time", 0)
					end
				end

				return
			end

			if change_empire.move_pc() == true then
				pc.setqf("next_use_time", get_time() + 86400 * 7)
			end
		end

		function move_pc()
			if pc.is_engaged() then
				say_title(locale_quest(148))
				say_reward(locale_quest(152))
				say(locale_quest(126))
				return false
			end

			if pc.is_married() then
				say_title(locale_quest(148))
				say_reward(locale_quest(152))
				say(locale_quest(127))
				return false
			end

			if pc.is_polymorphed() then
				say_title(locale_quest(148))
				say_reward(locale_quest(128))
				say(locale_quest(129))
				return false
			end

			if pc.has_guild() then
				say_title(locale_quest(148))
				say_reward(locale_quest(130))
				say(locale_quest(131))
				return false
			end

			if pc.get_money() < 500000 then
				say_title(locale_quest(148))
				say_reward(locale_quest(132))
				say(locale_quest(133))
				return false
			end

			say(locale_quest(134))
			local s = select("Shinsoo", "Chunjo", "Jinno", locale_quest(39))

			if 4 == s then
				return false
			end

			say_reward(locale_quest(139))

			local a = select(locale_quest(4473), locale_quest(2426))
			if 2 == a then
				return false
			end

			local ret = pc.change_empire(s)

			if ret == 999 then
				say_title(locale_quest(140))
				say_reward(locale_quest(141))
				pc.change_gold(-500000)
				pc.remove_item(71054)
				return true
			else
				if ret == 1 then
					say(locale_quest(143))
				elseif ret == 2 then
					say(locale_quest(144))
				elseif ret == 3 then
					say(locale_quest(145))
				else
					say(locale_quest(153))
				end
			end

			return false
		end
	end
end
