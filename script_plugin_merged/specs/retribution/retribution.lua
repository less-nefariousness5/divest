-- Retribution Paladin Implementation
local APL = require("core/apl")
local State = require("core/state")

-- Load APL modules
local S = require("specs/retribution/ids")
local Cooldowns = require("specs/retribution/apl/cooldowns")
local Generators = require("specs/retribution/apl/generators")
local Finishers = require("specs/retribution/apl/finishers")

-- Retribution Paladin specific implementation
FS.Retribution = {
    -- Spell IDs from ids.lua

    -- Variables used by the APL
    variables = {
        holy_power = 0,
        max_holy_power = 5,
        enemies_8y = {},
        enemies_8y_count = 0,
        combat_time = 0,
        fight_remains = 11111,
        boss_fight_remains = 11111,
        ---@type Spell
        verdict_spell = nil,
        -- Buff tracking
        crusade_up = false,
        crusade_stacks = 0,
        divine_hammer_active = false,
        divine_purpose_up = false,
        divine_resonance_up = false,
        echoes_of_wrath_up = false,
        empyrean_legacy_up = false,
        empyrean_power_up = false,
        executioners_will_up = false,
        final_verdict_up = false,
        inquisitors_up = false,
        radiant_decree_up = false,
        righteous_verdict_up = false,
        templar_slash_up = false,
        templar_strike_up = false,
        vanguards_momentum_up = false,
        -- Debuff tracking
        execution_sentence_up = false,
        final_reckoning_up = false,
        judgment_up = false
    },

    update_variables = function(self)
        -- Update holy power
        self.variables.holy_power = FS.state.player:holy_power()

        -- Update enemy counts
        self.variables.enemies_8y = FS.state.player:get_enemies_in_range(8)
        if FS.APL.aoe_on() then
            self.variables.enemies_8y_count = #self.variables.enemies_8y
        else
            self.variables.enemies_8y_count = 1
        end

        -- Update combat time and fight remains
        self.variables.combat_time = FS.state.combat_time
        self.variables.fight_remains = FS.state.fight_remains
        self.variables.boss_fight_remains = FS.state.boss_fight_remains

        -- Update verdict spell
        self.variables.verdict_spell = S.FinalVerdict:is_available() and S.FinalVerdict or
            S.TemplarsVerdict

        -- Update buff tracking
        self.variables.crusade_up = FS.state.player:buff_up(S.CrusadeBuff)
        self.variables.crusade_stacks = FS.state.player:buff_stack(S.CrusadeBuff)
        self.variables.divine_purpose_up = FS.state.player:buff_up(S.DivinePurposeBuff)
        self.variables.divine_resonance_up = FS.state.player:buff_up(S.DivineResonanceBuff)
        self.variables.echoes_of_wrath_up = FS.state.player:buff_up(S.EchoesOfWrathBuff)
        self.variables.empyrean_legacy_up = FS.state.player:buff_up(S.EmpyreanLegacyBuff)
        self.variables.empyrean_power_up = FS.state.player:buff_up(S.EmpyreanPowerBuff)
        self.variables.executioners_will_up = FS.state.player:buff_up(S.ExecutionersWillBuff)
        self.variables.final_verdict_up = FS.state.player:buff_up(S.FinalVerdictBuff)
        self.variables.inquisitors_up = FS.state.player:buff_up(S.InquisitorsBuff)
        self.variables.radiant_decree_up = FS.state.player:buff_up(S.RadiantDecreeBuff)
        self.variables.righteous_verdict_up = FS.state.player:buff_up(S.RighteousVerdictBuff)
        self.variables.templar_slash_up = FS.state.player:buff_up(S.TemplarSlashBuff)
        self.variables.templar_strike_up = FS.state.player:buff_up(S.TemplarStrikesBuff)
        self.variables.vanguards_momentum_up = FS.state.player:buff_up(S.VanguardsMomentumBuff)

        -- Update debuff tracking
        if FS.state.target_is_valid then
            self.variables.execution_sentence_up = FS.state.target:debuff_up(S.ExecutionSentenceDebuff)
            self.variables.final_reckoning_up = FS.state.target:debuff_up(S.FinalReckoningDebuff)
            self.variables.judgment_up = FS.state.target:debuff_up(S.JudgmentDebuff)
        end
    end,

    run = function(self)
        -- Update variables
        self:update_variables()

        -- Run appropriate action list
        if not FS.state.player:is_in_combat() then
            -- Precombat
            if S.ShieldOfVengeance:is_castable() then
                if APL.cast(S.ShieldOfVengeance, nil, FS.state, "shield_of_vengeance precombat") then return true end
            end

            if self.variables.verdict_spell:is_ready() and self.variables.holy_power >= 4 then
                if APL.cast(self.variables.verdict_spell, FS.state.target, FS.state, "verdict precombat") then return true end
            end

            if S.BladeOfJustice:is_castable() then
                if APL.cast(S.BladeOfJustice, FS.state.target, FS.state, "blade_of_justice precombat") then return true end
            end

            if S.Judgment:is_castable() then
                if APL.cast(S.Judgment, FS.state.target, FS.state, "judgment precombat") then return true end
            end

            if S.HammerOfWrath:is_ready() then
                if APL.cast(S.HammerOfWrath, FS.state.target, FS.state, "hammer_of_wrath precombat") then return true end
            end

            if S.CrusaderStrike:is_castable() then
                if APL.cast(S.CrusaderStrike, FS.state.target, FS.state, "crusader_strike precombat") then return true end
            end
        elseif FS.state.target_is_valid then
            -- Combat
            if Cooldowns() then return true end
            if Generators() then return true end
            -- Note: Finishers are called from within Generators when appropriate
        end

        return false
    end,

    render_menu = function()
        -- Retribution specific menu options can be added here
    end
}

-- Initialize
local function init()
    core.log("Retribution Paladin rotation has been updated for patch 11.0.2.")
end

init()

return FS.Retribution
