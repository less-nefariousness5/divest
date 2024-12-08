function FS.retribution.cooldowns()
    if FS.retribution.spells.lights_judgment:is_castable() and (FS.retribution.spells.lights_judgment:targets() >= 2) then
        if FS.api.cast(FS.retribution.spells.lights_judgment, FS.state.target, "lights_judgment cooldowns 1") then
            return true
        end
    end
    --if FS.retribution.spells.fireblood:is_castable() and (FS.state.player:buff_up(FS.retribution.spells.avenging_wrath) or FS.state.player:buff_up(FS.retribution.spells.crusade) and FS.state.player:buff_stack(FS.retribution.spells.crusade) == 10 or FS.state.player:debuff_up(FS.retribution.spells.execution_sentence)) then
    --    if FS.api.cast(FS.retribution.spells.fireblood,FS.state.target, "fireblood cooldowns 2") then
    --        return true
    --    end
    --end
    if FS.retribution.spells.shield_of_vengeance:is_castable() and (FS.api:fight_remains() > 15 and (not FS.retribution.spells.execution_sentence:is_learned() or not FS.state.player:debuff_up(FS.retribution.auras.execution_sentence))) then
        if FS.api.cast(FS.retribution.spells.shield_of_vengeance, FS.state.target, "shield_of_vengeance cooldowns 3") then
            return true
        end
    end
    if FS.retribution.spells.execution_sentence:is_castable() and ((not FS.state.player:buff_up(FS.retribution.auras.crusade) and FS.retribution.spells.crusade:cooldown_remaining() > 15 or FS.state.player:buff_stack(FS.retribution.auras.crusade) == 10 or FS.retribution.spells.avenging_wrath:cooldown_remaining() < 0.75 or FS.retribution.spells.avenging_wrath:cooldown_remaining() > 15 or FS.retribution.talents.radiant_glory:is_learned()) and (FS.retribution.variables.holy_power >= 4 and FS.state.combat_time < 5 or FS.retribution.variables.holy_power >= 3 and FS.state.combat_time > 5 or FS.retribution.variables.holy_power >= 2 and (FS.retribution.talents.divine_auxiliary:is_learned() or FS.retribution.talents.radiant_glory:is_learned())) and (FS.state.target:time_to_die() > 8 and not FS.retribution.talents.executioners_will:is_learned() or FS.state.target:time_to_die() > 12) and FS.retribution.spells.wake_of_ashes:cooldown_remaining() < FS.state.player:gcd()) then
        if FS.api.cast(FS.retribution.spells.execution_sentence, FS.state.target, "execution_sentence cooldowns 4") then
            return true
        end
    end
    if FS.retribution.spells.avenging_wrath:is_castable() and ((FS.retribution.variables.holy_power >= 4 and FS.state.combat_time < 5 or FS.retribution.variables.holy_power >= 3 and FS.state.combat_time > 5 or FS.retribution.variables.holy_power >= 2 and FS.retribution.talents.divine_auxiliary:is_learned() and (FS.retribution.spells.execution_sentence:cooldown_remaining() == 0 or FS.retribution.spells.final_reckoning:cooldown_remaining() == 0)) and (FS.state.target:time_to_die() > 10)) then
        if FS.api.cast(FS.retribution.spells.avenging_wrath, FS.state.target, "avenging_wrath cooldowns 5") then
            return true
        end
    end
    if FS.retribution.spells.crusade:is_castable() and (FS.retribution.variables.holy_power >= 5 and FS.state.combat_time < 5 or FS.retribution.variables.holy_power >= 3 and FS.state.combat_time > 5) then
        if FS.api.cast(FS.retribution.spells.crusade, FS.state.target, "crusade cooldowns 6") then
            return true
        end
    end
    if FS.retribution.spells.final_reckoning:is_castable() and ((FS.retribution.variables.holy_power >= 4 and FS.state.combat_time < 8 or FS.retribution.variables.holy_power >= 3 and FS.state.combat_time >= 8 or FS.retribution.variables.holy_power >= 2 and (FS.retribution.talents.divine_auxiliary:is_learned() or FS.retribution.talents.radiant_glory:is_learned())) and (FS.retribution.spells.avenging_wrath:cooldown_remaining() > 10 or FS.retribution.spells.crusade:cooldown_remaining() and (not FS.state.player:buff_up(FS.retribution.auras.crusade) or FS.state.player:buff_stack(FS.retribution.auras.crusade) >= 10) or FS.retribution.talents.radiant_glory:is_learned() and (FS.state.player:buff_up(FS.retribution.auras.avenging_wrath) or FS.retribution.spells.crusade:is_learned() and FS.retribution.spells.wake_of_ashes:cooldown_remaining() < FS.state.player:gcd()))) then
        if FS.api.cast(FS.retribution.spells.final_reckoning, FS.state.target, "final_reckoning cooldowns 7") then
            return true
        end
    end

    return false
end
