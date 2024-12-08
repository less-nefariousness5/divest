local APL = require("core/apl")
local State = require("core/state")
local S = require("classes/shaman/enhancement/ids")

local function Single()
    local Enhancement = FS.Enhancement

    if S.feral_spirit:is_castable() and (S.elemental_spirits:is_learned().enabled) then
    if APL.cast(S.feral_spirit, State.target, State, "feral_spirit single 1") then
        return true
    end
end
    if S.windstrike:is_castable() and (S.thorims_invocation:is_learned().enabled and State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) > 0 and ti_lightning_bolt and not S.elemental_spirits:is_learned().enabled) then
    if APL.cast(S.windstrike, State.target, State, "windstrike single 2") then
        return true
    end
end
    if S.primordial_wave:is_castable() and (not State.target:debuff_up(S.flame_shock) and S.molten_assault:is_learned().enabled) then
    if APL.cast(S.primordial_wave, State.target, State, "primordial_wave single 3") then
        return true
    end
end
    if S.lava_lash:is_castable() and (S.lashing_flames:is_learned().enabled and debuff.lashing_flames.down) then
    if APL.cast(S.lava_lash, State.target, State, "lava_lash single 4") then
        return true
    end
end
    if S.stormstrike:is_castable() and (State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) < 2 and S.ascendance:cooldown_remaining() == 0) then
    if APL.cast(S.stormstrike, State.target, State, "stormstrike single 5") then
        return true
    end
end
    if S.feral_spirit:is_castable() then
    if APL.cast(S.feral_spirit, State.target, State, "feral_spirit single 6") then
        return true
    end
end
    if S.tempest:is_castable() and (cast_time == 0 and S.ascendance:is_learned() and S.ascendance:cooldown_remaining() < 2*State.player:gcd() and S.thorims_invocation:is_learned() and not ti_lightning_bolt) then
    if APL.cast(S.tempest, State.target, State, "tempest single 7") then
        return true
    end
end
    if S.lightning_bolt:is_castable() and (cast_time == 0 and S.ascendance:is_learned() and S.ascendance:cooldown_remaining() < 2*State.player:gcd() and S.thorims_invocation:is_learned() and not ti_lightning_bolt) then
    if APL.cast(S.lightning_bolt, State.target, State, "lightning_bolt single 8") then
        return true
    end
end
    if S.ascendance:is_castable() and (State.target:debuff_up(S.flame_shock) and ti_lightning_bolt and active_enemies == 1 and State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) >= 2) then
    if APL.cast(S.ascendance, State.target, State, "ascendance single 9") then
        return true
    end
end
    if S.tempest:is_castable() and (State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) == buff.Enhancement.variables.maelstrom_weapon.max_stack or (State.player:buff_stack(S.tempest) == buff.tempest.max_stack and (tempest_mael_count > 30 or State.player:buff_stack(S.awakening_storms) == 2) and State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) >= 5)) then
    if APL.cast(S.tempest, State.target, State, "tempest single 10") then
        return true
    end
end
    if S.elemental_blast:is_castable() and (State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) == buff.Enhancement.variables.maelstrom_weapon.max_stack and S.elemental_spirits:is_learned().enabled and feral_spirit.active >= 6 and (charges_fractional >= 1.8 or State.player:buff_up(S.ascendance))) then
    if APL.cast(S.elemental_blast, State.target, State, "elemental_blast single 11") then
        return true
    end
end
    if S.windstrike:is_castable() and (S.thorims_invocation:is_learned().enabled and State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) > 0 and ti_lightning_bolt and charges == max_charges) then
    if APL.cast(S.windstrike, State.target, State, "windstrike single 12") then
        return true
    end
end
    if S.doom_winds:is_castable() and (S.elemental_spirits:is_learned().enabled and S.ascendance:is_learned().enabled and State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) >= 2) then
    if APL.cast(S.doom_winds, State.target, State, "doom_winds single 13") then
        return true
    end
