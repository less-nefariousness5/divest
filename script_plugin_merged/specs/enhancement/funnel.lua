-- Funnel APL for Enhancement Shaman
local buff_manager = require("common/modules/buff_manager")
local spell_helper = require("common/utility/spell_helper")
local unit_helper = require("common/utility/unit_helper")

local S = FS.Enhancement.Spells
local Helpers = require("specs/enhancement/helpers")

local function Funnel()
    local Enh = FS.Enhancement.Variables
    local State = FS.state

    -- feral_spirit,if=talent.elemental_spirits.enabled
    if S.FeralSpirit:IsCastable() and (S.ElementalSpirits:IsAvailable()) then
        if FS.APL.cast(S.FeralSpirit, nil, State, "feral_spirit funnel 2") then return true end
    end

    -- surging_totem
    if S.SurgingTotem:IsReady() then
        if FS.APL.cast(S.SurgingTotem, nil, State, "surging_totem funnel 4") then return true end
    end

    -- ascendance
    if Helpers.CDsON() and S.Ascendance:IsCastable() then
        if FS.APL.cast(S.Ascendance, nil, State, "ascendance funnel 6") then return true end
    end

    -- windstrike,if=(talent.thorims_invocation.enabled&buff.maelstrom_weapon.stack>0)|buff.converging_storms.stack=buff.converging_storms.max_stack
    if S.Windstrike:IsCastable() and ((S.ThorimsInvocation:IsAvailable() and Enh.maelstrom_stacks > 0) or State.Player:BuffStack(S.ConvergingStormsBuff) == Helpers.MaxConvergingStormsStacks) then
        if FS.APL.cast(S.Windstrike, State.Target, State, "windstrike funnel 8") then return true end
    end

    -- tempest,if=buff.maelstrom_weapon.stack=buff.maelstrom_weapon.max_stack|(buff.maelstrom_weapon.stack>=5&(tempest_mael_count>30|buff.awakening_storms.stack=2))
    if S.TempestAbility:IsReady() and (Enh.maelstrom_stacks == Enh.max_maelstrom_stacks or (Enh.maelstrom_stacks >= 5 and (Enh.tempest_maelstrom > 30 or State.Player:BuffStack(S.AwakeningStormsBuff) == 2))) then
        if FS.APL.cast(S.TempestAbility, State.Target, State, "tempest funnel 10") then return true end
    end

    -- lightning_bolt,if=((active_dot.flame_shock=active_enemies|active_dot.flame_shock=6)&buff.primordial_wave.up&buff.maelstrom_weapon.stack=buff.maelstrom_weapon.max_stack&(!buff.splintered_elements.up|fight_remains<=12))
    if S.LightningBolt:IsCastable() and ((S.FlameShockDebuff:AuraActiveCount(State.Player) == Enh.enemies_melee_count or S.FlameShockDebuff:AuraActiveCount(State.Player) >= 6) and State.Player:buff_up(S.PrimordialWaveBuff) and Enh.maelstrom_stacks == Enh.max_maelstrom_stacks and (State.Player:BuffDown(S.SplinteredElementsBuff) or Enh.fight_remains <= 12)) then
        if FS.APL.cast(S.LightningBolt, State.Target, State, "lightning_bolt funnel 12") then return true end
    end

    -- elemental_blast,if=buff.maelstrom_weapon.stack>=5&talent.elemental_spirits.enabled&feral_spirit.active>=4
    if S.ElementalBlast:IsReady() and (Enh.maelstrom_stacks >= 5 and S.ElementalSpirits:IsAvailable() and Enh.feral_spirit_count >= 4) then
        if FS.APL.cast(S.ElementalBlast, State.Target, State, "elemental_blast funnel 14") then return true end
    end

    -- lightning_bolt,if=talent.supercharge.enabled&buff.maelstrom_weapon.stack=buff.maelstrom_weapon.max_stack&(variable.expected_lb_funnel>variable.expected_cl_funnel)
    if S.LightningBolt:IsCastable() and (S.Supercharge:IsAvailable() and Enh.maelstrom_stacks == Enh.max_maelstrom_stacks and (Enh.expected_lb_funnel > Enh.expected_cl_funnel)) then
        if FS.APL.cast(S.LightningBolt, State.Target, State, "lightning_bolt funnel 16") then return true end
    end

    -- chain_lightning,if=(talent.supercharge.enabled&buff.maelstrom_weapon.stack=buff.maelstrom_weapon.max_stack)|buff.arc_discharge.up&buff.maelstrom_weapon.stack>=5
    if S.ChainLightning:IsCastable() and ((S.Supercharge:IsAvailable() and Enh.maelstrom_stacks == Enh.max_maelstrom_stacks) or State.Player:buff_up(S.ArcDischargeBuff) and Enh.maelstrom_stacks >= 5) then
        if FS.APL.cast(S.ChainLightning, State.Target, State, "chain_lightning funnel 18") then return true end
    end

    -- lava_lash,if=(talent.molten_assault.enabled&dot.flame_shock.ticking&(active_dot.flame_shock<active_enemies)&active_dot.flame_shock<6)|(talent.ashen_catalyst.enabled&buff.ashen_catalyst.stack=buff.ashen_catalyst.max_stack)
    if S.LavaLash:IsCastable() and ((S.MoltenAssault:IsAvailable() and State.Target:Debuff_up(S.FlameShockDebuff) and (S.FlameShockDebuff:AuraActiveCount(State.Player) < Enh.enemies_melee_count) and S.FlameShockDebuff:AuraActiveCount(State.Player) < 6) or (S.AshenCatalyst:IsAvailable() and State.Player:BuffStack(S.AshenCatalystBuff) == Helpers.MaxAshenCatalystStacks)) then
        if FS.APL.cast(S.LavaLash, State.Target, State, "lava_lash funnel 20") then return true end
    end

    -- primordial_wave,target_if=min:dot.flame_shock.remains,if=!buff.primordial_wave.up
    if S.PrimordialWave:IsReady() and (State.Player:BuffDown(S.PrimordialWaveBuff)) then
        if FS.APL.castTargetIf(true, S.PrimordialWave, Enh.enemies_melee, "min", Helpers.EvaluateTargetIfFilterPrimordialWave, nil, State, "primordial_wave funnel 22") then return true end
    end

    -- elemental_blast,if=(!talent.elemental_spirits.enabled|(talent.elemental_spirits.enabled&(charges=max_charges|buff.feral_spirit.up)))&buff.maelstrom_weapon.stack=buff.maelstrom_weapon.max_stack
    if S.ElementalBlast:IsReady() and ((not S.ElementalSpirits:IsAvailable() or (S.ElementalSpirits:IsAvailable() and (S.ElementalBlast:Charges() == S.ElementalBlast:MaxCharges() or State.Player:buff_up(S.FeralSpiritBuff)))) and Enh.maelstrom_stacks == Enh.max_maelstrom_stacks) then
        if FS.APL.cast(S.ElementalBlast, State.Target, State, "elemental_blast funnel 24") then return true end
    end

    -- feral_spirit
    if S.FeralSpirit:IsCastable() then
        if FS.APL.cast(S.FeralSpirit, nil, State, "feral_spirit funnel 26") then return true end
    end

    -- doom_winds
    if S.DoomWinds:IsCastable() then
        if FS.APL.cast(S.DoomWinds, State.Target, State, "doom_winds funnel 28") then return true end
    end

    -- stormstrike,if=buff.converging_storms.stack=buff.converging_storms.max_stack
    if S.Stormstrike:IsReady() and (State.Player:BuffStack(S.ConvergingStormsBuff) == Helpers.MaxConvergingStormsStacks) then
        if FS.APL.cast(S.Stormstrike, State.Target, State, "stormstrike funnel 30") then return true end
    end

    -- lava_burst,if=(buff.molten_weapon.stack>buff.crackling_surge.stack)&buff.maelstrom_weapon.stack=buff.maelstrom_weapon.max_stack
    if S.LavaBurst:IsReady() and ((Enh.molten_weapon_stacks > Enh.crackling_surge_stacks) and Enh.maelstrom_stacks == Enh.max_maelstrom_stacks) then
        if FS.APL.cast(S.LavaBurst, State.Target, State, "lava_burst funnel 32") then return true end
    end

    -- lightning_bolt,if=buff.maelstrom_weapon.stack=buff.maelstrom_weapon.max_stack&(variable.expected_lb_funnel>variable.expected_cl_funnel)
    if S.LightningBolt:IsCastable() and (Enh.maelstrom_stacks == Enh.max_maelstrom_stacks and (Enh.expected_lb_funnel > Enh.expected_cl_funnel)) then
        if FS.APL.cast(S.LightningBolt, State.Target, State, "lightning_bolt funnel 34") then return true end
    end

    -- chain_lightning,if=buff.maelstrom_weapon.stack=buff.maelstrom_weapon.max_stack
    if S.ChainLightning:IsCastable() and (Enh.maelstrom_stacks == Enh.max_maelstrom_stacks) then
        if FS.APL.cast(S.ChainLightning, State.Target, State, "chain_lightning funnel 36") then return true end
    end

    -- crash_lightning,if=buff.doom_winds.up|!buff.crash_lightning.up|(talent.alpha_wolf.enabled&feral_spirit.active&alpha_wolf_min_remains=0)|(talent.converging_storms.enabled&buff.converging_storms.stack<buff.converging_storms.max_stack)
    if S.CrashLightning:IsReady() and (State.Player:buff_up(S.DoomWindsBuff) or State.Player:BuffDown(S.CrashLightningBuff) or (S.AlphaWolf:IsAvailable() and State.Player:buff_up(S.FeralSpiritBuff) and Helpers.AlphaWolfMinRemains() == 0) or (S.ConvergingStorms:IsAvailable() and State.Player:BuffStack(S.ConvergingStormsBuff) < Helpers.MaxConvergingStormsStacks)) then
        if FS.APL.cast(S.CrashLightning, State.Target, State, "crash_lightning funnel 38") then return true end
    end

    -- sundering,if=buff.doom_winds.up|talent.earthsurge.enabled
    if S.Sundering:IsReady() and (State.Player:buff_up(S.DoomWindsBuff) or S.Earthsurge:IsAvailable()) then
        if FS.APL.cast(S.Sundering, State.Target, State, "sundering funnel 40") then return true end
    end

    -- fire_nova,if=active_dot.flame_shock=6|(active_dot.flame_shock>=4&active_dot.flame_shock=active_enemies)
    if S.FireNova:IsReady() and (S.FlameShockDebuff:AuraActiveCount(State.Player) == 6 or (S.FlameShockDebuff:AuraActiveCount(State.Player) >= 4 and S.FlameShockDebuff:AuraActiveCount(State.Player) >= Enh.enemies_melee_count)) then
        if FS.APL.cast(S.FireNova, nil, State, "fire_nova funnel 42") then return true end
    end

    -- ice_strike,if=talent.hailstorm.enabled&!buff.ice_strike.up
    if S.IceStrike:IsReady() and (S.Hailstorm:IsAvailable() and State.Player:BuffDown(S.IceStrikeBuff)) then
        if FS.APL.cast(S.IceStrike, State.Target, State, "ice_strike funnel 44") then return true end
    end

    -- frost_shock,if=talent.hailstorm.enabled&buff.hailstorm.up
    if S.FrostShock:IsCastable() and (S.Hailstorm:IsAvailable() and State.Player:buff_up(S.HailstormBuff)) then
        if FS.APL.cast(S.FrostShock, State.Target, State, "frost_shock funnel 46") then return true end
    end

    -- sundering
    if S.Sundering:IsReady() then
        if FS.APL.cast(S.Sundering, State.Target, State, "sundering funnel 48") then return true end
    end

    -- flame_shock,if=talent.molten_assault.enabled&!ticking
    if S.FlameShock:IsReady() and (S.MoltenAssault:IsAvailable() and State.Target:DebuffDown(S.FlameShockDebuff)) then
        if FS.APL.cast(S.FlameShock, State.Target, State, "flame_shock funnel 50") then return true end
    end

    -- flame_shock,target_if=min:dot.flame_shock.remains,if=(talent.fire_nova.enabled|talent.primordial_wave.enabled)&(active_dot.flame_shock<active_enemies)&active_dot.flame_shock<6
    if S.FlameShock:IsReady() and ((S.FireNova:IsAvailable() or S.PrimordialWave:IsAvailable()) and (S.FlameShockDebuff:AuraActiveCount(State.Player) < Enh.enemies_melee_count) and S.FlameShockDebuff:AuraActiveCount(State.Player) < 6) then
        if FS.APL.cast(S.FlameShock, State.Target, State, "flame_shock funnel 52") then return true end
    end

    -- fire_nova,if=active_dot.flame_shock>=3
    if S.FireNova:IsReady() and (S.FlameShockDebuff:AuraActiveCount(State.Player) >= 3) then
        if FS.APL.cast(S.FireNova, nil, State, "fire_nova funnel 54") then return true end
    end

    -- stormstrike,if=buff.crash_lightning.up&talent.deeply_rooted_elements.enabled
    if S.Stormstrike:IsReady() and (State.Player:buff_up(S.CrashLightningBuff) and S.DeeplyRootedElements:IsAvailable()) then
        if FS.APL.cast(S.Stormstrike, State.Target, State, "stormstrike funnel 56") then return true end
    end

    -- crash_lightning,if=talent.crashing_storms.enabled&buff.cl_crash_lightning.up&active_enemies>=4
    if S.CrashLightning:IsReady() and (S.CrashingStorms:IsAvailable() and State.Player:buff_up(S.CLCrashLightningBuff) and Enh.enemies_melee_count >= 4) then
        if FS.APL.cast(S.CrashLightning, State.Target, State, "crash_lightning funnel 58") then return true end
    end

    -- windstrike
    if S.Windstrike:IsCastable() then
        if FS.APL.cast(S.Windstrike, State.Target, State, "windstrike funnel 60") then return true end
    end

    -- stormstrike
    if S.Stormstrike:IsReady() then
        if FS.APL.cast(S.Stormstrike, State.Target, State, "stormstrike funnel 62") then return true end
    end

    -- ice_strike
    if S.IceStrike:IsReady() then
        if FS.APL.cast(S.IceStrike, State.Target, State, "ice_strike funnel 64") then return true end
    end

    -- lava_lash
    if S.LavaLash:IsCastable() then
        if FS.APL.cast(S.LavaLash, State.Target, State, "lava_lash funnel 66") then return true end
    end

    -- crash_lightning
    if S.CrashLightning:IsReady() then
        if FS.APL.cast(S.CrashLightning, State.Target, State, "crash_lightning funnel 68") then return true end
    end

    -- fire_nova,if=active_dot.flame_shock>=2
    if S.FireNova:IsReady() and (S.FlameShockDebuff:AuraActiveCount(State.Player) >= 2) then
        if FS.APL.cast(S.FireNova, nil, State, "fire_nova funnel 70") then return true end
    end

    -- elemental_blast,if=(!talent.elemental_spirits.enabled|(talent.elemental_spirits.enabled&(charges=max_charges|buff.feral_spirit.up)))&buff.maelstrom_weapon.stack>=5
    if S.ElementalBlast:IsReady() and ((not S.ElementalSpirits:IsAvailable() or (S.ElementalSpirits:IsAvailable() and (S.ElementalBlast:Charges() == S.ElementalBlast:MaxCharges() or State.Player:buff_up(S.FeralSpiritBuff)))) and Enh.maelstrom_stacks >= 5) then
        if FS.APL.cast(S.ElementalBlast, State.Target, State, "elemental_blast funnel 72") then return true end
    end

    -- lava_burst,if=(buff.molten_weapon.stack>buff.crackling_surge.stack)&buff.maelstrom_weapon.stack>=5
    if S.LavaBurst:IsReady() and ((Enh.molten_weapon_stacks > Enh.crackling_surge_stacks) and Enh.maelstrom_stacks >= 5) then
        if FS.APL.cast(S.LavaBurst, State.Target, State, "lava_burst funnel 74") then return true end
    end

    -- lightning_bolt,if=buff.maelstrom_weapon.stack>=5&(variable.expected_lb_funnel>variable.expected_cl_funnel)
    if S.LightningBolt:IsCastable() and (Enh.maelstrom_stacks >= 5 and (Enh.expected_lb_funnel > Enh.expected_cl_funnel)) then
        if FS.APL.cast(S.LightningBolt, State.Target, State, "lightning_bolt funnel 76") then return true end
    end

    -- chain_lightning,if=buff.maelstrom_weapon.stack>=5
    if S.ChainLightning:IsReady() and (Enh.maelstrom_stacks >= 5) then
        if FS.APL.cast(S.ChainLightning, State.Target, State, "chain_lightning funnel 78") then return true end
    end

    -- flame_shock,if=!ticking
    if S.FlameShock:IsReady() and (State.Target:DebuffDown(S.FlameShockDebuff)) then
        if FS.APL.cast(S.FlameShock, State.Target, State, "flame_shock funnel 80") then return true end
    end

    -- frost_shock,if=!talent.hailstorm.enabled
    if S.FrostShock:IsCastable() and (not S.Hailstorm:IsAvailable()) then
        if FS.APL.cast(S.FrostShock, State.Target, State, "frost_shock funnel 82") then return true end
    end

    return false
end

return Funnel
