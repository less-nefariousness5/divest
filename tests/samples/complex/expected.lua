-- Generated by PS SimC Parser
local PS = ...
local Spell = PS.Spell
local Player = PS.Player
local Target = Player.Target
local Enemies = Player.Enemies
local Cache = {}

-- Initialize cache
function Cache:Get(key, default)
    return self[key] or default
end

function Cache:Set(key, value)
    self[key] = value
end

local Rotation = {
    Name = "Complex",
    Profile = "VDH-Complex",
    Class = "demonhunter",
    Spec = "vengeance",
    Role = "tank",
    Cache = Cache,
}

function Rotation:Execute()
    -- Check if we have a valid target
    if not Target:Exists() or Target:IsDead() then
        return
    end
    
    -- Update variables
    Cache:Set("defensive_condition", 
        Player:HealthPercent() < 65 or 
        Player:IncomingDamage(5) > 100000 or 
        (not Player.Buff(Spell.DemonSpikes):Exists() and Enemies:Count() >= 3)
    )
    Cache:Set("emergency_condition",
        Player:HealthPercent() < 40 and not Player.Buff(Spell.Metamorphosis):Exists()
    )
    Cache:Set("pool_fury",
        Player.Fury > 80 and 
        not Player.Buff(Spell.Metamorphosis):Exists() and 
        Spell.FelDevastation:CooldownRemains() <= 2
    )
    
    -- Cast Metamorphosis in emergency
    if Spell.Metamorphosis:IsReady() and Cache:Get("emergency_condition") then
        return Cast(Spell.Metamorphosis)
    end
    
    -- Cast Demon Spikes defensively
    if Spell.DemonSpikes:IsReady() and Cache:Get("defensive_condition") and not Player.Buff(Spell.DemonSpikes):Exists() then
        return Cast(Spell.DemonSpikes)
    end
    
    -- Cast Fiery Brand defensively
    if Spell.FieryBrand:IsReady() and Cache:Get("defensive_condition") and not Player.Buff(Spell.FieryBrand):Exists() then
        return Cast(Spell.FieryBrand)
    end
    
    -- Cast Spirit Bomb
    if Spell.SpiritBomb:IsReady() and Player.SoulFragments >= 4 and (Player.Buff(Spell.Metamorphosis):Exists() or not Cache:Get("pool_fury")) then
        return Cast(Spell.SpiritBomb)
    end
    
    -- Cast Fel Devastation
    if Spell.FelDevastation:IsReady() and (not Cache:Get("pool_fury") or Player.Buff(Spell.Metamorphosis):Exists()) then
        return Cast(Spell.FelDevastation)
    end
    
    -- Cast Soul Cleave
    if Spell.SoulCleave:IsReady() and Player.Fury >= 80 and not Cache:Get("pool_fury") then
        return Cast(Spell.SoulCleave)
    end
end

return Rotation 