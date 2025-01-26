from typing import List

class LuaTemplate:
    def render_imports(self, imports: List[str]) -> str:
        return f"local {', '.join(imports)} = PS.API\n"

    def format_imports(self, imports: List[str]) -> str:
        """Format imports section (renamed from render_imports)"""
        return f"local {', '.join(imports)} = PS.API\n"

    @staticmethod
    def format_rotation(name: str, profile: str, class_name: str, spec: str, role: str = 'dps', action_lists: str = '') -> str:
        """Format the rotation table"""
        return f"""
    local Rotation = {{
        Name = "{name}",
        Profile = "{profile}",
        Class = "{class_name}",
        Spec = "{spec}",
        Role = "{role}",

        -- Configuration
        Settings = {{
            RotationMode = "Auto",
            UseCooldowns = true,
            UseDefensives = true,
            UseInterrupts = true,
            UseRacials = true,
            UseTrinkets = true,
            MinimumHealingPercent = 65,
            MinimumDefensivePercent = 40,
            MinimumInterruptPercent = 0,
            MaxEnemies = 8,
            MinEnemies = 1,
        }},

        -- Cache
        Cache = Cache,

        -- State
        LastCast = LastCast,
        LastGCD = LastGCD,
        LastOffGCD = LastOffGCD,
        CombatTime = CombatTime,
        TargetGUID = TargetGUID,
    }}

    function Rotation:Execute()
        -- Update state
        self:UpdateState()

        -- Cache frequently used values
        local Player = PS.Player
        local Target = Player.Target
        local Spell = PS.Spell
        local Item = PS.Item
        local Enemies = Player.Enemies

        -- Check if we have a valid target
        if not Target:Exists() or Target:IsDead() then
            return
        end

        -- Resource values
        local Fury = Player.Fury
        local SoulFragments = Player.SoulFragments

        -- Combat state
        local InCombat = Player:AffectingCombat()
        local HealthPercent = Player:HealthPercent()
        local TargetHealthPercent = Target:HealthPercent()
        local EnemiesCount = self:GetEnemiesInRange(8)
        local IsAOE = self:IsAOE()
        local IsCleave = self:IsCleave()

        -- Handle interrupts
        local interrupt = self:UseInterrupts()
        if interrupt then return interrupt end

        -- Handle defensives
        local defensive = self:UseDefensives()
        if defensive then return defensive end

        -- Handle items
        local item = self:UseItems()
        if item then return item end

        -- Main rotation
        return self:RunRotation()
    end

    function Rotation:RunRotation()
        -- Check for movement/casting
        if self:ShouldStop() then return end

        -- Check GCD
        if not self:CanUseGCD() then return end

        -- Run action lists
        local result = nil
        {action_lists}
        return result
    end

    return Rotation
    """

    def render(self, context: dict) -> str:
        """Render the template with the given context"""
        lua_code = []

        # Add imports
        if 'imports' in context:
            lua_code.append(self.format_imports(context['imports']))

        # Add metadata
        metadata = context.get('metadata', {})
        profile = metadata.get('profile', '')
        class_name = metadata.get('class', '')
        spec = metadata.get('spec', '')
        role = metadata.get('role', 'dps')
        name = metadata.get('name', '')

        # Add action lists
        action_lists_str = context.get('action_lists', '')

        # Add rotation
        lua_code.append(self.format_rotation(
            name=name,
            profile=profile,
            class_name=class_name,
            spec=spec,
            role=role,
            action_lists=action_lists_str
        ))

        return '\n'.join(lua_code) 