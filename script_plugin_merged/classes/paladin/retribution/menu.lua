local tag = "retribution_paladin_apl_"
---@type control_panel_helper
local control_panel_helper = require("common/utility/control_panel_helper")
---@type plugin_helper
local plugin_helper = require("common/utility/plugin_helper")
---@type key_helper
local key_helper = require("common/utility/key_helper")

FS.retribution.menu = {
    main_tree = core.menu.tree_node(),
    enable_script_check = core.menu.checkbox(false, tag .. "enable_script_check"),

    enable_toggle = core.menu.keybind(999, false, tag .. "enable_toggle"),
}

function FS.retribution.render_menu()
    FS.retribution.menu.main_tree:render("FS Retri Paladin", function()
        FS.retribution.menu.enable_toggle:render("Enable Script")
        if not plugin_helper:is_toggle_enabled(FS.retribution.menu.enable_toggle) then return end
    end)
end

function FS.retribution.render_control_panel()
    local control_panel_elements = {}

    -- Main toggle
    control_panel_helper:insert_toggle(control_panel_elements,
        {
            name = "[FS Retri Paladin] Enable (" ..
                key_helper:get_key_name(FS.retribution.menu.enable_toggle:get_key_code()) .. ") ",
            keybind = FS.retribution.menu.enable_toggle
        })

    return control_panel_elements
end
