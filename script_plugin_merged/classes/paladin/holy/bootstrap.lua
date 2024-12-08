require("core/unit")
local menu = require("classes/paladin/holy/menu")

FS.holy = {
    menu = menu,
    variables = {
        holy_power = 0,
        max_holy_power = 5,
        ---@type Unit[]
        heal_targets = {},
        lowest_health = nil,
        ---@type Unit?
        lowest_tank = nil,
        ---@type Unit?
        weighted_lowest = nil,
        ---@type Unit?
        weighted_lowest_tank = nil,
        ---@type Unit[]
        tanks = {},
        ---@type Unit?
        tank_with_aggro = nil,
        ---@type Unit?
        highest_threat_tank = nil,
        ---@type Unit[]
        enemy_targets = {},
        can_cast_judgment = false,
        can_cast_hammer_of_wrath = false,
        -- Buff tracking
        avenging_crusader_up = false,
        awakening_max_up = false,
        beacon_of_virtue_up = false,
        divine_purpose_up = false,
        rising_sunlight_up = false,
        shining_righteousness_up = false,
        holy_shock_charges = 0,
        hp_cost = 3
    },
    settings = {
        ---@type fun(): boolean
        kamala_mode = function() return FS.api.plugin_helper:is_toggle_enabled(FS.holy.menu.elements.kamala_mode_toggle) end,
        ---@type fun(): number
        loh_hp = function() return FS.holy.menu.elements.loh_hp:get() / 100 end,
        ---@type fun(): boolean
        enable_ac = function() return FS.api.plugin_helper:is_toggle_enabled(FS.holy.menu.elements.enable_ac) end,
        ---@type fun(): integer
        bov_count = function() return FS.holy.menu.elements.bov_count:get() end,
        ---@type fun(): number
        bov_hp = function() return FS.holy.menu.elements.bov_hp:get() / 100 end,
        ---@type fun(): integer
        ac_count = function() return FS.holy.menu.elements.ac_count:get() end,
        ---@type fun(): number
        ac_hp = function() return FS.holy.menu.elements.ac_hp:get() / 100 end,
        ---@type fun(): integer
        dt_count = function() return FS.holy.menu.elements.dt_count:get() end,
        ---@type fun(): number
        dt_hp = function() return FS.holy.menu.elements.dt_hp:get() / 100 end,
        ---@type fun(): number
        holy_shock_hp = function() return FS.holy.menu.elements.holy_shock_hp:get() / 100 end,
        ---@type fun(): number
        holy_shock_hp2 = function() return FS.holy.menu.elements.holy_shock_hp2:get() / 100 end,
        ---@type fun(): number
        holy_shock_hp_rs = function() return FS.holy.menu.elements.holy_shock_hp_rs:get() / 100 end,
        ---@type fun(): number
        wog_hp = function() return FS.holy.menu.elements.wog_hp:get() / 100 end,
        ---@type fun(): number
        wog_tank_hp = function() return FS.holy.menu.elements.wog_tank_hp:get() / 100 end
    }
}

require("classes/paladin/holy/ids")

function FS.holy.update_variables()
    -- Update holy power
    FS.holy.variables.holy_power = FS.state.player:holy_power()

    -- Update buff tracking
    FS.holy.variables.empyrean_legacy_up = FS.state.player:buff_up(FS.holy.auras.empyrean_legacy)
    FS.holy.variables.awakening_max_remaining = FS.state.player:buff_remains(FS.holy.auras.awakening_max)
    FS.holy.variables.awakening_max_up = FS.state.player:buff_up(FS.holy.auras.awakening_max)
    FS.holy.variables.avenging_crusader_remaining = FS.state.player:buff_remains(FS.holy.auras.avenging_crusader)
    FS.holy.variables.avenging_crusader_up = FS.state.player:buff_up(FS.holy.auras.avenging_crusader)
    FS.holy.variables.beacon_of_virtue_up = FS.state.player:buff_up(FS.holy.auras.beacon_of_virtue)
    FS.holy.variables.divine_purpose_remaining = FS.state.player:buff_remains(FS.holy.auras.divine_purpose)
    FS.holy.variables.divine_purpose_up = FS.state.player:buff_up(FS.holy.auras.divine_purpose)
    FS.holy.variables.rising_sunlight_up = FS.state.player:buff_up(FS.holy.auras.rising_sunlight)
    FS.holy.variables.shining_righteousness_up = FS.state.player:buff_up(FS.holy.auras.shining_righteousness)
    FS.holy.variables.holy_shock_charges = FS.holy.spells.holy_shock:charges()
    FS.holy.variables.can_use_spenders = FS.holy.variables.divine_purpose_up
        or FS.holy.variables.holy_power >= FS.holy.variables.hp_cost
        or FS.holy.variables.shining_righteousness_up
    FS.holy.variables.can_cast_hammer_of_wrath = FS.state.target_is_valid and FS.state.target:health_percentage() < 0.2
    FS.holy.variables.should_cast_word_of_glory = FS.holy.variables.empyrean_legacy_up and
        (FS.holy.variables.holy_power >= 3 or FS.holy.variables.divine_purpose_up)
    --or FS.state.player:buff_up(FS.holy.auras.veneration)
    --or FS.holy.talents.avenging_wrath:is_learned()
    --and (FS.state.player:buff_up(FS.holy.auras.avenging_wrath) or FS.state.player:buff_up(FS.holy.auras.avenging_crusader))
