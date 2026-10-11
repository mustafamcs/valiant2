quest shop_talks begin
	state start begin
		when 9002.chat.HeaderChat(LC(), 30000) begin
			setskin (NOWINDOW)
			npc.open_shop(920)
		end
		when 9002.chat.HeaderChat(LC(), 30001) begin
			setskin (NOWINDOW)
			npc.open_shop(921)
		end
		when 9001.chat.HeaderChat(LC(), 30002) begin
			setskin (NOWINDOW)
			npc.open_shop(922)
		end
		when 9001.chat.HeaderChat(LC(), 30003) begin
			setskin (NOWINDOW)
			npc.open_shop(923)
		end
		when 9002.chat.HeaderChat(LC(), 30004) begin
			setskin (NOWINDOW)
			npc.open_shop(924)
		end
		when 20421.chat.HeaderChat(LC(), 30006) begin
			setskin (NOWINDOW)
			npc.open_shop(926)
		end
		when 60003.chat.HeaderChat(LC(), 30005) begin
			setskin (NOWINDOW)
			npc.open_shop(7)
		end
		when 20013.chat.HeaderChat(LC(), 30005) begin
			setskin (NOWINDOW)
			npc.open_shop(2)
		end

		-- BETA NPC

		-- when 45022.chat."Get Level" begin
			-- local choice = select("Level 30", "Level 50", "Level 75", "Level 90", "Level 105", "Level 120")

			-- if choice == 1 then
				-- pc.set_level(30)
			-- elseif choice == 2 then
				-- pc.set_level(50)
			-- elseif choice == 3 then
				-- pc.set_level(75)
			-- elseif choice == 4 then
				-- pc.set_level(90)
			-- elseif choice == 5 then
				-- pc.set_level(105)
			-- elseif choice == 6 then
				-- pc.set_level(120)
			-- end
			-- say("Getting level was sucessfull!")
		-- end

		-- when 45022.chat."Get Yang" begin
			-- if pc.getgold() >= 100000000000 then
				-- say("You can not get more yang!")
			
			-- else
				-- pc.changegold(10000000000)
				-- say("You received 10kkk yang!")
			-- end
		-- end

		-- when 45022.chat.HeaderChat(LC(), 30005) begin
			-- setskin (NOWINDOW)
			-- npc.open_shop(1000)
		-- end
		-- when 45022.chat.HeaderChat(LC(), 30005) begin
			-- setskin (NOWINDOW)
			-- npc.open_shop(1001)
		-- end
		-- when 45022.chat.HeaderChat(LC(), 30005) begin
			-- setskin (NOWINDOW)
			-- npc.open_shop(1002)
		-- end
		-- when 45022.chat.HeaderChat(LC(), 30005) begin
			-- setskin (NOWINDOW)
			-- npc.open_shop(1003)
		-- end
	end
end