"""
Database module for PS SimC Parser
Contains mappings and data structures for PS API
"""
from typing import Dict, Any
from .utils.constants import SUPPORTED_SPECS

# Core spell categories
SPELL = 'spell'
BUFF = 'buff'
DEBUFF = 'debuff'
COOLDOWN = 'cooldown'
RESOURCE = 'resource'

# Spell info structure
SPELL_INFO = {
    'vengeance': {
        # Core abilities
        'immolation_aura': {
            'id': 258920,
            'name': 'Immolation Aura',
            'type': SPELL,
            'range': 8,
            'gcd': True,
        },
        'fel_devastation': {
            'id': 212084,
            'name': 'Fel Devastation',
            'type': SPELL,
            'range': 20,
            'gcd': True,
            'resource_cost': 50,
            'resource_type': 'fury',
        },
        'spirit_bomb': {
            'id': 247454,
            'name': 'Spirit Bomb',
            'type': SPELL,
            'range': 8,
            'gcd': True,
            'requires': 'soul_fragments',
        },
        'soul_cleave': {
            'id': 228477,
            'name': 'Soul Cleave',
            'type': SPELL,
            'range': 5,
            'gcd': True,
            'resource_cost': 30,
            'resource_type': 'fury',
        },
        
        # Defensive abilities
        'demon_spikes': {
            'id': 203720,
            'name': 'Demon Spikes',
            'type': SPELL,
            'buff_id': 203819,
            'gcd': False,
            'charges': 2,
            'recharge_time': 20,
        },
        'fiery_brand': {
            'id': 204021,
            'name': 'Fiery Brand',
            'type': SPELL,
            'debuff_id': 207771,
            'gcd': True,
            'cooldown': 60,
        },
        
        # Utility abilities
        'sigil_of_flame': {
            'id': 204596,
            'name': 'Sigil of Flame',
            'type': SPELL,
            'range': 30,
            'gcd': True,
            'charges': 1,
            'recharge_time': 30,
        },
        'throw_glaive': {
            'id': 204157,
            'name': 'Throw Glaive',
            'type': SPELL,
            'range': 30,
            'gcd': True,
        },

        # Additional core abilities
        'fracture': {
            'id': 263642,
            'name': 'Fracture',
            'type': SPELL,
            'range': 5,
            'gcd': True,
            'charges': 2,
            'recharge_time': 12,
            'resource_cost': 20,
            'resource_type': 'fury',
            'generates': {
                'soul_fragments': 2,
            },
        },
        'shear': {
            'id': 203782,
            'name': 'Shear',
            'type': SPELL,
            'range': 5,
            'gcd': True,
            'resource_cost': 10,
            'resource_type': 'fury',
            'generates': {
                'soul_fragments': 1,
            },
        },

        # Major cooldowns
        'metamorphosis': {
            'id': 187827,
            'name': 'Metamorphosis',
            'type': SPELL,
            'buff_id': 187827,
            'gcd': False,
            'cooldown': 180,
        },
        'bulk_extraction': {
            'id': 320341,
            'name': 'Bulk Extraction',
            'type': SPELL,
            'range': 8,
            'gcd': True,
            'cooldown': 90,
            'generates': {
                'soul_fragments': 5,
            },
        },

        # Movement abilities
        'infernal_strike': {
            'id': 189110,
            'name': 'Infernal Strike',
            'type': SPELL,
            'range': 30,
            'gcd': False,
            'charges': 2,
            'recharge_time': 20,
        },
        'felblade': {
            'id': 232893,
            'name': 'Felblade',
            'type': SPELL,
            'range': 15,
            'gcd': True,
            'cooldown': 15,
            'generates': {
                'fury': 40,
            },
        },

        # Sigils
        'sigil_of_misery': {
            'id': 207684,
            'name': 'Sigil of Misery',
            'type': SPELL,
            'range': 30,
            'gcd': True,
            'cooldown': 90,
        },
        'sigil_of_silence': {
            'id': 202137,
            'name': 'Sigil of Silence',
            'type': SPELL,
            'range': 30,
            'gcd': True,
            'cooldown': 60,
        },
        'sigil_of_chains': {
            'id': 202138,
            'name': 'Sigil of Chains',
            'type': SPELL,
            'range': 30,
            'gcd': True,
            'cooldown': 90,
        },

        # Talents
        'agonizing_flames': {
            'id': 207548,
            'name': 'Agonizing Flames',
            'type': SPELL,
            'passive': True,
        },
        'feast_of_souls': {
            'id': 207697,
            'name': 'Feast of Souls',
            'type': SPELL,
            'buff_id': 207693,
            'passive': True,
        },
        'fallout': {
            'id': 227174,
            'name': 'Fallout',
            'type': SPELL,
            'passive': True,
        },
        'burning_alive': {
            'id': 207739,
            'name': 'Burning Alive',
            'type': SPELL,
            'passive': True,
        },
        'charred_flesh': {
            'id': 336639,
            'name': 'Charred Flesh',
            'type': SPELL,
            'passive': True,
        },

        # Additional talents
        'concentrated_sigils': {
            'id': 207666,
            'name': 'Concentrated Sigils',
            'type': SPELL,
            'passive': True,
        },
        'quickened_sigils': {
            'id': 209281,
            'name': 'Quickened Sigils',
            'type': SPELL,
            'passive': True,
        },
        'demonic': {
            'id': 213410,
            'name': 'Demonic',
            'type': BUFF,
            'duration': 6,
        },
        'soul_barrier': {
            'id': 263648,
            'name': 'Soul Barrier',
            'type': BUFF,
            'duration': 12,
            'cooldown': 30,
            'requires': 'soul_fragments',
        },
        'feed_the_demon': {
            'id': 218612,
            'name': 'Feed the Demon',
            'type': SPELL,
            'passive': True,
        },
        'fracture': {
            'id': 263642,
            'name': 'Fracture',
            'type': SPELL,
            'range': 5,
            'gcd': True,
            'resource_cost': 40,
            'resource_type': 'fury',
            'charges': 2,
            'recharge_time': 12,
        },
        'last_resort': {
            'id': 209258,
            'name': 'Last Resort',
            'type': SPELL,
            'passive': True,
            'buff_id': 209261,
        },
        'void_reaver': {
            'id': 268175,
            'name': 'Void Reaver',
            'type': SPELL,
            'passive': True,
        },
        'spirit_bomb': {
            'id': 247454,
            'name': 'Spirit Bomb',
            'type': SPELL,
            'range': 8,
            'gcd': True,
            'requires': 'soul_fragments',
            'min_fragments': 1,
            'max_fragments': 5,
        },
        # Covenant abilities
        'elysian_decree': {
            'id': 306830,
            'name': 'Elysian Decree',
            'type': SPELL,
            'range': 30,
            'gcd': True,
            'cooldown': 60,
        },
        'sinful_brand': {
            'id': 317009,
            'name': 'Sinful Brand',
            'type': SPELL,
            'debuff_id': 317009,
            'range': 5,
            'gcd': True,
            'cooldown': 60,
        },
        
        # Additional defensive abilities
        'empower_wards': {
            'id': 218256,
            'name': 'Empower Wards',
            'type': SPELL,
            'buff_id': 218256,
            'gcd': False,
            'cooldown': 20,
            'duration': 6,
        },
        
        # Additional talents
        'abyssal_strike': {
            'id': 207550,
            'name': 'Abyssal Strike',
            'type': SPELL,
            'passive': True,
        },
        'consume_magic': {
            'id': 278326,
            'name': 'Consume Magic',
            'type': SPELL,
            'range': 30,
            'gcd': False,
            'cooldown': 10,
        },
        'torment': {
            'id': 185245,
            'name': 'Torment',
            'type': SPELL,
            'range': 30,
            'gcd': False,
            'cooldown': 8,
        },
    }
}

