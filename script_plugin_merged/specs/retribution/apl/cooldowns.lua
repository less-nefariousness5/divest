-- Retribution Paladin Cooldowns
local APL = require("core/apl")
local State = require("core/state")
local S = require("specs/retribution/ids")

local function Cooldowns()
    local Ret = FS.Retribution

    -- shield_of_vengeance,if=fight_remains>15&(!talent.execution_sentence|!debuff.execution_sentence.up)
    if S.ShieldOfVengeance:is_castable() and
        (Ret.variables.fight_remains > 15 and
            (not S.ExecutionSentence:is_available() or State.target:debuff_down(S.ExecutionSentenceDebuff))) then
        if APL.cast(S.ShieldOfVengeance, nil, State, "shield_of_vengeance cooldowns 2") then return true end
    end

    -- execution_sentence,if=(!buff.crusade.up&cooldown.crusade.remains>15|buff.crusade.stack=10|cooldown.avenging_wrath.remains<0.75|cooldown.avenging_wrath.remains>15|talent.radiant_glory)&(holy_power>=4&time<5|holy_power>=3&time>5|holy_power>=2&(talent.divine_auxiliary|talent.radiant_glory))&(target.time_to_die>8&!talent.executioners_will|target.time_to_die>12)&cooldown.wake_of_ashes.remains<gcd
    if S.ExecutionSentence:is_castable() and
        ((State.player:buff_down(S.CrusadeBuff) and S.Crusade:cooldown_remains() > 15 or
                State.player:buff_stack(S.CrusadeBuff) == 10 or
                S.AvengingWrath:cooldown_remains() < 0.75 or
                S.AvengingWrath:cooldown_remains() > 15 or
                S.RadiantGlory:is_available()) and
            (Ret.variables.holy_power >= 4 and Ret.variables.combat_time < 5 or
                Ret.variables.holy_power >= 3 and Ret.variables.combat_time > 5 or
                Ret.variables.holy_power >= 2 and (S.DivineAuxiliary:is_available() or S.RadiantGlory:is_available())) and
            (State.target:time_to_die() > 8 and not S.ExecutionersWill:is_available() or State.target:time_to_die() > 12) and
            S.WakeOfAshes:cooldown_remains() <= State.player:gcd()) then
        if APL.cast(S.ExecutionSentence, State.target, State, "execution_sentence cooldowns 4") then return true end
    end

    -- avenging_wrath,if=(holy_power>=4&time<5|holy_power>=3&time>5|holy_power>=2&talent.divine_auxiliary&(cooldown.execution_sentence.remains=0|cooldown.final_reckoning.remains=0))&(!raid_event.adds.up|target.time_to_die>10)
    if S.AvengingWrath:is_castable() and
        ((Ret.variables.holy_power >= 4 and Ret.variables.combat_time < 5 or
                Ret.variables.holy_power >= 3 and Ret.variables.combat_time > 5 or
                Ret.variables.holy_power >= 2 and S.DivineAuxiliary:is_available() and
                (S.ExecutionSentence:cooldown_up() or S.FinalReckoning:cooldown_up())) and
            (Ret.variables.enemies_8y_count == 1 or State.target:time_to_die() > 10)) then
        if APL.cast(S.AvengingWrath, nil, State, "avenging_wrath cooldowns 6") then return true end
    end

    -- crusade,if=holy_power>=5&time<5|holy_power>=3&time>5
    if S.Crusade:is_castable() and
        (Ret.variables.holy_power >= 5 and Ret.variables.combat_time < 5 or
            Ret.variables.holy_power >= 3 and Ret.variables.combat_time >= 5) then
        if APL.cast(S.Crusade, nil, State, "crusade cooldowns 8") then return true end
    end

    -- final_reckoning,if=(holy_power>=4&time<8|holy_power>=3&time>=8|holy_power>=2&(talent.divine_auxiliary|talent.radiant_glory))&(cooldown.avenging_wrath.remains>10|cooldown.crusade.remains&(!buff.crusade.up|buff.crusade.stack>=10)|talent.radiant_glory&(buff.avenging_wrath.up|talent.crusade&cooldown.wake_of_ashes.remains<gcd))
    if S.FinalReckoning:is_castable() and
        ((Ret.variables.holy_power >= 4 and Ret.variables.combat_time < 8 or
                Ret.variables.holy_power >= 3 and Ret.variables.combat_time >= 8 or
                Ret.variables.holy_power >= 2 and (S.DivineAuxiliary:is_available() or S.RadiantGlory:is_available())) and
            (S.AvengingWrath:cooldown_remains() > 10 or
                S.Crusade:cooldown_down() and (State.player:buff_down(S.CrusadeBuff) or State.player:buff_stack(S.CrusadeBuff) >= 10) or
                S.RadiantGlory:is_available() and (State.player:buff_up(S.AvengingWrathBuff) or
                    S.Crusade:is_available() and S.WakeOfAshes:cooldown_remains() <= State.player:gcd()))) then
        if APL.cast(S.FinalReckoning, State.target, State, "final_reckoning cooldowns 10") then return true end
    end

    return false
end

return Cooldowns
