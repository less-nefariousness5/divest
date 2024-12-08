function FS.retribution.finishers()
    if FS.retribution.spells.hammer_of_light:is_castable() then
        if FS.api.cast(FS.retribution.spells.hammer_of_light, FS.state.target, "hammer_of_light finishers 2") then
            return true
        end
    end

    if FS.retribution.spells.divine_hammer:is_castable() and (FS.retribution.variables.holy_power == 5) then
        if FS.api.cast(FS.retribution.spells.divine_hammer, FS.state.target, "divine_hammer finishers 3") then
            return true
        end
    end

    FS.retribution.variables.ds_castable =
        (FS.retribution.spells.divine_storm:targets() >= 2
            or FS.state.player:buff_up(FS.retribution.auras.empyrean_power)
            or not FS.retribution.talents.final_verdict:enabled()
            and FS.retribution.talents.tempest_of_the_lightbringer:enabled())
        and not FS.state.player:buff_up(FS.retribution.auras.empyrean_legacy)
        and
        not (FS.state.player:buff_up(FS.retribution.auras.divine_arbiter) and FS.state.player:buff_stack(FS.retribution.auras.divine_arbiter) > 24)


    if FS.retribution.spells.divine_storm:is_castable()
        and not FS.retribution.spells.hammer_of_light:is_castable()
        and (
            FS.retribution.variables.ds_castable
            and (
                not FS.retribution.talents.crusade:enabled()
                or FS.retribution.spells.crusade:cooldown_remaining() > FS.state.player:gcd() * 3
                or FS.state.player:buff_up(FS.retribution.auras.crusade)
                and FS.state.player:buff_stack(FS.retribution.auras.crusade) < 10
                or FS.retribution.talents.radiant_glory:enabled()
            )
            and (
                not FS.state.player:buff_up(FS.retribution.auras.divine_hammer)
                or FS.retribution.spells.divine_hammer:cooldown_remaining() > 110
                and FS.retribution.variables.holy_power >= 4
            )
        ) then
        if FS.api.cast(FS.retribution.spells.divine_storm, FS.state.target, "divine_storm finishers 4") then
            return true
        end
    end
    if FS.retribution.spells.justicars_vengeance:is_castable() and ((not FS.retribution.spells.crusade:is_learned() or FS.retribution.spells.crusade:cooldown_remaining() > FS.state.player:gcd() * 3 or FS.state.player:buff_up(FS.retribution.spells.crusade) and FS.state.player:buff_stack(FS.retribution.spells.crusade) < 10 or FS.retribution.talents.radiant_glory:is_learned()) and not FS.state.player:buff_up(FS.retribution.auras.hammer_of_light_ready) and (not FS.state.player:buff_up(FS.retribution.spells.divine_hammer) or FS.retribution.spells.divine_hammer:cooldown_remaining() > 110 and FS.retribution.variables.holy_power >= 4)) then
        if FS.api.cast(FS.retribution.spells.justicars_vengeance, FS.state.target, "justicars_vengeance finishers 5") then
            return true
        end
    end
    if FS.retribution.spells.templars_verdict:is_castable() and ((not FS.retribution.spells.crusade:is_learned() or FS.retribution.spells.crusade:cooldown_remaining() > FS.state.player:gcd() * 3 or FS.state.player:buff_up(FS.retribution.spells.crusade) and FS.state.player:buff_stack(FS.retribution.auras.crusade) < 10 or FS.retribution.talents.radiant_glory:is_learned()) and not FS.state.player:buff_up(FS.retribution.auras.hammer_of_light_ready) and (not FS.state.player:buff_up(FS.retribution.spells.divine_hammer) or FS.retribution.spells.divine_hammer:cooldown_remaining() > 110 and FS.retribution.variables.holy_power >= 4)) then
        if FS.api.cast(FS.retribution.spells.templars_verdict, FS.state.target, "templars_verdict finishers 6") then
            return true
        end
    end

    FS.retribution.variables.finished = true

    return false
end
