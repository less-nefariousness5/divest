-- Multi-Spec Plugin Implementation

---@type color
local color = require("common/color")
---@type plugin_helper
local plugin_helper = require("common/utility/plugin_helper")

local tag = "multi_spec_"

-- Initialize menu elements table first
local menu_elements = {
    main_tree = core.menu.tree_node(),
    enable_script_check = core.menu.checkbox(true, tag .. "enable_script_check"),
    spec_mode = core.menu.combobox(1, tag .. "spec_mode"),  -- Changed default to 1 to match 1-based indexing
    enable_bitch_mode = core.menu.keybind(999, false, tag .. "enable_bitch_mode"),
    humanizer = core.menu.header(),
    min_delay = core.menu.slider_int(0, 1500, 125, tag .. "min_delay"),
    max_delay = core.menu.slider_int(1, 1500, 250, tag .. "max_delay"),
}

-- Initialize FS table if it doesn't exist
FS = FS or {}

-- Initialize settings after menu_elements is defined
FS.settings = {
    ---@type fun(): boolean
    bitch_mode = function() return plugin_helper:is_toggle_enabled(menu_elements.enable_bitch_mode) end,
    ---@type fun(): integer
    min_delay = function() return menu_elements.min_delay:get() end,
    ---@type fun(): integer
    max_delay = function() return menu_elements.max_delay:get() end,
}

local function my_menu_render()
    menu_elements.main_tree:render("FS", function()
        menu_elements.enable_script_check:render("Enable Script")
        if not menu_elements.enable_script_check:get_state() then return end
        
        menu_elements.spec_mode:render("Hero Talent", {"Death-Bringer", "San'layn", "Blood"}, "Choose between Death-Bringer, San'layn, or Blood")
        menu_elements.enable_bitch_mode:render("Enable BitchMode", "In BitchMode you'll get humanized AF.")
        menu_elements.humanizer:render("Humanizer", color.white())
        menu_elements.min_delay:render("Min delay", "Min delay until next run.")
        menu_elements.max_delay:render("Max delay", "Min delay until next run.")
        
        -- Render spec-specific menus
        local selected_spec = menu_elements.spec_mode:get()
        if selected_spec == 2 then  -- San'layn spec
            if FS.is_blood_deathknight and FS.sanlayn then
                FS.sanlayn.menu.render()
            end
        elseif selected_spec == 3 then  -- Blood spec
            if FS.is_blood_deathknight and FS.blood then
                FS.blood.menu.render()
            end
        elseif FS.is_holy_paladin and FS.Holy then
            FS.holy.menu.render()
        elseif FS.is_enhancement_shaman and FS.Enhancement then
            -- Enhancement shaman menu rendering here
        elseif FS.is_retribution_paladin and FS.Retribution then
            FS.retribution.render_menu()
        end
    end)
end

local function on_control_panel_render()
    local control_panel_elements = {}

    -- Main toggle
    FS.api.control_panel_helper:insert_toggle(control_panel_elements,
        {
            name = "[FS] Enable BitchMode (" ..
                FS.api.key_helper:get_key_name(menu_elements.enable_bitch_mode:get_key_code()) .. ") ",
            keybind = menu_elements.enable_bitch_mode
        })

    if FS.is_holy_paladin and FS.Holy then
        control_panel_elements = FS.holy.menu.render_control_panel(control_panel_elements)
    elseif FS.is_enhancement_shaman and FS.Enhancement then
        -- Enhancement shaman menu rendering here
    elseif FS.is_retribution_paladin and FS.Retribution then
        return FS.retribution.render_control_panel()
    elseif FS.is_blood_deathknight and FS.blood then
        return FS.blood.menu.render_control_panel(control_panel_elements)
    end
    return control_panel_elements
end

local function my_on_update()
    if not menu_elements.enable_script_check:get_state() then
        return false
    end
    -- Basic checks

    -- Check if FS exists and is initialized
    if not FS then
        core.log("Error: FS is not initialized")
        return
    end

    -- Check if State exists and is initialized
    if not FS.state then
        core.log("Error: FS.State is not initialized")
        return
    end

    -- Check if State.player exists
    if not FS.state.player then
        core.log("Error: FS.State.player is not initialized")
        return
    end

    -- Check if we should run
    if not FS.state.should_run() then
        return
    end

    -- Update state
    FS.state.update_next_run()
    if not FS.state.update() then
        core.log("did not update")
        return false
    end

    -- Update spec-specific variables
    local selected_spec = menu_elements.spec_mode:get()
    if selected_spec == 2 then  -- San'layn spec
        if FS.is_blood_deathknight and FS.sanlayn then
            FS.sanlayn.update()
        end
    elseif selected_spec == 3 then  -- Blood spec
        if FS.is_blood_deathknight and FS.blood then
            FS.blood.update()
        end
    end

    -- Run spec-specific logic
    if FS.is_holy_paladin and FS.Holy then
        return FS.holy.run()
    elseif FS.is_enhancement_shaman and FS.Enhancement then
        -- Enhancement shaman logic here
    elseif FS.is_retribution_paladin and FS.Retribution then
        return FS.retribution.run()
    elseif FS.is_blood_deathknight and FS.blood then
        return FS.blood.run()
    end

    return false
end

local function my_on_render()
    local local_player = core.object_manager.get_local_player()
    if not local_player then return end

    if FS.is_holy_paladin and FS.holy and FS.holy.menu and not plugin_helper:is_toggle_enabled(FS.holy.menu.elements.enable_toggle) then
        plugin_helper:draw_text_character_center("DISABLED", color.yellow())
    end

    if FS.is_retribution_paladin and FS.retribution and FS.retribution.menu and not plugin_helper:is_toggle_enabled(FS.retribution.menu.enable_toggle) then
        plugin_helper:draw_text_character_center("DISABLED", color.yellow())
    end
end

-- Initialize
local function init()
    require("core/api")
    require("core/state")
    require("core/heal_absorb_manager")

    -- Load spec-specific modules
    if FS.is_holy_paladin then
        require("classes/paladin/holy/bootstrap")
    elseif FS.is_enhancement_shaman then
        require("classes/shaman/enhancement/bootstrap")
    elseif FS.is_retribution_paladin then
        require("classes/paladin/retribution/bootstrap")
    elseif FS.is_blood_deathknight then
        require("classes/deathknight/blood/bootstrap")
        require("classes/deathknight/sanlayn/bootstrap")  -- Add San'layn bootstrap
    end

    -- Verify FS was created
    if not FS then
        core.log("Error: FS was not created")
        return false
    end

    -- Verify State was initialized
    if not FS.state then
        core.log("Error: FS.state was not initialized")
        return false
    end

    local local_player = core.object_manager.get_local_player()
    if not local_player then return end
    FS.state.initialize(local_player)

    -- Verify State.player was initialized
    if not FS.state.player then
        core.log("Error: FS.state.player was not initialized")
        return false
    end

    return true
end

-- Start initialization
if init() then
    -- Only register callbacks if initialization was successful
    core.register_on_update_callback(my_on_update)
    core.register_on_render_callback(my_on_render)
    core.register_on_render_menu_callback(my_menu_render)
    core.register_on_render_control_panel_callback(on_control_panel_render)
    core.log("Plugin initialization complete")
else
    core.log("Failed to initialize plugin")
end