# Resource information
RESOURCE_INFO = {
    'fury': {
        'type': 'primary',
        'max': 120,
        'min': 0,
        'getter': 'Player.Fury'
    },
    'soul_fragments': {
        'type': 'secondary',
        'max': 5,
        'min': 0,
        'getter': 'Player.SoulFragments'
    },
    'health': {
        'type': 'vital',
        'max': 100,
        'min': 0,
        'getter': 'Player.Health'
    }
}

# Tier Set Information
TIER_SET_INFO = {
    'vengeance': {
        't29_2pc': {
            'id': 393628,
            'name': "Blazing Determination",
            'description': "Immolation Aura increases your Armor by 20% for 5 sec.",
            'type': BUFF
        },
        't29_4pc': {
            'id': 393629,
            'name': "Burning Focus",
            'description': "While Immolation Aura is active, your abilities cost 10% less Fury.",
            'type': BUFF
        },
        't30_2pc': {
            'id': 405579,
            'name': "Fel Bombardment",
            'description': "Immolation Aura deals 20% increased damage and has a 15% chance to reset the cooldown of Fel Devastation.",
            'type': BUFF
        },
        't30_4pc': {
            'id': 405580,
            'name': "Overwhelming Power",
            'description': "When Fel Devastation deals damage, you gain a stack of Overwhelming Power, increasing your Mastery by 2% for 8 sec, stacking up to 5 times.",
            'type': BUFF
        }
    }
}

