local plugin = {}

plugin["name"] = "FS Multi-Spec Plugin"
plugin["version"] = "1.0.0"
plugin["author"] = "FS"
plugin["load"] = true

-- Get local player
local local_player = core.object_manager.get_local_player()
if not local_player then
    core.log("Failed to load: Could not get local player")
    plugin["load"] = false
    return plugin
end

-- Get player info and log it
local player_class = local_player:get_class()
local player_spec_id = core.spell_book.get_specialization_id()
core.log(string.format("Debug - Player Class ID: %d, Spec ID: %d", player_class, player_spec_id))

---@type enums
local enums = require("common/enums")
core.log(string.format("Debug - Death Knight Class ID: %d", enums.class_id.DEATHKNIGHT))

-- Initialize FS global
FS = {}

-- Set class/spec flags with debug logging
FS.is_enhancement_shaman = player_class == enums.class_id.SHAMAN and
    player_spec_id == enums.class_spec_id.get_spec_id_from_enum(enums.class_spec_id.spec_enum.ENHANCEMENT_SHAMAN)
if FS.is_enhancement_shaman then core.log("Enhancement Shaman detected") end

FS.is_retribution_paladin = player_class == enums.class_id.PALADIN and
    player_spec_id == enums.class_spec_id.get_spec_id_from_enum(enums.class_spec_id.spec_enum.RETRIBUTION_PALADIN)
if FS.is_retribution_paladin then core.log("Retribution Paladin detected") end

FS.is_holy_paladin = player_class == enums.class_id.PALADIN and
    player_spec_id == enums.class_spec_id.get_spec_id_from_enum(enums.class_spec_id.spec_enum.HOLY_PALADIN)
if FS.is_holy_paladin then core.log("Holy Paladin detected") end

FS.is_blood_deathknight = player_class == enums.class_id.DEATHKNIGHT and
    player_spec_id == enums.class_spec_id.get_spec_id_from_enum(enums.class_spec_id.spec_enum.BLOOD_DEATHKNIGHT)
if FS.is_blood_deathknight then core.log("Blood Death Knight detected") end

-- Log the spec check results
core.log(string.format("Spec Check Results - Enhancement: %s, Ret: %s, Holy: %s, Blood: %s",
    tostring(FS.is_enhancement_shaman),
    tostring(FS.is_retribution_paladin),
    tostring(FS.is_holy_paladin),
    tostring(FS.is_blood_deathknight)))

-- Only load for supported classes
if not FS.is_enhancement_shaman and 
   not FS.is_retribution_paladin and 
   not FS.is_holy_paladin and 
   not FS.is_blood_deathknight then
    core.log("No supported spec detected - plugin will not load")
    plugin["load"] = false
    return plugin
end

-- Log loaded spec
if FS.is_enhancement_shaman then
    core.log("Enhancement Shaman rotation loaded")
elseif FS.is_retribution_paladin then
    core.log("Retribution Paladin rotation loaded")
elseif FS.is_holy_paladin then
    core.log("Holy Paladin rotation loaded")
elseif FS.is_blood_deathknight then
    core.log("Blood Death Knight rotation loaded")
end

return plugin
