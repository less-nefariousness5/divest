local APL = require("core/apl")
local State = require("core/state")
local S = require("specs/protection/ids")

local function Finishers()
    local Protection = FS.Protection

    Protection.variables.ds_castable = (S.shield_slam:targets() >= 2 or State.player:buff_up(S.unstoppable_force) or not S.booming_voice:is_learned() and S.heavy_repercussions:is_learned()) and not State.player:buff_up(S.best_served_cold) and not (State.player:buff_up(S.bolster_defenses) and State.player:buff_stack(S.bolster_defenses) > 24)
    if S.shield_slam:is_castable() and (Protection.variables.ds_castable and not State.player:buff_up(S.shield_block_ready) and (not S.shield_block:is_learned() or S.shield_block:cooldown_remaining() > State.player:gcd() * 3 or State.player:buff_up(S.shield_block) and State.player:buff_stack(S.shield_block) < 10 or S.last_stand:is_learned()) and (not State.player:buff_up(S.avatar) or S.avatar:cooldown_remaining() > 110 and Protection.variables.rage >= 4)) then
    if APL.cast(S.shield_slam, State.target, State, "shield_slam finishers 1") then
        return true
    end
end

    return false
end

return Finishers