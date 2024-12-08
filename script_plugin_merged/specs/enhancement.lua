-- Enhancement Shaman Implementation
local buff_manager = require("common/modules/buff_manager")
local spell_helper = require("common/utility/spell_helper")
local unit_helper = require("common/utility/unit_helper")

-- Declare APL modules
local Single, SingleTotemic, Aoe, AoeTotemic, Funnel

-- Load our modules
local S = require("enhancement/ids")
local Helpers = require("enhancement/helpers")

-- Enhancement Shaman specific implementation
FS.Enhancement = {
    -- Spell IDs from ids.lua
    Spells = S,

    -- Variables used by the APL
    Variables = {
        maelstrom_stacks = 0,
        max_maelstrom_stacks = 0,
        enemies_melee = {},
        enemies_melee_count = 0,
        enemies_40y_count = 0,
        boss_fight_remains = 11111,
        fight_remains = 11111,
        ti_action = S.LightningBolt,
        -- Spirit wolf tracking
        molten_weapon_stacks = 0,
        icy_edge_stacks = 0,
        crackling_surge_stacks = 0,
        feral_spirit_count = 0,
        -- Tempest tracking
        tempest_maelstrom = 0
    },

    Settings = {
        Enhancement = {
            HealWith5Maelstrom = 60,
            HealWithout5Maelstrom = 40,
            Rotation = "Standard",
            TempestOnMTOnly = false
        },
        Commons = {
            ShieldsOOC = true,
            WeaponBuffsOOC = true,
            PreferEarthShield = false,
            IgnoreEarthShield = false
        }
    },

    update_variables = function(self)
        -- Update maelstrom
        self.Variables.maelstrom_stacks = FS.state.player:BuffStack(S.MaelstromWeaponBuff)
        self.Variables.max_maelstrom_stacks = S.RagingMaelstrom:IsAvailable() and 10 or 5

        -- Update enemy counts
        self.Variables.enemies_melee = FS.state.playerget_enemies_in_range(10)
        if Helpers.AoEON() then
            self.Variables.enemies_melee_count = #self.Variables.enemies_melee
            self.Variables.enemies_40y_count = Helpers.RangedTargetCount(40)
        else
            self.Variables.enemies_melee_count = 1
            self.Variables.enemies_40y_count = 1
        end

        -- Update fight remains
        if FS.state.TargetIsValid or FS.state.player:AffectingCombat() then
            self.Variables.boss_fight_remains = FS.APL:BossFightRemains()
            self.Variables.fight_remains = self.Variables.boss_fight_remains
            if self.Variables.fight_remains == 11111 then
                self.Variables.fight_remains = FS.APL:FightRemains()
            end
        end

        -- Update spirit wolves
        if FS.state.player:buff_up(S.FeralSpiritBuff) then
            self.Variables.molten_weapon_stacks = FS.state.player:BuffStack(382917)   -- Molten Weapon
            self.Variables.icy_edge_stacks = FS.state.player:BuffStack(382888)        -- Icy Edge
            self.Variables.crackling_surge_stacks = FS.state.player:BuffStack(382891) -- Crackling Surge
            self.Variables.feral_spirit_count = 6                                     -- TODO: Implement proper spirit counting
        else
            self.Variables.molten_weapon_stacks = 0
            self.Variables.icy_edge_stacks = 0
            self.Variables.crackling_surge_stacks = 0
            self.Variables.feral_spirit_count = 0
        end

        -- Update Tempest tracking
        if FS.state.player:buff_up(S.TempestBuff) then
            self.Variables.tempest_maelstrom = 30 -- TODO: Implement proper tempest tracking
        else
            self.Variables.tempest_maelstrom = 0
        end

        -- Update Thorim's Invocation tracking
        if FS.state.player:AffectingCombat() then
            if FS.state.player.last_spell_id == S.ChainLightning:ID() then
                self.Variables.ti_action = S.ChainLightning
            elseif FS.state.player.last_spell_id == S.LightningBolt:ID() then
                self.Variables.ti_action = S.LightningBolt
            end
        end
    end,

    run = function(self)
        -- Update our variables
        self:update_variables()

        -- Run the appropriate rotation based on enemy count and talents
        if self.Variables.enemies_melee_count < 2 and not S.SurgingTotem:IsAvailable() then
            return Single()
        elseif self.Variables.enemies_melee_count < 2 and S.SurgingTotem:IsAvailable() then
            return SingleTotemic()
        elseif Helpers.AoEON() and self.Variables.enemies_melee_count > 1 then
            if self.Settings.Enhancement.Rotation == "Standard" then
                if not S.SurgingTotem:IsAvailable() then
                    return Aoe()
                else
                    return AoeTotemic()
                end
            else
                return Funnel()
            end
        end
        return false
    end,

    render_menu = function()
        -- Enhancement specific menu options can be added here
    end
}

-- Initialize
local function init()
    -- Load APL modules
    Single = require("enhancement/single")
    SingleTotemic = require("enhancement/single_totemic")
    Aoe = require("enhancement/aoe")
    AoeTotemic = require("enhancement/aoe_totemic")
    Funnel = require("enhancement/funnel")
end

init()

return FS.Enhancement
