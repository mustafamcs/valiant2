quest basic_weapon begin
	state start begin
		when login with pc.getqf("basic_weapon") == 0 begin
			pc.setqf("basic_weapon",1)
			pc.give_item2(70038, 1)
			pc.give_item2(200087, 1)

			if pc.get_sex() == 0 then
				pc.give_item2(36000, 1)
				pc.give_item2(36001, 1)
			else 
				pc.give_item2(36002, 1)
				pc.give_item2(36003, 1)
			end

			local playerRace = pc.get_race()

			if playerRace == 0 or playerRace == 4 then
				pc.give_item2(36004, 1)
				pc.give_item2(36007, 1)
			elseif playerRace == 1 or playerRace == 5 then
				pc.give_item2(36004, 1)
				pc.give_item2(36005, 1)
				pc.give_item2(36006, 1)
			elseif playerRace == 2 or playerRace == 6 then
				pc.give_item2(36004, 1)
			else
				pc.give_item2(36008, 1)
				pc.give_item2(36009, 1)
			end

		end
	end
end