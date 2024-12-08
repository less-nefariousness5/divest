FS.heal_absorb_manager = {
    absorb_debuffs = {
        [443305] = true, -- Crimson Rain
        [442437] = true, -- Ingest Black Blood
        [443274] = true, -- Unstable Infusion
        [442799] = true, -- Sanguine Overflow
        [442660] = true, -- Experimental Dosage
        [455404] = true, -- Feast
        [426736] = true, -- Shadow Shroud
        [450095] = true, -- Curse of Entropy
        [451224] = true, -- Enveloping Shadowflame
        [442285] = true, -- Corrupted Coating
    }
}

---comment
---@param unit Unit
function FS.heal_absorb_manager.get_absorbs(unit)
    local debuffs = unit.go:get_debuffs()
    local heal_absorb = 0
    for k, v in pairs(debuffs) do
        ---@type buff
        local debuff = debuffs[k]
        if debuff ~= nil and debuff.type ~= -1 and FS.heal_absorb_manager.absorb_debuffs[debuff.buff_id] then
            local tooltip_data = core.spell_book.get_buff_description(debuff)
            local tooltip_numbers = {}
            if tooltip_data ~= nil then
                for t in tooltip_data:gmatch("(-?%d[%d%.,]*)") do
                    t = t:gsub("%.", "");
                    t = t:gsub(",", "");
                    table.insert(tooltip_numbers, tonumber(t))
                end
                local highest_number = 0
                for i = 1, #tooltip_numbers do
                    local number = tooltip_numbers[i]
                    if number > highest_number then
                        highest_number = number
                    end
                end
                heal_absorb = heal_absorb + highest_number
            end
        end
    end
    return heal_absorb
end
