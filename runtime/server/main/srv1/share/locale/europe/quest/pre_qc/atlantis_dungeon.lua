quest atlantis_dungeon begin
	state start begin
--------------------------------------------------------------------------------------------------
----------------------------------------FUNCTION--------------------------------------------------
--------------------------------------------------------------------------------------------------
		function setting()
		return {
				["floor_cordinat"] = {
					{ 9415, 7038 },--slot
					{ 9415, 7038 },--metin
					{ 9415, 7038 },--totem
					{ 9415, 7038 },--mini_boss
					{ 9415, 7038 },--boss
				},
				["map_index"] = 306,
				--metin - totem - mini_boss - boss
				["mob_vnum"] = { 40141, 40140, 40142, 40143 },
				["totem_item_vnum"] = 200555,
				["totem_cordinat"] = {
					{ 185, 204 },
					{ 214, 204 },
					{ 214, 162 },
					{ 185, 162 },
				},
			}
		end

		function spawn_totem()
			local setting = atlantis_dungeon.setting() 
			local totemCord = setting.totem_cordinat
			local t1 = d.spawn_mob_ac_dir(setting.mob_vnum[2], totemCord[1][1], totemCord[1][2], 0)
			local t2 = d.spawn_mob_ac_dir(setting.mob_vnum[2], totemCord[2][1], totemCord[2][2], 0)
			local t3 = d.spawn_mob_ac_dir(setting.mob_vnum[2], totemCord[3][1], totemCord[3][2], 0)
			local t4 = d.spawn_mob_ac_dir(setting.mob_vnum[2], totemCord[4][1], totemCord[4][2], 0)
			d.setf("totem_vid1",t1)
			d.setf("totem_vid2",t2)
			d.setf("totem_vid3",t3)
			d.setf("totem_vid4",t4)
			d.setf("totemCount", 4)
		end
		
		function purge_totem()
			local totemCount = d.getf("totemCount")
			if totemCount == 4 then
				d.purge_vid(d.getf("totem_vid1"))
			elseif totemCount == 3 then
				d.purge_vid(d.getf("totem_vid2"))
			elseif totemCount == 2 then
				d.purge_vid(d.getf("totem_vid3"))
			elseif totemCount == 1 then
				d.purge_vid(d.getf("totem_vid4"))
				atlantis_dungeon.NextFloor()
			end
			d.setf("totemCount", totemCount - 1)
		end

		function set_regen(level)
			local regenList = {
				[1] = "data/dungeon/atlantis/regen_slot.txt",
				[2] = "data/dungeon/atlantis/regen_metin.txt",
				[3] = "data/dungeon/atlantis/regen_totem_slot.txt",
				[4] = "data/dungeon/atlantis/regen_mini_boss.txt",
				[5] = "data/dungeon/atlantis/regen_boss.txt"}
			d.set_regen_file(regenList[level])
			if level == 3 then
				atlantis_dungeon.spawn_totem()
			end
		end

		function make_dungeon()
			pc.setf("dungeon","floor", 1)
			atlantis_dungeon.set_regen(1)
			pc.chat(503)
			server_timer("Atlantisdungeon_finish_15",5*60, d.get_map_index())
		end

		function clear_timer()
			clear_server_timer("Atlantisdungeon_finish_15", get_server_timer_arg())
			clear_server_timer("Atlantisdungeon_finish_10", get_server_timer_arg())
			clear_server_timer("Atlantisdungeon_finish_5", get_server_timer_arg())
			clear_server_timer("Atlantisdungeon_finish_1", get_server_timer_arg())
			clear_server_timer("Atlantisdungeon_time_out", get_server_timer_arg())
			clear_server_timer("Atlantisdungeon_exit", get_server_timer_arg())
			clear_server_timer("Atlantisdungeon_floor_up", get_server_timer_arg())
			cleartimer("Atlantisdungeon_level")
		end

		function GetMapIndex()
			local setting = atlantis_dungeon.setting()
			return setting.map_index
		end

		function InDungeon()
			if pc.get_map_index() >= (atlantis_dungeon.GetMapIndex() * 10000) and pc.get_map_index() <= ((atlantis_dungeon.GetMapIndex() * 10000) + 9999) then
				return true
			end
			return false
		end