# Combat mechanics
COMBAT_MECHANICS = {
    'player': {
        'active_mitigation': 'Player:HasActiveMitigation()',
        'defensives_active': 'Player:HasDefensivesActive()',
        'health_actual': 'Player:HealthActual()',
        'health_max': 'Player:HealthMax()',
        'health_pct': 'Player:HealthPercent()',
        'in_combat': 'Player:InCombat()',
        'is_casting': 'Player:IsCasting()',
        'is_moving': 'Player:IsMoving()',
        'position': 'Player:Position()',
        'time_to_die': 'Player:TimeToDie()'
    },
    'target': {
        'health_actual': 'Target:HealthActual()',
        'health_max': 'Target:HealthMax()',
        'health_pct': 'Target:HealthPercent()',
        'is_boss': 'Target:IsBoss()',
        'is_demon': 'Target:IsDemon()',
        'time_to_die': 'Target:TimeToDie()',
        'distance': 'Target:Distance()'
    }
}

# Racial abilities
RACIAL_INFO = {
    'bloodelf': {
        'arcane_torrent': {
            'id': 202719,
            'name': 'Arcane Torrent',
            'type': SPELL,
            'gcd': False,
            'resource_gain': 15,
            'resource_type': 'fury'
        }
    },
    'nightborne': {
        'arcane_pulse': {
            'id': 260364,
            'name': 'Arcane Pulse',
            'type': SPELL,
            'gcd': True
        }
    }
}

# Trinket effects
TRINKET_INFO = {
    'algethar_puzzle_box': {
        'id': 193701,
        'name': "Algeth'ar Puzzle Box",
        'type': SPELL,
        'gcd': False,
        'cooldown': 180,
        'buff': {
            'id': 383781,
            'name': 'Prophetic Vision',
            'duration': 30
        }
    }
}

# Legendary effects
LEGENDARY_INFO = {
    'vengeance': {
        'darkglare_medallion': {
            'id': 355886,
            'name': "Darkglare Medallion",
            'effects': {
                'fel_devastation': {
                    'cooldown_reduction': 20,
                    'duration_increase': 2,
                },
            },
        },
        'fiery_soul': {
            'id': 355996,
            'name': "Fiery Soul",
            'effects': {
                'fiery_brand': {
                    'charges': 1,
                    'duration_increase': 4,
                },
            },
        },
        'razelikhs_defilement': {
            'id': 355890,
            'name': "Razelikh's Defilement",
            'effects': {
                'sigil_of_flame': {
                    'damage_increase': 1.25,
                    'generates': {'soul_fragments': 2},
                },
            },
        },
    }
}

# Conduit effects
CONDUIT_INFO = {
    'vengeance': {
        'growing_inferno': {
            'id': 339228,
            'name': "Growing Inferno",
            'effects': {
                'immolation_aura': {
                    'damage_increase_per_tick': 0.26,  # Scales with rank
                },
            },
        },
        'fel_defender': {
            'id': 339229,
            'name': "Fel Defender",
            'effects': {
                'demon_spikes': {
                    'duration_increase': 0.9,  # Scales with rank
                },
            },
        },
        'royal_decree': {
            'id': 340030,
            'name': "Royal Decree",
            'effects': {
                'elysian_decree': {
                    'damage_increase': 0.25,  # Scales with rank
                },
            },
        },
    }
}

# Spell interactions and modifiers
SPELL_INTERACTIONS = {
    'vengeance': {
        'metamorphosis': {
            'modifies': {
                'all_fury_generation': 1.5,  # 50% increased generation
                'armor': 1.2,  # 20% increased armor
            },
        },
        'demon_spikes': {
            'modifies': {
                'armor': 1.2,  # 20% increased armor
                'parry': 0.1,  # 10% increased parry
            },
        },
        'fiery_brand': {
            'modifies': {
                'target_damage': 0.4,  # 40% damage reduction
                'damage_taken': 0.6,  # With talent
            },
        },
    }
}

