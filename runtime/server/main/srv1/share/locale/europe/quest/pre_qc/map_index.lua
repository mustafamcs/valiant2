quest mapindex begin
	state start begin
		when login with pc.is_gm() begin
			chat("Current Map's Index: "..pc.get_map_index().."")
		end
	end
end