quest teleporter begin
	state start begin
		when 70058.use begin
			local s = select(gameforge[LC()][2479],gameforge[LC()][2478],gameforge[LC()][2480],gameforge[LC()][1434],gameforge[LC()][1437],gameforge[LC()][1438],gameforge[LC()][1435],gameforge[LC()][8277],gameforge[LC()][6689],gameforge[LC()][6486],gameforge[LC()][6482],gameforge[LC()][6487],gameforge[LC()][6461],gameforge[LC()][3572],gameforge[LC()][19000],gameforge[LC()][19041],gameforge[LC()][39])
			local empire = pc.get_empire()
			pc.window_close_all()
			if s == 1 then
				local yellowkingdom = select (gameforge[LC()][10570],gameforge[LC()][10571],gameforge[LC()][39])
				if yellowkingdom == 1 then
					pc.warp(55700, 158000)
					setskin(NOWINDOW)
				elseif yellowkingdom == 2 then
					pc.warp(137600 , 234600)
					setskin(NOWINDOW)
				end

			elseif s == 2 then
				local redkingdom = select (gameforge[LC()][10572],gameforge[LC()][10573],gameforge[LC()][39])
				if redkingdom == 1 then
					pc.warp(469300, 964200)
					setskin(NOWINDOW)
				elseif redkingdom == 2 then
					pc.warp(363000, 875300)
					setskin(NOWINDOW)
				end


			elseif s == 3 then
				local bluekingdom = select (gameforge[LC()][10574],gameforge[LC()][10575],gameforge[LC()][39])
				if bluekingdom == 1 then
					pc.warp(969300, 278400)
					setskin(NOWINDOW)
				elseif bluekingdom == 2 then
					pc.warp(872600, 243100)
					setskin(NOWINDOW)
				end

			elseif s == 4 then
				local valley = select (gameforge[LC()][19001],gameforge[LC()][19002],gameforge[LC()][19003] ,gameforge[LC()][39])

				if valley == 1 then
					if(pc.get_level() < 20) then
						say_title(gameforge[LC()][31000])
						say(string.format(gameforge[LC()][31001], 20))
						return
					else
						pc.warp(418900, 740600)
						setskin(NOWINDOW)
					end

				elseif valley == 2 then
					if(pc.get_level() < 20) then
						say_title(gameforge[LC()][31000])
						say(string.format(gameforge[LC()][31001], 20))
						return
					else
						pc.warp(361600, 755600)
						setskin(NOWINDOW)
					end

				elseif valley == 3 then
					if(pc.get_level() < 20) then
						say_title(gameforge[LC()][31000])
						say(string.format(gameforge[LC()][31001], 20))
						return
					else
						pc.warp(351100, 805600)
						setskin(NOWINDOW)
					end
				end

			elseif s == 5 then
				local desert = select (gameforge[LC()][19004],gameforge[LC()][19005],gameforge[LC()][19006] ,gameforge[LC()][39])
				
				if desert == 1 then
					if(pc.get_level() < 30) then
						say_title(gameforge[LC()][31000])
						say(string.format(gameforge[LC()][31001], 30))
						return
					else
						pc.warp(238400, 516300)
						setskin(NOWINDOW)
					end

				elseif desert == 2 then
					if(pc.get_level() < 30) then
						say_title(gameforge[LC()][31000])
						say(string.format(gameforge[LC()][31001], 30))
						return
					else
						pc.warp(296800, 547400)
						setskin(NOWINDOW)
					end

				elseif desert == 3 then
					if(pc.get_level() < 30) then
						say_title(gameforge[LC()][31000])
						say(string.format(gameforge[LC()][31001], 30))
						return
					else
						pc.warp(291100, 605900)
						setskin(NOWINDOW)
					end
				end

			elseif s == 6 then
				local hwang = select (gameforge[LC()][19007],gameforge[LC()][19008],gameforge[LC()][19009] ,gameforge[LC()][39])
				
				if hwang == 1 then
					if(pc.get_level() < 40) then
						say_title(gameforge[LC()][31000])
						say(string.format(gameforge[LC()][31001], 40))
						return
					else
						pc.warp(553700, 144000)
						setskin(NOWINDOW)
					end

				elseif hwang == 2 then
					if(pc.get_level() < 40) then
						say_title(gameforge[LC()][31000])
						say(string.format(gameforge[LC()][31001], 40))
						return
					else
						pc.warp(605400, 65200)
						setskin(NOWINDOW)
					end

				elseif hwang == 3 then
					if(pc.get_level() < 40) then
						say_title(gameforge[LC()][31000])
						say(string.format(gameforge[LC()][31001], 40))
						return
					else
						pc.warp(628700, 142400)
						setskin(NOWINDOW)
					end
				end

			elseif s == 7 then
				local sohan = select (gameforge[LC()][19010],gameforge[LC()][19011],gameforge[LC()][19012] ,gameforge[LC()][39])
				
				if sohan == 1 then
					if(pc.get_level() < 50) then
						say_title(gameforge[LC()][31000])
						say(string.format(gameforge[LC()][31001], 50))
						return
					else
						pc.warp(498800, 292600)
						setskin(NOWINDOW)
					end

				elseif sohan == 2 then
					if(pc.get_level() < 50) then
						say_title(gameforge[LC()][31000])
						say(string.format(gameforge[LC()][31001], 50))
						return
					else
						pc.warp(436400, 215600)
						setskin(NOWINDOW)
					end

				elseif sohan == 3 then
					if(pc.get_level() < 50) then
						say_title(gameforge[LC()][31000])
						say(string.format(gameforge[LC()][31001], 50))
						return
					else
						pc.warp(482900, 242900)
						setskin(NOWINDOW)
					end
				end

			elseif s == 8 then
				local spiderdungeon = select (gameforge[LC()][19034],gameforge[LC()][19035],gameforge[LC()][19036] ,gameforge[LC()][39])

				if spiderdungeon == 1 then
					if(pc.get_level() < 40) then
						say_title(gameforge[LC()][31000])
						say(string.format(gameforge[LC()][31001], 40))
						return
					else
						pc.warp(92100, 525500)
						setskin(NOWINDOW)
					end

				elseif spiderdungeon == 2 then
					if(pc.get_level() < 50) then
						say_title(gameforge[LC()][31000])
						say(string.format(gameforge[LC()][31001], 50))
						return
					else
						pc.warp(704100, 524800)
						setskin(NOWINDOW)
					end

				elseif spiderdungeon == 3 then
					if(pc.get_level() < 55) then
						say_title(gameforge[LC()][31000])
						say(string.format(gameforge[LC()][31001], 55))
						return
					else
						pc.warp(69000, 689800)
						setskin(NOWINDOW)
					end
				end

			elseif s == 9 then
				local doyum = select (gameforge[LC()][19013],gameforge[LC()][19014],gameforge[LC()][19015],gameforge[LC()][39])

				if doyum == 1 then
					if(pc.get_level() < 60) then
						say_title(gameforge[LC()][31000])
						say(string.format(gameforge[LC()][31001], 60))
						return
					else
						pc.warp(728900, 628900)
						setskin(NOWINDOW)
					end

				elseif doyum == 2 then
					if(pc.get_level() < 60) then
						say_title(gameforge[LC()][31000])
						say(string.format(gameforge[LC()][31001], 60))
						return
					else
						pc.warp(600800, 687400)
						setskin(NOWINDOW)
					end

				elseif doyum == 3 then
					if(pc.get_level() < 60) then
						say_title(gameforge[LC()][31000])
						say(string.format(gameforge[LC()][31001], 60))
						return
					else
						pc.warp(599500, 757500)
						setskin(NOWINDOW)
					end
				end

			elseif s == 10 then
				local ghostforest = select (gameforge[LC()][19016],gameforge[LC()][19017],gameforge[LC()][19018] ,gameforge[LC()][39])

				if ghostforest == 1 then
					if(pc.get_level() < 70) then
						say_title(gameforge[LC()][31000])
						say(string.format(gameforge[LC()][31001], 70))
						return
					else
						pc.warp(295700, 5700)
						setskin(NOWINDOW)
					end

				elseif ghostforest == 2 then
					if(pc.get_level() < 70) then
						say_title(gameforge[LC()][31000])
						say(string.format(gameforge[LC()][31001], 70))
						return
					else
						pc.warp(303700, 26900)
						setskin(NOWINDOW)
					end

				elseif ghostforest == 3 then
					if(pc.get_level() < 70) then
						say_title(gameforge[LC()][31000])
						say(string.format(gameforge[LC()][31001], 70))
						return
					else
						pc.warp(288300, 42300)
						setskin(NOWINDOW)
					end
				end

			elseif s == 11 then
				local surgun = select (gameforge[LC()][19037],gameforge[LC()][19038],gameforge[LC()][19039],gameforge[LC()][19040],gameforge[LC()][39])

				if surgun == 1 then
					if(pc.get_level() < 75) then
						say_title(gameforge[LC()][31000])
						say(string.format(gameforge[LC()][31001], 75))
						return
					else
						pc.warp(10000, 1209000)
						setskin(NOWINDOW)
					end

				elseif surgun == 2 then
					if(pc.get_level() < 75) then
						say_title(gameforge[LC()][31000])
						say(string.format(gameforge[LC()][31001], 75))
						return
					else
						pc.warp(135000, 1343700)
						setskin(NOWINDOW)
					end

				elseif surgun == 3 then
					if(pc.get_level() < 80) then
						say_title(gameforge[LC()][31000])
						say(string.format(gameforge[LC()][31001], 80))
						return
					else
						pc.warp(241700, 1273800)
						setskin(NOWINDOW)
					end

				elseif surgun == 4 then
					if(pc.get_level() < 80) then
						say_title(gameforge[LC()][31000])
						say(string.format(gameforge[LC()][31001], 80))
						return
					else
						pc.warp(201500, 1220800)
						setskin(NOWINDOW)
					end
				end

			elseif s == 12 then
				local lungsam = select (gameforge[LC()][19019],gameforge[LC()][19020],gameforge[LC()][19021] ,gameforge[LC()][39])

				if lungsam == 1 then
					if(pc.get_level() < 75) then
						say_title(gameforge[LC()][31000])
						say(string.format(gameforge[LC()][31001], 75))
						return
					else
						pc.warp(1119800, 70500)
						setskin(NOWINDOW)
					end

				elseif lungsam == 2 then
					if(pc.get_level() < 75) then
						say_title(gameforge[LC()][31000])
						say(string.format(gameforge[LC()][31001], 75))
						return
					else
						pc.warp(1075300, 46200)
						setskin(NOWINDOW)
					end

				elseif lungsam == 3 then
					if(pc.get_level() < 75) then
						say_title(gameforge[LC()][31000])
						say(string.format(gameforge[LC()][31001], 75))
						return
					else
						pc.warp(1119400, 5100)
						setskin(NOWINDOW)
					end
				end

			elseif s == 13 then
				local guatama = select (gameforge[LC()][19025],gameforge[LC()][19026],gameforge[LC()][19027] ,gameforge[LC()][39])

				if guatama == 1 then
					if(pc.get_level() < 90) then
						say_title(gameforge[LC()][31000])
						say(string.format(gameforge[LC()][31001], 90))
						return
					else
						pc.warp(1226600, 1680700)
						setskin(NOWINDOW)
					end

				elseif guatama == 2 then
					if(pc.get_level() < 90) then
						say_title(gameforge[LC()][31000])
						say(string.format(gameforge[LC()][31001], 90))
						return
					else
						pc.warp(1279900, 1734000)
						setskin(NOWINDOW)
					end

				elseif guatama == 3 then
					if(pc.get_level() < 90) then
						say_title(gameforge[LC()][31000])
						say(string.format(gameforge[LC()][31001], 90))
						return
					else
						pc.warp(1338800, 1724800)
						setskin(NOWINDOW)
					end
				end

			elseif s == 14 then
				local buyulu = select (gameforge[LC()][19028],gameforge[LC()][19029],gameforge[LC()][19030] ,gameforge[LC()][39])

				if buyulu == 1 then
					if(pc.get_level() < 105) then
						say_title(gameforge[LC()][31000])
						say(string.format(gameforge[LC()][31001], 105))
						return
					else
						pc.warp(1099100, 583500)
						setskin(NOWINDOW)
					end

				elseif buyulu == 2 then
					if(pc.get_level() < 105) then
						say_title(gameforge[LC()][31000])
						say(string.format(gameforge[LC()][31001], 105))
						return
					else
						pc.warp(1113700, 512100)
						setskin(NOWINDOW)
					end

				elseif buyulu == 3 then
					if(pc.get_level() < 105) then
						say_title(gameforge[LC()][31000])
						say(string.format(gameforge[LC()][31001], 105))
						return
					else
						pc.warp(1072300, 498100)
						setskin(NOWINDOW)
					end
				end

			elseif s == 15 then
				local antik = select (gameforge[LC()][19031],gameforge[LC()][19032],gameforge[LC()][19033] ,gameforge[LC()][39])

				if antik == 1 then
					if(pc.get_level() < 120) then
						say_title(gameforge[LC()][31000])
						say(string.format(gameforge[LC()][31001], 120))
						return
					else
						pc.warp(637600, 784900)
						setskin(NOWINDOW)
					end

				elseif antik == 2 then
					if(pc.get_level() < 120) then
						say_title(gameforge[LC()][31000])
						say(string.format(gameforge[LC()][31001], 120))
						return
					else
						pc.warp(689000, 837900)
						setskin(NOWINDOW)
					end

				elseif antik == 3 then
					if(pc.get_level() < 120) then
						say_title(gameforge[LC()][31000])
						say(string.format(gameforge[LC()][31001], 120))
						return
					else
						pc.warp(756400, 804700)
						setskin(NOWINDOW)
					end
				end

			elseif s == 16 then
				pc.warp(864600, 1008700)
				setskin(NOWINDOW)
			end
		end
	end
end
