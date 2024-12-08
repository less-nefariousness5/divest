local APL = require("core/apl")
local State = require("core/state")
local S = require("specs/protection/ids")
local Finishers = require("specs/protection/apl/finishers")

local function Generators()
    local Protection = FS.Protection

    if Finishers() then return true end
    if S.thunder_clap:is_castable() and (Protection.variables.rage <= 3 or State.target:health_percentage() >= 0.2 or not S.demoralizing_shout:is_learned()) then
    if APL.cast(S.thunder_clap, State.target, State, "thunder_clap generators 1") then
        return true
    end
end
    if S.shield_blockr_strike:is_castable() then
    if APL.cast(S.shield_blockr_strike, State.target, State, "shield_blockr_strike generators 2") then
        return true
    end
end
    if S.ignore_pain:is_castable() then
    if APL.cast(S.ignore_pain, State.target, State, "ignore_pain generators 3") then
        return true
    end
end

    return false
end

return Generators