quest dragon_soul begin
	state start begin
		when 20001.chat.locale_quest(961) begin
			say_title_center(mob_name(20001))
			say_reward_center(locale_quest(962))
			ds.open_refine_window()
		end

		when 20001.chat.locale_quest(203) begin
			setskin(NOWINDOW)
			command("cube open")
		end

		when 20001.chat.locale_quest(208) begin
			say_title_center(mob_name(20001))
			say("")say("")
			say_reward_center(locale_quest(202))
		end

		when 20001.take with item.vnum >= 115400 and item.vnum <= 115460 begin
			say_title_center(mob_name(20001))
			say("")
			say_show_item(115400)
			say_reward_center(string.format(locale_quest(200),item_name(115400)))
			say_show_item(115300)
			say_reward_center(string.format(locale_quest(201),item_name(115300)))
			say("")say("")
			local s = select(locale_quest(2625), locale_quest(40))
			if s == 1 then
				item.remove()
				pc.give_item2(115300)
			else
				return
			end
		end

		when 20001.take with item.vnum >= 125400 and item.vnum <= 125460 begin
			say_title_center(mob_name(20001))
			say("")
			say_show_item(125400)
			say_reward_center(string.format(locale_quest(200),item_name(125400)))
			say_show_item(125300)
			say_reward_center(string.format(locale_quest(201),item_name(125300)))
			say("")say("")
			local s = select(locale_quest(2625), locale_quest(40))
			if s == 1 then
				item.remove()
				pc.give_item2(125300)
			else
				return
			end
		end

		when 20001.take with item.vnum >= 135400 and item.vnum <= 135460 begin
			say_title_center(mob_name(20001))
			say("")
			say_show_item(135400)
			say_reward_center(string.format(locale_quest(200),item_name(135400)))
			say_show_item(135300)
			say_reward_center(string.format(locale_quest(201),item_name(135300)))
			say("")say("")
			local s = select(locale_quest(2625), locale_quest(40))
			if s == 1 then
				item.remove()
				pc.give_item2(135300)
			else
				return
			end
		end

		when 20001.take with item.vnum >= 145400 and item.vnum <= 145460 begin
			say_title_center(mob_name(20001))
			say("")
			say_show_item(145400)
			say_reward_center(string.format(locale_quest(200),item_name(145400)))
			say_show_item(145300)
			say_reward_center(string.format(locale_quest(201),item_name(145300)))
			say("")say("")
			local s = select(locale_quest(2625), locale_quest(40))
			if s == 1 then
				item.remove()
				pc.give_item2(145300)
			else
				return
			end
		end

		when 20001.take with item.vnum >= 155400 and item.vnum <= 155460 begin
			say_title_center(mob_name(20001))
			say("")
			say_show_item(155400)
			say_reward_center(string.format(locale_quest(200),item_name(155400)))
			say_show_item(155300)
			say_reward_center(string.format(locale_quest(201),item_name(155300)))
			say("")say("")
			local s = select(locale_quest(2625), locale_quest(40))
			if s == 1 then
				item.remove()
				pc.give_item2(155300)
			else
				return
			end
		end

		when 20001.take with item.vnum >= 165400 and item.vnum <= 165460 begin
			say_title_center(mob_name(20001))
			say("")
			say_show_item(165400)
			say_reward_center(string.format(locale_quest(200),item_name(165400)))
			say_show_item(165300)
			say_reward_center(string.format(locale_quest(201),item_name(165300)))
			say("")say("")
			local s = select(locale_quest(2625), locale_quest(40))
			if s == 1 then
				item.remove()
				pc.give_item2(165300)
			else
				return
			end
		end

	end
end
