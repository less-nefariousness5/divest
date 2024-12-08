local APL = require("core/apl")
local State = require("core/state")
local S = require("classes/shaman/enhancement/ids")

local function Aoe()
    local Enhancement = FS.Enhancement

    if S.feral_spirit:is_castable() and (S.elemental_spirits:is_learned().enabled or S.alpha_wolf:is_learned().enabled) then
        if APL.cast(S.feral_spirit, State.target, State, "feral_spirit aoe 1") then
            return true
        end
    end
    if S.tempest:is_castable() and (cast_time == 0 and S.ascendance:is_learned() and S.ascendance:cooldown_remaining() < 2 * State.player:gcd() and S.thorims_invocation:is_learned() and not ti_chain_lightning) then
        if APL.cast(S.tempest, State.target, State, "tempest aoe 2") then
            return true
        end
    end
    if S.chain_lightning:is_castable() and (cast_time == 0 and S.ascendance:is_learned() and S.ascendance:cooldown_remaining() < 2 * State.player:gcd() and S.thorims_invocation:is_learned() and not ti_chain_lightning) then
        if APL.cast(S.chain_lightning, State.target, State, "chain_lightning aoe 3") then
            return true
        end
    end
    if S.ascendance:is_castable() and (State.target:debuff_up(S.flame_shock) and (S.lava_lash:cooldown_remaining() or active_dot.flame_shock >= active_enemies or active_dot.flame_shock == 6) and ti_chain_lightning) then
        if APL.cast(S.ascendance, State.target, State, "ascendance aoe 4") then
            return true
        end
    end
    if S.tempest:is_castable() and (not State.player:buff_up(S.arc_discharge) and ((State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) == buff.Enhancement.variables.maelstrom_weapon.max_stack and not S.raging_Enhancement.variables.maelstrom:is_learned().enabled) or (State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) >= 8)) or (State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) >= 5 and (tempest_mael_count > 30 or State.player:buff_stack(S.awakening_storms) == 2))) then
        if APL.cast(S.tempest, State.target, State, "tempest aoe 5") then
            return true
        end
    end
    if S.windstrike:is_castable() and (S.thorims_invocation:is_learned().enabled and State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) > 0 and ti_chain_lightning) then
        if APL.cast(S.windstrike, State.target, State, "windstrike aoe 6") then
            return true
        end
    end
    if S.crash_lightning:is_castable() and (S.crashing_storms:is_learned().enabled and ((S.unruly_winds:is_learned().enabled and active_enemies >= 10) or active_enemies >= 15)) then
        if APL.cast(S.crash_lightning, State.target, State, "crash_lightning aoe 7") then
            return true
        end
    end
    if S.lightning_bolt:is_castable() and ((not S.tempest:is_learned().enabled or (tempest_mael_count <= 10 and State.player:buff_stack(S.awakening_storms) <= 1)) and ((active_dot.flame_shock >= active_enemies or active_dot.flame_shock == 6) and State.player:buff_up(S.primordial_wave) and State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) == buff.Enhancement.variables.maelstrom_weapon.max_stack and (not State.player:buff_up(S.splintered_elements) or FS.api:fight_remains() <= 12 or raid_event.adds.remains <= State.player:gcd()))) then
        if APL.cast(S.lightning_bolt, State.target, State, "lightning_bolt aoe 8") then
            return true
        end
    end
    if S.flame_shock:is_castable() and (State.player:buff_up(S.voltaic_blaze) and State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) <= 8) then
        if APL.cast(S.flame_shock, State.target, State, "flame_shock aoe 9") then
            return true
        end
    end
    if S.lava_lash:is_castable() and (S.molten_assault:is_learned().enabled and (S.primordial_wave:is_learned().enabled or S.fire_nova:is_learned().enabled) and State.target:debuff_up(S.flame_shock) and (active_dot.flame_shock < active_enemies) and active_dot.flame_shock < 6) then
        if APL.cast(S.lava_lash, State.target, State, "lava_lash aoe 10") then
            return true
        end
    end
    if S.primordial_wave:is_castable() and (not State.player:buff_up(S.primordial_wave)) then
        if APL.cast(S.primordial_wave, State.target, State, "primordial_wave aoe 11") then
            return true
        end
    end
    if S.chain_lightning:is_castable() and (State.player:buff_up(S.arc_discharge) and State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) >= 5) then
        if APL.cast(S.chain_lightning, State.target, State, "chain_lightning aoe 12") then
            return true
        end
    end
    if S.elemental_blast:is_castable() and ((not S.elemental_spirits:is_learned().enabled or (S.elemental_spirits:is_learned().enabled and (charges == max_charges or feral_spirit.active >= 2))) and State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) == buff.Enhancement.variables.maelstrom_weapon.max_stack and (not S.crashing_storms:is_learned().enabled or active_enemies <= 3)) then
        if APL.cast(S.elemental_blast, State.target, State, "elemental_blast aoe 13") then
            return true
        end
    end
    if S.chain_lightning:is_castable() and ((State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) == buff.Enhancement.variables.maelstrom_weapon.max_stack and not S.raging_Enhancement.variables.maelstrom:is_learned().enabled) or (State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) >= 7)) then
        if APL.cast(S.chain_lightning, State.target, State, "chain_lightning aoe 14") then
            return true
        end
    end
    if S.feral_spirit:is_castable() then
        if APL.cast(S.feral_spirit, State.target, State, "feral_spirit aoe 15") then
            return true
        end
    end
    if S.doom_winds:is_castable() and (ti_chain_lightning and (State.player:buff_up(S.legacy_of_the_frost_witch) or not S.legacy_of_the_frost_witch:is_learned().enabled)) then
        if APL.cast(S.doom_winds, State.target, State, "doom_winds aoe 16") then
            return true
        end
    end
    if S.crash_lightning:is_castable() and ((State.player:buff_up(S.doom_winds) and active_enemies >= 4) or not State.player:buff_up(S.crash_lightning) or (S.alpha_wolf:is_learned().enabled and feral_spirit.active and alpha_wolf_min_remains == 0)) then
        if APL.cast(S.crash_lightning, State.target, State, "crash_lightning aoe 17") then
            return true
        end
    end
    if S.sundering:is_castable() and (State.player:buff_up(S.doom_winds) or S.earthsurge:is_learned().enabled) then
        if APL.cast(S.sundering, State.target, State, "sundering aoe 18") then
            return true
        end
    end
    if S.fire_nova:is_castable() and (active_dot.flame_shock == 6 or (active_dot.flame_shock >= 4 and active_dot.flame_shock >= cycle_enemies)) then
        if APL.cast(S.fire_nova, State.target, State, "fire_nova aoe 19") then
            return true
        end
    end
    if S.stormstrike:is_castable() and (S.stormblast:is_learned().enabled and S.stormflurry:is_learned().enabled) then
        if APL.cast(S.stormstrike, State.target, State, "stormstrike aoe 20") then
            return true
        end
    end
    if S.flame_shock:is_castable() and (State.player:buff_up(S.voltaic_blaze)) then
        if APL.cast(S.flame_shock, State.target, State, "flame_shock aoe 21") then
            return true
        end
    end
    if S.lava_lash:is_castable() and (S.lashing_flames:is_learned().enabled) then
        if APL.cast(S.lava_lash, State.target, State, "lava_lash aoe 22") then
            return true
        end
    end
    if S.lava_lash:is_castable() and (S.molten_assault:is_learned().enabled and State.target:debuff_up(S.flame_shock)) then
        if APL.cast(S.lava_lash, State.target, State, "lava_lash aoe 23") then
            return true
        end
    end
    if S.ice_strike:is_castable() and (S.hailstorm:is_learned().enabled and not State.player:buff_up(S.ice_strike)) then
        if APL.cast(S.ice_strike, State.target, State, "ice_strike aoe 24") then
            return true
        end
    end
    if S.frost_shock:is_castable() and (S.hailstorm:is_learned().enabled and State.player:buff_up(S.hailstorm)) then
        if APL.cast(S.frost_shock, State.target, State, "frost_shock aoe 25") then
            return true
        end
    end
    if S.sundering:is_castable() then
        if APL.cast(S.sundering, State.target, State, "sundering aoe 26") then
            return true
        end
    end
    if S.flame_shock:is_castable() and (S.molten_assault:is_learned().enabled and not ticking) then
        if APL.cast(S.flame_shock, State.target, State, "flame_shock aoe 27") then
            return true
        end
    end
    if S.flame_shock:is_castable() and (refreshable and (S.fire_nova:is_learned().enabled or S.primordial_wave:is_learned().enabled) and (active_dot.flame_shock < active_enemies) and active_dot.flame_shock < 6) then
        if APL.cast(S.flame_shock, State.target, State, "flame_shock aoe 28") then
            return true
        end
    end
    if S.fire_nova:is_castable() and (active_dot.flame_shock >= 3) then
        if APL.cast(S.fire_nova, State.target, State, "fire_nova aoe 29") then
            return true
        end
    end
    if S.stormstrike:is_castable() and (State.player:buff_up(S.crash_lightning) and (S.deeply_rooted_elements:is_learned().enabled or State.player:buff_stack(S.converging_storms) == buff.converging_storms.max_stack)) then
        if APL.cast(S.stormstrike, State.target, State, "stormstrike aoe 30") then
            return true
        end
    end
    if S.crash_lightning:is_castable() and (S.crashing_storms:is_learned().enabled and State.player:buff_up(S.cl_crash_lightning) and active_enemies >= 4) then
        if APL.cast(S.crash_lightning, State.target, State, "crash_lightning aoe 31") then
            return true
        end
    end
    if S.windstrike:is_castable() then
        if APL.cast(S.windstrike, State.target, State, "windstrike aoe 32") then
            return true
        end
    end
    if S.stormstrike:is_castable() then
        if APL.cast(S.stormstrike, State.target, State, "stormstrike aoe 33") then
            return true
        end
    end
    if S.ice_strike:is_castable() then
        if APL.cast(S.ice_strike, State.target, State, "ice_strike aoe 34") then
            return true
        end
    end
    if S.lava_lash:is_castable() then
        if APL.cast(S.lava_lash, State.target, State, "lava_lash aoe 35") then
            return true
        end
    end
    if S.crash_lightning:is_castable() then
        if APL.cast(S.crash_lightning, State.target, State, "crash_lightning aoe 36") then
            return true
        end
    end
    if S.fire_nova:is_castable() and (active_dot.flame_shock >= 2) then
        if APL.cast(S.fire_nova, State.target, State, "fire_nova aoe 37") then
            return true
        end
    end
    if S.elemental_blast:is_castable() and ((not S.elemental_spirits:is_learned().enabled or (S.elemental_spirits:is_learned().enabled and (charges == max_charges or feral_spirit.active >= 2))) and State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) >= 5 and (not S.crashing_storms:is_learned().enabled or active_enemies <= 3)) then
        if APL.cast(S.elemental_blast, State.target, State, "elemental_blast aoe 38") then
            return true
        end
    end
    if S.chain_lightning:is_castable() and (State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) >= 5) then
        if APL.cast(S.chain_lightning, State.target, State, "chain_lightning aoe 39") then
            return true
        end
    end
    if S.flame_shock:is_castable() and (not ticking) then
        if APL.cast(S.flame_shock, State.target, State, "flame_shock aoe 40") then
            return true
        end
    end
    if S.frost_shock:is_castable() and (not S.hailstorm:is_learned().enabled) then
        if APL.cast(S.frost_shock, State.target, State, "frost_shock aoe 41") then
            return true
        end
    end

    return false
end

return Aoe
