-- Shared APL (Action Priority List) Class
local Wrapper = require("core/wrapper")

---@class APL
local APL = {
    ---Convert boolean to number
    ---@param value boolean
    ---@return integer
    num = function(value)
        if value then return 1 else return 0 end
    end,

    ---Cast spell on target
    ---@param spell Spell
    ---@param target Unit | Player | nil
    ---@param state table
    ---@param message string
    ---@return boolean
    cast = function(spell, target, state, message)
        return Wrapper.cast(spell, target, state, message)
    end,

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
    cast_target_if = function(aoe_on, spell, targets, target_if_mode, target_if_condition, condition, state, message)
        return Wrapper.cast_target_if(aoe_on, spell, targets, target_if_mode, target_if_condition, condition, state,
            message)
    end,

    ---Get boss fight remains
    ---@return number
    boss_fight_remains = function()
        return Wrapper.boss_fight_remains()
    end,

    ---Get fight remains
    ---@return number
    fight_remains = function()
        return Wrapper.fight_remains()
    end,

    ---Get combat time
    ---@return number
    combat_time = function()
        return Wrapper.combat_time()
    end,

    ---Check if cooldowns should be used
    ---@return boolean
    cds_on = function()
        return Wrapper.cds_on()
    end,

    ---Check if AoE should be used
    ---@return boolean
    aoe_on = function()
        return Wrapper.aoe_on()
    end,

    ---Get target count in range
    ---@param range number
    ---@return number
    ranged_target_count = function(range)
        return Wrapper.ranged_target_count(range)
    end,

    ---Get weighted heal target
    ---@param targets table<Unit>
    ---@param tank_weight number
    ---@param healer_weight number
    ---@return Unit?
    get_weighted_heal_target = function(targets, tank_weight, healer_weight)
        return Wrapper.get_weighted_heal_target(targets, tank_weight, healer_weight)
    end,

    ---Get emergency heal target
    ---@param targets table<Unit>
    ---@param threshold number
    ---@return Unit?
    get_emergency_heal_target = function(targets, threshold)
        return Wrapper.get_emergency_heal_target(targets, threshold)
    end,

    ---Get lowest health ally in range
    ---@param range number
    ---@param include_pets boolean
    ---@return Unit?
    get_lowest_health_ally_in_range = function(range, include_pets)
        return FS.state.player:get_lowest_health_ally_in_range(range, include_pets)
    end,

    ---Get all tanks in range
    ---@param range number
    ---@return table<Unit>
    get_tanks_in_range = function(range)
        return FS.state.player:get_tanks_in_range(range)
    end,

    ---Get all healers in range
    ---@param range number
    ---@return table<Unit>
    get_healers_in_range = function(range)
        return FS.state.player:get_healers_in_range(range)
    end,

    ---Get all enemies in melee range
    ---@return table<Unit>
    get_enemies_in_melee_range = function()
        return FS.state.player:get_enemies_in_melee_range()
    end,

    ---Get count of enemies in melee range
    ---@return number
    get_enemies_in_melee_range_count = function()
        return FS.state.player:get_enemies_in_melee_range_count()
    end,

    ---Get all enemies in range that can be attacked
    ---@param range number
    ---@return table<Unit>
    get_attackable_enemies_in_range = function(range)
        return FS.state.player:get_attackable_enemies_in_range(range)
    end
}

return APL
