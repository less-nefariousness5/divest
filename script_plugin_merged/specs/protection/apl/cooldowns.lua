local APL = require("core/apl")
local State = require("core/state")
local S = require("specs/protection/ids")

local function Cooldowns()
    local Protection = FS.Protection

    if S.shield_block:is_castable() and (Protection.variables.rage >= 5 and State.combat_time < 5 or Protection.variables.rage >= 3 and State.combat_time > 5) then
    if APL.cast(S.shield_block, State.target, State, "shield_block cooldowns 1") then
        return true
    end
end

    return false
end

return Cooldowns