end
    if S.windstrike:is_castable() and (S.thorims_invocation:is_learned().enabled and State.player:buff_up(S.Enhancement.variables.maelstrom_weapon) and ti_lightning_bolt) then
    if APL.cast(S.windstrike, State.target, State, "windstrike single 14") then
        return true
    end
end
    if S.flame_shock:is_castable() and (not ticking and S.ashen_catalyst:is_learned().enabled) then
    if APL.cast(S.flame_shock, State.target, State, "flame_shock single 15") then
        return true
    end
end
    if S.lightning_bolt:is_castable() and (State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) == buff.Enhancement.variables.maelstrom_weapon.max_stack and State.player:buff_up(S.primordial_wave)) then
    if APL.cast(S.lightning_bolt, State.target, State, "lightning_bolt single 16") then
        return true
    end
end
    if S.tempest:is_castable() and ((not S.overflowing_Enhancement.variables.maelstrom:is_learned().enabled and State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) >= 5) or (State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) >= 10-2*S.elemental_spirits:is_learned().enabled)) then
    if APL.cast(S.tempest, State.target, State, "tempest single 17") then
        return true
    end
end
    if S.primordial_wave:is_castable() and (not S.deeply_rooted_elements:is_learned().enabled) then
    if APL.cast(S.primordial_wave, State.target, State, "primordial_wave single 18") then
        return true
    end
end
    if S.elemental_blast:is_castable() and (State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) >= 8 and feral_spirit.active >= 4 and (not State.player:buff_up(S.ascendance) or charges_fractional >= 1.8)) then
    if APL.cast(S.elemental_blast, State.target, State, "elemental_blast single 19") then
        return true
    end
end
    if S.lightning_bolt:is_castable() and (State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) >= 8+2*S.legacy_of_the_frost_witch:is_learned().enabled) then
    if APL.cast(S.lightning_bolt, State.target, State, "lightning_bolt single 20") then
        return true
    end
end
    if S.lightning_bolt:is_castable() and (State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) >= 5 and not S.legacy_of_the_frost_witch:is_learned().enabled and (S.deeply_rooted_elements:is_learned().enabled or not S.overflowing_Enhancement.variables.maelstrom:is_learned().enabled or not S.witch_doctors_ancestry:is_learned().enabled)) then
    if APL.cast(S.lightning_bolt, State.target, State, "lightning_bolt single 21") then
        return true
    end
end
    if S.flame_shock:is_castable() and (State.player:buff_up(S.voltaic_blaze) and S.elemental_spirits:is_learned().enabled and not S.witch_doctors_ancestry:is_learned().enabled) then
    if APL.cast(S.flame_shock, State.target, State, "flame_shock single 22") then
        return true
    end
end
    if S.lightning_bolt:is_castable() and (State.player:buff_up(S.arc_discharge) and S.deeply_rooted_elements:is_learned().enabled) then
    if APL.cast(S.lightning_bolt, State.target, State, "lightning_bolt single 23") then
        return true
    end
end
    if S.lava_lash:is_castable() and (State.player:buff_up(S.hot_hand) or (State.player:buff_stack(S.ashen_catalyst) == buff.ashen_catalyst.max_stack)) then
    if APL.cast(S.lava_lash, State.target, State, "lava_lash single 24") then
        return true
    end
end
    if S.stormstrike:is_castable() and (State.player:buff_up(S.doom_winds) or (S.stormblast:is_learned().enabled and State.player:buff_up(S.stormsurge) and charges == max_charges)) then
    if APL.cast(S.stormstrike, State.target, State, "stormstrike single 25") then
        return true
    end
end
    if S.lava_lash:is_castable() and (S.lashing_flames:is_learned().enabled and not State.player:buff_up(S.doom_winds)) then
    if APL.cast(S.lava_lash, State.target, State, "lava_lash single 26") then
        return true
    end
