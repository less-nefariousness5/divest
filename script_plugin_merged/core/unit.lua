require("core/class")

---@class Unit
---@field last_spell_id integer
Unit = Class(function(a, b)
    if a == nil and b == nil then return true end
    if a == nil and b ~= nil then return true end
    if a ~= nil and b == nil then return true end
    return a ~= nil and a.go == b.go
end)

---Create a Unit instance
---@param go game_object
---@return Unit
function Unit:New(go)
    self.go = go
    self.heal_absorb = 0.0
    self.cache = {}
    return self
end

function Unit:is_valid()
    if self.cache.is_valid == nil then
        self.cache.is_valid = self.go:is_valid()
    end
    return self.cache.is_valid
end

---comment
---@param target Unit
---@return boolean
function Unit:can_attack(target)
    if self.cache.can_attack == nil then
        self.cache.can_attack = self.go:can_attack(target.go)
    end
    return self.cache.can_attack
end

---Check if unit is in combat
---@return boolean
function Unit:is_in_combat()
    if self.cache.is_in_combat == nil then
        self.cache.is_in_combat = self.go:is_in_combat()
    end
    return self.cache.is_in_combat
end

---Get predicted time to die
---@return any
function Unit:time_to_die()
    if self.cache.time_to_die == nil then
        self.cache.time_to_die = FS.api.combat_forecast:get_forecast_single(self.go, true)
    end
    return self.cache.time_to_die
end

---Check if unit is a training dummy
---@return boolean
function Unit:is_dummy()
    if self.cache.is_dummy == nil then
        self.cache.is_dummy = FS.api.unit_helper:is_dummy(self.go)
    end
    return self.cache.is_dummy
end

---Get buff stack count
---@param spell Spell
---@return number
function Unit:buff_stack(spell)
    if self.cache.buff_stack == nil then
        self.cache.buff_stack = {}
    end
    if self.cache.buff_stack[spell:id()] == nil then
        ---@diagnostic disable-next-line: missing-fields
        self.cache.buff_stack[spell:id()] = FS.api.buff_manager:get_buff_data(self.go, { spell:id() }).stacks
    end
    return self.cache.buff_stack[spell:id()]
end

---Check if buff is active
---@param spell Spell
---@return boolean
function Unit:buff_up(spell)
    if self.cache.buff_up == nil then
        self.cache.buff_up = {}
    end
    if self.cache.buff_up[spell:id()] == nil then
        ---@diagnostic disable-next-line: missing-fields
        self.cache.buff_up[spell:id()] = FS.api.buff_manager:get_buff_data(self.go, { spell:id() }).is_active or
            ---@diagnostic disable-next-line: missing-fields
            FS.api.buff_manager:get_aura_data(self.go, { spell:id() }).is_active
    end
    return self.cache.buff_up[spell:id()]
end

---Check if buff is not active
---@param spell Spell
---@return boolean
function Unit:buff_down(spell)
    return not self:buff_up(spell)
end

---Get remaining buff duration
---@param spell Spell
---@return number
---@diagnostic disable-next-line: missing-fields
function Unit:buff_remains(spell)
    if self.cache.buff_remains == nil then
        self.cache.buff_remains = {}
    end
    if self.cache.buff_remains[spell:id()] == nil then
        ---@diagnostic disable-next-line: missing-fields
        self.cache.buff_remains[spell:id()] = FS.api.buff_manager:get_buff_data(self.go, { spell:id() }).remaining / 1000
    end
    return self.cache.buff_remains[spell:id()]
end

---Get debuff stack count
---@param spell Spell
---@return number
function Unit:debuff_stack(spell)
    if self.cache.debuff_stack == nil then
        self.cache.debuff_stack = {}
    end
    if self.cache.debuff_stack[spell:id()] == nil then
        ---@diagnostic disable-next-line: missing-fields
        self.cache.debuff_stack[spell:id()] = FS.api.buff_manager:get_debuff_data(self.go, { spell:id() }).stacks
    end
    return self.cache.debuff_stack[spell:id()]
end

---Check if debuff is active
---@param spell Spell
---@return boolean
function Unit:debuff_up(spell)
    if self.cache.debuff_up == nil then
        self.cache.debuff_up = {}
    end
    if self.cache.debuff_up[spell:id()] == nil then
        ---@diagnostic disable-next-line: missing-fields
        self.cache.debuff_up[spell:id()] = FS.api.buff_manager:get_debuff_data(self.go, { spell:id() }).is_active
    end
    return self.cache.debuff_up[spell:id()]
end

---Check if debuff is not active
---@param spell Spell
---@return boolean
function Unit:debuff_down(spell)
    return not self:debuff_up(spell)
