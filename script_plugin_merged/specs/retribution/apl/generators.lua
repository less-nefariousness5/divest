-- Retribution Paladin Generators
local APL = require("core/apl")
local State = require("core/state")
local Finishers = require("specs/retribution/apl/finishers")
local S = require("specs/retribution/ids")

local function TemplarStrikesRemains()
    local Remains = 5 - S.TemplarStrike:time_since_last_cast()
    if S.TemplarSlash:time_since_last_cast() < S.TemplarStrike:time_since_last_cast() then
        Remains = 0
    end
    return Remains > 0 and Remains or 0
end

local function Generators()
    local Ret = FS.Retribution


    -- call_action_list,name=finishers,if=holy_power=5|holy_power=4&buff.divine_resonance.up
    if Ret.variables.holy_power == 5 or Ret.variables.holy_power == 4 and State.player:buff_up(S.DivineResonanceBuff) then
        local ShouldReturn = Finishers(); if ShouldReturn then return ShouldReturn; end
    end
    -- templar_slash,if=buff.templar_strikes.remains<gcd*2
    if S.TemplarSlash:is_ready() and (TemplarStrikesRemains() <= State.player:gcd() * 2) then
        if APL.cast(S.TemplarSlash, State.target, State, "templar_slash generators 2") then
            return true
        end
    end
    -- blade_of_justice,if=!dot.expurgation.ticking&talent.holy_flames
    if S.BladeOfJustice:is_castable() and (State.target:debuff_down(S.ExpurgationDebuff) and S.HolyFlames:is_available()) then
        if APL.cast(S.BladeOfJustice, State.target, State, "blade_of_justice generators 4") then
            return true
        end
    end
    -- wake_of_ashes,if=(!talent.lights_guidance|holy_power>=2&talent.lights_guidance)&(cooldown.avenging_wrath.remains>6|cooldown.crusade.remains>6|talent.radiant_glory)&(!talent.execution_sentence|cooldown.execution_sentence.remains>4|target.time_to_die<8)&(!raid_event.adds.exists|raid_event.adds.in>10|raid_event.adds.up)
    if S.WakeOfAshes:is_castable() and ((not S.LightsGuidance:is_available() or Ret.variables.holy_power >= 2 and S.LightsGuidance:is_available()) and (false or S.AvengingWrath:cooldown_remains() > 6 or S.Crusade:cooldown_remains() > 6 or S.RadiantGlory:is_available()) and (not S.ExecutionSentence:is_available() or S.ExecutionSentence:cooldown_remains() > 4 or Ret.variables.fight_remains < 8)) then
        if APL.cast(S.WakeOfAshes, State.target, State, "wake_of_ashes generators 6") then
            return true
        end
    end
    -- divine_toll,if=holy_power<=2&(!raid_event.adds.exists|raid_event.adds.in>10|raid_event.adds.up)&(cooldown.avenging_wrath.remains>15|cooldown.crusade.remains>15|talent.radiant_glory|fight_remains<8)
    if S.DivineToll:is_castable() and (Ret.variables.holy_power <= 2 and (false or S.AvengingWrath:cooldown_remains() > 15 or S.Crusade:cooldown_remains() > 15 or S.RadiantGlory:is_available() or Ret.variables.boss_fight_remains < 8)) then
        if APL.cast(S.DivineToll, State.target, State, "divine_toll generators 8") then
            return true
        end
    end
    -- call_action_list,name=finishers,if=holy_power>=3&buff.crusade.up&buff.crusade.stack<10
    if Ret.variables.holy_power >= 3 and State.player:buff_up(S.CrusadeBuff) and State.player:buff_stack(S.CrusadeBuff) < 10 then
        local ShouldReturn = Finishers(); if ShouldReturn then return ShouldReturn; end
    end
    -- templar_slash,if=buff.templar_strikes.remains<gcd&spell_targets.divine_storm>=2
    if S.TemplarSlash:is_ready() and (TemplarStrikesRemains() <= State.player:gcd() and Ret.variables.enemies_8y_count >= 2) then
        if APL.cast(S.TemplarSlash, State.target, State, "templar_slash generators 10") then
            return true
        end
    end
    -- blade_of_justice,if=(holy_power<=3|!talent.holy_blade)&(spell_targets.divine_storm>=2&talent.blade_of_vengeance)
    if S.BladeOfJustice:is_castable() and ((Ret.variables.holy_power <= 3 or not S.HolyBlade:is_available()) and (Ret.variables.enemies_8y_count >= 2 and S.BladeOfVengeance:is_available())) then
        if APL.cast(S.BladeOfJustice, State.target, State, "blade_of_justice generators 12") then
            return true
        end
    end
    -- hammer_of_wrath,if=(spell_targets.divine_storm<2|!talent.blessed_champion)&(holy_power<=3|target.health.pct>20|!talent.vanguards_momentum)&(target.health.pct<35&talent.vengeful_wrath|buff.blessing_of_anshe.up)
    if S.HammerOfWrath:is_ready() and ((Ret.variables.enemies_8y_count < 2 or not S.BlessedChampion:is_available()) and (Ret.variables.holy_power <= 3 or State.target:health_percentage() > 20 or not S.VanguardsMomentum:is_available()) and (State.target:health_percentage() < 35 and S.VengefulWrath:is_available() or State.player:buff_up(S.BlessingOfAnsheRetBuff))) then
        if APL.cast(S.HammerOfWrath, State.target, State, "hammer_of_wrath generators 14") then
            return true
        end
    end
    -- templar_strike
    if S.TemplarStrike:is_castable() then
        if APL.cast(S.TemplarStrike, State.target, State, "templar_strike generators 16") then
            return true
        end
    end
    -- judgment,if=holy_power<=3|!talent.boundless_judgment
    if S.Judgment:is_castable() and (Ret.variables.holy_power <= 3 or not S.BoundlessJudgment:is_available()) then
        if APL.cast(S.Judgment, State.target, State, "judgment generators 18") then
            return true
        end
    end
    -- blade_of_justice,if=holy_power<=3|!talent.holy_blade
    if S.BladeOfJustice:is_castable() and (Ret.variables.holy_power <= 3 or not S.HolyBlade:is_available()) then
        if APL.cast(S.BladeOfJustice, State.target, State, "blade_of_justice generators 20") then
            return true
        end
    end
    -- hammer_of_wrath,if=(spell_targets.divine_storm<2|!talent.blessed_champion)&(holy_power<=3|target.health.pct>20|!talent.vanguards_momentum)
    if S.HammerOfWrath:is_ready() and ((Ret.variables.enemies_8y_count < 2 or not S.BlessedChampion:is_available()) and (Ret.variables.holy_power <= 3 or State.target:health_percentage() > 20 or not S.VanguardsMomentum:is_available())) then
        if APL.cast(S.HammerOfWrath, State.target, State, "hammer_of_wrath generators 22") then
            return true
        end
    end
    -- templar_slash
    if S.TemplarSlash:is_ready() then
        if APL.cast(S.TemplarSlash, State.target, State, "templar_slash generators 24") then
            return true
        end
    end
    -- call_action_list,name=finishers,if=(target.health.pct<=20|buff.avenging_wrath.up|buff.crusade.up|buff.empyrean_power.up)
    if State.target:health_percentage() <= 20 or State.player:buff_up(S.AvengingWrathBuff) or State.player:buff_up(S.CrusadeBuff) or State.player:buff_up(S.EmpyreanPowerBuff) then
        local ShouldReturn = Finishers(); if ShouldReturn then return ShouldReturn; end
    end
    -- crusader_strike,if=cooldown.crusader_strike.charges_fractional>=1.75&(holy_power<=2|holy_power<=3&cooldown.blade_of_justice.remains>gcd*2|holy_power=4&cooldown.blade_of_justice.remains>gcd*2&cooldown.judgment.remains>gcd*2)
    if S.CrusaderStrike:is_castable() and (S.CrusaderStrike:charges_fractional(6) >= 1.75 and (Ret.variables.holy_power <= 2 or Ret.variables.holy_power <= 3 and S.BladeOfJustice:cooldown_remains() >= State.player:gcd() * 2 or Ret.variables.holy_power == 4 and S.BladeOfJustice:cooldown_remains() >= State.player:gcd() * 2 and S.Judgment:cooldown_remains() >= State.player:gcd() * 2)) then
        if APL.cast(S.CrusaderStrike, State.target, State, "crusader_strike generators 26") then
            return true
        end
    end
    -- call_action_list,name=finishers
    local ShouldReturn = Finishers(); if ShouldReturn then return ShouldReturn; end
    -- hammer_of_wrath,if=holy_power<=3|target.health.pct>20|!talent.vanguards_momentum
    if S.HammerOfWrath:is_ready() and (Ret.variables.holy_power <= 3 or State.target:health_percentage() > 20 or not S.VanguardsMomentum:is_available()) then
        if APL.cast(S.HammerOfWrath, State.target, State, "hammer_of_wrath generators 28") then
            return true
        end
    end
    -- crusader_strike
    if S.CrusaderStrike:is_castable() then
        if APL.cast(S.CrusaderStrike, State.target, State, "crusader_strike generators 30") then
            return true
        end
    end
    -- arcane_torrent
    if S.ArcaneTorrent:is_castable() then
        if APL.cast(S.ArcaneTorrent, State.target, State, "arcane_torrent generators 32") then
            return true
        end
    end

    return false
end

return Generators
