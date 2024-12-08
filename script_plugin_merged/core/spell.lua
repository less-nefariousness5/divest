---@class Spell
Spell = Class(function(a, b) return a:id() == b:id() end)

---comment
---@param id1 integer
---@param id2 integer?
---@return Spell
function Spell:New(id1, id2)
    self.ids = { id1 }
    if id2 ~= nil then
        table.insert(self.ids, id2)
    end
    ---@type integer?
    self.id = nil
    self.max_enemies = 1
    self.max_stack = 1
    if self:id() == 344179 then
        if FS.enhancement.talents.raging_maelstrom:is_learned() then
            self.max_stack = 10
        else
            self.max_stack = 5
        end
    end
    self._time_since_last_cast = 0
    ---@type fun(): boolean
    self.custom_condition = nil
    return self
end

---Get the active spell ID
---@return integer
function Spell:id()
    if self._id ~= nil then
        return self._id
    end
    for _, id in pairs(self.ids) do
        if core.spell_book.is_spell_learned(id) or #self.ids == 1 then
            self._id = id
            return self._id
        end
    end
    return self._id or 0
end

---Check if spell is learned
---@return boolean
function Spell:enabled()
    return core.spell_book.is_spell_learned(self:id())
end

---Check if spell is learned
---@return boolean
function Spell:is_learned()
    return core.spell_book.is_spell_learned(self:id())
end

---Get active aura count on target
---@param target Unit
---@return number
function Spell:aura_active_count(target)
    ---@diagnostic disable-next-line: missing-fields
    return FS.api.buff_manager:get_aura_data(target.go, { self:id() }).stacks
end

---Get current charges
---@return integer
function Spell:charges()
    return core.spell_book.get_spell_charge(self:id())
end

---Get maximum charges
---@return integer
function Spell:max_charges()
    return core.spell_book.get_spell_charge_max(self:id())
end

---Get fractional charges with recharge modifier
---@param recharge_mod integer
---@return integer
function Spell:charges_fractional(recharge_mod)
    local charges = self:charges()
    local max_charges = self:max_charges()
    if charges == max_charges then
        return charges
    end
    local cooldown = self:cooldown_remains()
    local recharge = cooldown > 0 and cooldown or 0
    return charges + ((recharge_mod - recharge) / recharge_mod)
end

---comment
---@return integer
function Spell:targets()
    local range = self:id() == 53385 and 8 or core.spell_book.get_spell_max_range(self:id())
    local targets = FS.api.unit_helper:get_enemy_list_around(FS.state.player:get_position(),
        range, false, false)
    return #targets
end

---Get remaining cooldown
---@return number
function Spell:cooldown_remains()
    return core.spell_book.get_spell_cooldown(self:id())
end

---Get remaining cooldown
---@return number
function Spell:cooldown_remaining()
    return core.spell_book.get_spell_cooldown(self:id())
end

---Check if cooldown is up
---@return boolean
function Spell:cooldown_up()
    return not FS.api.spell_helper:is_spell_on_cooldown(self:id())
end

---Check if cooldown is down
---@return boolean
function Spell:cooldown_down()
    return FS.api.spell_helper:is_spell_on_cooldown(self:id())
end

---Get spell damage
---@param enemy_count integer?
---@return number
function Spell:damage(enemy_count)
    local damage = FS.api.spell_helper:get_spell_damage(self:id())
    if enemy_count ~= nil and enemy_count ~= 0 then
        damage = damage * math.min(enemy_count, self.max_enemies)
    end
    return damage
end

---Check if spell is ready to cast
---@return boolean
function Spell:is_ready()
    local has_custom_condition = false
    if self.custom_condition ~= nil then
        has_custom_condition = self.custom_condition()
    end
    return has_custom_condition or (self.custom_condition == nil and self:is_equipped() and self:is_learned()) and
        FS.api.spell_helper:is_spell_castable(self:id(), FS.state.player.go,
            FS.api.target and FS.api.target.go or FS.state.player.go,
            false, false)
end

---Check if spell is equipped
---@return boolean
function Spell:is_equipped()
    return FS.api.spell_helper:has_spell_equipped(self:id())
end

---Check if spell is castable (alias for is_ready)
---@return boolean
function Spell:is_castable()
    ---@diagnostic disable-next-line: undefined-field
    if self._usable ~= nil then
        ---@diagnostic disable-next-line: undefined-field
        return self:_usable() -- and self:is_ready()
    end
    return self:is_ready()
end

---Check if spell is castable on specific target
---@param target Unit
---@return boolean
function Spell:is_castable_on_target(target)
    return FS.api.spell_helper:is_spell_castable(self:id(), FS.state.player.go, target.go,
        false, false)
end

---Check if spell is available (learned or custom condition)
---@return boolean
function Spell:is_available()
    local has_custom_condition = false
    if self.custom_condition ~= nil then
        has_custom_condition = self.custom_condition()
    end
    return has_custom_condition or (self.custom_condition == nil and core.spell_book.is_spell_learned(self:id()))
end

---Get time since last cast
---@return integer
function Spell:time_since_last_cast()
    return core:game_time() - self._time_since_last_cast
end

---Get base duration
---@return number
function Spell:base_duration()
    local Duration = FS.api.spell_duration[self:id()]
    if not Duration or Duration == 0 then return 0 end
    return Duration[1] / 1000
end

---Get maximum duration
---@return number
function Spell:max_duration()
    local Duration = FS.api.spell_duration[self:id()]
    if not Duration or Duration == 0 then return 0 end
    return Duration[2] / 1000
end

---Get pandemic threshold
---@return number
function Spell:pandemic_threshold()
    local base_duration = self:base_duration()
    if not base_duration or base_duration == 0 then return 0 end
    return base_duration * 0.3
end

---Check if spell is a Holy Power generator (Retribution)
---@return boolean
function Spell:is_holy_power_generator()
    local generators = {
        [35395] = true,  -- Crusader Strike
        [184575] = true, -- Blade of Justice
        [24275] = true,  -- Hammer of Wrath
        [20271] = true,  -- Judgment
        [255937] = true  -- Wake of Ashes
    }
    return generators[self:id()] or false
end

---Check if spell is a Holy Power spender (Retribution)
---@return boolean
function Spell:is_holy_power_spender()
    local spenders = {
        [85256] = true,  -- Templar's Verdict
        [383328] = true, -- Final Verdict
        [53385] = true,  -- Divine Storm
        [215661] = true  -- Justicar's Vengeance
    }
    return spenders[self:id()] or false
end

---Check if spell is a Maelstrom Weapon consumer (Enhancement)
---@return boolean
function Spell:is_maelstrom_weapon_consumer()
    local consumers = {
        [188196] = true, -- Lightning Bolt
        [187874] = true, -- Chain Lightning
        [51505] = true,  -- Lava Burst
        [117014] = true  -- Elemental Blast
    }
    return consumers[self:id()] or false
end

return Spell