# Combat state tracking
COMBAT_STATES = {
    'player': {
        'in_combat': 'Player:AffectingCombat()',
        'moving': 'Player:IsMoving()',
        'casting': 'Player:IsCasting()',
        'channeling': 'Player:IsChanneling()',
        'jumping': 'Player:IsJumping()',
        'falling': 'Player:IsFalling()',
        'mounted': 'Player:IsMounted()',
        'flying': 'Player:IsFlying()',
        'resting': 'Player:IsResting()',
        'stealthed': 'Player:IsStealthed()',
        'in_vehicle': 'Player:InVehicle()',
    },
    'target': {
        'exists': 'Target:Exists()',
        'is_enemy': 'Target:IsEnemy()',
        'is_boss': 'Target:IsABoss()',
        'is_player': 'Target:IsAPlayer()',
        'classification': 'Target:Classification()',
        'is_casting': 'Target:IsCasting()',
        'cast_remains': 'Target:CastRemains()',
        'cast_pct': 'Target:CastPercentage()',
    },
    'combat': {
        'time': 'Combat:GetTime()',
        'remains': 'Combat:Remains()',
        'execute_phase': 'Combat:IsInExecutePhase()',
        'bloodlust': 'Combat:HasBloodlust()',
    },
}

# Common expressions and their PS API equivalents
EXPRESSION_MAPPINGS = {
    # Resources
    'fury': 'Player.Fury',
    'soul_fragments': 'Player.SoulFragments',
    
    # Target info
    'target.health.pct': 'Target.HealthPercent',
    'target.time_to_die': 'Target.TimeToDie',
    'target.distance': 'Target.Distance',
    
    # Player info
    'health.pct': 'Player.HealthPercent',
    'spell_targets': 'Enemies.Count',
    'active_enemies': 'Enemies.Count',
    
    # Combat timing
    'time': 'Combat:GetTime()',
    'gcd.max': 'Player.GCD',
    
    # Combat state
    'in_combat': 'Player:AffectingCombat()',
    'moving': 'Player:IsMoving()',
    'fight_remains': 'Combat:Remains()',
    
    # Resources
    'fury.deficit': 'Player.FuryDeficit',
    'fury.max': 'Player.FuryMax',
    'fury.pct': 'Player.FuryPercent',
    'soul_fragments.deficit': 'Player.SoulFragmentsDeficit',
    
    # Spell states
    'charges': 'Spell.{spell}:Charges()',
    'full_recharge_time': 'Spell.{spell}:FullRechargeTime()',
    'cast_time': 'Spell.{spell}:CastTime()',
    'execute_time': 'Spell.{spell}:ExecuteTime()',
    
    # Buff/debuff tracking
    'buff.duration': 'Player.Buff({spell}).Duration',
    'buff.remains': 'Player.Buff({spell}).Remains',
    'buff.stack': 'Player.Buff({spell}).Stack',
    'debuff.duration': 'Target.Debuff({spell}).Duration',
    'debuff.remains': 'Target.Debuff({spell}).Remains',
    'debuff.stack': 'Target.Debuff({spell}).Stack',

    # Advanced combat states
    'boss': 'Target:IsABoss()',
    'raid_event.movement.in': 'Combat:NextMovementIn()',
    'raid_event.adds.in': 'Combat:NextAddsIn()',
    'desired_targets': 'Combat:GetDesiredTargets()',
    
    # Advanced resource tracking
    'fury.time_to_max': 'Player:TimeToMaxFury()',
    'fury.deficit_pct': 'Player:FuryDeficitPercentage()',
    'soul_fragments.time_to_max': 'Player:TimeToMaxSoulFragments()',
    
    # Advanced buff tracking
    'buff.X.refreshable': 'Player.Buff({spell}):IsRefreshable()',
    'buff.X.expiring': 'Player.Buff({spell}):IsExpiring()',
    'debuff.X.refreshable': 'Target.Debuff({spell}):IsRefreshable()',
    'debuff.X.expiring': 'Target.Debuff({spell}):IsExpiring()',
    
    # Spell queueing and planning
    'next_wi_bomb': 'Player:NextWildfireInfusion()',
    'contagion': 'Target:ContagionRemains()',
    'time_to_shard': 'Player:TimeToShard()',
}