end

---Get remaining debuff duration
---@param spell Spell
---@return number
function Unit:debuff_remains(spell)
    if self.cache.debuff_remains == nil then
        self.cache.debuff_remains = {}
    end
    if self.cache.debuff_remains[spell:id()] == nil then
        ---@diagnostic disable-next-line: missing-fields
        self.cache.debuff_remains[spell:id()] = FS.api.buff_manager:get_debuff_data(self.go, { spell:id() }).remaining *
            1000
    end
    return self.cache.debuff_remains[spell:id()]
end

---Check if debuff can be refreshed
---@param spell Spell
---@return boolean
function Unit:debuff_refreshable(spell)
    if self.cache.debuff_refreshable == nil then
        self.cache.debuff_refreshable = {}
    end
    if self.cache.debuff_refreshable[spell:id()] == nil then
        local pandemic_threshold = spell:pandemic_threshold()
        self.cache.debuff_refreshable[spell:id()] = self:debuff_remains(spell) <= pandemic_threshold
    end
    return self.cache.debuff_refreshable[spell:id()]
end

---Get unit health percentage
---@return number
function Unit:health_percentage()
    if self.cache.health_percentage == nil then
        self.cache.health_percentage = self.go:get_health() / self.go:get_max_health()
    end
    return self.cache.health_percentage
end

---Get unit's current health
---@return number
function Unit:health()
    if self.cache.health == nil then
        self.cache.health = self.go:get_health()
    end
    return self.cache.health
end

---Get unit's maximum health
---@return number
function Unit:max_health()
    if self.cache.max_health == nil then
        self.cache.max_health = self.go:get_max_health()
    end
    return self.cache.max_health
end

---Check if unit is dead
---@return boolean
function Unit:is_dead()
    if self.cache.is_dead == nil then
        self.cache.is_dead = self.go:is_dead()
    end
    return self.cache.is_dead
end

---Check if unit is an enemy
---@param other Unit
---@return boolean
function Unit:is_enemy_with(other)
    return self.go:is_enemy_with(other.go)
end

---Get enemies in range
---@param range number
---@return table<Unit>
function Unit:get_enemies_in_range(range)
    if self.cache.enemies_in_range == nil then
        self.cache.enemies_in_range = {}
    end
    if self.cache.enemies_in_range[range] == nil then
        local enemies = FS.api.unit_helper:get_enemy_list_around(self.go:get_position(), range, false)
        local units = {}
        for _, enemy in pairs(enemies) do
            table.insert(units, Unit(enemy))
        end
        self.cache.enemies_in_range[range] = units
    end
    return self.cache.enemies_in_range[range]
end

---Get allies in range
---@param range number
---@param include_pets boolean
---@param include_self boolean
---@return table<Unit>
function Unit:get_allies_in_range(range, include_pets, include_self)
    if self.cache.allies_in_range == nil then
        self.cache.allies_in_range = {}
    end
    if self.cache.allies_in_range[range] == nil then
        local allies = FS.api.unit_helper:get_ally_list_around(self.go:get_position(), range, include_pets, include_self)
        local units = {}
        for _, ally in pairs(allies) do
            table.insert(units, Unit(ally))
        end
        self.cache.allies_in_range[range] = units
    end
    return self.cache.allies_in_range[range]
end

---Check if unit is a tank
---@return boolean
function Unit:is_tank()
    if self.cache.is_tank == nil then
        self.cache.is_tank = FS.api.unit_helper:is_tank(self.go)
    end
    return self.cache.is_tank
end

---Get threat situation against target
---@param target Unit
---@return table
function Unit:get_threat_situation(target)
    return self.go:get_threat_situation(target.go)
end

---Get unit's current position
---@return vec3
function Unit:get_position()
    if self.cache.position == nil then
        self.cache.position = self.go:get_position()
    end
    return self.cache.position
end

---comment
---@param spell Spell
---@return boolean
function Unit:aura_up(spell)
    if self.cache.aura_up == nil then
        self.cache.aura_up = {}
    end
    if self.cache.aura_up[spell:id()] == nil then
        ---@diagnostic disable-next-line: missing-fields
        self.cache.aura_up[spell:id()] = FS.api.buff_manager:get_aura_data(self.go, { spell:id() }).is_active
    end
    return self.cache.aura_up[spell:id()]
end

---comment
---@return number
function Unit:holy_power()
    if self.cache.holy_power == nil then
        self.cache.holy_power = self.go:get_power(9)
    end
    return self.cache.holy_power
end

function Unit:gcd()
    if self.cache.gcd == nil then
        self.cache.gcd = core.spell_book.get_global_cooldown() + 0.01
    end
    return self.cache.gcd
end
