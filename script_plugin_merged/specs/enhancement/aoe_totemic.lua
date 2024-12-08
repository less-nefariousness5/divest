-- AoE Totemic APL for Enhancement Shaman
local buff_manager = require("common/modules/buff_manager")
local spell_helper = require("common/utility/spell_helper")
local unit_helper = require("common/utility/unit_helper")

local S = FS.Enhancement.Spells
local Helpers = require("specs/enhancement/helpers")

local function AoeTotemic()
    local Enh = FS.Enhancement.Variables
    local State = FS.state

    -- surging_totem
    if S.SurgingTotem:IsReady() then
        if FS.APL.cast(S.SurgingTotem, nil, State, "surging_totem aoe_totemic 2") then return true end
    end

    -- ascendance,if=ti_chain_lightning
    if Helpers.CDsON() and S.Ascendance:IsCastable() and (Enh.ti_action == S.ChainLightning) then
        if FS.APL.cast(S.Ascendance, nil, State, "ascendance aoe_totemic 4") then return true end
    end

    -- sundering,if=buff.ascendance.up&pet.surging_totem.active&talent.earthsurge.enabled&(buff.legacy_of_the_frost_witch.up|!talent.legacy_of_the_frost_witch.enabled)
    if S.Sundering:IsReady() and (State.Player:buff_up(S.AscendanceBuff) and Helpers.TotemFinder(S.SurgingTotem) and S.Earthsurge:IsAvailable() and (State.Player:buff_up(S.LegacyoftheFrostWitchBuff) or not S.LegacyoftheFrostWitch:IsAvailable())) then
        if FS.APL.cast(S.Sundering, State.Target, State, "sundering aoe_totemic 6") then return true end
    end

    -- crash_lightning,if=talent.crashing_storms.enabled&(active_enemies>=15-5*talent.unruly_winds.enabled)
    if S.CrashLightning:IsReady() and (S.CrashingStorms:IsAvailable() and (Enh.enemies_melee_count >= 15 - 5 * FS.APL:num(S.UnrulyWinds:IsAvailable()))) then
        if FS.APL.cast(S.CrashLightning, State.Target, State, "crash_lightning aoe_totemic 8") then return true end
    end

    -- lightning_bolt,if=((active_dot.flame_shock=active_enemies|active_dot.flame_shock=6)&buff.primordial_wave.up&buff.maelstrom_weapon.stack=buff.maelstrom_weapon.max_stack&(!buff.splintered_elements.up|fight_remains<=12))
    if S.LightningBolt:IsCastable() and ((S.FlameShockDebuff:AuraActiveCount(State.Player) == Enh.enemies_melee_count or S.FlameShockDebuff:AuraActiveCount(State.Player) >= 6) and State.Player:buff_up(S.PrimordialWaveBuff) and Enh.maelstrom_stacks == Enh.max_maelstrom_stacks and (State.Player:BuffDown(S.SplinteredElementsBuff) or Enh.fight_remains <= 12)) then
        if FS.APL.cast(S.LightningBolt, State.Target, State, "lightning_bolt aoe_totemic 10") then return true end
    end

    -- doom_winds,if=!talent.elemental_spirits.enabled&(buff.legacy_of_the_frost_witch.up|!talent.legacy_of_the_frost_witch.enabled)
    if S.DoomWinds:IsCastable() and (not S.ElementalSpirits:IsAvailable() and (State.Player:buff_up(S.LegacyoftheFrostWitchBuff) or not S.LegacyoftheFrostWitch:IsAvailable())) then
        if FS.APL.cast(S.DoomWinds, State.Target, State, "doom_winds aoe_totemic 12") then return true end
    end

    -- lava_lash,if=talent.molten_assault.enabled&(talent.primordial_wave.enabled|talent.fire_nova.enabled)&dot.flame_shock.ticking&(active_dot.flame_shock<active_enemies)&active_dot.flame_shock<6
    if S.LavaLash:IsCastable() and (S.MoltenAssault:IsAvailable() and (S.PrimordialWave:IsAvailable() or S.FireNova:IsAvailable()) and State.Target:Debuff_up(S.FlameShockDebuff) and (S.FlameShockDebuff:AuraActiveCount(State.Player) < Enh.enemies_melee_count) and S.FlameShockDebuff:AuraActiveCount(State.Player) < 6) then
        if FS.APL.cast(S.LavaLash, State.Target, State, "lava_lash aoe_totemic 14") then return true end
    end

    -- primordial_wave,target_if=min:dot.flame_shock.remains,if=!buff.primordial_wave.up
    if S.PrimordialWave:IsReady() and (State.Player:BuffDown(S.PrimordialWaveBuff)) then
        if FS.APL.castTargetIf(true, S.PrimordialWave, Enh.enemies_melee, "min", Helpers.EvaluateTargetIfFilterPrimordialWave, Helpers.EvaluateTargetIfPrimordialWave, State, "primordial_wave aoe_totemic 16") then return true end
    end

    -- elemental_blast,if=(!talent.elemental_spirits.enabled|(talent.elemental_spirits.enabled&(charges=max_charges|feral_spirit.active>=2)))&buff.maelstrom_weapon.stack=buff.maelstrom_weapon.max_stack&(!talent.crashing_storms.enabled|active_enemies<=3)
    if S.ElementalBlast:IsReady() and ((not S.ElementalSpirits:IsAvailable() or (S.ElementalSpirits:IsAvailable() and (S.ElementalBlast:Charges() == S.ElementalBlast:MaxCharges() or Enh.feral_spirit_count >= 2))) and Enh.maelstrom_stacks == Enh.max_maelstrom_stacks and (not S.CrashingStorms:IsAvailable() or Enh.enemies_melee_count <= 3)) then
        if FS.APL.cast(S.ElementalBlast, State.Target, State, "elemental_blast aoe_totemic 18") then return true end
    end

    -- chain_lightning,if=buff.maelstrom_weapon.stack>=10
    if S.ChainLightning:IsReady() and (Enh.maelstrom_stacks >= 10) then
        if FS.APL.cast(S.ChainLightning, State.Target, State, "chain_lightning aoe_totemic 20") then return true end
    end

    -- feral_spirit
    if S.FeralSpirit:IsCastable() then
        if FS.APL.cast(S.FeralSpirit, nil, State, "feral_spirit aoe_totemic 22") then return true end
    end

    -- doom_winds,if=buff.legacy_of_the_frost_witch.up|!talent.legacy_of_the_frost_witch.enabled
    if S.DoomWinds:IsCastable() and (State.Player:buff_up(S.LegacyoftheFrostWitchBuff) or not S.LegacyoftheFrostWitch:IsAvailable()) then
        if FS.APL.cast(S.DoomWinds, State.Target, State, "doom_winds aoe_totemic 24") then return true end
    end

    -- crash_lightning,if=buff.doom_winds.up|!buff.crash_lightning.up|(talent.alpha_wolf.enabled&feral_spirit.active&alpha_wolf_min_remains=0)
    if S.CrashLightning:IsReady() and (State.Player:buff_up(S.DoomWindsBuff) or State.Player:BuffDown(S.CrashLightningBuff) or (S.AlphaWolf:IsAvailable() and State.Player:buff_up(S.FeralSpiritBuff) and Helpers.AlphaWolfMinRemains() == 0)) then
        if FS.APL.cast(S.CrashLightning, State.Target, State, "crash_lightning aoe_totemic 26") then return true end
    end

    -- sundering,if=buff.doom_winds.up|talent.earthsurge.enabled&(buff.legacy_of_the_frost_witch.up|!talent.legacy_of_the_frost_witch.enabled)&pet.surging_totem.active
    if S.Sundering:IsReady() and (State.Player:buff_up(S.DoomWindsBuff) or S.Earthsurge:IsAvailable() and (State.Player:buff_up(S.LegacyoftheFrostWitchBuff) or not S.LegacyoftheFrostWitch:IsAvailable()) and Helpers.TotemFinder(S.SurgingTotem)) then
        if FS.APL.cast(S.Sundering, State.Target, State, "sundering aoe_totemic 28") then return true end
    end

    -- fire_nova,if=active_dot.flame_shock=6|(active_dot.flame_shock>=4&active_dot.flame_shock=active_enemies)
    if S.FireNova:IsReady() and (S.FlameShockDebuff:AuraActiveCount(State.Player) == 6 or (S.FlameShockDebuff:AuraActiveCount(State.Player) >= 4 and S.FlameShockDebuff:AuraActiveCount(State.Player) >= Enh.enemies_melee_count)) then
        if FS.APL.cast(S.FireNova, nil, State, "fire_nova aoe_totemic 30") then return true end
    end

    -- voltaic_blaze
    if S.VoltaicBlazeAbility:IsReady() then
        if FS.APL.cast(S.VoltaicBlazeAbility, State.Target, State, "voltaic_blaze aoe_totemic 32") then return true end
    end

    -- lava_lash,target_if=min:debuff.lashing_flames.remains,if=talent.lashing_flames.enabled
    if S.LavaLash:IsCastable() and (S.LashingFlames:IsAvailable()) then
        if FS.APL.castTargetIf(true, S.LavaLash, Enh.enemies_melee, "min", Helpers.EvaluateTargetIfFilterLavaLash, nil, State, "lava_lash aoe_totemic 34") then return true end
    end

    -- lava_lash,if=talent.molten_assault.enabled&dot.flame_shock.ticking
    if S.LavaLash:IsCastable() and (S.MoltenAssault:IsAvailable() and State.Target:Debuff_up(S.FlameShockDebuff)) then
        if FS.APL.cast(S.LavaLash, State.Target, State, "lava_lash aoe_totemic 36") then return true end
    end

    -- ice_strike,if=talent.hailstorm.enabled&!buff.ice_strike.up
    if S.IceStrike:IsReady() and (S.Hailstorm:IsAvailable() and State.Player:BuffDown(S.IceStrikeBuff)) then
        if FS.APL.cast(S.IceStrike, State.Target, State, "ice_strike aoe_totemic 38") then return true end
    end

    -- frost_shock,if=talent.hailstorm.enabled&buff.hailstorm.up
    if S.FrostShock:IsCastable() and (S.Hailstorm:IsAvailable() and State.Player:buff_up(S.HailstormBuff)) then
        if FS.APL.cast(S.FrostShock, State.Target, State, "frost_shock aoe_totemic 40") then return true end
    end

    -- sundering,if=(buff.legacy_of_the_frost_witch.up|!talent.legacy_of_the_frost_witch.enabled)&pet.surging_totem.active
    if S.Sundering:IsReady() and ((State.Player:buff_up(S.LegacyoftheFrostWitchBuff) or not S.LegacyoftheFrostWitch:IsAvailable()) and Helpers.TotemFinder(S.SurgingTotem)) then
        if FS.APL.cast(S.Sundering, State.Target, State, "sundering aoe_totemic 42") then return true end
    end

    -- flame_shock,if=talent.molten_assault.enabled&!ticking
    if S.FlameShock:IsReady() and (S.MoltenAssault:IsAvailable() and State.Target:DebuffDown(S.FlameShockDebuff)) then
        if FS.APL.cast(S.FlameShock, State.Target, State, "flame_shock aoe_totemic 44") then return true end
    end

    -- flame_shock,target_if=min:dot.flame_shock.remains,if=(talent.fire_nova.enabled|talent.primordial_wave.enabled)&(active_dot.flame_shock<active_enemies)&active_dot.flame_shock<6
    if S.FlameShock:IsReady() and ((S.FireNova:IsAvailable() or S.PrimordialWave:IsAvailable()) and (S.FlameShockDebuff:AuraActiveCount(State.Player) < Enh.enemies_melee_count) and S.FlameShockDebuff:AuraActiveCount(State.Player) < 6) then
        if FS.APL.castTargetIf(true, S.FlameShock, Enh.enemies_melee, "min", Helpers.EvaluateTargetIfFilterPrimordialWave, Helpers.EvaluateCycleFlameShock, State, "flame_shock aoe_totemic 46") then return true end
    end

    -- fire_nova,if=active_dot.flame_shock>=3
    if S.FireNova:IsReady() and (S.FlameShockDebuff:AuraActiveCount(State.Player) >= 3) then
        if FS.APL.cast(S.FireNova, nil, State, "fire_nova aoe_totemic 48") then return true end
    end

    -- stormstrike,if=buff.crash_lightning.up&(talent.deeply_rooted_elements.enabled|buff.converging_storms.stack=buff.converging_storms.max_stack)
    if S.Stormstrike:IsReady() and (State.Player:buff_up(S.CrashLightningBuff) and (S.DeeplyRootedElements:IsAvailable() or State.Player:BuffStack(S.ConvergingStormsBuff) == Helpers.MaxConvergingStormsStacks)) then
        if FS.APL.cast(S.Stormstrike, State.Target, State, "stormstrike aoe_totemic 50") then return true end
    end

    -- crash_lightning,if=talent.crashing_storms.enabled&buff.cl_crash_lightning.up&active_enemies>=4
    if S.CrashLightning:IsReady() and (S.CrashingStorms:IsAvailable() and State.Player:buff_up(S.CLCrashLightningBuff) and Enh.enemies_melee_count >= 4) then
        if FS.APL.cast(S.CrashLightning, State.Target, State, "crash_lightning aoe_totemic 52") then return true end
    end

    -- windstrike
    if S.Windstrike:IsCastable() then
        if FS.APL.cast(S.Windstrike, State.Target, State, "windstrike aoe_totemic 54") then return true end
    end

    -- stormstrike
    if S.Stormstrike:IsReady() then
        if FS.APL.cast(S.Stormstrike, State.Target, State, "stormstrike aoe_totemic 56") then return true end
    end

    -- ice_strike
    if S.IceStrike:IsReady() then
        if FS.APL.cast(S.IceStrike, State.Target, State, "ice_strike aoe_totemic 58") then return true end
    end

    -- lava_lash
    if S.LavaLash:IsCastable() then
        if FS.APL.cast(S.LavaLash, State.Target, State, "lava_lash aoe_totemic 60") then return true end
    end

    -- crash_lightning
    if S.CrashLightning:IsReady() then
        if FS.APL.cast(S.CrashLightning, State.Target, State, "crash_lightning aoe_totemic 62") then return true end
    end

    -- fire_nova,if=active_dot.flame_shock>=2
    if S.FireNova:IsReady() and (S.FlameShockDebuff:AuraActiveCount(State.Player) >= 2) then
        if FS.APL.cast(S.FireNova, nil, State, "fire_nova aoe_totemic 64") then return true end
    end

    -- elemental_blast,target_if=min:debuff.lightning_rod.remains,if=(!talent.elemental_spirits.enabled|(talent.elemental_spirits.enabled&(charges=max_charges|feral_spirit.active>=2)))&buff.maelstrom_weapon.stack>=5&(!talent.crashing_storms.enabled|active_enemies<=3)
    if S.ElementalBlast:IsReady() and ((not S.ElementalSpirits:IsAvailable() or (S.ElementalSpirits:IsAvailable() and (S.ElementalBlast:Charges() == S.ElementalBlast:MaxCharges() or Enh.feral_spirit_count >= 2))) and Enh.maelstrom_stacks >= 5 and (not S.CrashingStorms:IsAvailable() or Enh.enemies_melee_count <= 3)) then
        if FS.APL.castTargetIf(true, S.ElementalBlast, Enh.enemies_melee, "min", Helpers.EvaluateTargetIfFilterLightningRodRemains, nil, State, "elemental_blast aoe_totemic 66") then return true end
    end

    -- chain_lightning,target_if=min:debuff.lightning_rod.remains,if=buff.maelstrom_weapon.stack>=5
    if S.ChainLightning:IsReady() and (Enh.maelstrom_stacks >= 5) then
        if FS.APL.castTargetIf(true, S.ChainLightning, Enh.enemies_melee, "min", Helpers.EvaluateTargetIfFilterLightningRodRemains, nil, State, "chain_lightning aoe_totemic 68") then return true end
    end

    -- flame_shock,if=!ticking
    if S.FlameShock:IsReady() and (State.Target:DebuffDown(S.FlameShockDebuff)) then
        if FS.APL.cast(S.FlameShock, State.Target, State, "flame_shock aoe_totemic 70") then return true end
    end

    return false
end

return AoeTotemic
