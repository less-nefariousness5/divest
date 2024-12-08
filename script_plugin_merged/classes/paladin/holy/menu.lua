-- By Project Sylvanas
-- Holy Paladin Plugin: Menu

local tag = "holy_paladin_apl_"
---@type control_panel_helper
local control_panel_helper = require("common/utility/control_panel_helper")
---@type plugin_helper
local plugin_helper = require("common/utility/plugin_helper")
---@type key_helper
local key_helper = require("common/utility/key_helper")

local menu_elements = {
    main_tree = core.menu.tree_node(),
    enable_script_check = core.menu.checkbox(false, tag .. "enable_script_check"),

    enable_toggle = core.menu.keybind(999, false, tag .. "enable_toggle"),
    kamala_mode_toggle = core.menu.keybind(999, false, tag .. "kamala_mode_toggle"),

    cooldowns_tree = core.menu.tree_node(),
    healing_tree = core.menu.tree_node(),
    beacon_tree = core.menu.tree_node(),

    -- Cooldown settings
    loh_hp = core.menu.slider_int(0, 100, 35, tag .. "loh_hp"),
    ac_count = core.menu.slider_int(1, 10, 4, tag .. "ac_count"),
    ac_hp = core.menu.slider_int(0, 100, 80, tag .. "ac_hp"),
    dt_count = core.menu.slider_int(1, 10, 3, tag .. "dt_count"),
    dt_hp = core.menu.slider_int(0, 100, 75, tag .. "dt_hp"),

    -- Core healing settings
    holy_shock_hp = core.menu.slider_int(0, 100, 85, tag .. "holy_shock_hp"),
    holy_shock_hp2 = core.menu.slider_int(0, 100, 80, tag .. "holy_shock_hp2"),
    holy_shock_hp_rs = core.menu.slider_int(0, 100, 90, tag .. "holy_shock_hp_rs"),
    wog_hp = core.menu.slider_int(0, 100, 85, tag .. "wog_hp"),
    wog_tank_hp = core.menu.slider_int(0, 100, 90, tag .. "wog_tank_hp"),

    -- Beacon settings
    bov_count = core.menu.slider_int(1, 10, 4, tag .. "bov_count"),
    bov_hp = core.menu.slider_int(0, 100, 85, tag .. "bov_hp"),

    enable_ac = core.menu.keybind(999, false, tag .. "enable_ac"),
}

local function render_menu()
    menu_elements.main_tree:render("FS Holy Paladin", function()
        menu_elements.enable_toggle:render("Enable Script")
        menu_elements.kamala_mode_toggle:render("Kamala Mode", "Auto Target enemies for damaging spells")
        --if not plugin_helper:is_toggle_enabled(menu_elements.enable_toggle) then return end

        menu_elements.cooldowns_tree:render("Cooldowns", function()
            menu_elements.enable_ac:render("Auto AC", "Enables automatic usage of AC with the settings below")
            menu_elements.loh_hp:render("Lay on Hands HP%", "Health percentage to use Lay on Hands")
            menu_elements.ac_count:render("Avenging Crusader Count", "Minimum number of targets below HP threshold")
            menu_elements.ac_hp:render("Avenging Crusader HP%", "Health percentage threshold for Avenging Crusader")
            menu_elements.dt_count:render("Divine Toll Count", "Minimum number of targets below HP threshold")
            menu_elements.dt_hp:render("Divine Toll HP%", "Health percentage threshold for Divine Toll")
        end)

        menu_elements.healing_tree:render("Core Abilities", function()
            menu_elements.holy_shock_hp:render("Holy Shock HP%", "Health percentage to use Holy Shock")
            menu_elements.holy_shock_hp2:render("Holy Shock HP% (2 Charges)",
                "Health percentage to use Holy Shock with 2 charges")
            menu_elements.holy_shock_hp_rs:render("Holy Shock HP% (Rising Sunlight)",
                "Health percentage to use Holy Shock with Rising Sunlight")
            menu_elements.wog_hp:render("Word of Glory HP%", "Health percentage to use Word of Glory")
            menu_elements.wog_tank_hp:render("Word of Glory Tank HP%", "Health percentage to use Word of Glory on tanks")
        end)

        menu_elements.beacon_tree:render("Beacon Settings", function()
            menu_elements.bov_count:render("Beacon of Virtue Count", "Minimum number of targets below HP threshold")
            menu_elements.bov_hp:render("Beacon of Virtue HP%", "Health percentage threshold for Beacon of Virtue")
        end)
    end)
end

local function render_control_panel(control_panel_elements)
    -- Main toggle
    control_panel_helper:insert_toggle(control_panel_elements,
        {
            name = "[FS Holy Paladin] Enable (" ..
                key_helper:get_key_name(menu_elements.enable_toggle:get_key_code()) .. ") ",
            keybind = menu_elements.enable_toggle
        })
    control_panel_helper:insert_toggle(control_panel_elements,
        {
            name = "[FS Holy Paladin] Auto AC (" ..
                key_helper:get_key_name(menu_elements.enable_ac:get_key_code()) .. ") ",
            keybind = menu_elements.enable_ac
        })
    control_panel_helper:insert_toggle(control_panel_elements,
        {
            name = "[FS Holy Paladin] Kamala Mode (" ..
                key_helper:get_key_name(menu_elements.kamala_mode_toggle:get_key_code()) .. ") ",
            keybind = menu_elements.kamala_mode_toggle
        })

    return control_panel_elements
end

return {
    elements = menu_elements,
    render = render_menu,
    render_control_panel = render_control_panel,
}
