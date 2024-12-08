local function Aoe_totemic()
    if FS.enhancement.spells.surging_totem:is_castable() then
        if FS.api.cast_at_cursor(FS.enhancement.spells.surging_totem, FS.state.target, "surging_totem aoe_totemic 1") then
            return true
        end
    end
    --if FS.enhancement.spells.chain_lightning:is_castable() and (cast_time == 0 and FS.enhancement.talents.ascendance:is_learned() and S.ascendance:cooldown_remaining() < 2 * FS.state.player:gcd() and FS.enhancement.talents.thorims_invocation:is_learned() and not FS.enhancement.variables.ti_chain_lightning) then
    --    if FS.api.cast(FS.enhancement.spells.chain_lightning,FS.state.target, "chain_lightning aoe_totemic 2") then
    --        return true
    --    end
    --end
    if FS.enhancement.spells.ascendance:is_castable() and (FS.enhancement.variables.ti_chain_lightning) then
        if FS.api.cast(FS.enhancement.spells.ascendance, FS.state.target, "ascendance aoe_totemic 3") then
            return true
        end
    end
    if FS.enhancement.spells.sundering:is_castable() and (FS.state.player:buff_up(FS.enhancement.auras.ascendance) and FS.enhancement.talents.earthsurge:is_learned() and (FS.state.player:buff_up(FS.enhancement.auras.legacy_of_the_frost_witch) or not FS.enhancement.talents.legacy_of_the_frost_witch:is_learned())) then
        if FS.api.cast(FS.enhancement.spells.sundering, FS.state.target, "sundering aoe_totemic 4") then
            return true
        end
    end
    if FS.enhancement.spells.crash_lightning:is_castable() and (FS.enhancement.talents.crashing_storms:is_learned() and (#FS.state.active_enemies >= 15 - 5 * FS.enhancement.talents.unruly_winds:is_learned())) then
        if FS.api.cast(FS.enhancement.spells.crash_lightning, FS.state.target, "crash_lightning aoe_totemic 5") then
            return true
        end
    end
    if FS.enhancement.spells.lightning_bolt:is_castable() and (((FS.enhancement.variables.flame_shock_count >= #FS.state.active_enemies or FS.enhancement.variables.flame_shock_count == 6) and FS.state.player:buff_up(FS.enhancement.auras.primordial_wave) and FS.state.player:buff_stack(FS.enhancement.auras.maelstrom_weapon) == FS.enhancement.auras.maelstrom_weapon.max_stack and (not FS.state.player:buff_up(FS.enhancement.auras.splintered_elements) or FS.state.fight_remains <= 12))) then
        if FS.api.cast(FS.enhancement.spells.lightning_bolt, FS.state.target, "lightning_bolt aoe_totemic 6") then
            return true
        end
    end
    if FS.enhancement.spells.doom_winds:is_castable() and (not FS.enhancement.talents.elemental_spirits:is_learned() and (FS.state.player:buff_up(FS.enhancement.auras.legacy_of_the_frost_witch) or not FS.enhancement.talents.legacy_of_the_frost_witch:is_learned())) then
        if FS.api.cast(FS.enhancement.spells.doom_winds, FS.state.target, "doom_winds aoe_totemic 7") then
            return true
        end
    end
    if FS.enhancement.spells.lava_lash:is_castable() and (FS.enhancement.talents.molten_assault:is_learned() and (FS.enhancement.talents.primordial_wave:is_learned() or FS.enhancement.talents.fire_nova:is_learned()) and FS.state.target:debuff_up(FS.enhancement.auras.flame_shock) and FS.enhancement.variables.flame_shock_count < #FS.state.active_enemies and FS.enhancement.variables.flame_shock_count < 6) then
        if FS.api.cast(FS.enhancement.spells.lava_lash, FS.state.target, "lava_lash aoe_totemic 8") then
            return true
        end
    end
    if FS.enhancement.spells.primordial_wave:is_castable() and (not FS.state.player:buff_up(FS.enhancement.auras.primordial_wave)) then
        if FS.api.cast(FS.enhancement.spells.primordial_wave, FS.state.target, "primordial_wave aoe_totemic 9") then
            return true
        end
    end
    if FS.enhancement.spells.elemental_blast:is_castable() and ((not FS.enhancement.talents.elemental_spirits:is_learned() or (FS.enhancement.talents.elemental_spirits:is_learned() and (FS.enhancement.spells.elemental_blast:charges() == FS.enhancement.spells.elemental_blast:max_charges() or FS.enhancement.variables.feral_spirit_count >= 2))) and FS.state.player:buff_stack(FS.enhancement.auras.maelstrom_weapon) == FS.enhancement.auras.maelstrom_weapon.max_stack and (not FS.enhancement.talents.crashing_storms:is_learned() or #FS.state.active_enemies <= 3)) then
        if FS.api.cast(FS.enhancement.spells.elemental_blast, FS.state.target, "elemental_blast aoe_totemic 10") then
            return true
        end
    end
    if FS.enhancement.spells.chain_lightning:is_castable() and (FS.state.player:buff_stack(FS.enhancement.auras.maelstrom_weapon) >= 10) then
        if FS.api.cast(FS.enhancement.spells.chain_lightning, FS.state.target, "chain_lightning aoe_totemic 11") then
            return true
        end
    end
    if FS.enhancement.spells.feral_spirit:is_castable() then
        if FS.api.cast(FS.enhancement.spells.feral_spirit, FS.state.target, "feral_spirit aoe_totemic 12") then
            return true
        end
    end
    if FS.enhancement.spells.doom_winds:is_castable() and (FS.state.player:buff_up(FS.enhancement.auras.legacy_of_the_frost_witch) or not FS.enhancement.talents.legacy_of_the_frost_witch:is_learned()) then
        if FS.api.cast(FS.enhancement.spells.doom_winds, FS.state.target, "doom_winds aoe_totemic 13") then
            return true
        end
    end
    if FS.enhancement.spells.crash_lightning:is_castable() and (FS.state.player:buff_up(FS.enhancement.auras.doom_winds) or not FS.state.player:buff_up(FS.enhancement.auras.crash_lightning) or (FS.enhancement.talents.alpha_wolf:is_learned() and FS.enhancement.variables.feral_spirit_count and FS.enhancement.variables.alpha_wolf_min_remains == 0)) then
        if FS.api.cast(FS.enhancement.spells.crash_lightning, FS.state.target, "crash_lightning aoe_totemic 14") then
            return true
        end
    end
    if FS.enhancement.spells.sundering:is_castable() and (FS.state.player:buff_up(FS.enhancement.auras.doom_winds) or FS.enhancement.talents.earthsurge:is_learned() and (FS.state.player:buff_up(FS.enhancement.auras.legacy_of_the_frost_witch) or not FS.enhancement.talents.legacy_of_the_frost_witch:is_learned())) then
        if FS.api.cast(FS.enhancement.spells.sundering, FS.state.target, "sundering aoe_totemic 15") then
            return true
        end
    end
    if FS.enhancement.spells.fire_nova:is_castable() and (FS.enhancement.variables.flame_shock_count == 6 or (FS.enhancement.variables.flame_shock_count >= 4)) then -- and FS.enhancement.variables.flame_shock_count >= cycle_enemies)) then
        if FS.api.cast(FS.enhancement.spells.fire_nova, FS.state.target, "fire_nova aoe_totemic 16") then
            return true
        end
    end
    if FS.enhancement.spells.flame_shock:is_castable() and (FS.state.player:buff_up(FS.enhancement.auras.voltaic_blaze)) then
        if FS.api.cast(FS.enhancement.spells.flame_shock, FS.state.target, "flame_shock aoe_totemic 17") then
            return true
        end
    end
    if FS.enhancement.spells.lava_lash:is_castable() and (FS.enhancement.talents.lashing_flames:is_learned()) then
        if FS.api.cast(FS.enhancement.spells.lava_lash, FS.state.target, "lava_lash aoe_totemic 18") then
            return true
        end
    end
    if FS.enhancement.spells.lava_lash:is_castable() and (FS.enhancement.talents.molten_assault:is_learned() and FS.state.target:debuff_up(FS.enhancement.auras.flame_shock)) then
        if FS.api.cast(FS.enhancement.spells.lava_lash, FS.state.target, "lava_lash aoe_totemic 19") then
            return true
        end
    end
    if FS.enhancement.spells.ice_strike:is_castable() and (FS.enhancement.talents.hailstorm:is_learned() and not FS.state.player:buff_up(FS.enhancement.auras.ice_strike)) then
        if FS.api.cast(FS.enhancement.spells.ice_strike, FS.state.target, "ice_strike aoe_totemic 20") then
            return true
        end
    end
    if FS.enhancement.spells.frost_shock:is_castable() and (FS.enhancement.talents.hailstorm:is_learned() and FS.state.player:buff_up(FS.enhancement.auras.hailstorm)) then
        if FS.api.cast(FS.enhancement.spells.frost_shock, FS.state.target, "frost_shock aoe_totemic 21") then
            return true
        end
    end
    if FS.enhancement.spells.sundering:is_castable() and ((FS.state.player:buff_up(FS.enhancement.auras.legacy_of_the_frost_witch) or not FS.enhancement.talents.legacy_of_the_frost_witch:is_learned())) then
        if FS.api.cast(FS.enhancement.spells.sundering, FS.state.target, "sundering aoe_totemic 22") then
            return true
        end
    end
    if FS.enhancement.spells.flame_shock:is_castable() and (FS.enhancement.talents.molten_assault:is_learned()) then -- and not ticking) then
        if FS.api.cast(FS.enhancement.spells.flame_shock, FS.state.target, "flame_shock aoe_totemic 23") then
            return true
        end
    end
    if FS.enhancement.spells.flame_shock:is_castable() and ( --[[refreshable and--]] (FS.enhancement.talents.fire_nova:is_learned() or FS.enhancement.talents.primordial_wave:is_learned()) and (FS.enhancement.variables.flame_shock_count < #FS.state.active_enemies) and FS.enhancement.variables.flame_shock_count < 6) then
        if FS.api.cast(FS.enhancement.spells.flame_shock, FS.state.target, "flame_shock aoe_totemic 24") then
            return true
        end
    end
    if FS.enhancement.spells.fire_nova:is_castable() and (FS.enhancement.variables.flame_shock_count >= 3) then
        if FS.api.cast(FS.enhancement.spells.fire_nova, FS.state.target, "fire_nova aoe_totemic 25") then
            return true
        end
    end
    if FS.enhancement.spells.stormstrike:is_castable() and (FS.state.player:buff_up(FS.enhancement.auras.crash_lightning) and (FS.enhancement.talents.deeply_rooted_elements:is_learned() or FS.state.player:buff_stack(FS.enhancement.auras.converging_storms) == FS.enhancement.auaras.converging_storms.max_stack)) then
        if FS.api.cast(FS.enhancement.spells.stormstrike, FS.state.target, "stormstrike aoe_totemic 26") then
            return true
        end
    end
    if FS.enhancement.spells.crash_lightning:is_castable() and (FS.enhancement.talents.crashing_storms:is_learned() and FS.state.player:buff_up(FS.enhancement.auras.cl_crash_lightning) and #FS.state.active_enemies >= 4) then
        if FS.api.cast(FS.enhancement.spells.crash_lightning, FS.state.target, "crash_lightning aoe_totemic 27") then
            return true
        end
    end
    if FS.enhancement.spells.windstrike:is_castable() then
        if FS.api.cast(FS.enhancement.spells.windstrike, FS.state.target, "windstrike aoe_totemic 28") then
            return true
        end
    end
    if FS.enhancement.spells.stormstrike:is_castable() then
        if FS.api.cast(FS.enhancement.spells.stormstrike, FS.state.target, "stormstrike aoe_totemic 29") then
            return true
        end
    end
    if FS.enhancement.spells.ice_strike:is_castable() then
        if FS.api.cast(FS.enhancement.spells.ice_strike, FS.state.target, "ice_strike aoe_totemic 30") then
            return true
        end
    end
    if FS.enhancement.spells.lava_lash:is_castable() then
        if FS.api.cast(FS.enhancement.spells.lava_lash, FS.state.target, "lava_lash aoe_totemic 31") then
            return true
        end
    end
    if FS.enhancement.spells.crash_lightning:is_castable() then
        if FS.api.cast(FS.enhancement.spells.crash_lightning, FS.state.target, "crash_lightning aoe_totemic 32") then
            return true
        end
    end
    if FS.enhancement.spells.fire_nova:is_castable() and (FS.enhancement.variables.flame_shock_count >= 2) then
        if FS.api.cast(FS.enhancement.spells.fire_nova, FS.state.target, "fire_nova aoe_totemic 33") then
            return true
        end
    end
    if FS.enhancement.spells.elemental_blast:is_castable() and ((not FS.enhancement.talents.elemental_spirits:is_learned() or (FS.enhancement.talents.elemental_spirits:is_learned() and (FS.enhancement.spells.elemental_blast:charges() == FS.enhancement.spells.elemental_blast:max_charges() or FS.enhancement.variables.feral_spirit_count >= 2))) and FS.state.player:buff_stack(FS.enhancement.auras.maelstrom_weapon) >= 5 and (not FS.enhancement.talents.crashing_storms:is_learned() or #FS.state.active_enemies <= 3)) then
        if FS.api.cast(FS.enhancement.spells.elemental_blast, FS.state.target, "elemental_blast aoe_totemic 34") then
            return true
        end
    end
    if FS.enhancement.spells.chain_lightning:is_castable() and (FS.state.player:buff_stack(FS.enhancement.auras.maelstrom_weapon) >= 5) then
        if FS.api.cast(FS.enhancement.spells.chain_lightning, FS.state.target, "chain_lightning aoe_totemic 35") then
            return true
        end
    end
    if FS.enhancement.spells.flame_shock:is_castable() then -- and (not ticking) then
        if FS.api.cast(FS.enhancement.spells.flame_shock, FS.state.target, "flame_shock aoe_totemic 36") then
            return true
        end
    end

    return false
end

return Aoe_totemic