end
    if S.flame_shock:is_castable() and (State.player:buff_up(S.voltaic_blaze) and S.elemental_spirits:is_learned().enabled and not State.player:buff_up(S.doom_winds)) then
    if APL.cast(S.flame_shock, State.target, State, "flame_shock single 27") then
        return true
    end
end
    if S.crash_lightning:is_castable() and (S.unrelenting_storms:is_learned().enabled and S.elemental_spirits:is_learned().enabled and not S.deeply_rooted_elements:is_learned().enabled) then
    if APL.cast(S.crash_lightning, State.target, State, "crash_lightning single 28") then
        return true
    end
end
    if S.ice_strike:is_castable() and (S.elemental_assault:is_learned().enabled and S.swirling_Enhancement.variables.maelstrom:is_learned().enabled and S.witch_doctors_ancestry:is_learned().enabled) then
    if APL.cast(S.ice_strike, State.target, State, "ice_strike single 29") then
        return true
    end
end
    if S.stormstrike:is_castable() then
    if APL.cast(S.stormstrike, State.target, State, "stormstrike single 30") then
        return true
    end
end
    if S.lightning_bolt:is_castable() and (State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) >= 5 and S.ascendance:is_learned().enabled and not S.legacy_of_the_frost_witch:is_learned().enabled) then
    if APL.cast(S.lightning_bolt, State.target, State, "lightning_bolt single 31") then
        return true
    end
end
    if S.crash_lightning:is_castable() and (S.unrelenting_storms:is_learned().enabled) then
    if APL.cast(S.crash_lightning, State.target, State, "crash_lightning single 32") then
        return true
    end
end
    if S.flame_shock:is_castable() and (State.player:buff_up(S.voltaic_blaze)) then
    if APL.cast(S.flame_shock, State.target, State, "flame_shock single 33") then
        return true
    end
end
    if S.sundering:is_castable() and (not S.elemental_spirits:is_learned().enabled) then
    if APL.cast(S.sundering, State.target, State, "sundering single 34") then
        return true
    end
end
    if S.frost_shock:is_castable() and (State.player:buff_up(S.hailstorm) and State.player:buff_up(S.ice_strike) and S.swirling_Enhancement.variables.maelstrom:is_learned().enabled and S.ascendance:is_learned().enabled) then
    if APL.cast(S.frost_shock, State.target, State, "frost_shock single 35") then
        return true
    end
end
    if S.elemental_blast:is_castable() and (State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) >= 5 and feral_spirit.active >= 4 and S.deeply_rooted_elements:is_learned().enabled and (charges_fractional >= 1.8 or (State.player:buff_stack(S.molten_weapon)+State.player:buff_stack(S.icy_edge) >= 4)) and not S.flowing_spirits:is_learned().enabled) then
    if APL.cast(S.elemental_blast, State.target, State, "elemental_blast single 36") then
        return true
    end
end
    if S.crash_lightning:is_castable() and (S.alpha_wolf:is_learned().enabled and feral_spirit.active and alpha_wolf_min_remains == 0) then
    if APL.cast(S.crash_lightning, State.target, State, "crash_lightning single 37") then
        return true
    end
end
    if S.flame_shock:is_castable() and (not ticking and not S.tempest:is_learned().enabled) then
    if APL.cast(S.flame_shock, State.target, State, "flame_shock single 38") then
        return true
    end
end
    if S.doom_winds:is_castable() and (S.elemental_spirits:is_learned().enabled) then
    if APL.cast(S.doom_winds, State.target, State, "doom_winds single 39") then
        return true
    end
end
    if S.lava_lash:is_castable() and (S.elemental_assault:is_learned().enabled and S.tempest:is_learned().enabled and S.molten_assault:is_learned().enabled and S.deeply_rooted_elements:is_learned().enabled and State.target:debuff_up(S.flame_shock)) then
    if APL.cast(S.lava_lash, State.target, State, "lava_lash single 40") then
        return true
    end