--------------------------------------------------------------------------------------------------
------------------------------------FLOOR LEVEL UP------------------------------------------------
--------------------------------------------------------------------------------------------------
		function NextFloor()
			d.kill_all()
			d.kill_all()
			d.clear_regen()
			d.zodiac_notice_clear()
			pc.zodiac_chat(510)
			timer("Atlantisdungeon_level",5)
			pc.setf("dungeon","floor", pc.getf("dungeon","floor") + 1)
		end

		when Atlantisdungeon_level.timer begin
			local floor = pc.getf("dungeon","floor")
			local setting = atlantis_dungeon.setting()
			-- local floorCordinat = setting.floor_cordinat[floor]
			-- pc.goto(floorCordinat[1],floorCordinat[2])
			atlantis_dungeon.set_regen(floor)

			d.zodiac_notice_clear()
			if floor == 1 then
				pc.zodiac_chat(514)
			elseif floor == 2 then
				pc.zodiac_chat(515)
			elseif floor == 3 then
				pc.zodiac_chat(516)
			elseif floor == 4 then
				pc.zodiac_chat(517)
			elseif floor == 5 then
				pc.zodiac_chat(518)
			end
		end

--------------------------------------------------------------------------------------------------
--------------------------------LOGÝN LOGOUT------------------------------------------------------
--------------------------------------------------------------------------------------------------
		when login begin
			local setting = atlantis_dungeon.setting()
			local playerMapIdx = pc.get_map_index()
			local dungeonMapIdx = setting.map_index
			if playerMapIdx >= (dungeonMapIdx * 10000) and playerMapIdx <= ((dungeonMapIdx * 10000) + 9999) then
				if d.getf("isLoaded") < 1 then
					atlantis_dungeon.make_dungeon()
					d.setf("isLoaded", 1)
					d.setInfo()
					pc.setf("dungeon","complete", 0)
				elseif pc.getf("dungeon","complete") == 0 then
					local floor = pc.getf("dungeon","floor")
					if floor > 1 then
						local floorCordinat = setting.floor_cordinat[floor]
						pc.goto(floorCordinat[1],floorCordinat[2])
					end
				end
			elseif dungeonMapIdx == playerMapIdx then
				if pc.getf("dungeon","complete") == 0 then
					local floor = pc.getf("dungeon","floor")
					if floor > 0 then
						local floorCordinat = setting.floor_cordinat[floor]
						d.turnBack(floorCordinat[1] * 100, floorCordinat[2] * 100)
					end
				end
			end
		end

		when logout with atlantis_dungeon.InDungeon() begin
			if pc.getf("dungeon","complete") == 1 then
				atlantis_dungeon.clear_timer()
			end
		end
--------------------------------------------------------------------------------------------------
-----------------------------------------FLOOR 1--------------------------------------------------
--------------------------------------------------------------------------------------------------
		when kill with atlantis_dungeon.InDungeon() and pc.getf("dungeon","floor") == 1 begin
			local count = d.getf("killcount") + 1
			if count < 100 then
				d.setf("killcount", count)
				pc.zodiac_chat(509, "%s", 100 - count)
			else
				atlantis_dungeon.NextFloor()
				d.setf("killcount", 0)
			end
		end
--------------------------------------------------------------------------------------------------
-----------------------------------------FLOOR 2--------------------------------------------------
--------------------------------------------------------------------------------------------------
		when kill with atlantis_dungeon.InDungeon() and pc.getf("dungeon","floor") == 2 begin
			local setting = atlantis_dungeon.setting()
			if npc.get_race() == setting.mob_vnum[1] then
				local count = d.getf("killcount") + 1
				if count < 6 then
					d.setf("killcount", count)
					pc.zodiac_chat(511, "%s", 6 - count)
				else
					atlantis_dungeon.NextFloor()
					d.setf("killcount", 0)
				end
			end
		end