# Condition templates for common checks
CONDITION_TEMPLATES = {
    'buff.X.up': 'Player.Buff({spell}).Exists',
    'buff.X.down': 'not Player.Buff({spell}).Exists',
    'debuff.X.up': 'Target.Debuff({spell}).Exists',
    'debuff.X.down': 'not Target.Debuff({spell}).Exists',
    'cooldown.X.ready': 'Spell.{spell}:IsReady()',
    'charges_fractional': 'Spell.{spell}:ChargesFractional()',
    'full_recharge_time': 'Spell.{spell}:FullRechargeTime()',
    'fury.deficit': 'Player.FuryDeficit',
    'fury.max': 'Player.FuryMax',
    'fury.pct': 'Player.FuryPercent',
    'soul_fragments.deficit': 'Player.SoulFragmentsDeficit',
    'buff.X.remains': 'Player.Buff({spell}).Remains',
    'buff.X.duration': 'Player.Buff({spell}).Duration',
    'buff.X.stack': 'Player.Buff({spell}).Stack',
    'buff.X.react': 'Player.Buff({spell}).React',
    'debuff.X.remains': 'Target.Debuff({spell}).Remains',
    'debuff.X.duration': 'Target.Debuff({spell}).Duration',
    'debuff.X.stack': 'Target.Debuff({spell}).Stack',
    'cooldown.X.remains': 'Spell.{spell}:CooldownRemains()',
    'cooldown.X.duration': 'Spell.{spell}:CooldownDuration()',
    'cooldown.X.charges': 'Spell.{spell}:Charges()',
    'cooldown.X.full_recharge_time': 'Spell.{spell}:FullRechargeTime()',
    'time_to_die': 'Target.TimeToDie',
    'time_to_shard': 'TimeToShard()',
    'in_combat': 'Player:AffectingCombat()',
    'moving': 'Player:IsMoving()',
    'range': 'Target.Distance',
    'prev_gcd.X': 'Player:PrevGCD(1, Spell.{spell})',
    'prev.X': 'Player:PrevOffGCD(1, Spell.{spell})',
    'casting.X': 'Player:IsCasting(Spell.{spell})',

    # Advanced combat conditions
    'boss&fight_remains>': 'Target:IsABoss() and Combat:Remains() > {value}',
    'target.time_to_pct_X': 'Target:TimeToHealthPercentage({value})',
    'target.health.pct_to_die': 'Target:HealthPercentageToPoint({value})',
    
    # Advanced resource conditions
    'fury.time_to_max<': 'Player:TimeToMaxFury() < {value}',
    'soul_fragments.time_to_X': 'Player:TimeToSoulFragments({value})',
    
    # Advanced buff conditions
    'buff.X.stack_react': 'Player.Buff({spell}):StackReact()',
    'buff.X.remains_expected': 'Player.Buff({spell}):RemainsExpected()',
    'debuff.X.stack_react': 'Target.Debuff({spell}):StackReact()',
    
    # Spell interaction conditions
    'spell_targets.X': 'Enemies:GetCount({spell})',
    'active_dot.X': 'Enemies:ActiveDotCount({spell})',
    'active_enemies': 'Enemies:GetCount()',
}

# Additional Combat States
COMBAT_STATES.update({
    'player': {
        'active_mitigation': 'Player:HasActiveMitigation()',
        'defensives_active': 'Player:HasDefensivesActive()',
        'health_actual': 'Player:HealthActual()',
        'health_max': 'Player:HealthMax()',
        'health_deficit': 'Player:HealthDeficit()',
        'health_loss_per_second': 'Player:HealthLossPerSecond()',
        'incoming_damage_5s': 'Player:IncomingDamage(5)',
        'time_to_die': 'Player:TimeToDie()',
        'distance_to_target': 'Player:DistanceToTarget()',
    },
    'enemies': {
        'in_melee': 'Enemies:InMeleeRange()',
        'in_range': 'Enemies:InRange({range})',
        'count_in_range': 'Enemies:CountInRange({range})',
        'strongest': 'Enemies:Strongest()',
        'weakest': 'Enemies:Weakest()',
        'time_to_die': 'Enemies:TimeToDie()',
        'cast_remains': 'Enemies:CastRemains()',
    },
    'group': {
        'in_party': 'Player:InParty()',
        'in_raid': 'Player:InRaid()',
        'group_size': 'Group:Size()',
        'tanks': 'Group:Tanks()',
        'healers': 'Group:Healers()',
        'dps': 'Group:DPS()',
    },
})

