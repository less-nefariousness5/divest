function FS.retribution.generators()
    if FS.retribution.spells.hammer_of_light:is_castable() then
        if FS.api.cast(FS.retribution.spells.hammer_of_light, FS.state.target, "hammer_of_light generators 1") then
            return true
        end
    end
    FS.retribution.variables.finished = false
    if (FS.retribution.variables.holy_power == 5 or FS.retribution.variables.holy_power == 4 and FS.state.player:buff_up(FS.retribution.auras.divine_resonance)) and FS.retribution.finishers() then return true end
    if FS.retribution.spells.templar_slash:is_castable() and (FS.state.player:buff_remains(FS.retribution.auras.templar_strikes) < FS.state.player:gcd() * 2) then
        if FS.api.cast(FS.retribution.spells.templar_slash, FS.state.target, "templar_slash generators 3") then
            return true
        end
    end
    if FS.retribution.spells.blade_of_justice:is_castable() and (not FS.state.target:debuff_up(FS.retribution.auras.expurgation) and FS.retribution.talents.holy_flames:is_learned()) then
        if FS.api.cast(FS.retribution.spells.blade_of_justice, FS.state.target, "blade_of_justice generators 4") then
            return true
        end
    end
    if FS.retribution.spells.wake_of_ashes:is_castable() and ((not FS.retribution.talents.lights_guidance:is_learned() or FS.retribution.variables.holy_power >= 2 and FS.retribution.talents.lights_guidance:is_learned()) and (FS.retribution.spells.avenging_wrath:cooldown_remaining() > 6 or FS.retribution.spells.crusade:cooldown_remaining() > 6 or FS.retribution.talents.radiant_glory:is_learned()) and (not FS.retribution.spells.execution_sentence:is_learned() or FS.retribution.spells.execution_sentence:cooldown_remaining() > 4 or FS.state.target:time_to_die() < 8)) then
        if FS.api.cast(FS.retribution.spells.wake_of_ashes, FS.state.target, "wake_of_ashes generators 5") then
            return true
        end
    end
    if FS.retribution.spells.divine_toll:is_castable() and (FS.retribution.variables.holy_power <= 2 and (FS.retribution.spells.avenging_wrath:cooldown_remaining() > 15 or FS.retribution.spells.crusade:cooldown_remaining() > 15 or FS.retribution.talents.radiant_glory:is_learned() or FS.api:fight_remains() < 8)) then
        if FS.api.cast(FS.retribution.spells.divine_toll, FS.state.target, "divine_toll generators 6") then
            return true
        end
    end
    if FS.retribution.finishers() then return true end
    if FS.retribution.spells.templar_slash:is_castable() and (FS.state.player:buff_remains(FS.retribution.auras.templar_strikes) < FS.state.player:gcd() and FS.retribution.spells.divine_storm:targets() >= 2) then
        if FS.api.cast(FS.retribution.spells.templar_slash, FS.state.target, "templar_slash generators 7") then
            return true
        end
    end
    if FS.retribution.spells.blade_of_justice:is_castable() and ((FS.retribution.variables.holy_power <= 3 or not FS.retribution.talents.holy_blade:is_learned()) and (FS.retribution.spells.divine_storm:targets() >= 2 and FS.retribution.talents.blade_of_vengeance:is_learned())) then
        if FS.api.cast(FS.retribution.spells.blade_of_justice, FS.state.target, "blade_of_justice generators 8") then
            return true
        end
    end
    if FS.retribution.spells.hammer_of_wrath:is_castable() and ((FS.retribution.spells.divine_storm:targets() < 2 or not FS.retribution.talents.blessed_champion:is_learned()) and (FS.retribution.variables.holy_power <= 3 or FS.state.target:health_percentage() >= (20 / 100) or not FS.retribution.talents.vanguards_momentum:is_learned()) and (FS.state.target:health_percentage() <= (35 / 100) and FS.retribution.talents.vengeful_wrath:is_learned() or FS.state.player:buff_up(FS.retribution.auras.blessing_of_anshe))) then
        if FS.api.cast(FS.retribution.spells.hammer_of_wrath, FS.state.target, "hammer_of_wrath generators 9") then
            return true
        end
    end
    if FS.retribution.spells.templar_strike:is_castable() then
        if FS.api.cast(FS.retribution.spells.templar_strike, FS.state.target, "templar_strike generators 10") then
            return true
        end
    end
    if FS.retribution.spells.judgment:is_castable() and (FS.retribution.variables.holy_power <= 3 or not FS.retribution.talents.boundless_judgment:is_learned()) then
        if FS.api.cast(FS.retribution.spells.judgment, FS.state.target, "judgment generators 11") then
            return true
        end
    end
    if FS.retribution.spells.blade_of_justice:is_castable() and (FS.retribution.variables.holy_power <= 3 or not FS.retribution.talents.holy_blade:is_learned()) then
        if FS.api.cast(FS.retribution.spells.blade_of_justice, FS.state.target, "blade_of_justice generators 12") then
            return true
        end
    end
    if FS.retribution.spells.hammer_of_wrath:is_castable() and ((FS.retribution.spells.divine_storm:targets() < 2 or not FS.retribution.talents.blessed_champion:is_learned()) and (FS.retribution.variables.holy_power <= 3 or FS.state.target:health_percentage() >= (20 / 100) or not FS.retribution.talents.vanguards_momentum:is_learned())) then
        if FS.api.cast(FS.retribution.spells.hammer_of_wrath, FS.state.target, "hammer_of_wrath generators 13") then
            return true
        end
    end
    if FS.retribution.spells.templar_slash:is_castable() then
        if FS.api.cast(FS.retribution.spells.templar_slash, FS.state.target, "templar_slash generators 14") then
            return true
        end
    end
    if ((FS.state.target:health_percentage() <= (20 / 100) or FS.state.player:buff_up(FS.retribution.auras.avenging_wrath) or FS.state.player:buff_up(FS.retribution.auras.crusade) or FS.state.player:buff_up(FS.retribution.auras.empyrean_power)) and not FS.retribution.variables.finished) and FS.retribution.finishers() then return true end
    if FS.retribution.spells.crusader_strike:is_castable() and (FS.retribution.auras.crusader_strike:charges_fractional() >= 1.75 and (FS.retribution.variables.holy_power <= 2 or FS.retribution.variables.holy_power <= 3 and FS.retribution.spells.blade_of_justice:cooldown_remaining() > FS.state.player:gcd() * 2 or FS.retribution.variables.holy_power == 4 and FS.retribution.spells.blade_of_justice:cooldown_remaining() > FS.state.player:gcd() * 2 and FS.retribution.spells.judgment:cooldown_remaining() > FS.state.player:gcd() * 2)) then
        if FS.api.cast(FS.retribution.spells.crusader_strike, FS.state.target, "crusader_strike generators 15") then
            return true
        end
    end
    if not FS.retribution.variables.finished and FS.retribution.finishers() then return true end
    if FS.retribution.spells.hammer_of_wrath:is_castable() and (FS.retribution.variables.holy_power <= 3 or FS.state.target:health_percentage() >= (20 / 100) or not FS.retribution.talents.vanguards_momentum:is_learned()) then
        if FS.api.cast(FS.retribution.spells.hammer_of_wrath, FS.state.target, "hammer_of_wrath generators 16") then
            return true
        end
    end
    if FS.retribution.spells.crusader_strike:is_castable() then
        if FS.api.cast(FS.retribution.spells.crusader_strike, FS.state.target, "crusader_strike generators 17") then
            return true
        end
    end
    --if FS.retribution.spells.arcane_torrent:is_castable() then
    --    if FS.api.cast(FS.retribution.spells.arcane_torrent, FS.state.target, "arcane_torrent generators 18") then
    --        return true
    --    end
    --end

    return false
end