end

function FS.holy.update_targets()
    local targets = FS.api.unit_helper:get_enemy_list_around(FS.state.player:get_position(), 40,
        false, false, false, false)
    FS.holy.variables.enemy_targets = {}
    for _, v in pairs(targets) do
        table.insert(FS.holy.variables.enemy_targets, Unit(v))
    end
    FS.holy.variables.highest_threat_target = nil
    for k, v in pairs(FS.holy.variables.enemy_targets) do
        ---@type Unit
        local target = FS.holy.variables.enemy_targets[k]
        if target.go:is_boss() then
            FS.holy.variables.highest_threat_target = target
            break
        end
    end
    if FS.holy.variables.highest_threat_target == nil then
        local highest_enemy_life = 0
        for k, v in pairs(FS.holy.variables.enemy_targets) do
            ---@type Unit
            local target = FS.holy.variables.enemy_targets[k]
            if target.go:get_health() > highest_enemy_life then
                FS.holy.variables.highest_threat_target = target
            end
        end
    end

    -- Update heal targets
    local ally_targets = FS.api.unit_helper:get_ally_list_around(FS.state.player:get_position(), 40,
            true, true, false) or
        {}
    FS.holy.variables.heal_targets = {}
    for _, v in pairs(ally_targets) do
        table.insert(FS.holy.variables.heal_targets, Unit(v))
    end
    table.insert(FS.holy.variables.heal_targets, FS.state.player)

    -- Update tank information
    FS.holy.variables.tanks = {}
    for k, v in pairs(FS.holy.variables.heal_targets) do
        ---@type Unit
        local target = FS.holy.variables.heal_targets[k]
        if FS.api.unit_helper:is_tank(target.go) then
            table.insert(FS.holy.variables.tanks, target)
            if FS.holy.variables.highest_threat_target ~= nil then
                if target:get_threat_situation(FS.holy.variables.highest_threat_target).is_tanking then
                    FS.holy.variables.tank_with_aggro = target
                end
            else
                FS.holy.variables.tank_with_aggro = target
            end
        end
    end
    for k, _ in pairs(FS.holy.variables.heal_targets) do
        local unit = FS.holy.variables.heal_targets[k]
        unit.heal_absorb = FS.heal_absorb_manager.get_absorbs(unit)
    end

    if FS.holy.settings.kamala_mode() then
        local ts_targets = FS.api.target_selector:get_targets(1)
        if #ts_targets == 0 then
            FS.holy.variables.force_target = nil
        else
            FS.holy.variables.force_target = Unit(ts_targets[1])
        end
    end
end

