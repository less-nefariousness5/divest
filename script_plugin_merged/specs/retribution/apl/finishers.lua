-- Retribution Paladin Finishers
local APL = require("core/apl")
local State = require("core/state")
local S = require("specs/retribution/ids")

local function Finishers()
    local Ret = FS.Retribution

    -- variable,name=ds_castable,value=(spell_targets.divine_storm>=2|buff.empyrean_power.up|!talent.final_verdict&talent.tempest_of_the_lightbringer)&!buff.empyrean_legacy.up&!(buff.divine_arbiter.up&buff.divine_arbiter.stack>24)
    VarDSCastable =
        (Ret.variables.enemies_8y_count >= 2
            or State.player:buff_up(S.EmpyreanPowerBuff)
            or not S.FinalVerdict:is_available()
            and S.TempestOfTheLightbringer:is_available())
        and State.player:buff_down(S.EmpyreanLegacyBuff)
        and
        not (State.player:buff_up(S.DivineArbiterBuff) and State.player:buff_stack(S.DivineArbiterBuff) > 24)
    -- hammer_of_light
    if S.HammerOfLight:is_ready() then
        if APL.cast(S.HammerOfLight, State.target, State, "hammer_of_light finishers 2") then
            return true
        end
    end
    -- divine_hammer,if=holy_power=5
    if S.DivineHammer:is_castable() and (Ret.variables.holy_power == 5) then
        if APL.cast(S.DivineHammer, State.target, State, "divine_hammer finishers 4") then
            return true
        end
    end
    -- divine_storm,if=variable.ds_castable&!buff.hammer_of_light_ready.up&(!talent.crusade|cooldown.crusade.remains>gcd*3|buff.crusade.up&buff.crusade.stack<10|talent.radiant_glory)&(!buff.divine_hammer.up|cooldown.divine_hammer.remains>110&holy_power>=4)
    if S.DivineStorm:is_ready() and (VarDSCastable and not S.HammerOfLight:is_ready() and (false or not S.Crusade:is_available() or S.Crusade:cooldown_remains() >= State.player:gcd() * 3 or State.player:buff_up(S.CrusadeBuff) and State.player:buff_stack(S.CrusadeBuff) < 10 or S.RadiantGlory:is_available()) and (not Ret.variables.divine_hammer_active or S.DivineHammer:cooldown_remains() > 110 and Ret.variables.holy_power >= 4)) then
        if APL.cast(S.DivineStorm, State.target, State, "divine_storm finishers 6") then
            return true
        end
    end
    -- justicars_vengeance,if=(!talent.crusade|cooldown.crusade.remains>gcd*3|buff.crusade.up&buff.crusade.stack<10|talent.radiant_glory)&!buff.hammer_of_light_ready.up&(!buff.divine_hammer.up|cooldown.divine_hammer.remains>110&holy_power>=4)
    if S.JusticarsVengeance:is_ready() and ((false or not S.Crusade:is_available() or S.Crusade:cooldown_remains() >= State.player:gcd() * 3 or State.player:buff_up(S.CrusadeBuff) and State.player:buff_stack(S.CrusadeBuff) < 10 or S.RadiantGlory:is_available()) and not S.HammerOfLight:is_ready() and (not Ret.variables.divine_hammer_active or S.DivineHammer:cooldown_remains() > 110 and Ret.variables.holy_power >= 4)) then
        if APL.cast(S.JusticarsVengeance, State.target, State, "justicars_vengeance finishers 8") then
            return true
        end
    end
    -- templars_verdict,if=(!talent.crusade|cooldown.crusade.remains>gcd*3|buff.crusade.up&buff.crusade.stack<10|talent.radiant_glory)&!buff.hammer_of_light_ready.up&(!buff.divine_hammer.up|cooldown.divine_hammer.remains>110&holy_power>=4)
    if Ret.variables.verdict_spell:is_ready() and ((false or not S.Crusade:is_available() or S.Crusade:cooldown_remains() >= State.player:gcd() * 3 or State.player:buff_up(S.CrusadeBuff) and State.player:buff_stack(S.CrusadeBuff) < 10 or S.RadiantGlory:is_available()) and not S.HammerOfLight:is_ready() and (not Ret.variables.divine_hammer_active or S.DivineHammer:cooldown_remains() > 110 and Ret.variables.holy_power >= 4)) then
        if APL.cast(Ret.variables.verdict_spell, State.target, State, "either verdict finishers 10") then
            return true
        end
    end

    return false
end

return Finishers
