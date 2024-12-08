-- Single Target APL for Enhancement Shaman
local buff_manager = require("common/modules/buff_manager")
local spell_helper = require("common/utility/spell_helper")
local unit_helper = require("common/utility/unit_helper")

local S = FS.Enhancement.Spells
local Helpers = require("specs/enhancement/helpers")

local function Single()
    local Enh = FS.Enhancement.Variables
    local State = FS.state

    -- feral_spirit,if=talent.elemental_spirits.enabled
    if S.FeralSpirit:IsCastable() and (S.ElementalSpirits:IsAvailable()) then
        if FS.APL.cast(S.FeralSpirit, nil, State, "feral_spirit single 2") then return true end
    end

    -- windstrike,if=talent.thorims_invocation.enabled&buff.maelstrom_weapon.stack>0&ti_lightning_bolt&!talent.elemental_spirits.enabled
    if S.Windstrike:IsCastable() and (S.ThorimsInvocation:IsAvailable() and Enh.maelstrom_stacks > 0 and Enh.ti_action == S.LightningBolt and not S.ElementalSpirits:IsAvailable()) then
        if FS.APL.cast(S.Windstrike, State.Target, State, "windstrike single 4") then return true end
    end

    -- primordial_wave,if=!dot.flame_shock.ticking&talent.molten_assault.enabled
    if S.PrimordialWave:IsReady() and (State.Target:DebuffDown(S.FlameShockDebuff) and S.MoltenAssault:IsAvailable()) then
        if FS.APL.cast(S.PrimordialWave, State.Target, State, "primordial_wave single 6") then return true end
    end

    -- lava_lash,if=talent.lashing_flames.enabled&debuff.lashing_flames.down
    if S.LavaLash:IsCastable() and (S.LashingFlames:IsAvailable() and State.Target:DebuffDown(S.LashingFlamesDebuff)) then
        if FS.APL.cast(S.LavaLash, State.Target, State, "lava_lash single 8") then return true end
    end

    -- stormstrike,if=buff.maelstrom_weapon.stack<2&cooldown.ascendance.remains=0
    if S.Stormstrike:IsReady() and (Enh.maelstrom_stacks < 2 and S.Ascendance:CooldownUp()) then
        if FS.APL.cast(S.Stormstrike, State.Target, State, "stormstrike single 10") then return true end
    end

    -- feral_spirit
    if S.FeralSpirit:IsCastable() then
        if FS.APL.cast(S.FeralSpirit, nil, State, "feral_spirit single 12") then return true end
    end

    -- ascendance,if=dot.flame_shock.ticking&(ti_lightning_bolt&active_enemies=1)&buff.maelstrom_weapon.stack>=2
    if Helpers.CDsON() and S.Ascendance:IsCastable() and (State.Target:Debuff_up(S.FlameShockDebuff) and (Enh.ti_action == S.LightningBolt and Enh.enemies_melee_count == 1) and Enh.maelstrom_stacks >= 2) then
        if FS.APL.cast(S.Ascendance, nil, State, "ascendance single 14") then return true end
    end

    -- tempest,if=buff.maelstrom_weapon.stack=buff.maelstrom_weapon.max_stack|(buff.tempest.stack=buff.tempest.max_stack&(tempest_mael_count>30|buff.awakening_storms.stack=2)&buff.maelstrom_weapon.stack>=5)
    if S.TempestAbility:IsReady() and (Enh.maelstrom_stacks == Enh.max_maelstrom_stacks or (State.Player:BuffStack(S.TempestBuff) == Helpers.MaxTempestStacks and (Enh.tempest_maelstrom > 30 or State.Player:BuffStack(S.AwakeningStormsBuff) == 2) and Enh.maelstrom_stacks >= 5)) then
        if FS.APL.cast(S.TempestAbility, State.Target, State, "tempest single 16") then return true end
    end

    -- elemental_blast,if=buff.maelstrom_weapon.stack=buff.maelstrom_weapon.max_stack&talent.elemental_spirits.enabled&feral_spirit.active>=6&(charges_fractional>=1.8|buff.ascendance.up)
    if S.ElementalBlast:IsReady() and (Enh.maelstrom_stacks == Enh.max_maelstrom_stacks and S.ElementalSpirits:IsAvailable() and Enh.feral_spirit_count >= 6 and (S.ElementalBlast:ChargesFractional(12) >= 1.8 or State.Player:buff_up(S.AscendanceBuff))) then
        if FS.APL.cast(S.ElementalBlast, State.Target, State, "elemental_blast single 18") then return true end
    end

    -- windstrike,if=talent.thorims_invocation.enabled&buff.maelstrom_weapon.stack>0&ti_lightning_bolt&charges=max_charges
    if S.Windstrike:IsCastable() and (S.ThorimsInvocation:IsAvailable() and Enh.maelstrom_stacks > 0 and Enh.ti_action == S.LightningBolt and S.Windstrike:Charges() == S.Windstrike:MaxCharges()) then
        if FS.APL.cast(S.Windstrike, State.Target, State, "windstrike single 20") then return true end
    end

    -- doom_winds,if=raid_event.adds.in>=action.doom_winds.cooldown&talent.elemental_spirits.enabled&talent.ascendance.enabled&buff.maelstrom_weapon.stack>=2
    if S.DoomWinds:IsReady() and (S.ElementalSpirits:IsAvailable() and S.Ascendance:IsAvailable() and Enh.maelstrom_stacks >= 2) then
        if FS.APL.cast(S.DoomWinds, State.Target, State, "doom_winds single 22") then return true end
    end

    -- windstrike,if=talent.thorims_invocation.enabled&buff.maelstrom_weapon.stack>0&ti_lightning_bolt
    if S.Windstrike:IsCastable() and (S.ThorimsInvocation:IsAvailable() and Enh.maelstrom_stacks > 0 and Enh.ti_action == S.LightningBolt) then
        if FS.APL.cast(S.Windstrike, State.Target, State, "windstrike single 24") then return true end
    end

    -- flame_shock,if=!ticking&talent.ashen_catalyst.enabled
    if S.FlameShock:IsReady() and (State.Target:DebuffDown(S.FlameShockDebuff) and not S.AshenCatalyst:IsAvailable()) then
        if FS.APL.cast(S.FlameShock, State.Target, State, "flame_shock single 26") then return true end
    end

    -- lightning_bolt,if=buff.maelstrom_weapon.stack=buff.maelstrom_weapon.max_stack&buff.primordial_wave.up
    if S.LightningBolt:IsCastable() and (Enh.maelstrom_stacks >= Enh.max_maelstrom_stacks and State.Player:buff_up(S.PrimordialWaveBuff)) then
        if FS.APL.cast(S.LightningBolt, State.Target, State, "lightning_bolt single 28") then return true end
    end

    -- tempest,if=(!talent.overflowing_maelstrom.enabled&buff.maelstrom_weapon.stack>=5)|(buff.maelstrom_weapon.stack>=10-2*talent.elemental_spirits.enabled)
    if S.TempestAbility:IsReady() and ((not S.OverflowingMaelstrom:IsAvailable() and Enh.maelstrom_stacks >= 5) or (Enh.maelstrom_stacks >= 10 - 2 * FS.APL:num(S.ElementalSpirits:IsAvailable()))) then
        if FS.APL.cast(S.TempestAbility, State.Target, State, "tempest single 30") then return true end
    end

    -- primordial_wave,if=!talent.deeply_rooted_elements.enabled
    if S.PrimordialWave:IsReady() and (not S.DeeplyRootedElements:IsAvailable()) then
        if FS.APL.cast(S.PrimordialWave, State.Target, State, "primordial_wave single 32") then return true end
    end

    -- elemental_blast,if=buff.maelstrom_weapon.stack>=8&feral_spirit.active>=4&(!buff.ascendance.up|charges_fractional>=1.8)
    if S.ElementalBlast:IsReady() and (Enh.maelstrom_stacks >= 8 and Enh.feral_spirit_count >= 4 and (State.Player:BuffDown(S.AscendanceBuff) or S.ElementalBlast:ChargesFractional(12) >= 1.8)) then
        if FS.APL.cast(S.ElementalBlast, State.Target, State, "elemental_blast single 34") then return true end
    end

    -- lightning_bolt,if=buff.maelstrom_weapon.stack>=8+2*talent.legacy_of_the_frost_witch.enabled
    if S.LightningBolt:IsCastable() and (Enh.maelstrom_stacks >= 8 + 2 * FS.APL:num(S.LegacyoftheFrostWitch:IsAvailable())) then
        if FS.APL.cast(S.LightningBolt, State.Target, State, "lightning_bolt single 36") then return true end
    end

    -- lightning_bolt,if=buff.maelstrom_weapon.stack>=5&!talent.legacy_of_the_frost_witch.enabled&(talent.deeply_rooted_elements.enabled|!talent.overflowing_maelstrom.enabled|!talent.witch_doctors_ancestry.enabled)
    if S.LightningBolt:IsCastable() and (Enh.maelstrom_stacks >= 5 and not S.LegacyoftheFrostWitch:IsAvailable() and (S.DeeplyRootedElements:IsAvailable() or not S.OverflowingMaelstrom:IsAvailable() or not S.WitchDoctorsAncestry:IsAvailable())) then
        if FS.APL.cast(S.LightningBolt, State.Target, State, "lightning_bolt single 38") then return true end
    end

    -- voltaic_blaze,if=talent.elemental_spirits.enabled&!talent.witch_doctors_ancestry.enabled
    if S.VoltaicBlazeAbility:IsReady() and (S.ElementalSpirits:IsAvailable() and not S.WitchDoctorsAncestry:IsAvailable()) then
        if FS.APL.cast(S.VoltaicBlazeAbility, State.Target, State, "voltaic_blaze single 40") then return true end
    end

    -- lightning_bolt,if=buff.arc_discharge.up&talent.deeply_rooted_elements.enabled
    if S.LightningBolt:IsCastable() and (State.Player:buff_up(S.ArcDischargeBuff) and S.DeeplyRootedElements:IsAvailable()) then
        if FS.APL.cast(S.LightningBolt, State.Target, State, "lightning_bolt single 42") then return true end
    end

    -- lava_lash,if=buff.hot_hand.up|(buff.ashen_catalyst.stack=buff.ashen_catalyst.max_stack)
    if S.LavaLash:IsCastable() and (State.Player:buff_up(S.HotHandBuff) or (State.Player:BuffStack(S.AshenCatalystBuff) == Helpers.MaxAshenCatalystStacks)) then
        if FS.APL.cast(S.LavaLash, State.Target, State, "lava_lash single 44") then return true end
    end

    -- stormstrike,if=buff.doom_winds.up|(talent.stormblast.enabled&buff.stormsurge.up&charges=max_charges)
    if S.Stormstrike:IsReady() and (State.Player:buff_up(S.DoomWindsBuff) or (S.Stormblast:IsAvailable() and State.Player:buff_up(S.StormsurgeBuff) and S.Stormstrike:Charges() == S.Stormstrike:MaxCharges())) then
        if FS.APL.cast(S.Stormstrike, State.Target, State, "stormstrike single 46") then return true end
    end

    -- lava_lash,if=talent.lashing_flames.enabled&!buff.doom_winds.up
    if S.LavaLash:IsCastable() and (S.LashingFlames:IsAvailable() and State.Player:BuffDown(S.DoomWindsBuff)) then
        if FS.APL.cast(S.LavaLash, State.Target, State, "lava_lash single 48") then return true end
    end

    -- voltaic_blaze,if=talent.elemental_spirits.enabled&!buff.doom_winds.up
    if S.VoltaicBlazeAbility:IsReady() and (S.ElementalSpirits:IsAvailable() and State.Player:BuffDown(S.DoomWindsBuff)) then
        if FS.APL.cast(S.VoltaicBlazeAbility, State.Target, State, "voltaic_blaze single 50") then return true end
    end

    -- crash_lightning,if=talent.unrelenting_storms.enabled&talent.elemental_spirits.enabled&!talent.deeply_rooted_elements.enabled
    if S.CrashLightning:IsReady() and (S.UnrelentingStorms:IsAvailable() and S.ElementalSpirits:IsAvailable() and not S.DeeplyRootedElements:IsAvailable()) then
        if FS.APL.cast(S.CrashLightning, State.Target, State, "crash_lightning single 52") then return true end
    end

    -- ice_strike,if=talent.elemental_assault.enabled&talent.swirling_maelstrom.enabled&talent.witch_doctors_ancestry.enabled
    if S.IceStrike:IsReady() and (S.ElementalAssault:IsAvailable() and S.SwirlingMaelstrom:IsAvailable() and S.WitchDoctorsAncestry:IsAvailable()) then
        if FS.APL.cast(S.IceStrike, State.Target, State, "ice_strike single 54") then return true end
    end

    -- stormstrike
    if S.Stormstrike:IsReady() then
        if FS.APL.cast(S.Stormstrike, State.Target, State, "stormstrike single 56") then return true end
    end

    -- lightning_bolt,if=buff.maelstrom_weapon.stack>=5&talent.ascendance.enabled&!talent.legacy_of_the_frost_witch.enabled
    if S.LightningBolt:IsCastable() and (Enh.maelstrom_stacks >= 5 and S.Ascendance:IsAvailable() and not S.LegacyoftheFrostWitch:IsAvailable()) then
        if FS.APL.cast(S.LightningBolt, State.Target, State, "lightning_bolt single 58") then return true end
    end

    -- crash_lightning,if=talent.unrelenting_storms.enabled
    if S.CrashLightning:IsReady() and (S.UnrelentingStorms:IsAvailable()) then
        if FS.APL.cast(S.CrashLightning, State.Target, State, "crash_lightning single 60") then return true end
    end

    -- voltaic_blaze
    if S.VoltaicBlazeAbility:IsReady() then
        if FS.APL.cast(S.VoltaicBlazeAbility, State.Target, State, "voltaic_blaze single 62") then return true end
    end

    -- sundering,if=!talent.elemental_spirits.enabled
    if S.Sundering:IsReady() and (not S.ElementalSpirits:IsAvailable()) then
        if FS.APL.cast(S.Sundering, State.Target, State, "sundering single 64") then return true end
    end

    -- frost_shock,if=buff.hailstorm.up&buff.ice_strike.up&talent.swirling_maelstrom.enabled&talent.ascendance.enabled
    if S.FrostShock:IsCastable() and (State.Player:buff_up(S.HailstormBuff) and State.Player:buff_up(S.IceStrikeBuff) and S.SwirlingMaelstrom:IsAvailable() and S.Ascendance:IsAvailable()) then
        if FS.APL.cast(S.FrostShock, State.Target, State, "frost_shock single 66") then return true end
    end

    -- elemental_blast,if=buff.maelstrom_weapon.stack>=5&feral_spirit.active>=4&talent.deeply_rooted_elements.enabled&(charges_fractional>=1.8|(buff.molten_weapon.stack+buff.icy_edge.stack>=4))&!talent.flowing_spirits.enabled
    if S.ElementalBlast:IsReady() and (Enh.maelstrom_stacks >= 5 and Enh.feral_spirit_count >= 4 and S.DeeplyRootedElements:IsAvailable() and (S.ElementalBlast:ChargesFractional(12) >= 1.8 or (Enh.molten_weapon_stacks + Enh.icy_edge_stacks >= 4)) and not S.FlowingSpirits:IsAvailable()) then
        if FS.APL.cast(S.ElementalBlast, State.Target, State, "elemental_blast single 68") then return true end
    end

    -- crash_lightning,if=talent.alpha_wolf.enabled&feral_spirit.active&alpha_wolf_min_remains=0
    if S.CrashLightning:IsReady() and (S.AlphaWolf:IsAvailable() and State.Player:buff_up(S.FeralSpiritBuff) and Helpers.AlphaWolfMinRemains() == 0) then
        if FS.APL.cast(S.CrashLightning, State.Target, State, "crash_lightning single 70") then return true end
    end

    -- flame_shock,if=!ticking&!talent.tempest.enabled
    if S.FlameShock:IsReady() and (State.Target:DebuffDown(S.FlameShockDebuff) and not S.Tempest:IsAvailable()) then
        if FS.APL.cast(S.FlameShock, State.Target, State, "flame_shock single 72") then return true end
    end

    -- doom_winds,if=talent.elemental_spirits.enabled
    if S.DoomWinds:IsReady() and (S.ElementalSpirits:IsAvailable()) then
        if FS.APL.cast(S.DoomWinds, State.Target, State, "doom_winds single 74") then return true end
    end

    -- lava_lash,if=talent.elemental_assault.enabled&talent.tempest.enabled&talent.molten_assault.enabled&talent.deeply_rooted_elements.enabled&dot.flame_shock.ticking
    if S.LavaLash:IsCastable() and (S.ElementalAssault:IsAvailable() and S.Tempest:IsAvailable() and S.MoltenAssault:IsAvailable() and S.DeeplyRootedElements:IsAvailable() and State.Target:Debuff_up(S.FlameShockDebuff)) then
        if FS.APL.cast(S.LavaLash, State.Target, State, "lava_lash single 76") then return true end
    end

    -- ice_strike,if=talent.elemental_assault.enabled&talent.swirling_maelstrom.enabled
    if S.IceStrike:IsReady() and (S.ElementalAssault:IsAvailable() and S.SwirlingMaelstrom:IsAvailable()) then
        if FS.APL.cast(S.IceStrike, State.Target, State, "ice_strike single 78") then return true end
    end

    -- lightning_bolt,if=buff.arc_discharge.up
    if S.LightningBolt:IsCastable() and (State.Player:buff_up(S.ArcDischargeBuff)) then
        if FS.APL.cast(S.LightningBolt, State.Target, State, "lightning_bolt single 80") then return true end
    end

    -- lava_lash,if=talent.elemental_assault.enabled&talent.tempest.enabled&talent.molten_assault.enabled&dot.flame_shock.ticking
    if S.LavaLash:IsCastable() and (S.ElementalAssault:IsAvailable() and S.Tempest:IsAvailable() and S.MoltenAssault:IsAvailable() and State.Target:Debuff_up(S.FlameShockDebuff)) then
        if FS.APL.cast(S.LavaLash, State.Target, State, "lava_lash single 82") then return true end
    end

    -- frost_shock,if=buff.hailstorm.up&buff.ice_strike.up&talent.swirling_maelstrom.enabled&talent.tempest.enabled
    if S.FrostShock:IsCastable() and (State.Player:buff_up(S.HailstormBuff) and State.Player:buff_up(S.IceStrikeBuff) and S.SwirlingMaelstrom:IsAvailable() and S.Tempest:IsAvailable()) then
        if FS.APL.cast(S.FrostShock, State.Target, State, "frost_shock single 84") then return true end
    end

    -- flame_shock,if=!ticking
    if S.FlameShock:IsReady() and (State.Target:DebuffDown(S.FlameShockDebuff)) then
        if FS.APL.cast(S.FlameShock, State.Target, State, "flame_shock single 86") then return true end
    end

    -- lava_lash,if=talent.lashing_flames.enabled
    if S.LavaLash:IsCastable() and (S.LashingFlames:IsAvailable()) then
        if FS.APL.cast(S.LavaLash, State.Target, State, "lava_lash single 88") then return true end
    end

    -- ice_strike,if=!buff.ice_strike.up
    if S.IceStrike:IsReady() and (State.Player:BuffDown(S.IceStrikeBuff)) then
        if FS.APL.cast(S.IceStrike, State.Target, State, "ice_strike single 90") then return true end
    end

    -- frost_shock,if=buff.hailstorm.up
    if S.FrostShock:IsCastable() and (State.Player:buff_up(S.HailstormBuff)) then
        if FS.APL.cast(S.FrostShock, State.Target, State, "frost_shock single 92") then return true end
    end

    -- crash_lightning,if=talent.converging_storms.enabled
    if S.CrashLightning:IsReady() and (S.ConvergingStorms:IsAvailable()) then
        if FS.APL.cast(S.CrashLightning, State.Target, State, "crash_lightning single 94") then return true end
    end

    -- lava_lash
    if S.LavaLash:IsCastable() then
        if FS.APL.cast(S.LavaLash, State.Target, State, "lava_lash single 96") then return true end
    end

    -- ice_strike
    if S.IceStrike:IsReady() then
        if FS.APL.cast(S.IceStrike, State.Target, State, "ice_strike single 98") then return true end
    end

    -- windstrike
    if S.Windstrike:IsCastable() then
        if FS.APL.cast(S.Windstrike, State.Target, State, "windstrike single 100") then return true end
    end

    -- stormstrike
    if S.Stormstrike:IsReady() then
        if FS.APL.cast(S.Stormstrike, State.Target, State, "stormstrike single 102") then return true end
    end

    -- sundering
    if S.Sundering:IsReady() then
        if FS.APL.cast(S.Sundering, State.Target, State, "sundering single 104") then return true end
    end

    -- frost_shock
    if S.FrostShock:IsCastable() then
        if FS.APL.cast(S.FrostShock, State.Target, State, "frost_shock single 106") then return true end
    end

    -- crash_lightning
    if S.CrashLightning:IsReady() then
        if FS.APL.cast(S.CrashLightning, State.Target, State, "crash_lightning single 108") then return true end
    end

    -- fire_nova,if=active_dot.flame_shock
    if S.FireNova:IsReady() and (State.Target:Debuff_up(S.FlameShockDebuff)) then
        if FS.APL.cast(S.FireNova, nil, State, "fire_nova single 110") then return true end
    end

    -- earth_elemental
    if S.EarthElemental:IsCastable() then
        if FS.APL.cast(S.EarthElemental, nil, State, "earth_elemental single 112") then return true end
    end

    -- flame_shock
    if S.FlameShock:IsReady() then
        if FS.APL.cast(S.FlameShock, State.Target, State, "flame_shock single 114") then return true end
    end

    return false
end

return Single