---comment
---@param spell Spell
---@param heal_targets Unit[]
---@param threshold integer
---@param min_targets integer
---@param clamp boolean
---@param force_target Unit?
---@param ignore_heal_absorb boolean
---@return boolean
function FS.holy.cast_with_condition(spell, heal_targets, threshold, min_targets, clamp, force_target, ignore_heal_absorb)
    if spell:cooldown_down() then
        return false
    end

    local lowest_target = nil
    local lowest_health = 999
    local low_targets = 0

    for k, v in pairs(heal_targets) do
        ---@type Unit
        local target = heal_targets[k]
        local max_health = target:max_health()
        local health = target:health()
        local heal_absorb = target.heal_absorb
        local hp_percentage = target:health_percentage()
        if not ignore_heal_absorb then
            hp_percentage = (health - math.min(heal_absorb, max_health * 0.8)) / max_health
            hp_percentage = math.max(0.05, hp_percentage)
        end
        if hp_percentage <= threshold and (FS.api.spell_helper:is_spell_castable(spell:id(), FS.state.player.go, target.go, false, false) or force_target ~= nil) then
            low_targets = low_targets + 1
            if hp_percentage < lowest_health then
                lowest_target = target
                lowest_health = hp_percentage
            end
        end
    end

    if lowest_target ~= nil and (low_targets >= min_targets or (clamp and #heal_targets == low_targets)) then
        if force_target and FS.api.spell_helper:is_spell_castable(spell:id(), FS.state.player.go, force_target.go, false, false) then
            return FS.api.cast(spell, force_target, "Casting: " .. tostring(spell:id()))
        elseif force_target == nil then
            return FS.api.cast(spell, lowest_target, "Casting: " .. tostring(spell:id()))
        end
    end
    return false
end

function FS.holy.holy_arnaments_logic()
    if FS.holy.spells.holy_bulwark:cooldown_down() then
        return false
    end
    if FS.holy.spells.sacred_weapon:is_learned() then
        FS.api.cast(FS.holy.spells.holy_bulwark, FS.state.player, "Doing SW")
        return true
    end
    if FS.holy.variables.tank_with_aggro ~= nil then
        FS.api.cast(FS.holy.spells.holy_bulwark, FS.holy.variables.tank_with_aggro, "")
        return true
    elseif FS.holy.cast_with_condition(FS.holy.spells.holy_bulwark, FS.holy.variables.heal_targets, 80, 1, true, nil, false) then
        return true
    else
        FS.api.cast(FS.holy.spells.holy_bulwark, FS.state.player, "")
        return true
    end
end

function FS.holy.run()
    if not FS.api.plugin_helper:is_toggle_enabled(FS.holy.menu.elements.enable_toggle) then return end

    -- Update our variables
    FS.holy.update_variables()
    FS.holy.update_targets()

    -- Beacon of Virtue
    if FS.holy.cast_with_condition(FS.holy.spells.beacon_of_virtue, FS.holy.variables.heal_targets, FS.holy.settings.bov_hp(), FS.holy.settings.bov_count(), true, nil, false) then
        return true
    end

    -- Judgment during Awakening
    if FS.holy.variables.awakening_max_up and FS.state.target_is_valid then
        if FS.holy.cast_with_condition(FS.holy.spells.judgment, FS.holy.variables.heal_targets, FS.holy.settings.ac_hp(), FS.holy.settings.ac_count(), true, FS.state.target, false) then
            return true
        end
    end

    -- Avenging Crusader
    if
        FS.state.target_is_valid
        and FS.api.spell_helper:is_spell_in_range(
            FS.holy.spells.crusader_strike:id(),
            FS.state.target.go,
            FS.state.player:get_position(),
            FS.state.target:get_position()
        )
        and FS.holy.settings.enable_ac()
        and FS.holy.cast_with_condition(
            FS.holy.spells.avenging_crusader,
            FS.holy.variables.heal_targets,
            FS.holy.settings.ac_hp(),
            FS.holy.settings.ac_count(),
            true,
            nil,
            false
        ) then
        return true
    end

    -- Avenging Crusader rotation
    if FS.holy.variables.avenging_crusader_up then
        if FS.api.cast_at_enemy(FS.holy.spells.judgment, FS.holy.variables.force_target) then return true end
        if FS.api.cast_at_enemy(FS.holy.spells.crusader_strike, FS.holy.variables.force_target) then return true end
        if FS.holy.variables.holy_power >= 5 and FS.holy.cast_with_condition(FS.holy.spells.word_of_glory, FS.holy.variables.heal_targets, FS.holy.settings.wog_hp(), 1, true, nil, false) then return true end
        if FS.holy.holy_shock_logic() then return true end
        if FS.holy.variables.can_cast_hammer_of_wrath and FS.api.cast_at_enemy(FS.holy.spells.hammer_of_wrath, FS.holy.variables.force_target) then return true end
        --if FS.holy.holy_shock_logic(true) then return true end
    end

    if FS.holy.variables.should_cast_word_of_glory and FS.holy.spells.word_of_glory:cooldown_up() then
        if FS.holy.cast_with_condition(FS.holy.spells.word_of_glory, FS.holy.variables.heal_targets, 95, 1, true, nil, false) then
            return true
        end
        if FS.api.cast(FS.holy.spells.word_of_glory, FS.state.player, "") then
            return true
        end
    end

    if
        not FS.api.spell_helper:is_spell_on_cooldown(FS.holy.spells.word_of_glory:id())
        and (FS.holy.variables.holy_power >= 5 or (FS.holy.variables.divine_purpose_up)) then
        if FS.holy.cast_with_condition(FS.holy.spells.word_of_glory, FS.holy.variables.heal_targets, 95, 1, true, nil, false) then
            return true
        end
        if FS.holy.variables.empyrean_legacy_up and FS.api.cast(FS.holy.spells.word_of_glory, FS.state.player, "") then
            return true
        end
        if FS.api.cast_at_enemy(FS.holy.spells.shield_of_the_righteous, FS.holy.variables.force_target) then
            return true
        end
        if FS.api.cast(FS.holy.spells.word_of_glory, FS.state.player, "") then
            return true
        end
    end

    if FS.holy.holy_arnaments_logic() then return true end

    if FS.holy.variables.awakening_max_up and FS.holy.variables.target_is_valid then
        if FS.holy.cast_with_condition(FS.holy.spells.judgment, FS.holy.variables.heal_targets, FS.holy.settings.ac_hp(), FS.holy.settings.ac_count(), true, FS.holy.variables.target, false) then
            return true
        end
    end

    -- Divine Toll
    if FS.holy.cast_with_condition(FS.holy.spells.divine_toll, FS.holy.variables.heal_targets, FS.holy.settings.dt_hp(), FS.holy.settings.dt_count(), true, nil, false) then
        return true
    end

    -- Holy Prism
    if FS.holy.holy_prism_logic() then return true end

    -- Word of Glory on tanks
    if FS.holy.tank_word_of_glory_logic() then return true end

    -- Seasons
    if FS.holy.seasons_logic() then return true end

    -- Word of Glory
    if FS.holy.word_of_glory_logic() then return true end

    -- Holy Shock
    if FS.holy.holy_shock_logic() then return true end

    if
        not FS.api.spell_helper:is_spell_on_cooldown(
            FS.holy.spells.word_of_glory:id()
        )
        and (
            FS.holy.variables.holy_power >= 5
            or (
                FS.holy.variables.divine_purpose_up
            )
        ) then
        if FS.holy.cast_with_condition(FS.holy.spells.word_of_glory, FS.holy.variables.heal_targets, 95, 1, true, nil, false) then
            return
        end
        if FS.holy.variables.empyrean_legacy_up and FS.api.cast(FS.holy.spells.word_of_glory, FS.state.player, "") then
            return true
        end
        if FS.api.cast_at_enemy(FS.holy.spells.shield_of_the_righteous, FS.holy.variables.force_target) then
            return
        end
        if FS.api.cast(FS.holy.spells.word_of_glory, FS.state.player, "") then
            return true
        end
    end

    if
        FS.holy.variables.divine_purpose_up
        and FS.holy.variables.divine_purpose_remaining < 2
        and FS.holy.cast_with_condition(FS.holy.spells.word_of_glory, FS.holy.variables.heal_targets, 100, 1, true, nil, false)
    then
        return
    end

    if (
            not FS.holy.variables.awakening_max_up
            or (
                FS.holy.variables.awakening_max_up
                and FS.holy.variables.awakening_max_remaining < 4
            )
        ) and FS.api.cast_at_enemy(FS.holy.spells.judgment, FS.holy.variables.force_target) then
        return
    end

    if FS.holy.variables.awakening_max_up then
        core.log(tostring(FS.holy.variables.awakening_max_remaining))
    end

    -- Crusader Strike
    if FS.api.cast_at_enemy(FS.holy.spells.crusader_strike, FS.holy.variables.force_target) then return true end

    if
        FS.state.target ~= nil
        and FS.api.spell_helper:is_spell_in_range(
            FS.holy.spells.crusader_strike:id(),
            FS.state.target.go,
            FS.state.player:get_position(),
            FS.state.target:get_position()
        )
        and FS.api.cast_at_enemy(FS.holy.spells.consecration, FS.holy.variables.force_target)
    then
        return true
    end

    -- Hammer of Wrath
    if FS.holy.variables.can_cast_hammer_of_wrath and FS.api.cast_at_enemy(FS.holy.spells.hammer_of_wrath, FS.holy.variables.force_target) then return true end

    --if FS.holy.spells.holy_shock:cooldown_up() and FS.holy.variables.holy_power < 3 then
    --    if FS.holy.cast_with_condition(FS.holy.spells.holy_shock, FS.holy.variables.heal_targets, 95, 1, true, nil, false) then
    --        return
    --    end
    --    if FS.state.target_is_valid and FS.api.cast(FS.holy.spells.holy_shock, FS.state.target, "") then
    --        return
    --    end
    --    if FS.api.cast(FS.holy.spells.holy_shock, FS.state.player, "") then
    --        return true
    --    end
    --end

    return false
end

function FS.holy.holy_shock_logic(ignore_overcap)
    if FS.api.spell_helper:is_spell_on_cooldown(FS.holy.spells.holy_shock:id()) then
        return false
    end

    local rising_sunlight_up = FS.holy.variables.rising_sunlight_up
    local hs_threshold = FS.holy.settings.holy_shock_hp()
    local hs_2_threshold = FS.holy.settings.holy_shock_hp2()
    local hs_rs_threshold = FS.holy.settings.holy_shock_hp_rs()
    local max_holy_power = rising_sunlight_up and 4 or 5
    local overcap_safe = ignore_overcap or FS.holy.variables.holy_power < max_holy_power

    if
        overcap_safe
        and not rising_sunlight_up
        and FS.holy.cast_with_condition(FS.holy.spells.holy_shock, FS.holy.variables.heal_targets, hs_threshold, 1, true, nil, false) then
        return true
    end

    if
        overcap_safe
        and FS.holy.variables.holy_shock_charges == 2
        and not rising_sunlight_up
        and FS.holy.cast_with_condition(FS.holy.spells.holy_shock, FS.holy.variables.heal_targets, hs_2_threshold, 1, true, nil, false) then
        return true
    end

    if
        overcap_safe
        and rising_sunlight_up
        and FS.holy.cast_with_condition(FS.holy.spells.holy_shock, FS.holy.variables.heal_targets, hs_rs_threshold, 1, true, nil, false) then
        return true
    end

    return false
end

function FS.holy.holy_prism_logic()
    if FS.api.spell_helper:is_spell_on_cooldown(FS.holy.spells.holy_prism:id()) then
        return false
    end

    if not FS.holy.variables.beacon_of_virtue_up then
        return false
    end

    if not FS.holy.cast_with_condition(FS.holy.spells.holy_prism, FS.holy.variables.heal_targets, 45, 1, true, nil, false) and FS.holy.variables.target_is_valid then
        return FS.holy.cast_at_enemy(FS.holy.spells.holy_prism, FS.holy.variables.force_target)
    end

    return false
end

function FS.holy.word_of_glory_logic()
    if not FS.holy.variables.can_use_spenders then
        return false
    end

    if FS.api.spell_helper:is_spell_on_cooldown(FS.holy.spells.word_of_glory:id()) then
        return false
    end

    return FS.holy.cast_with_condition(FS.holy.spells.word_of_glory, FS.holy.variables.heal_targets,
        FS.holy.settings.wog_hp(),
        1, true, nil, false)
end

function FS.holy.tank_word_of_glory_logic()
    if not FS.holy.variables.can_use_spenders then
        return false
    end

    if core.spell_book.get_spell_cooldown(FS.holy.spells.word_of_glory:id()) then
        return false
    end

    return FS.holy.cast_with_condition(FS.holy.spells.word_of_glory, FS.holy.variables.tanks,
        FS.holy.settings.wog_tank_hp(),
        1, true, nil, false)
end

function FS.holy.seasons_logic()
    if not FS.state.player.go:is_in_combat() then
        return false
    end

    if FS.api.spell_helper:is_spell_on_cooldown(FS.holy.spells.blessing_of_summer:id()) then
        return false
    end

    if not FS.api.spell_helper:is_spell_castable(FS.holy.spells.blessing_of_summer:id(), FS.state.player.go, FS.state.player.go, true, true) then
        return false
    end

    if FS.state.player.last_spell_id == FS.holy.spells.blessing_of_summer:id() then
        return false
    end

    -- Handle seasonal blessings
    return FS.api.cast(FS.holy.spells.blessing_of_summer, FS.state.player, "blessing_of_summer")
end
