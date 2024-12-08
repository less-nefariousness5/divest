local APL = require("core/apl")
local State = require("core/state")
local S = require("classes/shaman/enhancement/ids")

local function Single_totemic()
    local Enhancement = FS.Enhancement

    if S.surging_totem:is_castable() then
        if APL.cast(S.surging_totem, State.target, State, "surging_totem single_totemic 1") then
            return true
        end
    end
    if S.tempest:is_castable() and (cast_time == 0 and S.ascendance:is_learned() and S.ascendance:cooldown_remaining() < 2 * State.player:gcd() and S.thorims_invocation:is_learned() and not ti_lightning_bolt) then
        if APL.cast(S.tempest, State.target, State, "tempest single_totemic 2") then
            return true
        end
    end
    if S.lightning_bolt:is_castable() and (cast_time == 0 and S.ascendance:is_learned() and S.ascendance:cooldown_remaining() < 2 * State.player:gcd() and S.thorims_invocation:is_learned() and not ti_lightning_bolt) then
        if APL.cast(S.lightning_bolt, State.target, State, "lightning_bolt single_totemic 3") then
            return true
        end
    end
    if S.ascendance:is_castable() and (ti_lightning_bolt and pet.surging_totem.remains > 4 and (State.player:buff_stack(S.totemic_rebound) >= 3 or State.player:buff_up(S.Enhancement.variables.maelstrom_weapon))) then
        if APL.cast(S.ascendance, State.target, State, "ascendance single_totemic 4") then
            return true
        end
    end
    if S.doom_winds:is_castable() and (not S.elemental_spirits:is_learned().enabled and State.player:buff_up(S.legacy_of_the_frost_witch)) then
        if APL.cast(S.doom_winds, State.target, State, "doom_winds single_totemic 5") then
            return true
        end
    end
    if S.sundering:is_castable() and (State.player:buff_up(S.ascendance) and pet.surging_totem.active and S.earthsurge:is_learned().enabled and State.player:buff_up(S.legacy_of_the_frost_witch) and State.player:buff_stack(S.totemic_rebound) >= 5 and State.player:buff_stack(S.earthen_weapon) >= 2) then
        if APL.cast(S.sundering, State.target, State, "sundering single_totemic 6") then
            return true
        end
    end
    if S.crash_lightning:is_castable() and (S.unrelenting_storms:is_learned().enabled and S.alpha_wolf:is_learned().enabled and alpha_wolf_min_remains == 0 and State.player:buff_stack(S.earthen_weapon) >= 8) then
        if APL.cast(S.crash_lightning, State.target, State, "crash_lightning single_totemic 7") then
            return true
        end
    end
    if S.windstrike:is_castable() and (S.thorims_invocation:is_learned().enabled and State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) > 0 and ti_lightning_bolt and not S.elemental_spirits:is_learned().enabled) then
        if APL.cast(S.windstrike, State.target, State, "windstrike single_totemic 8") then
            return true
        end
    end
    if S.sundering:is_castable() and (State.player:buff_up(S.legacy_of_the_frost_witch) and S.ascendance:cooldown_remaining() >= 10 and pet.surging_totem.active and State.player:buff_stack(S.totemic_rebound) >= 3 and not State.player:buff_up(S.ascendance)) then
        if APL.cast(S.sundering, State.target, State, "sundering single_totemic 9") then
            return true
        end
    end
    if S.primordial_wave:is_castable() and (not State.target:debuff_up(S.flame_shock) and S.molten_assault:is_learned().enabled) then
        if APL.cast(S.primordial_wave, State.target, State, "primordial_wave single_totemic 10") then
            return true
        end
    end
    if S.feral_spirit:is_castable() then
        if APL.cast(S.feral_spirit, State.target, State, "feral_spirit single_totemic 11") then
            return true
        end
    end
    if S.elemental_blast:is_castable() and (State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) == buff.Enhancement.variables.maelstrom_weapon.max_stack and S.elemental_spirits:is_learned().enabled and feral_spirit.active >= 6 and (charges_fractional >= 1.8 or State.player:buff_up(S.ascendance))) then
        if APL.cast(S.elemental_blast, State.target, State, "elemental_blast single_totemic 12") then
            return true
        end
    end
    if S.flame_shock:is_castable() and (State.player:buff_up(S.voltaic_blaze) and State.player:buff_up(S.whirling_earth)) then
        if APL.cast(S.flame_shock, State.target, State, "flame_shock single_totemic 13") then
            return true
        end
    end
    if S.crash_lightning:is_castable() and (S.unrelenting_storms:is_learned().enabled and S.alpha_wolf:is_learned().enabled and alpha_wolf_min_remains == 0) then
        if APL.cast(S.crash_lightning, State.target, State, "crash_lightning single_totemic 14") then
            return true
        end
    end
    if S.flame_shock:is_castable() and (not ticking and S.lashing_flames:is_learned().enabled) then
        if APL.cast(S.flame_shock, State.target, State, "flame_shock single_totemic 15") then
            return true
        end
    end
    if S.lava_lash:is_castable() and (State.player:buff_up(S.hot_hand) and not S.legacy_of_the_frost_witch:is_learned().enabled) then
        if APL.cast(S.lava_lash, State.target, State, "lava_lash single_totemic 16") then
            return true
        end
    end
    if S.elemental_blast:is_castable() and (State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) >= 5 and charges == max_charges) then
        if APL.cast(S.elemental_blast, State.target, State, "elemental_blast single_totemic 17") then
            return true
        end
    end
    if S.lightning_bolt:is_castable() and (State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) >= 8 and State.player:buff_up(S.primordial_wave) and (not State.player:buff_up(S.splintered_elements) or FS.api:fight_remains() <= 12)) then
        if APL.cast(S.lightning_bolt, State.target, State, "lightning_bolt single_totemic 18") then
            return true
        end
    end
    if S.elemental_blast:is_castable() and (State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) >= 8 and (feral_spirit.active >= 2 or not S.elemental_spirits:is_learned().enabled)) then
        if APL.cast(S.elemental_blast, State.target, State, "elemental_blast single_totemic 19") then
            return true
        end
    end
    if S.lava_burst:is_castable() and (not S.thorims_invocation:is_learned().enabled and State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) >= 5) then
        if APL.cast(S.lava_burst, State.target, State, "lava_burst single_totemic 20") then
            return true
        end
    end
    if S.primordial_wave:is_castable() then
        if APL.cast(S.primordial_wave, State.target, State, "primordial_wave single_totemic 21") then
            return true
        end
    end
    if S.elemental_blast:is_castable() and (State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) >= 5 and (charges_fractional >= 1.8 or (State.player:buff_stack(S.molten_weapon) + State.player:buff_stack(S.icy_edge) >= 4)) and S.ascendance:is_learned().enabled and (feral_spirit.active >= 4 or not S.elemental_spirits:is_learned().enabled)) then
        if APL.cast(S.elemental_blast, State.target, State, "elemental_blast single_totemic 22") then
            return true
        end
    end
    if S.elemental_blast:is_castable() and (S.ascendance:is_learned().enabled and (State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) >= 10 or (State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) >= 5 and State.player:buff_up(S.whirling_air) and not State.player:buff_up(S.legacy_of_the_frost_witch)))) then
        if APL.cast(S.elemental_blast, State.target, State, "elemental_blast single_totemic 23") then
            return true
        end
    end
    if S.lightning_bolt:is_castable() and (S.ascendance:is_learned().enabled and (State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) >= 10 or (State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) >= 5 and State.player:buff_up(S.whirling_air) and not State.player:buff_up(S.legacy_of_the_frost_witch)))) then
        if APL.cast(S.lightning_bolt, State.target, State, "lightning_bolt single_totemic 24") then
            return true
        end
    end
    if S.lava_lash:is_castable() and (State.player:buff_up(S.hot_hand) and S.molten_assault:is_learned().enabled and pet.searing_totem.active) then
        if APL.cast(S.lava_lash, State.target, State, "lava_lash single_totemic 25") then
            return true
        end
    end
    if S.windstrike:is_castable() then
        if APL.cast(S.windstrike, State.target, State, "windstrike single_totemic 26") then
            return true
        end
    end
    if S.stormstrike:is_castable() then
        if APL.cast(S.stormstrike, State.target, State, "stormstrike single_totemic 27") then
            return true
        end
    end
    if S.lava_lash:is_castable() and (S.molten_assault:is_learned().enabled) then
        if APL.cast(S.lava_lash, State.target, State, "lava_lash single_totemic 28") then
            return true
        end
    end
    if S.crash_lightning:is_castable() and (S.unrelenting_storms:is_learned().enabled) then
        if APL.cast(S.crash_lightning, State.target, State, "crash_lightning single_totemic 29") then
            return true
        end
    end
    if S.lightning_bolt:is_castable() and (State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) >= 5 and S.ascendance:is_learned().enabled) then
        if APL.cast(S.lightning_bolt, State.target, State, "lightning_bolt single_totemic 30") then
            return true
        end
    end
    if S.ice_strike:is_castable() and (not State.player:buff_up(S.ice_strike)) then
        if APL.cast(S.ice_strike, State.target, State, "ice_strike single_totemic 31") then
            return true
        end
    end
    if S.frost_shock:is_castable() and (State.player:buff_up(S.hailstorm) and pet.searing_totem.active) then
        if APL.cast(S.frost_shock, State.target, State, "frost_shock single_totemic 32") then
            return true
        end
    end
    if S.lava_lash:is_castable() then
        if APL.cast(S.lava_lash, State.target, State, "lava_lash single_totemic 33") then
            return true
        end
    end
    if S.elemental_blast:is_castable() and (State.player:buff_stack(S.Enhancement.variables.maelstrom_weapon) >= 5 and feral_spirit.active >= 4 and S.deeply_rooted_elements:is_learned().enabled and (charges_fractional >= 1.8 or (State.player:buff_stack(S.icy_edge) + State.player:buff_stack(S.molten_weapon) >= 4))) then
        if APL.cast(S.elemental_blast, State.target, State, "elemental_blast single_totemic 34") then
            return true
        end
    end
    if S.doom_winds:is_castable() and (S.elemental_spirits:is_learned().enabled) then
        if APL.cast(S.doom_winds, State.target, State, "doom_winds single_totemic 35") then
            return true
        end
    end
    if S.flame_shock:is_castable() and (not ticking and not S.voltaic_blaze:is_learned().enabled) then
        if APL.cast(S.flame_shock, State.target, State, "flame_shock single_totemic 36") then
            return true
        end
    end
    if S.frost_shock:is_castable() and (State.player:buff_up(S.hailstorm)) then
        if APL.cast(S.frost_shock, State.target, State, "frost_shock single_totemic 37") then
            return true
        end
    end
    if S.crash_lightning:is_castable() and (S.converging_storms:is_learned().enabled) then
        if APL.cast(S.crash_lightning, State.target, State, "crash_lightning single_totemic 38") then
            return true
        end
    end
    if S.frost_shock:is_castable() then
        if APL.cast(S.frost_shock, State.target, State, "frost_shock single_totemic 39") then
            return true
        end
    end
    if S.crash_lightning:is_castable() then
        if APL.cast(S.crash_lightning, State.target, State, "crash_lightning single_totemic 40") then
            return true
        end
    end
    if S.fire_nova:is_castable() and (active_dot.flame_shock) then
        if APL.cast(S.fire_nova, State.target, State, "fire_nova single_totemic 41") then
            return true
        end
    end
    if S.earth_elemental:is_castable() then
        if APL.cast(S.earth_elemental, State.target, State, "earth_elemental single_totemic 42") then
            return true
        end
    end
    if S.flame_shock:is_castable() and (not S.voltaic_blaze:is_learned().enabled) then
        if APL.cast(S.flame_shock, State.target, State, "flame_shock single_totemic 43") then
            return true
        end
    end

    return false
end

return Single_totemic
