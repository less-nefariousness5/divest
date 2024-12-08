-- Retribution Paladin Spell IDs
local Spell = require("core/spell")

local S = {
    -- Abilities
    ---@type Spell
    ArcaneTorrent            = Spell(50613),
    ---@type Spell
    AvengingWrath            = Spell(31884),
    ---@type Spell
    BladeOfJustice           = Spell(184575),
    ---@type Spell
    BlessingOfAnsheRet       = Spell(391054),
    ---@type Spell
    CrusaderStrike           = Spell(35395),
    ---@type Spell
    Crusade                  = Spell(231895),
    ---@type Spell
    DivineStorm              = Spell(53385),
    ---@type Spell
    DivineToll               = Spell(375576),
    ---@type Spell
    ExecutionSentence        = Spell(343527),
    ---@type Spell
    FinalReckoning           = Spell(343721),
    ---@type Spell
    FinalVerdict             = Spell(383328),
    ---@type Spell
    HammerOfLight            = Spell(427453),
    ---@type Spell
    HammerOfWrath            = Spell(24275),
    ---@type Spell
    Judgment                 = Spell(20271),
    ---@type Spell
    ShieldOfVengeance        = Spell(184662),
    ---@type Spell
    TemplarSlash             = Spell(406647),
    ---@type Spell
    TemplarStrike            = Spell(407480),
    ---@type Spell
    TemplarsVerdict          = Spell(85256),
    ---@type Spell
    WakeOfAshes              = Spell(255937),

    -- Talents
    ---@type Spell
    BlessedChampion          = Spell(403010),
    ---@type Spell
    BladeOfVengeance         = Spell(403042),
    ---@type Spell
    BoundlessJudgment        = Spell(405278),
    ---@type Spell
    CrusadingStrikes         = Spell(404542),
    ---@type Spell
    DivineAuxiliary          = Spell(406158),
    ---@type Spell
    DivineHammer             = Spell(198034),
    ---@type Spell
    ExecutionersWill         = Spell(406940),
    ---@type Spell
    HolyBlade                = Spell(383342),
    ---@type Spell
    HolyFlames               = Spell(406106),
    ---@type Spell
    JusticarsVengeance       = Spell(215661),
    ---@type Spell
    LightsGuidance           = Spell(391124),
    ---@type Spell
    RadiantGlory             = Spell(458359),
    ---@type Spell
    TempestOfTheLightbringer = Spell(383396),
    ---@type Spell
    VanguardsMomentum        = Spell(383314),
    ---@type Spell
    VengefulWrath            = Spell(384052),

    -- Buffs
    ---@type Spell
    AvengingWrathBuff        = Spell(31884),
    ---@type Spell
    BlessingOfAnsheRetBuff   = Spell(391054),
    ---@type Spell
    CrusadeBuff              = Spell(231895),
    ---@type Spell
    DivineArbiterBuff        = Spell(406975),
    ---@type Spell
    DivinePurposeBuff        = Spell(223819),
    ---@type Spell
    DivineResonanceBuff      = Spell(384029),
    ---@type Spell
    EchoesOfWrathBuff        = Spell(409438),
    ---@type Spell
    EmpyreanLegacyBuff       = Spell(387178),
    ---@type Spell
    EmpyreanPowerBuff        = Spell(326733),
    ---@type Spell
    ExecutionersWillBuff     = Spell(406940),
    ---@type Spell
    FinalVerdictBuff         = Spell(383328),
    ---@type Spell
    InquisitorsBuff          = Spell(384376),
    ---@type Spell
    RadiantDecreeBuff        = Spell(384293),
    ---@type Spell
    RighteousVerdictBuff     = Spell(267611),
    ---@type Spell
    TemplarSlashBuff         = Spell(406647),
    ---@type Spell
    TemplarStrikesBuff       = Spell(407480),
    ---@type Spell
    VanguardsMomentumBuff    = Spell(383314),

    -- Debuffs
    ---@type Spell
    ExecutionSentenceDebuff  = Spell(343527),
    ---@type Spell
    ExpurgationDebuff        = Spell(383346),
    ---@type Spell
    FinalReckoningDebuff     = Spell(343721),
    ---@type Spell
    JudgmentDebuff           = Spell(197277)
}

S.Crusade.custom_condition = function()
    return not S.RadiantGlory:is_learned()
end

S.CrusaderStrike.custom_condition = function()
    return not S.CrusadingStrikes:is_learned()
end

S.HammerOfWrath.custom_condition = function()
    if FS.state.target_is_valid and FS.state.target:health_percentage() < 20 then
        return true
    end
    return FS.state.player:buff_up(Spell(454373))
end

S.HammerOfLight.custom_condition = function()
    return FS.state.player:aura_up(Spell(427441))
end

return S
