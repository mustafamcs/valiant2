quest attr67 begin
	state start begin
		when 20095.chat.locale_quest(204) begin
			if pc.get_67attr_item() then
				if pc.getf2("67attr.time") < get_global_time() then
					if pc.getf2("67attr.succes") == 1 then
						say_reward_center(locale_quest(205))
					else
						say_reward_center(locale_quest(206))
					end
					pc.give_67attr_item()
					pc.delf("67attr","succes")
					pc.delf("67attr","time")
				else
					say_reward_center(string.format(locale_quest(207),CalculateTime(pc.getf2("67attr.time") - get_global_time())))
				end
			else
				setskin(NOWINDOW)
				game.open_67_attr()
			end
		end
	end
end