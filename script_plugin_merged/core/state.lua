require("core/unit")
require("core/spell")

-- Create State module with self-initialization
FS.state = {
    -- Module state
    _initialized = false,
    _initializing = false,

    -- Public state
    ---@type Unit
    player = nil,
    ---@type Unit
    target = nil,
    target_is_valid = false,
    next_run = 0,
    last_update = 0,
    combat_time = 0,
    fight_remains = 11111,
    boss_fight_remains = 11111,
}

-- Private functions
local function verify_state()
    if not FS.state.player then
        return false, "player is not initialized"
    end
    if not FS.state.initialize then
        return false, "initialize function is missing"
    end
    if not FS.state.update then
        return false, "update function is missing"
    end
    if not FS.state.can_run then
        return false, "can_run function is missing"
    end
    return true
end

-- Public functions
function FS.state.initialize(player_go)
    -- Prevent recursive initialization
    if FS.state._initializing then
        return FS.state
    end

    -- Skip if already initialized
    if FS.state._initialized then
        return FS.state
    end

    FS.state._initializing = true

    -- Validate input
    if not player_go then
        FS.state._initializing = false
        error("Cannot initialize State: player_go is nil")
    end

    -- Create new Player instance
    FS.state.player = Unit(player_go)

    -- Initialize target if it exists
    local target = player_go:get_target()
    if target then
        FS.state.target = Unit(target)
        FS.state.target_is_valid = FS.state.player:can_attack(FS.state.target)
    else
        FS.state.target = nil
        FS.state.target_is_valid = false
    end

    -- Initialize timers
    FS.state.next_run = core:game_time()
    FS.state.last_update = core:game_time()
    FS.state.combat_time = 0

    -- Verify initialization
    local success, err = verify_state()
    if not success then
        FS.state._initializing = false
        error("State verification failed: " .. err)
    end

    FS.state._initialized = true
    FS.state._initializing = false
    return FS.state
end

function FS.state.update()
    if not FS.state._initialized then
        error("Cannot update State: not initialized")
    end

    -- Create new Player instance
    FS.state.player = Unit(core.object_manager.get_local_player())

    if FS.state.player.go == nil then
        return false
    end

    -- Update target
    local target = FS.state.player.go:get_target()
    if target then
        FS.state.target = Unit(target)
        FS.state.target_is_valid = FS.state.player:can_attack(FS.state.target) and not target:is_dead()
    else
        FS.state.target = nil
        FS.state.target_is_valid = false
    end

    -- Update combat time and fight remains
    if FS.state.target_is_valid or FS.state.player:is_in_combat() then
        FS.state.combat_time = FS.api.plugin_helper:get_current_combat_length_seconds()
        FS.state.boss_fight_remains = FS.api.combat_forecast:get_forecast() / 1000
        FS.state.fight_remains = FS.state.boss_fight_remains
        FS.state.active_enemies = FS.api.unit_helper:get_enemy_list_around(FS.state.player:get_position(), 40, false,
            false,
            false, false)
        if FS.state.fight_remains <= 0 then
            FS.state.fight_remains = 11111
        end
    end

    FS.state.last_update = core:game_time()

    return true
end

function FS.state.update_next_run()
    local delay = FS.state.get_random_delay()
    FS.state.next_run = core:game_time() + delay
end

function FS.state.get_random_delay()
    return math.random(FS.settings.min_delay(), FS.settings.max_delay());
    --return math.random(5000, 20000);
end

function FS.state.can_run()
    if not FS.state._initialized then
        return false
    end
    return core:game_time() >= FS.state.next_run
end

function FS.state.should_run()
    if not FS.state.can_run() then
        return false
    end
    return true
end

-- Verify module integrity
if not FS.state.initialize then
    error("State module failed to initialize properly: initialize function is missing")
end
