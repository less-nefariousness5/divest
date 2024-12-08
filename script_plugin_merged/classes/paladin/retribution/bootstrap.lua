FS.retribution = {
    variables = {
        holy_power = 0
    },
}

require("classes/paladin/retribution/ids")
require("classes/paladin/retribution/menu")

--local Precombat = require("classes/paladin/retribution/apl/precombat")
require("classes/paladin/retribution/apl/finishers")
require("classes/paladin/retribution/apl/cooldowns")
require("classes/paladin/retribution/apl/generators")

function FS.retribution.update_variables()
    FS.retribution.variables.holy_power = FS.state.player:holy_power()
end

function FS.retribution.run()
    if not FS.api.plugin_helper:is_toggle_enabled(FS.retribution.menu.enable_toggle) then return end

    -- Run appropriate action list
    if not FS.state.player:is_in_combat() then
        -- Precombat
    elseif FS.state.target_is_valid and FS.state.player:is_in_combat() then
        -- Update variables
        FS.retribution:update_variables()

        FS.retribution.variables.finished = false
        if FS.retribution.cooldowns() then return true end
        FS.retribution.variables.finished = true
        if FS.retribution.generators() then return true end
    end

    return false
end

-- Initialize
local function init()
    core.log("Retribution Paladin rotation")
end

init()
