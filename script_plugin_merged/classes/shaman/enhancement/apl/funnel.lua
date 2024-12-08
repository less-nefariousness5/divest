local APL = require("core/apl")
local State = require("core/state")
local S = require("classes/shaman/enhancement/ids")

local function Funnel()
    local Enhancement = FS.Enhancement

    if S.feral_spirit:is_castable() and (S.elemental_spirits:is_learned().enabled) then
        if APL.cast(S.feral_spirit, State.target, State, "feral_spirit funnel 1") then
            return true
        end
    end
    if S.surging_totem:is_castable() then
        if APL.cast(S.surging_totem, State.target, State, "surging_totem funnel 2") then
            return true
        end
    end
    if S.ascendance:is_castable() then
        if APL.cast(S.ascendance, State.target, State, "ascendance funnel 3") then
            return true
        end
    end
    if S.windstrike:is_castable() and ((S.thorims_invocation:is_learned().enabled and State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) > 0) or State.player:buff_stack(S.converging_storms) == buff.converging_storms.max_stack) then
        if APL.cast(S.windstrike, State.target, State, "windstrike funnel 4") then
            return true
        end
    end
    if S.tempest:is_castable() and (State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) == buff.Enhancement.variables.maelstrom_weapon.max_stack or (State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) >= 5 and (tempest_mael_count > 30 or State.player:buff_stack(S.awakening_storms) == 2))) then
        if APL.cast(S.tempest, State.target, State, "tempest funnel 5") then
            return true
        end
    end
    if S.lightning_bolt:is_castable() and ((active_dot.flame_shock >= active_enemies or active_dot.flame_shock == 6) and State.player:buff_up(S.primordial_wave) and State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) == buff.Enhancement.variables.maelstrom_weapon.max_stack and (not State.player:buff_up(S.splintered_elements) or FS.api:fight_remains() <= 12 or raid_event.adds.remains <= State.player:gcd())) then
        if APL.cast(S.lightning_bolt, State.target, State, "lightning_bolt funnel 6") then
            return true
        end
    end
    if S.elemental_blast:is_castable() and (State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) >= 5 and S.elemental_spirits:is_learned().enabled and feral_spirit.active >= 4) then
        if APL.cast(S.elemental_blast, State.target, State, "elemental_blast funnel 7") then
            return true
        end
    end
    if S.lightning_bolt:is_castable() and (S.supercharge:is_learned().enabled and State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) == buff.Enhancement.variables.maelstrom_weapon.max_stack and (Enhancement.variables.expected_lb_funnel > Enhancement.variables.expected_cl_funnel)) then
        if APL.cast(S.lightning_bolt, State.target, State, "lightning_bolt funnel 8") then
            return true
        end
    end
    if S.chain_lightning:is_castable() and ((S.supercharge:is_learned().enabled and State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) == buff.Enhancement.variables.maelstrom_weapon.max_stack) or State.player:buff_up(S.arc_discharge) and State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) >= 5) then
        if APL.cast(S.chain_lightning, State.target, State, "chain_lightning funnel 9") then
            return true
        end
    end
    if S.lava_lash:is_castable() and ((S.molten_assault:is_learned().enabled and State.target:debuff_up(S.flame_shock) and (active_dot.flame_shock < active_enemies) and active_dot.flame_shock < 6) or (S.ashen_catalyst:is_learned().enabled and State.player:buff_stack(S.ashen_catalyst) == buff.ashen_catalyst.max_stack)) then
        if APL.cast(S.lava_lash, State.target, State, "lava_lash funnel 10") then
            return true
        end
    end
    if S.primordial_wave:is_castable() and (not State.player:buff_up(S.primordial_wave)) then
        if APL.cast(S.primordial_wave, State.target, State, "primordial_wave funnel 11") then
            return true
        end
    end
    if S.elemental_blast:is_castable() and ((not S.elemental_spirits:is_learned().enabled or (S.elemental_spirits:is_learned().enabled and (charges == max_charges or State.player:buff_up(S.feral_spirit)))) and State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) == buff.Enhancement.variables.maelstrom_weapon.max_stack) then
        if APL.cast(S.elemental_blast, State.target, State, "elemental_blast funnel 12") then
            return true
        end
    end
    if S.feral_spirit:is_castable() then
        if APL.cast(S.feral_spirit, State.target, State, "feral_spirit funnel 13") then
            return true
        end
    end
    if S.doom_winds:is_castable() then
        if APL.cast(S.doom_winds, State.target, State, "doom_winds funnel 14") then
            return true
        end
    end
    if S.stormstrike:is_castable() and (State.player:buff_stack(S.converging_storms) == buff.converging_storms.max_stack) then
        if APL.cast(S.stormstrike, State.target, State, "stormstrike funnel 15") then
            return true
        end
    end
    if S.lava_burst:is_castable() and ((State.player:buff_stack(S.molten_weapon) > State.player:buff_stack(S.crackling_surge)) and State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) == buff.Enhancement.variables.maelstrom_weapon.max_stack) then
        if APL.cast(S.lava_burst, State.target, State, "lava_burst funnel 16") then
            return true
        end
    end
    if S.lightning_bolt:is_castable() and (State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) == buff.Enhancement.variables.maelstrom_weapon.max_stack and (Enhancement.variables.expected_lb_funnel > Enhancement.variables.expected_cl_funnel)) then
        if APL.cast(S.lightning_bolt, State.target, State, "lightning_bolt funnel 17") then
            return true
        end
    end
    if S.chain_lightning:is_castable() and (State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) == buff.Enhancement.variables.maelstrom_weapon.max_stack) then
        if APL.cast(S.chain_lightning, State.target, State, "chain_lightning funnel 18") then
            return true
        end
    end
    if S.crash_lightning:is_castable() and (State.player:buff_up(S.doom_winds) or not State.player:buff_up(S.crash_lightning) or (S.alpha_wolf:is_learned().enabled and feral_spirit.active and alpha_wolf_min_remains == 0) or (S.converging_storms:is_learned().enabled and State.player:buff_stack(S.converging_storms) < buff.converging_storms.max_stack)) then
        if APL.cast(S.crash_lightning, State.target, State, "crash_lightning funnel 19") then
            return true
        end
    end
    if S.sundering:is_castable() and (State.player:buff_up(S.doom_winds) or S.earthsurge:is_learned().enabled) then
        if APL.cast(S.sundering, State.target, State, "sundering funnel 20") then
            return true
        end
    end
    if S.fire_nova:is_castable() and (active_dot.flame_shock == 6 or (active_dot.flame_shock >= 4 and active_dot.flame_shock >= active_enemies)) then
        if APL.cast(S.fire_nova, State.target, State, "fire_nova funnel 21") then
            return true
        end
    end
    if S.ice_strike:is_castable() and (S.hailstorm:is_learned().enabled and not State.player:buff_up(S.ice_strike)) then
        if APL.cast(S.ice_strike, State.target, State, "ice_strike funnel 22") then
            return true
        end
    end
    if S.frost_shock:is_castable() and (S.hailstorm:is_learned().enabled and State.player:buff_up(S.hailstorm)) then
        if APL.cast(S.frost_shock, State.target, State, "frost_shock funnel 23") then
            return true
        end
    end
    if S.sundering:is_castable() then
        if APL.cast(S.sundering, State.target, State, "sundering funnel 24") then
            return true
        end
    end
    if S.flame_shock:is_castable() and (S.molten_assault:is_learned().enabled and not ticking) then
        if APL.cast(S.flame_shock, State.target, State, "flame_shock funnel 25") then
            return true
        end
    end
    if S.flame_shock:is_castable() and (refreshable and (S.fire_nova:is_learned().enabled or S.primordial_wave:is_learned().enabled) and (active_dot.flame_shock < active_enemies) and active_dot.flame_shock < 6) then
        if APL.cast(S.flame_shock, State.target, State, "flame_shock funnel 26") then
            return true
        end
    end
    if S.fire_nova:is_castable() and (active_dot.flame_shock >= 3) then
        if APL.cast(S.fire_nova, State.target, State, "fire_nova funnel 27") then
            return true
        end
    end
    if S.stormstrike:is_castable() and (State.player:buff_up(S.crash_lightning) and S.deeply_rooted_elements:is_learned().enabled) then
        if APL.cast(S.stormstrike, State.target, State, "stormstrike funnel 28") then
            return true
        end
    end
    if S.crash_lightning:is_castable() and (S.crashing_storms:is_learned().enabled and State.player:buff_up(S.cl_crash_lightning) and active_enemies >= 4) then
        if APL.cast(S.crash_lightning, State.target, State, "crash_lightning funnel 29") then
            return true
        end
    end
    if S.windstrike:is_castable() then
        if APL.cast(S.windstrike, State.target, State, "windstrike funnel 30") then
            return true
        end
    end
    if S.stormstrike:is_castable() then
        if APL.cast(S.stormstrike, State.target, State, "stormstrike funnel 31") then
            return true
        end
    end
    if S.ice_strike:is_castable() then
        if APL.cast(S.ice_strike, State.target, State, "ice_strike funnel 32") then
            return true
        end
    end
    if S.lava_lash:is_castable() then
        if APL.cast(S.lava_lash, State.target, State, "lava_lash funnel 33") then
            return true
        end
    end
    if S.crash_lightning:is_castable() then
        if APL.cast(S.crash_lightning, State.target, State, "crash_lightning funnel 34") then
            return true
        end
    end
    if S.fire_nova:is_castable() and (active_dot.flame_shock >= 2) then
        if APL.cast(S.fire_nova, State.target, State, "fire_nova funnel 35") then
            return true
        end
    end
    if S.elemental_blast:is_castable() and ((not S.elemental_spirits:is_learned().enabled or (S.elemental_spirits:is_learned().enabled and (charges == max_charges or State.player:buff_up(S.feral_spirit)))) and State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) >= 5) then
        if APL.cast(S.elemental_blast, State.target, State, "elemental_blast funnel 36") then
            return true
        end
    end
    if S.lava_burst:is_castable() and ((State.player:buff_stack(S.molten_weapon) > State.player:buff_stack(S.crackling_surge)) and State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) >= 5) then
        if APL.cast(S.lava_burst, State.target, State, "lava_burst funnel 37") then
            return true
        end
    end
    if S.lightning_bolt:is_castable() and (State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) >= 5 and (Enhancement.variables.expected_lb_funnel > Enhancement.variables.expected_cl_funnel)) then
        if APL.cast(S.lightning_bolt, State.target, State, "lightning_bolt funnel 38") then
            return true
        end
    end
    if S.chain_lightning:is_castable() and (State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) >= 5) then
        if APL.cast(S.chain_lightning, State.target, State, "chain_lightning funnel 39") then
            return true
        end
    end
    if S.flame_shock:is_castable() and (not ticking) then
        if APL.cast(S.flame_shock, State.target, State, "flame_shock funnel 40") then
            return true
        end
    end
    if S.frost_shock:is_castable() and (not S.hailstorm:is_learned().enabled) then
        if APL.cast(S.frost_shock, State.target, State, "frost_shock funnel 41") then
            return true
        end
    end

    return false
end

return Funnel