end
    if S.ice_strike:is_castable() and (S.elemental_assault:is_learned().enabled and S.swirling_Enhancement.variables.maelstrom:is_learned().enabled) then
    if APL.cast(S.ice_strike, State.target, State, "ice_strike single 41") then
        return true
    end
end
    if S.lightning_bolt:is_castable() and (State.player:buff_up(S.arc_discharge)) then
    if APL.cast(S.lightning_bolt, State.target, State, "lightning_bolt single 42") then
        return true
    end
end
    if S.crash_lightning:is_castable() and (S.unrelenting_storms:is_learned().enabled) then
    if APL.cast(S.crash_lightning, State.target, State, "crash_lightning single 43") then
        return true
    end
end
    if S.lava_lash:is_castable() and (S.elemental_assault:is_learned().enabled and S.tempest:is_learned().enabled and S.molten_assault:is_learned().enabled and State.target:debuff_up(S.flame_shock)) then
    if APL.cast(S.lava_lash, State.target, State, "lava_lash single 44") then
        return true
    end
end
    if S.frost_shock:is_castable() and (State.player:buff_up(S.hailstorm) and State.player:buff_up(S.ice_strike) and S.swirling_Enhancement.variables.maelstrom:is_learned().enabled and S.tempest:is_learned().enabled) then
    if APL.cast(S.frost_shock, State.target, State, "frost_shock single 45") then
        return true
    end
end
    if S.flame_shock:is_castable() and (not ticking) then
    if APL.cast(S.flame_shock, State.target, State, "flame_shock single 46") then
        return true
    end
end
    if S.lava_lash:is_castable() and (S.lashing_flames:is_learned().enabled) then
    if APL.cast(S.lava_lash, State.target, State, "lava_lash single 47") then
        return true
    end
end
    if S.ice_strike:is_castable() and (not State.player:buff_up(S.ice_strike)) then
    if APL.cast(S.ice_strike, State.target, State, "ice_strike single 48") then
        return true
    end
end
    if S.frost_shock:is_castable() and (State.player:buff_up(S.hailstorm)) then
    if APL.cast(S.frost_shock, State.target, State, "frost_shock single 49") then
        return true
    end
end
    if S.crash_lightning:is_castable() and (S.converging_storms:is_learned().enabled) then
    if APL.cast(S.crash_lightning, State.target, State, "crash_lightning single 50") then
        return true
    end
end
    if S.lava_lash:is_castable() then
    if APL.cast(S.lava_lash, State.target, State, "lava_lash single 51") then
        return true
    end
end
    if S.ice_strike:is_castable() then
    if APL.cast(S.ice_strike, State.target, State, "ice_strike single 52") then
        return true
    end
end
    if S.windstrike:is_castable() then
    if APL.cast(S.windstrike, State.target, State, "windstrike single 53") then
        return true
    end
end
    if S.stormstrike:is_castable() then
    if APL.cast(S.stormstrike, State.target, State, "stormstrike single 54") then
        return true
    end
end
    if S.sundering:is_castable() then
    if APL.cast(S.sundering, State.target, State, "sundering single 55") then
        return true
    end
end
    if S.frost_shock:is_castable() then
    if APL.cast(S.frost_shock, State.target, State, "frost_shock single 56") then
        return true
    end
end
    if S.crash_lightning:is_castable() then
    if APL.cast(S.crash_lightning, State.target, State, "crash_lightning single 57") then
        return true
    end
end
    if S.fire_nova:is_castable() and (active_dot.flame_shock) then
    if APL.cast(S.fire_nova, State.target, State, "fire_nova single 58") then
        return true
    end
end
    if S.earth_elemental:is_castable() then
    if APL.cast(S.earth_elemental, State.target, State, "earth_elemental single 59") then
        return true
    end
end
    if S.flame_shock:is_castable() and (settings.filler_shock) then
    if APL.cast(S.flame_shock, State.target, State, "flame_shock single 60") then
        return true
    end
end

    return false
end

return Single