# Additional Expressions
EXPRESSION_MAPPINGS.update({
    # Advanced combat mechanics
    'incoming_damage_5s': 'Player:IncomingDamage(5)',
    'incoming_damage_30s': 'Player:IncomingDamage(30)',
    'incoming_magic_5s': 'Player:IncomingMagicDamage(5)',
    'incoming_physical_5s': 'Player:IncomingPhysicalDamage(5)',
    'health_actual': 'Player:HealthActual()',
    'health_loss_per_second': 'Player:HealthLossPerSecond()',
    'time_to_die': 'Player:TimeToDie()',
    
    # Advanced targeting
    'enemies_in_melee': 'Enemies:InMeleeRange()',
    'enemies_in_range': 'Enemies:InRange({range})',
    'strongest_enemy': 'Enemies:Strongest()',
    'weakest_enemy': 'Enemies:Weakest()',
    
    # Advanced resource tracking
    'soul_fragments.active': 'Player:ActiveSoulFragments()',
    'soul_fragments.total': 'Player:TotalSoulFragments()',
    'soul_fragments.incoming': 'Player:IncomingSoulFragments()',
    
    # Advanced buff/debuff tracking
    'buff.X.extended_by': 'Player.Buff({spell}):ExtendedBy()',
    'debuff.X.extended_by': 'Target.Debuff({spell}):ExtendedBy()',
    'buff.X.remains_expected': 'Player.Buff({spell}):RemainsExpected()',
    
    # Advanced spell tracking
    'spell.X.in_flight': 'Spell.{spell}:InFlight()',
    'spell.X.traveling': 'Spell.{spell}:Traveling()',
    'spell.X.impact_time': 'Spell.{spell}:ImpactTime()',
})

# Additional Conditions
CONDITION_TEMPLATES.update({
    # Advanced combat conditions
    'incoming_damage_5s>': 'Player:IncomingDamage(5) > {value}',
    'health_loss_per_second>': 'Player:HealthLossPerSecond() > {value}',
    'enemies_in_range.X': 'Enemies:CountInRange({value})',
    'strongest_enemy.health.pct>': 'Enemies:Strongest():HealthPercentage() > {value}',
    
    # Advanced resource conditions
    'soul_fragments.active>=': 'Player:ActiveSoulFragments() >= {value}',
    'soul_fragments.incoming>=': 'Player:IncomingSoulFragments() >= {value}',
    
    # Advanced buff conditions
    'buff.X.extended_by.Y': 'Player.Buff({spell}):ExtendedBy({value})',
    'debuff.X.extended_by.Y': 'Target.Debuff({spell}):ExtendedBy({value})',
    
    # Advanced spell conditions
    'spell.X.in_flight': 'Spell.{spell}:InFlight()',
    'spell.X.traveling': 'Spell.{spell}:Traveling()',
    
    # Group conditions
    'group.size>=': 'Group:Size() >= {value}',
    'group.tanks>=': 'Group:Tanks() >= {value}',
    'group.healers>=': 'Group:Healers() >= {value}',
})

# Helper functions
def get_tier_bonus(spec: str, tier: str, piece_count: int) -> Dict[str, Any]:
    """Get tier set bonus information"""
    if spec not in TIER_SET_INFO:
        return {}
    bonus_name = f't{tier}_{piece_count}pc'
    return TIER_SET_INFO[spec].get(bonus_name, {})

def get_racial_ability(race: str, ability_name: str) -> Dict[str, Any]:
    """Get racial ability information"""
    if race not in RACIAL_INFO:
        return {}
    return RACIAL_INFO[race].get(ability_name, {})

def get_trinket_effect(trinket_name: str) -> Dict[str, Any]:
    """Get trinket effect information"""
    return TRINKET_INFO.get(trinket_name, {})

def get_combat_mechanic(mechanic_type: str, ability_name: str) -> str:
    """Get combat mechanic information"""
    if mechanic_type not in COMBAT_MECHANICS:
        return ''
    return COMBAT_MECHANICS[mechanic_type].get(ability_name, '')

def get_spell_info(spec: str, spell_name: str) -> Dict[str, Any]:
    """Get spell information for a given spec and spell name"""
    if spec not in SPELL_INFO:
        return {}
    return SPELL_INFO[spec].get(spell_name, {})

def get_resource_info(resource_type: str) -> Dict[str, Any]:
    """Get resource information for a given resource type"""
    return RESOURCE_INFO.get(resource_type, {})

def get_expression_mapping(expr: str) -> str:
    """Get PS API equivalent for a SimC expression"""
    return EXPRESSION_MAPPINGS.get(expr, '')