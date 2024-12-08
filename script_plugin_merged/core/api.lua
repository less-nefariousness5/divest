-- Shared Wrapper Class
---@type buff_manager
local buff_manager = require("common/modules/buff_manager")
---@type combat_forecast
local combat_forecast = require("common/modules/combat_forecast")
---@type spell_helper
local spell_helper = require("common/utility/spell_helper")
---@type spell_queue
local spell_queue = require("common/modules/spell_queue")
---@type unit_helper
local unit_helper = require("common/utility/unit_helper")
---@type target_selector
local target_selector = require("common/modules/target_selector")
---@type plugin_helper
local plugin_helper = require("common/utility/plugin_helper")
---@type control_panel_helper
local control_panel_helper = require("common/utility/control_panel_helper")
---@type key_helper
local key_helper = require("common/utility/key_helper")

-- Comparison operators table
local compare_table = {
    [">"] = function(a, b) return a > b end,
    ["<"] = function(a, b) return a < b end,
    [">="] = function(a, b) return a >= b end,
    ["<="] = function(a, b) return a <= b end,
    ["=="] = function(a, b) return a == b end,
    ["min"] = function(a, b) return a < b end,
    ["max"] = function(a, b) return a > b end,
}

local function compare(operator, a, b)
    return compare_table[operator](a, b)
end

-- Wrapper class
FS.api = {
    -- Core modules
    buff_manager = buff_manager,
    combat_forecast = combat_forecast,
    spell_helper = spell_helper,
    spell_queue = spell_queue,
    unit_helper = unit_helper,
    target_selector = target_selector,
    plugin_helper = plugin_helper,
    control_panel_helper = control_panel_helper,
    key_helper = key_helper,
}

-- Combat timing functions
---Get remaining boss fight time
---@return number
function FS.api.boss_fight_remains()
    local remaining_time = combat_forecast:get_forecast() / 1000
    if remaining_time <= 0 then
        remaining_time = 11111
    end
    return remaining_time
end

---Get remaining fight time
---@return number
function FS.api.fight_remains()
    local remaining_time = combat_forecast:get_forecast() / 1000
    if remaining_time <= 0 then
        remaining_time = 11111
    end
    return remaining_time
end

---Get time in combat
---@return number
function FS.api.combat_time()
    return core:game_time()
end

---Convert boolean to number
---@param value any
---@return integer
function FS.api.num(value)
    if value then return 1 else return 0 end
end

-- Spell casting functions
---Cast spell on target
---@param spell Spell
---@param target Unit | nil
---@param message string
---@return boolean
function FS.api.cast(spell, target, message)
    local cast_target = target or FS.state.player
    if not cast_target.go:is_valid() then
        return false
    end
    local spell_id = spell:id()
    if spell_helper:is_spell_on_cooldown(spell_id) then
        return false
    end
    if not spell_helper:is_spell_castable(spell_id, FS.state.player.go, cast_target.go, false, false) then
        return false
    end
    if FS.settings.bitch_mode() then
        core.log("adding queue: " .. message)
        FS.api.next_cast = function()
            core.log("Running queue: " .. message)
            spell._time_since_last_cast = core:game_time()
            FS.state.player.last_spell_id = spell_id
            spell_queue:queue_spell_target(spell_id, cast_target.go, 1, message)
        end
    else
        spell._time_since_last_cast = core:game_time()
        FS.state.player.last_spell_id = spell_id
        spell_queue:queue_spell_target(spell_id, cast_target.go, 1, message)
        FS.api.next_cast = nil
    end
    return true
end

-- Spell casting functions
---Cast spell on target
---@param spell Spell
---@param target Unit | nil
---@param message string
---@return boolean
function FS.api.cast_at_cursor(spell, target, message)
    local cast_target = target or FS.state.player
    if not cast_target.go:is_valid() then
        return false
    end
    local spell_id = spell:id()
    if spell_helper:is_spell_on_cooldown(spell_id) then
        return false
    end
    if not spell_helper:is_spell_castable(spell_id, FS.state.player.go, cast_target.go, false, false) then
        return false
    end
    spell_queue:queue_spell_position(spell_id, FS.state.player:get_position(), 1, message)
    spell._time_since_last_cast = core:game_time()
    FS.state.player.last_spell_id = spell_id
    return true
end

---comment
---@param spell Spell
---@param force_target Unit?
---@return boolean
function FS.api.cast_at_enemy(spell, force_target)
    if force_target == nil and not FS.state.target_is_valid then
        return false
    end
    return FS.api.cast(spell, force_target or FS.state.target, "Casting: " .. tostring(spell:id()))
end

---Cast spell with target selection logic
---@param aoe_on boolean
---@param spell Spell
---@param targets table<Unit>
---@param target_if_mode string
---@param target_if_condition function
---@param condition function?
---@param state table
---@param message string
---@return boolean
function FS.api.cast_target_if(aoe_on, spell, targets, target_if_mode, target_if_condition, condition, state, message)
    local target_condition = (not condition or (condition and condition(state.target)))
    if not aoe_on and target_condition then
        return FS.api.cast(spell, state.target, message)
    end
    if not aoe_on then
        return false
    end

    local best_unit = nil
    local best_condition_value = nil
    for _, target in pairs(targets) do
        if (not best_condition_value or compare(target_if_mode, target_if_condition(target), best_condition_value)) and
            (target:affecting_combat() or target:is_dummy()) and
            spell:is_castable_on_target(target) then
            best_unit = target
            best_condition_value = target_if_condition(target)
        end
    end

    if best_unit == nil then
        return false
    end

    if target_condition and (best_unit.go == state.target.go or best_condition_value == target_if_condition(state.target)) then
        return FS.api.cast(spell, state.target, message)
    elseif ((condition and condition(best_unit)) or not condition) then
        return FS.api.cast(spell, best_unit, message)
    end

    return false
end

-- Healing specific functions
---Get weighted heal target
---@param targets table<Unit>
---@param tank_weight number
---@param healer_weight number
---@return Unit?
function FS.api.get_weighted_heal_target(targets, tank_weight, healer_weight)
    local best_unit = nil
    local best_score = 0
    for _, target in pairs(targets) do
        local health = target:health_percentage()
        local weight = 1
        if target:is_tank() then
            weight = tank_weight
        elseif target:is_healer() then
            weight = healer_weight
        end
        local score = (100 - health) * weight
        if score > best_score then
            best_unit = target
            best_score = score
        end
    end
    return best_unit
end

---Get emergency heal target
---@param targets table<Unit>
---@param threshold number
---@return Unit?
function FS.api.get_emergency_heal_target(targets, threshold)
    local lowest = nil
    local lowest_health = 100
    for _, target in pairs(targets) do
        local health = target:health_percentage()
        if health < threshold and health < lowest_health then
            lowest = target
            lowest_health = health
        end
    end
    return lowest
end

-- Utility functions
---Check if cooldowns should be used
---@return boolean
function FS.api.cds_on()
    return true -- TODO: Add menu option
end

---Check if AoE should be used
---@return boolean
function FS.api.aoe_on()
    return true -- TODO: Add menu option
end

---Get target count in range
---@param range number
---@return number
function FS.api.ranged_target_count(range)
    return #unit_helper:get_enemy_list_around(core.object_manager.get_local_player():get_position(), range, false)
end
