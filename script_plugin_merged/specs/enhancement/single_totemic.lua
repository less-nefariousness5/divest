-- Single Target Totemic APL for Enhancement Shaman
local buff_manager = require("common/modules/buff_manager")
local spell_helper = require("common/utility/spell_helper")
local unit_helper = require("common/utility/unit_helper")

local S = FS.Enhancement.Spells
local Helpers = require("specs/enhancement/helpers")

local function SingleTotemic()
    local Enh = FS.Enhancement.Variables
    local State = FS.state

    -- surging_totem
    if S.SurgingTotem:IsReady() then
        if FS.APL.cast(S.SurgingTotem, nil, State, "surging_totem single_totemic 2") then return true end
    end

    -- ascendance,if=ti_lightning_bolt&pet.surging_totem.remains>4&(buff.totemic_rebound.stack>=3|buff.maelstrom_weapon.stack>0)
    if Helpers.CDsON() and S.Ascendance:IsCastable() and (Enh.ti_action == S.LightningBolt and Helpers.TotemFinder(S.SurgingTotem, true) > 4 and (State.Player:BuffStack(S.TotemicReboundBuff) >= 3 or Enh.maelstrom_stacks > 0)) then
        if FS.APL.cast(S.Ascendance, nil, State, "ascendance single_totemic 4") then return true end
    end

    -- doom_winds,if=!talent.elemental_spirits.enabled&buff.legacy_of_the_frost_witch.up
    if S.DoomWinds:IsReady() and (not S.ElementalSpirits:IsAvailable() and State.Player:buff_up(S.LegacyoftheFrostWitchBuff)) then
        if FS.APL.cast(S.DoomWinds, State.Target, State, "doom_winds single_totemic 6") then return true end
    end

    -- sundering,if=buff.ascendance.up&pet.surging_totem.active&talent.earthsurge.enabled&buff.legacy_of_the_frost_witch.up&buff.totemic_rebound.stack>=5&buff.earthen_weapon.stack>=2
    if S.Sundering:IsReady() and (State.Player:buff_up(S.AscendanceBuff) and Helpers.TotemFinder(S.SurgingTotem) and S.Earthsurge:IsAvailable() and State.Player:buff_up(S.LegacyoftheFrostWitchBuff) and State.Player:BuffStack(S.TotemicReboundBuff) >= 5 and State.Player:BuffStack(S.EarthenWeaponBuff) >= 2) then
        if FS.APL.cast(S.Sundering, State.Target, State, "sundering single_totemic 8") then return true end
    end

    -- crash_lightning,if=talent.unrelenting_storms.enabled&talent.alpha_wolf.enabled&alpha_wolf_min_remains=0&buff.earthen_weapon.stack>=8
    if S.CrashLightning:IsReady() and (S.UnrelentingStorms:IsAvailable() and S.AlphaWolf:IsAvailable() and Helpers.AlphaWolfMinRemains() == 0 and State.Player:BuffStack(S.EarthenWeaponBuff) >= 8) then
        if FS.APL.cast(S.CrashLightning, State.Target, State, "crash_lightning single_totemic 10") then return true end
    end

    -- windstrike,if=talent.thorims_invocation.enabled&buff.maelstrom_weapon.stack>0&ti_lightning_bolt&!talent.elemental_spirits.enabled
    if S.Windstrike:IsCastable() and (S.ThorimsInvocation:IsAvailable() and Enh.maelstrom_stacks > 0 and Enh.ti_action == S.LightningBolt and not S.ElementalSpirits:IsAvailable()) then
        if FS.APL.cast(S.Windstrike, State.Target, State, "windstrike single_totemic 12") then return true end
    end

    -- sundering,if=buff.legacy_of_the_frost_witch.up&cooldown.ascendance.remains>=10&pet.surging_totem.active&buff.totemic_rebound.stack>=3&!buff.ascendance.up
    if S.Sundering:IsReady() and (State.Player:buff_up(S.LegacyoftheFrostWitchBuff) and S.Ascendance:CooldownRemains() >= 10 and Helpers.TotemFinder(S.SurgingTotem) and State.Player:BuffStack(S.TotemicReboundBuff) >= 3 and State.Player:BuffDown(S.AscendanceBuff)) then
        if FS.APL.cast(S.Sundering, State.Target, State, "sundering single_totemic 14") then return true end
    end

    -- primordial_wave,if=!dot.flame_shock.ticking&talent.molten_assault.enabled
    if S.PrimordialWave:IsReady() and (State.Target:DebuffDown(S.FlameShockDebuff) and S.MoltenAssault:IsAvailable()) then
        if FS.APL.cast(S.PrimordialWave, State.Target, State, "primordial_wave single_totemic 16") then return true end
    end

    -- feral_spirit
    if S.FeralSpirit:IsCastable() then
        if FS.APL.cast(S.FeralSpirit, nil, State, "feral_spirit single_totemic 18") then return true end
    end

    -- elemental_blast,if=buff.maelstrom_weapon.stack=buff.maelstrom_weapon.max_stack&talent.elemental_spirits.enabled&feral_spirit.active>=6&(charges_fractional>=1.8|buff.ascendance.up)
    if S.ElementalBlast:IsReady() and (Enh.maelstrom_stacks == Enh.max_maelstrom_stacks and S.ElementalSpirits:IsAvailable() and Enh.feral_spirit_count >= 6 and (S.ElementalBlast:ChargesFractional(12) >= 1.8 or State.Player:buff_up(S.AscendanceBuff))) then
        if FS.APL.cast(S.ElementalBlast, State.Target, State, "elemental_blast single_totemic 20") then return true end
    end

    -- voltaic_blaze,if=buff.whirling_earth.up
    if S.VoltaicBlazeAbility:IsReady() and (State.Player:buff_up(S.WhirlingEarthBuff)) then
        if FS.APL.cast(S.VoltaicBlazeAbility, State.Target, State, "voltaic_blaze single_totemic 22") then return true end
    end

    -- crash_lightning,if=talent.unrelenting_storms.enabled&talent.alpha_wolf.enabled&alpha_wolf_min_remains=0
    if S.CrashLightning:IsReady() and (S.UnrelentingStorms:IsAvailable() and S.AlphaWolf:IsAvailable() and Helpers.AlphaWolfMinRemains() == 0) then
        if FS.APL.cast(S.CrashLightning, State.Target, State, "crash_lightning single_totemic 24") then return true end
    end

    -- flame_shock,if=!ticking&talent.lashing_flames.enabled
    if S.FlameShock:IsReady() and (State.Target:DebuffDown(S.FlameShockDebuff) and S.LashingFlames:IsAvailable()) then
        if FS.APL.cast(S.FlameShock, State.Target, State, "flame_shock single_totemic 26") then return true end
    end

    -- lava_lash,if=buff.hot_hand.up&!talent.legacy_of_the_frost_witch.enabled
    if S.LavaLash:IsCastable() and (State.Player:buff_up(S.HotHandBuff) and not S.LegacyoftheFrostWitch:IsAvailable()) then
        if FS.APL.cast(S.LavaLash, State.Target, State, "lava_lash single_totemic 28") then return true end
    end

    -- elemental_blast,if=buff.maelstrom_weapon.stack>=5&charges=max_charges
    if S.ElementalBlast:IsReady() and (Enh.maelstrom_stacks >= 5 and S.ElementalBlast:Charges() == S.ElementalBlast:MaxCharges()) then
        if FS.APL.cast(S.ElementalBlast, State.Target, State, "elemental_blast single_totemic 30") then return true end
    end

    -- lightning_bolt,if=buff.maelstrom_weapon.stack>=8&buff.primordial_wave.up&(!buff.splintered_elements.up|fight_remains<=12)
    if S.LightningBolt:IsCastable() and (Enh.maelstrom_stacks >= 8 and State.Player:buff_up(S.PrimordialWaveBuff) and (State.Player:BuffDown(S.SplinteredElementsBuff) or Enh.fight_remains <= 12)) then
        if FS.APL.cast(S.LightningBolt, State.Target, State, "lightning_bolt single_totemic 32") then return true end
    end

    -- elemental_blast,if=buff.maelstrom_weapon.stack>=8&(feral_spirit.active>=2|!talent.elemental_spirits.enabled)
    if S.ElementalBlast:IsReady() and (Enh.maelstrom_stacks >= 8 and (Enh.feral_spirit_count >= 2 or not S.ElementalSpirits:IsAvailable())) then
        if FS.APL.cast(S.ElementalBlast, State.Target, State, "elemental_blast single_totemic 34") then return true end
    end

    -- lava_burst,if=!talent.thorims_invocation.enabled&buff.maelstrom_weapon.stack>=5
    if S.LavaBurst:IsReady() and (not S.ThorimsInvocation:IsAvailable() and Enh.maelstrom_stacks >= 5) then
        if FS.APL.cast(S.LavaBurst, State.Target, State, "lava_burst single_totemic 36") then return true end
    end

    -- primordial_wave
    if S.PrimordialWave:IsReady() then
        if FS.APL.cast(S.PrimordialWave, State.Target, State, "primordial_wave single_totemic 38") then return true end
    end

    -- elemental_blast,if=buff.maelstrom_weapon.stack>=5&(charges_fractional>=1.8|(buff.molten_weapon.stack+buff.icy_edge.stack>=4))&talent.ascendance.enabled&(feral_spirit.active>=4|!talent.elemental_spirits.enabled)
    if S.ElementalBlast:IsReady() and (Enh.maelstrom_stacks >= 5 and (S.ElementalBlast:ChargesFractional(12) >= 1.8 or (Enh.molten_weapon_stacks + Enh.icy_edge_stacks >= 4)) and S.Ascendance:IsAvailable() and (Enh.feral_spirit_count >= 4 or not S.ElementalSpirits:IsAvailable())) then
        if FS.APL.cast(S.ElementalBlast, State.Target, State, "elemental_blast single_totemic 40") then return true end
    end

    -- elemental_blast,if=talent.ascendance.enabled&(buff.maelstrom_weapon.stack>=10|(buff.maelstrom_weapon.stack>=5&buff.whirling_air.up&!buff.legacy_of_the_frost_witch.up))
    if S.ElementalBlast:IsReady() and (S.Ascendance:IsAvailable() and (Enh.maelstrom_stacks >= 10 or (Enh.maelstrom_stacks >= 5 and State.Player:buff_up(S.WhirlingAirBuff) and not S.LegacyoftheFrostWitch:IsAvailable()))) then
        if FS.APL.cast(S.ElementalBlast, State.Target, State, "elemental_blast single_totemic 42") then return true end
    end

    -- lightning_bolt,if=talent.ascendance.enabled&(buff.maelstrom_weapon.stack>=10|(buff.maelstrom_weapon.stack>=5&buff.whirling_air.up&!buff.legacy_of_the_frost_witch.up))
    if S.LightningBolt:IsCastable() and (S.Ascendance:IsAvailable() and (Enh.maelstrom_stacks >= 10 or (Enh.maelstrom_stacks >= 5 and State.Player:buff_up(S.WhirlingAirBuff) and not S.LegacyoftheFrostWitch:IsAvailable()))) then
        if FS.APL.cast(S.LightningBolt, State.Target, State, "lightning_bolt single_totemic 44") then return true end
    end

    -- lava_lash,if=buff.hot_hand.up&talent.molten_assault.enabled&pet.searing_totem.active
    if S.LavaLash:IsCastable() and (State.Player:buff_up(S.HotHandBuff) and S.MoltenAssault:IsAvailable() and State.Player:buff_up(S.LivelyTotemsBuff)) then
        if FS.APL.cast(S.LavaLash, State.Target, State, "lava_lash single_totemic 46") then return true end
    end

    -- windstrike
    if S.Windstrike:IsCastable() then
        if FS.APL.cast(S.Windstrike, State.Target, State, "windstrike single_totemic 48") then return true end
    end

    -- stormstrike
    if S.Stormstrike:IsReady() then
        if FS.APL.cast(S.Stormstrike, State.Target, State, "stormstrike single_totemic 50") then return true end
    end

    -- lava_lash,if=talent.molten_assault.enabled
    if S.LavaLash:IsCastable() and (S.MoltenAssault:IsAvailable()) then
        if FS.APL.cast(S.LavaLash, State.Target, State, "lava_lash single_totemic 52") then return true end
    end

    -- crash_lightning,if=talent.unrelenting_storms.enabled
    if S.CrashLightning:IsReady() and (S.UnrelentingStorms:IsAvailable()) then
        if FS.APL.cast(S.CrashLightning, State.Target, State, "crash_lightning single_totemic 54") then return true end
    end

    -- lightning_bolt,if=buff.maelstrom_weapon.stack>=5&talent.ascendance.enabled
    if S.LightningBolt:IsCastable() and (Enh.maelstrom_stacks >= 5 and S.Ascendance:IsAvailable()) then
        if FS.APL.cast(S.LightningBolt, State.Target, State, "lightning_bolt single_totemic 56") then return true end
    end

    -- ice_strike,if=!buff.ice_strike.up
    if S.IceStrike:IsReady() and (State.Player:BuffDown(S.IceStrikeBuff)) then
        if FS.APL.cast(S.IceStrike, State.Target, State, "ice_strike single_totemic 58") then return true end
    end

    -- frost_shock,if=buff.hailstorm.up&pet.searing_totem.active
    if S.FrostShock:IsCastable() and (State.Player:buff_up(S.HailstormBuff) and State.Player:buff_up(S.LivelyTotemsBuff)) then
        if FS.APL.cast(S.FrostShock, State.Target, State, "frost_shock single_totemic 60") then return true end
    end

    -- lava_lash
    if S.LavaLash:IsCastable() then
        if FS.APL.cast(S.LavaLash, State.Target, State, "lava_lash single_totemic 62") then return true end
    end

    -- elemental_blast,if=buff.maelstrom_weapon.stack>=5&feral_spirit.active>=4&talent.deeply_rooted_elements.enabled&(charges_fractional>=1.8|(buff.icy_edge.stack+buff.molten_weapon.stack>=4))
    if S.ElementalBlast:IsReady() and (Enh.maelstrom_stacks >= 5 and Enh.feral_spirit_count >= 4 and S.DeeplyRootedElements:IsAvailable() and (S.ElementalBlast:ChargesFractional(12) >= 1.8 or (Enh.icy_edge_stacks + Enh.molten_weapon_stacks >= 4))) then
        if FS.APL.cast(S.ElementalBlast, State.Target, State, "elemental_blast single_totemic 64") then return true end
    end

    -- doom_winds,if=talent.elemental_spirits.enabled
    if S.DoomWinds:IsReady() and (S.ElementalSpirits:IsAvailable()) then
        if FS.APL.cast(S.DoomWinds, State.Target, State, "doom_winds single_totemic 66") then return true end
    end

    -- flame_shock,if=!ticking&!talent.voltaic_blaze.enabled
    if S.FlameShock:IsReady() and (State.Target:DebuffDown(S.FlameShockDebuff) and not S.VoltaicBlaze:IsAvailable()) then
        if FS.APL.cast(S.FlameShock, State.Target, State, "flame_shock single_totemic 68") then return true end
    end

    -- frost_shock,if=buff.hailstorm.up
    if S.FrostShock:IsCastable() and (State.Player:buff_up(S.HailstormBuff)) then
        if FS.APL.cast(S.FrostShock, State.Target, State, "frost_shock single_totemic 70") then return true end
    end

    -- crash_lightning,if=talent.converging_storms.enabled
    if S.CrashLightning:IsReady() and (S.ConvergingStorms:IsAvailable()) then
        if FS.APL.cast(S.CrashLightning, State.Target, State, "crash_lightning single_totemic 72") then return true end
    end

    -- frost_shock
    if S.FrostShock:IsCastable() then
        if FS.APL.cast(S.FrostShock, State.Target, State, "frost_shock single_totemic 74") then return true end
    end

    -- crash_lightning
    if S.CrashLightning:IsReady() then
        if FS.APL.cast(S.CrashLightning, State.Target, State, "crash_lightning single_totemic 76") then return true end
    end

    -- fire_nova,if=active_dot.flame_shock
    if S.FireNova:IsReady() and (State.Target:Debuff_up(S.FlameShockDebuff)) then
        if FS.APL.cast(S.FireNova, nil, State, "fire_nova single_totemic 78") then return true end
    end

    -- earth_elemental
    if S.EarthElemental:IsCastable() then
        if FS.APL.cast(S.EarthElemental, nil, State, "earth_elemental single_totemic 80") then return true end
    end

    -- flame_shock,if=!talent.voltaic_blaze.enabled
    if S.FlameShock:IsReady() and (not S.VoltaicBlaze:IsAvailable()) then
        if FS.APL.cast(S.FlameShock, State.Target, State, "flame_shock single_totemic 82") then return true end
    end

    return false
end

return SingleTotemic
