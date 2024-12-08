-- Helper functions for Enhancement Shaman APL
local unit_helper = require("common/utility/unit_helper")

local Helpers = {
    -- Shared variables
    MaxAshenCatalystStacks = 8,
    MaxConvergingStormsStacks = 6,
    MaxTempestStacks = 2,

    CDsON = function()
        return true
    end,

    AoEON = function()
        return true
    end,

    RangedTargetCount = function(range)
        local EnemiesTable = FS.state.Playerget_enemies_in_range(range)
        local TarCount = 1
        for k, v in pairs(EnemiesTable) do
            local Enemy = EnemiesTable[k]
            if Enemy ~= FS.state.Target and (Enemy:AffectingCombat() or Enemy:IsDummy()) then
                TarCount = TarCount + 1
            end
        end
        return TarCount
    end,

    TotemFinder = function(Totem, ReturnTime)
        return 0
    end,

    AlphaWolfMinRemains = function()
        if not S.AlphaWolf:IsAvailable() or FS.state.Player:BuffDown(S.FeralSpiritBuff) then
            return 0
        end
        local AWStart = math.min(S.CrashLightning:TimeSinceLastCast(), S.ChainLightning:TimeSinceLastCast())
        if AWStart > 8 or AWStart > S.FeralSpirit:TimeSinceLastCast() then
            return 0
        end
        return 8 - AWStart
    end,

    EvaluateTargetIfFilterLightningRodRemains = function(TargetUnit)
        return TargetUnit:DebuffRemains(S.LightningRodDebuff)
    end,

    EvaluateTargetIfFilterPrimordialWave = function(TargetUnit)
        return TargetUnit:DebuffRemains(S.FlameShockDebuff)
    end,

    EvaluateTargetIfPrimordialWave = function(TargetUnit)
        return FS.state.Player:BuffDown(S.PrimordialWaveBuff)
    end,

    EvaluateTargetIfFilterLavaLash = function(TargetUnit)
        return TargetUnit:DebuffRemains(S.LashingFlamesDebuff)
    end,

    EvaluateCycleFlameShock = function(TargetUnit)
        return TargetUnit:DebuffRefreshable(S.FlameShockDebuff)
    end
}

return Helpers