--------------------------------------------------------------------------------------------------
-----------------------------------------FLOOR 3--------------------------------------------------
--------------------------------------------------------------------------------------------------
		when kill with atlantis_dungeon.InDungeon() and pc.getf("dungeon","floor") == 3 begin
			if number(1,100) < 5 then
				local setting = atlantis_dungeon.setting()
				game.drop_item(setting.totem_item_vnum,1)
			end
		end

		when 200555.use with atlantis_dungeon.InDungeon() and pc.getf("dungeon","floor") == 3 begin
			if d.getf("totemCount") < 1 then
				return
			end
			local setting = atlantis_dungeon.setting()
			pc.remove_item(setting.totem_item_vnum, 1)
			atlantis_dungeon.purge_totem()
			if d.getf("totemCount") > 0 then
				d.zodiac_notice_clear()
				pc.zodiac_chat(513, "%s", d.getf("totemCount"))
			end
		end
--------------------------------------------------------------------------------------------------
-----------------------------------------FLOOR 4--------------------------------------------------
--------------------------------------------------------------------------------------------------
		when kill with atlantis_dungeon.InDungeon() and pc.getf("dungeon","floor") == 4 begin
			local setting = atlantis_dungeon.setting()
			if npc.get_race() == setting.mob_vnum[3] then
				atlantis_dungeon.NextFloor()
			end
		end
--------------------------------------------------------------------------------------------------
-----------------------------------------FLOOR 5--------------------------------------------------
--------------------------------------------------------------------------------------------------
		when kill with atlantis_dungeon.InDungeon() and pc.getf("dungeon","floor") == 5 begin
			local setting = atlantis_dungeon.setting()
			if npc.get_race() == setting.mob_vnum[4] then
				d.zodiac_notice_clear()
				pc.zodiac_chat(512)
				pc.setf("dungeon","complete", 1)
				d.setf("complete", 1)
				pc.complete_dungeon()
				d.battlepass_update_progress(setting.map_index)
				server_timer("Atlantisdungeon_exit",30, d.get_map_index())
			end
		end
--------------------------------------------------------------------------------------------------
-----------------------------------------DUNGEON TIMER---------------------------------------------
--------------------------------------------------------------------------------------------------
		when Atlantisdungeon_finish_15.server_timer begin
			if d.select(get_server_timer_arg()) then
				d.zodiac_notice_clear()
				d.zodiac_chat(504)
				server_timer("Atlantisdungeon_finish_10", 5*60, d.get_map_index())
			end
		end

		when Atlantisdungeon_finish_10.server_timer begin
			if d.select(get_server_timer_arg()) then
				d.zodiac_notice_clear()
				d.zodiac_chat(505)
				server_timer("Atlantisdungeon_finish_5",5*60, d.get_map_index())
			end
		end

		when Atlantisdungeon_finish_5.server_timer begin
			if d.select(get_server_timer_arg()) then
				d.zodiac_notice_clear()
				d.zodiac_chat(506)
				server_timer("Atlantisdungeon_finish_1",4*60, d.get_map_index())
			end
		end

		when Atlantisdungeon_finish_1.server_timer begin
			if d.select(get_server_timer_arg()) then
				d.zodiac_notice_clear()
				d.zodiac_chat(507)
				server_timer("Atlantisdungeon_time_out",60, d.get_map_index())
			end
		end

		when Atlantisdungeon_time_out.server_timer begin
			if d.select(get_server_timer_arg()) then
				d.kill_all()
				d.kill_all()
				d.clear_regen()
				d.zodiac_notice_clear()
				d.zodiac_chat(508)
				server_timer("Atlantisdungeon_exit",5, d.get_map_index())
				pc.setf("dungeon","complete", 1)
				d.setf("complete", 1)
			end
		end

		when Atlantisdungeon_exit.server_timer begin
			if d.select(get_server_timer_arg()) then
				d.gohome()
			end
		end
	end
end