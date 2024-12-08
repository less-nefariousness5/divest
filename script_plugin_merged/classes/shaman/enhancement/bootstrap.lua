FS.enhancement = {
    variables = {
        flame_shock_count = 0
    },
}

-- Load APL modules
--require("classes/shaman/enhancement/ids")
--local single = require("classes/shaman/enhancement/apl/single")
--local single_totemic = require("classes/shaman/enhancement/apl/single_totemic")
--local aoe = require("classes/shaman/enhancement/apl/aoe")
--local aoe_totemic = require("classes/shaman/enhancement/apl/aoe_totemic")
--local funnel = require("classes/shaman/enhancement/apl/funnel")

function FS.enhancement.run()
    -- Update variables

    -- Run appropriate action list
    if not FS.state.player:is_in_combat() then
        -- Precombat
    elseif FS.state.target_is_valid then
        --FS.enhancement.variables.flame_shock_count = 0
        --core.log(tostring(FS.enhancement.variables.flame_shock_count))

        -- Combat
        --if not FS.enhancement.talents.surging_totem:is_learned() and single() then return true end
        --if not FS.enhancement.talents.surging_totem:is_learned() and single_totemic() then return true end
        --if not FS.enhancement.talents.surging_totem:is_learned() and aoe() then return true end
        --if FS.enhancement.talents.surging_totem:is_learned() and aoe_totemic() then return true end
        --if not FS.enhancement.talents.surging_totem:is_learned() and funnel() then return true end
    end

    return false
end

-- Initialize
local function init()
    core.log("Enhancement Shaman rotation")
end

init()

return FS.Enhancement
