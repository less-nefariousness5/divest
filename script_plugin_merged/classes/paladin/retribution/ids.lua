-- Retribution Paladin Spell IDs
require("core/spell")

local T = {
    -- Talents
    ---@type Spell
    a_just_reward                   = Spell(469411),
    ---@type Spell
    afterimage                      = Spell(385414),
    ---@type Spell
    auras_of_the_resolute           = Spell(385633),
    ---@type Spell
    blessed_calling                 = Spell(469770),
    ---@type Spell
    blessing_of_freedom             = Spell(1044),
    ---@type Spell
    blessing_of_protection          = Spell(1022),
    ---@type Spell
    blessing_of_sacrifice           = Spell(6940),
    ---@type Spell
    blinding_light                  = Spell(115750),
    ---@type Spell
    cavalier                        = Spell(230332),
    ---@type Spell
    cleanse_toxins                  = Spell(213644),
    ---@type Spell
    consecrated_ground              = Spell(204054),
    ---@type Spell
    divine_purpose                  = Spell(408459),
    ---@type Spell
    divine_reach                    = Spell(469476),
    ---@type Spell
    divine_resonance                = Spell(384027),
    ---@type Spell
    divine_spurs                    = Spell(469409),
    ---@type Spell
    divine_steed                    = Spell(190784),
    ---@type Spell
    divine_toll                     = Spell(375576),
    ---@type Spell
    empyreal_ward                   = Spell(387791),
    ---@type Spell
    eye_for_an_eye                  = Spell(469309),
    ---@type Spell
    faiths_armor                    = Spell(406101),
    ---@type Spell
    fist_of_justice                 = Spell(234299),
    ---@type Spell
    golden_path                     = Spell(377128),
    ---@type Spell
    greater_judgment                = Spell(231663),
    ---@type Spell
    hammer_of_wrath                 = Spell(24275),
    ---@type Spell
    healing_hands                   = Spell(326734),
    ---@type Spell
    holy_aegis                      = Spell(385515),
    ---@type Spell
    holy_reprieve                   = Spell(469445),
    ---@type Spell
    holy_ritual                     = Spell(199422),
    ---@type Spell
    improved_blessing_of_protection = Spell(384909),
    ---@type Spell
    inspired_guard                  = Spell(469439),
    ---@type Spell
    judgment_of_light               = Spell(183778),
    ---@type Spell
    lay_on_hands                    = Spell(633),
    ---@type Spell
    lead_the_charge                 = Spell(469780),
    ---@type Spell
    lightbearer                     = Spell(469416),
    ---@type Spell
    lightforged_blessing            = Spell(403479),
    ---@type Spell
    lights_countenance              = Spell(469325),
    ---@type Spell
    lights_revocation               = Spell(146956),
    ---@type Spell
    obduracy                        = Spell(385427),
    ---@type Spell
    of_dusk_and_dawn                = Spell(385125),
    ---@type Spell
    punishment                      = Spell(403530),
    ---@type Spell
    quickened_invocation            = Spell(379391),
    ---@type Spell
    rebuke                          = Spell(96231),
    ---@type Spell
    recompense                      = Spell(384914),
    ---@type Spell
    repentance                      = Spell(20066),
    ---@type Spell
    righteous_protection            = Spell(469321),
    ---@type Spell
    sacred_strength                 = Spell(469337),
    ---@type Spell
    sacrifice_of_the_just           = Spell(384820),
    ---@type Spell
    sanctified_plates               = Spell(402964),
    ---@type Spell
    seal_of_might                   = Spell(385450),
    ---@type Spell
    seal_of_the_crusader            = Spell(416770),
    ---@type Spell
    selfless_healer                 = Spell(469434),
    ---@type Spell
    stand_against_evil              = Spell(469317),
    ---@type Spell
    steed_of_liberty                = Spell(469304),
    ---@type Spell
    stoicism                        = Spell(469316),
    ---@type Spell
    turn_evil                       = Spell(10326),
    ---@type Spell
    unbound_freedom                 = Spell(305394),
    ---@type Spell
    unbreakable_spirit              = Spell(114154),
    ---@type Spell
    vengeful_wrath                  = Spell(406835),
    ---@type Spell
    worthy_sacrifice                = Spell(469279),
    ---@type Spell
    wrench_evil                     = Spell(460720),

    -- Retribution
    ---@type Spell
    adjudication                    = Spell(406157),
    ---@type Spell
    aegis_of_protection             = Spell(403654),
    ---@type Spell
    art_of_war                      = Spell(406064),
    ---@type Spell
    avenging_wrath                  = Spell(31884),
    ---@type Spell
    blade_of_justice                = Spell(184575),
    ---@type Spell
    blade_of_vengeance              = Spell(403826),
    ---@type Spell
    blades_of_light                 = Spell(403664),
    ---@type Spell
    blessed_champion                = Spell(403010),
    ---@type Spell
    boundless_judgment              = Spell(405278),
    ---@type Spell
    burn_to_ash                     = Spell(446663),
    ---@type Spell
    burning_crusade                 = Spell(405289),
    ---@type Spell
    crusade                         = Spell(231895),
    ---@type Spell
    crusading_strikes               = Spell(404542),
    ---@type Spell
    divine_arbiter                  = Spell(404306),
    ---@type Spell
    divine_auxiliary                = Spell(406158),
    ---@type Spell
    divine_hammer                   = Spell(198034),
    ---@type Spell
    divine_storm                    = Spell(53385),
    ---@type Spell
    divine_wrath                    = Spell(406872),
    ---@type Spell
    empyrean_legacy                 = Spell(387170),
    ---@type Spell
    empyrean_power                  = Spell(326732),
    ---@type Spell
    execution_sentence              = Spell(343527),
    ---@type Spell
    executioners_will               = Spell(406940),
    ---@type Spell
    expurgation                     = Spell(383344),
    ---@type Spell
    final_reckoning                 = Spell(343721),
    ---@type Spell
    final_verdict                   = Spell(383328),
    ---@type Spell
    guided_prayer                   = Spell(404357),
    ---@type Spell
    heart_of_the_crusader           = Spell(406154),
    ---@type Spell
    highlords_wrath                 = Spell(404512),
    ---@type Spell
    holy_blade                      = Spell(383342),
    ---@type Spell
    holy_flames                     = Spell(406545),
    ---@type Spell
    improved_blade_of_justice       = Spell(403745),
    ---@type Spell
    improved_judgment               = Spell(405461),
    ---@type Spell
    inquisitors_ire                 = Spell(403975),
    ---@type Spell
    judge_jury_and_executioner      = Spell(405607),
    ---@type Spell
    judgment_of_justice             = Spell(403495),
    ---@type Spell
    jurisdiction                    = Spell(402971),
    ---@type Spell
    justicars_vengeance             = Spell(215661),
    ---@type Spell
    light_of_justice                = Spell(404436),
    ---@type Spell
    lights_celerity                 = Spell(403698),
    ---@type Spell
    penitence                       = Spell(403026),
    ---@type Spell
    radiant_glory                   = Spell(458359),
    ---@type Spell
    righteous_cause                 = Spell(402912),
    ---@type Spell
    rush_of_light                   = Spell(407067),
    ---@type Spell
    sanctify                        = Spell(382536),
    ---@type Spell
    searing_light                   = Spell(404540),
    ---@type Spell
    seething_flames                 = Spell(405355),
    ---@type Spell
    shield_of_vengeance             = Spell(184662),
    ---@type Spell
    swift_justice                   = Spell(383228),
    ---@type Spell
    tempest_of_the_lightbringer     = Spell(383396),
    ---@type Spell
    templar_strikes                 = Spell(406646),
    ---@type Spell
    vanguards_momentum              = Spell(383314),
    ---@type Spell
    wake_of_ashes                   = Spell(255937),
    ---@type Spell
    zealots_fervor                  = Spell(403509),

    -- Herald of the Sun
    ---@type Spell
    aurora                          = Spell(439760),
    ---@type Spell
    blessing_of_anshe               = Spell(445200),
    ---@type Spell
    dawnlight                       = Spell(431377),
    ---@type Spell
    eternal_flame                   = Spell(156322),
    ---@type Spell
    gleaming_rays                   = Spell(431480),
    ---@type Spell
    illumine                        = Spell(431423),
    ---@type Spell
    lingering_radiance              = Spell(431407),
    ---@type Spell
    luminosity                      = Spell(431402),
    ---@type Spell
    morning_star                    = Spell(431482),
    ---@type Spell
    second_sunrise                  = Spell(431474),
    ---@type Spell
    solar_grace                     = Spell(431404),
    ---@type Spell
    sun_sear                        = Spell(431413),
    ---@type Spell
    suns_avatar                     = Spell(431425),
    ---@type Spell
    will_of_the_dawn                = Spell(431406),

    -- Templar
    ---@type Spell
    bonds_of_fellowship             = Spell(432992),
    ---@type Spell
    endless_wrath                   = Spell(432615),
    ---@type Spell
    for_whom_the_bell_tolls         = Spell(432929),
    ---@type Spell
    hammerfall                      = Spell(432463),
    ---@type Spell
    higher_calling                  = Spell(431687),
    ---@type Spell
    lights_deliverance              = Spell(425518),
    ---@type Spell
    lights_guidance                 = Spell(427445),
    ---@type Spell
    sacrosanct_crusade              = Spell(431730),
    ---@type Spell
    sanctification                  = Spell(432977),
    ---@type Spell
    shake_the_heavens               = Spell(431533),
    ---@type Spell
    undisputed_ruling               = Spell(432626),
    ---@type Spell
    unrelenting_charger             = Spell(432990),
    ---@type Spell
    wrathful_descent                = Spell(431551),
    ---@type Spell
    zealous_vindication             = Spell(431463),
}

local _avenging_wrath = {
    id = function() return T.radiant_glory:enabled() and 454351 or 31884 end,
    duration = function()
        if T.radiant_glory:enabled() then return 8 end
        return T.divine_wrath:enabled() and 23 or 20
    end,
    max_stack = 1,
    copy = { 31884, 454351 }
}

local A = {
    -- Auras
    ---@type Spell
    ardent_defender            = {
        id = 31850,
        duration = 8,
        type = "Magic",
        max_stack = 1
    },
    -- Silenced.
    -- https://wowhead.com/beta/spell=31935
    ---@type Spell
    avengers_shield            = {
        id = 31935,
        duration = 3,
        type = "Magic",
        max_stack = 1
    },
    -- Crusader Strike and Judgment cool down $w2% faster.$?a384376[    Judgment, Crusader Strike, and auto-attack damage increased by $s1%.][]    $w6 nearby allies will be healed for $w5% of the damage done.
    -- https://wowhead.com/beta/spell=216331
    ---@type Spell
    avenging_crusader          = {
        id = 216331,
        duration = 20,
        max_stack = 1
    },
    -- Talent: $?$w2>0&$w4>0[Damage, healing and critical strike chance increased by $w2%.]?$w4==0&$w2>0[Damage and healing increased by $w2%.]?$w2==0&$w4>0[Critical strike chance increased by $w4%.][]$?a53376[ ][]$?a53376&a137029[Holy Shock's cooldown reduced by $w6%.]?a53376&a137028[Judgment generates $53376s3 additional Holy Power.]?a53376[Each Holy Power spent deals $326731s1 Holy damage to nearby enemies.][]
    -- https://wowhead.com/beta/spell=31884
    ---@type Spell
    avenging_wrath             = _avenging_wrath,
    ---@type Spell
    avenging_wrath_autocrit    = {
        id = 294027,
        duration = 20,
        max_stack = 1,
        copy = "avenging_wrath_crit"
    },
    -- Will be healed for $w1 upon expiration.
    -- https://wowhead.com/beta/spell=223306
    ---@type Spell
    bestow_faith               = {
        id = 223306,
        duration = 5,
        type = "Magic",
        max_stack = 1
    },
    ---@type Spell
    blade_of_wrath             = {
        id = 281178,
        duration = 10,
        max_stack = 1,
    },
    -- The healing or damage of your next Holy Shock is increased by $s1%.
    ---@type Spell
    blessing_of_anshe          = {
        id = 445206,
        duration = 20.0,
        max_stack = 1
    },
    -- Damage and healing increased by $w1%$?s385129[, and Holy Power-spending abilities dealing $w4% additional increased damage and healing.][.]
    -- https://wowhead.com/beta/spell=385127
    ---@type Spell
    blessing_of_dawn           = {
        id = 385127,
        duration = 20,
        max_stack = 2,
        copy = 337767
    },
    ---@type Spell
    blessing_of_dusk           = {
        id = 385126,
        duration = 10,
        max_stack = 1,
        copy = 337757
    },
    -- Talent: Immune to movement impairing effects. $?s199325[Movement speed increased by $199325m1%][]
    -- https://wowhead.com/beta/spell=1044
    ---@type Spell
    blessing_of_freedom        = {
        id = 1044,
        duration = 8,
        type = "Magic",
        max_stack = 1
    },
    -- Talent: Immune to Physical damage and harmful effects.
    -- https://wowhead.com/beta/spell=1022
    ---@type Spell
    blessing_of_protection     = {
        id = 1022,
        duration = 10,
        mechanic = "invulneraility",
        type = "Magic",
        max_stack = 1
    },
    -- Talent: $?$w1>0[$w1% of damage taken is redirected to $@auracaster.][Taking ${$s1*$e1}% of damage taken by target ally.]
    -- https://wowhead.com/beta/spell=6940
    ---@type Spell
    blessing_of_sacrifice      = {
        id = 6940,
        duration = 12,
        type = "Magic",
        max_stack = 1
    },
    ---@type Spell
    blessing_of_sanctuary      = {
        id = 210256,
        duration = 5,
        type = "Magic",
        max_stack = 1
    },
    -- Immune to magical damage and harmful effects.
    -- https://wowhead.com/beta/spell=204018
    ---@type Spell
    blessing_of_spellwarding   = {
        id = 204018,
        duration = 10,
        mechanic = "invulneraility",
        type = "Magic",
        max_stack = 1
    },
    -- Attack speed reduced by $w3%.  Movement speed reduced by $w4%.
    -- https://wowhead.com/beta/spell=388012
    ---@type Spell
    blessing_of_winter         = {
        id = 388012,
        duration = 6,
        type = "Magic",
        max_stack = 10,
        copy = 328506
    },
    -- Talent:
    -- https://wowhead.com/beta/spell=115750
    ---@type Spell
    blinding_light             = {
        id = 115750,
        duration = 6,
        type = "Magic",
        max_stack = 1
    },
    -- Interrupt and Silence effects reduced by $w1%. $?s339124[Fear effects are reduced by $w4%.][]
    -- https://wowhead.com/beta/spell=317920
    ---@type Spell
    concentration_aura         = {
        id = 317920,
        duration = 3600,
        max_stack = 1
    },
    ---@type Spell
    consecrated_blade          = {
        id = 382522,
        duration = 10,
        max_stack = 1,
    },
    -- Damage every $t1 sec.
    -- https://wowhead.com/beta/spell=26573
    ---@type Spell
    consecration               = {
        id = 26573,
        duration = 12,
        tick_time = 1,
        type = "Magic",
        max_stack = 1,
    },
    ---@type Spell
    crusade                    = {
        id = function() return T.radiant_glory:enabled() and 454373 or 231895 end,
        duration = function()
            if T.radiant_glory:enabled() then return 10 end
            return 27 + 3 * (T.divine_wrath:enabled() and 1 or 0)
        end,
        type = "Magic",
        max_stack = 10,
        copy = { 231895, 454373 }
    },
    -- Mounted speed increased by $w1%.$?$w5>0[  Incoming fear duration reduced by $w5%.][]
    -- https://wowhead.com/beta/spell=32223
    ---@type Spell
    crusader_aura              = {
        id = 32223,
        duration = 3600,
        max_stack = 1
    },
    -- $?j1g[Increases ground speed by $j1g%. ][]$?j1f[Increases flight speed by $j1f%. ][]$?j1s[Increases swim speed by $j1s%. ][]
    ---@type Spell
    crusaders_direhorn         = {
        id = 290608,
        duration = 3600,
        max_stack = 1,
    },
    -- Dealing $w1 Radiant damage and radiating $431581s1% of this damage to nearby enemies every $t1 sec.$?e2[; Movement speed reduced by $w3%.][]
    ---@type Spell
    dawnlight                  = {
        id = 431380,
        duration = function() return 8.0 * (FS.state.player:buff_up(_avenging_wrath) and 1.25 or 1) end,
        tick_time = 2.0,
        max_stack = 1,

        -- Affected by:
        -- suns_avatar[431425] #0: { 'type': APPLY_AURA, 'subtype': ADD_PCT_MODIFIER, 'target': TARGET_UNIT_CASTER, 'modifies': BUFF_DURATION, }
    },
    -- Damage taken reduced by $w1%.
    -- https://wowhead.com/beta/spell=465
    ---@type Spell
    devotion_aura              = {
        id = 465,
        duration = 3600,
        max_stack = 1
    },
    ---@type Spell
    divine_arbiter             = {
        id = 406975,
        duration = 30,
        max_stack = 25
    },
    ---@type Spell
    divine_hammer              = {
        id = 198034,
        duration = 12,
        max_stack = 1,
    },
    -- Movement speed reduced by ${$s3*-1}%.
    ---@type Spell
    divine_hammer_snare        = {
        id = 198137,
        duration = 1.5,
        max_stack = 1
    },
    -- Damage taken reduced by $w1%.
    -- https://wowhead.com/beta/spell=403876
    ---@type Spell
    divine_protection          = {
        id = 498,
        duration = 8,
        max_stack = 1,
        copy = 403876
    },
    ---@type Spell
    divine_purpose             = {
        id = 408458,
        duration = 12,
        max_stack = 1,
    },
    ---@type Spell
    divine_resonance           = {
        id = 387895,
        duration = 15,
        max_stack = 1,
        copy = { 355455, 384029, 386730 }
    },
    -- Immune to all attacks and harmful effects.
    -- https://wowhead.com/beta/spell=642
    ---@type Spell
    divine_shield              = {
        id = 642,
        duration = 8,
        mechanic = "invulneraility",
        type = "Magic",
        max_stack = 1
    },
    -- Talent: Increases ground speed by $s4%$?$w1<0[, and reduces damage taken by $w1%][].
    -- https://wowhead.com/beta/spell=221883
    ---@type Spell
    divine_steed               = {
        id = 221883,
        max_stack = 1,
        copy = { 221885, 221886 },
    },
    -- Suffering $s1 Holy damage every $t1 sec.
    ---@type Spell
    divine_vengeance           = {
        id = 267620,
        duration = 4.0,
        tick_time = 1.0,
        pandemic = true,
        max_stack = 1,
    },
    -- $?j1g[Increases ground speed by $j1g%. ][]$?j1f[Increases flight speed by $j1f%. ][]$?j1s[Increases swim speed by $j1s%. ][]
    ---@type Spell
    earthen_ordinants_ramolith = {
        id = 453785,
        duration = 3600,
        max_stack = 1,
    },
    -- Damage done to $@auracaster is reduced by $w3%.
    ---@type Spell
    empyrean_hammer            = {
        id = 431625,
        duration = 8.0,
        max_stack = 1,
    },
    ---@type Spell
    empyrean_legacy            = {
        id = 387178,
        duration = 20,
        max_stack = 1
    },
    ---@type Spell
    empyrean_legacy_icd        = {
        id = 387441,
        duration = 20,
        max_stack = 1
    },
    -- Talent: Your next Divine Storm is free and deals $w1% additional damage.
    -- https://wowhead.com/beta/spell=326733
    ---@type Spell
    empyrean_power             = {
        id = 326733,
        duration = 15,
        max_stack = 1
    },
    -- Healing $w1 health every $t1 sec.
    ---@type Spell
    eternal_flame              = {
        id = 156322,
        duration = 16.0,
        pandemic = true,
        max_stack = 1,
    },
    -- Talent: Sentenced to suffer $w1 Holy damage.
    -- https://wowhead.com/beta/spell=343527
    ---@type Spell
    execution_sentence         = {
        id = 343527,
        duration = function() return T.executioners_will:enabled() and 12 or 8 end,
        type = "Magic",
        max_stack = 1
    },
    -- Talent: Suffering $s1 damage every $t1 sec
    -- https://wowhead.com/beta/spell=383208
    ---@type Spell
    exorcism                   = {
        id = 383208,
        duration = 12,
        tick_time = 2,
        type = "Magic",
        max_stack = 1
    },
    ---@type Spell
    exorcism_stun              = {
        id = 385149,
        duration = 5,
        max_stack = 1,
    },
    -- Talent: Deals $w1 damage over $d1.
    -- https://wowhead.com/beta/spell=273481
    ---@type Spell
    expurgation                = {
        id = 383346,
        duration = 6,
        tick_time = 2,
        type = "Magic",
        max_stack = 1,
        copy = 344067
    },
    -- Talent: Counterattacking all melee attacks.
    -- https://wowhead.com/beta/spell=205191
    ---@type Spell
    eye_for_an_eye             = {
        id = 205191,
        duration = 10,
        max_stack = 1
    },
    ---@type Spell
    faiths_armor               = {
        id = 379017,
        duration = 4.5,
        max_stack = 1
    },
    -- Taking $w3% increased damage from $@auracaster's single target Holy Power abilities and $s4% increased damage from their other Holy Power abilities.
    ---@type Spell
    final_reckoning            = {
        id = 343721,
        duration = function() return 12 + 4 * (T.executioners_will:enabled() and 1 or 0) end,
        type = "Magic",
        max_stack = 1
    },
    ---@type Spell
    final_verdict              = {
        id = 383329,
        duration = 15,
        max_stack = 1,
        copy = 337228
    },
    -- Talent: Your next Holy Power spender costs $s2 less Holy Power.
    -- https://wowhead.com/beta/spell=209785
    ---@type Spell
    fires_of_justice           = {
        id = 209785,
        duration = 15,
        max_stack = 1,
        copy = "the_fires_of_justice" -- backward compatibility
    },
    -- Your Judgment deals ${$w2*$w4}% increased damage.
    ---@type Spell
    for_whom_the_bell_tolls    = {
        id = 433618,
        duration = 20.0,
        max_stack = 1,
    },
    ---@type Spell
    forbearance                = {
        id = 25771,
        duration = function() return T.holy_reprieve:enabled() and 20 or 30 end,
        max_stack = 1,
    },
    -- Your Holy Power spenders deal $s1% additional damage or healing while a Dawnlight is active.
    ---@type Spell
    gleaming_rays              = {
        id = 431481,
        duration = 30.0,
        max_stack = 1,
    },
    -- Damaged or healed whenever the Paladin casts Holy Shock.
    -- https://wowhead.com/beta/spell=287280
    ---@type Spell
    glimmer_of_light           = {
        id = 287280,
        duration = 30,
        type = "Magic",
        max_stack = 1
    },
    -- Stunned.
    -- https://wowhead.com/beta/spell=853
    ---@type Spell
    hammer_of_justice          = {
        id = 853,
        duration = 6,
        mechanic = "stun",
        type = "Magic",
        max_stack = 1
    },
    ---@type Spell
    hammer_of_light_ready      = {
        id = 427441,
        duration = 12,
        max_stack = 1
    },
    -- Talent: Movement speed reduced by $w1%.
    -- https://wowhead.com/beta/spell=183218
    ---@type Spell
    hand_of_hindrance          = {
        id = 183218,
        duration = 10,
        mechanic = "snare",
        type = "Magic",
        max_stack = 1
    },
    -- Taunted.
    -- https://wowhead.com/beta/spell=62124
    ---@type Spell
    hand_of_reckoning          = {
        id = 62124,
        duration = 3,
        mechanic = "taunt",
        max_stack = 1
    },
    ---@type Spell
    inquisition                = {
        id = 84963,
        duration = 45,
        max_stack = 1,
    },
    ---@type Spell
    inquisitors_ire            = {
        id = 403976,
        duration = 3600,
        max_stack = 10,
        -- TODO: Override .up and .stacks to increment every 2 seconds.
    },
    -- Your next $?s383328[Final Verdict]?s215661[Justicar's Vengeance][Templar's Verdict] hits ${$w1-1} additional targets.
    ---@type Spell
    judge_jury_and_executioner = {
        id = 453433,
        duration = 12.0,
        max_stack = 1,
    },
    -- Taking $w1% increased damage from $@auracaster's next Holy Power ability.
    -- https://wowhead.com/beta/spell=197277
    ---@type Spell
    judgment                   = {
        id = 197277,
        duration = 15,
        max_stack = function() return 1 + (T.greater_judgment:enabled() and 1 or 0) end,
        copy = 214222
    },
    ---@type Spell
    judgment_buff              = {
        id = 20271,
        duration = 5,
        max_stack = 1
    },
    ---@type Spell
    judgment_of_justice        = {
        id = 408383,
        duration = 8,
        max_stack = 1
    },
    -- Talent: Attackers are healed for $183811s1.
    -- https://wowhead.com/beta/spell=196941
    ---@type Spell
    judgment_of_light          = {
        id = 196941,
        duration = 30,
        max_stack = 5
    },
    -- Healing for $w1 every $t1 sec.
    -- https://wowhead.com/beta/spell=378412
    ---@type Spell
    light_of_the_titans        = {
        id = 378412,
        duration = 15,
        type = "Magic",
        max_stack = 1
    },
    ---@type Spell
    lights_deliverance         = {
        id = 433674,
        duration = 3600,
        max_stack = 60
    },
    -- The damage and healing of your next Dawnlight is increased by $w1%.
    ---@type Spell
    morning_star               = {
        id = 431539,
        duration = 15.0,
        max_stack = 1,
    },
    -- $s1% of all effective healing done will be added onto your next Holy Shock.
    ---@type Spell
    power_of_the_silver_hand   = {
        id = 200656,
        duration = 10.0,
        max_stack = 1,
    },
    -- Talent: Movement speed reduced by $s2%.
    -- https://wowhead.com/beta/spell=383469
    ---@type Spell
    radiant_decree             = {
        id = 383469,
        duration = 5,
        type = "Magic",
        max_stack = 1
    },
    -- Burning with holy fire for $w1 Holy damage every $t1 sec.
    -- https://wowhead.com/beta/spell=278145
    ---@type Spell
    radiant_incandescence      = {
        id = 278145,
        duration = 3,
        tick_time = 1,
        type = "Magic",
        max_stack = 1,
        copy = 278147
    },
    ---@type Spell
    recompense                 = {
        id = 397191,
        duration = 12,
        max_stack = 1,
    },
    -- Taking $w2% increased damage from $@auracaster's next Holy Power ability.
    -- https://wowhead.com/beta/spell=343724
    ---@type Spell
    reckoning                  = {
        id = 343724,
        duration = 15,
        type = "Magic",
        max_stack = 1,
    },
    -- Talent: State increased by $w1%.
    -- https://wowhead.com/beta/spell=383389
    ---@type Spell
    relentless_inquisitor      = {
        id = 383389,
        duration = 12,
        max_stack = 3,
        copy = 337315
    },
    -- Talent: Incapacitated.
    -- https://wowhead.com/beta/spell=20066
    ---@type Spell
    repentance                 = {
        id = 20066,
        duration = 60,
        mechanic = "incapacitate",
        type = "Magic",
        max_stack = 1
    },
    -- When any party or raid member within $a1 yards dies, you gain Avenging Wrath for $w1 sec.    When any party or raid member within $a1 yards takes more than $s3% of their health in damage, you gain Seraphim for $s4 sec. This cannot occur more than once every 30 sec.
    -- https://wowhead.com/beta/spell=183435
    ---@type Spell
    retribution_aura           = {
        id = 183435,
        duration = 3600,
        max_stack = 1
    },
    ---@type Spell
    righteous_verdict          = {
        id = 267611,
        duration = 6,
        max_stack = 1,
    },
    ---@type Spell
    rush_of_light              = {
        id = 407065,
        duration = 10,
        max_stack = 1,
    },
    -- Empyrean Hammer damage increased by $w1%
    ---@type Spell
    sanctification             = {
        id = 433671,
        duration = 10.0,
        max_stack = 1,
    },
    ---@type Spell
    sanctified_ground          = {
        id = 387480,
        duration = 3600,
        max_stack = 1,
    },
    ---@type Spell
    sanctify                   = {
        id = 382538,
        duration = 8,
        max_stack = 1,
    },
    ---@type Spell
    sealed_verdict             = {
        id = 387643,
        duration = 15,
        max_stack = 1
    },
    -- Talent: Flash of Light cast time reduced by $w1%.  Flash of Light heals for $w2% more.
    -- https://wowhead.com/beta/spell=114250
    ---@type Spell
    selfless_healer            = {
        id = 114250,
        duration = 15,
        max_stack = 4
    },
    -- Casting Empyrean Hammer on a nearby target every $t sec.
    ---@type Spell
    shake_the_heavens          = {
        id = 431536,
        duration = 8.0,
        max_stack = 1,
    },
    -- Talent: Absorbs $w1 damage and deals damage when the barrier fades or is fully consumed.
    -- https://wowhead.com/beta/spell=184662
    ---@type Spell
    shield_of_vengeance        = {
        id = 184662,
        duration = 15,
        mechanic = "shield",
        type = "Magic",
        max_stack = 1
    },
    -- State increased by $w1%.
    ---@type Spell
    solar_grace                = {
        id = 439841,
        duration = 12.0,
        max_stack = 1,
    },
    -- $?$w2>1[Absorbs the next ${$w2-1} damage.][Absorption exhausted.]  Refreshed to $w1 absorption every $t1 sec.
    -- https://wowhead.com/beta/spell=337824
    ---@type Spell
    shock_barrier              = {
        id = 337824,
        duration = 18,
        tick_time = 6,
        type = "Magic",
        max_stack = 1
    },
    -- Healing $w1 every $t1 sec.
    ---@type Spell
    sun_sear                   = {
        id = 431415,
        duration = 4.0,
        max_stack = 1
    },
    ---@type Spell
    the_magistrates_judgment   = {
        id = 337682,
        duration = 15,
        max_stack = 1,
    },
    -- $?(s403696)[Burning for $w2 damage every $t2 sec and movement speed reduced by $s1%.] [Movement speed reduced by $s1%.]
    ---@type Spell
    truths_wake                = {
        id = 403695,
        duration = 9.0,
        tick_time = 3.0,
        pandemic = true,
        max_stack = 1,
        copy = { 339376, 383351 }
    },
    -- Talent: Disoriented.
    -- https://wowhead.com/beta/spell=10326
    ---@type Spell
    turn_evil                  = {
        id = 10326,
        duration = 40,
        mechanic = "turn",
        type = "Magic",
        max_stack = 1
    },
    -- State increased by $w1%
    ---@type Spell
    undisputed_ruling          = {
        id = 432629,
        duration = 6.0,
        max_stack = 1,
    },
    -- Talent: Holy Damage increased by $w1%.
    -- https://wowhead.com/beta/spell=383311
    ---@type Spell
    vanguards_momentum         = {
        id = 383311,
        duration = 10,
        max_stack = 3,
        copy = 345046
    },
    ---@type Spell
    virtuous_command           = {
        id = 383307,
        duration = 5,
        max_stack = 1,
        copy = 339664
    },
    -- Talent: Movement speed reduced by $s2%.
    -- https://wowhead.com/beta/spell=255937
    ---@type Spell
    wake_of_ashes              = {
        id = 255937,
        duration = 5,
        type = "Magic",
        max_stack = 1
    },
    ---@type Spell
    wake_of_ashes_stun         = {
        id = 255941,
        duration = 5,
        max_stack = 1,
    },
    -- Movement speed increased by $w1%.
    ---@type Spell
    will_of_the_dawn           = {
        id = 431462,
        duration = 5.0,
        max_stack = 1,
    },
    -- Talent: Auto attack speed increased and deals additional Holy damage.
    -- https://wowhead.com/beta/spell=269571
    ---@type Spell
    zeal                       = {
        id = 269571,
        duration = 20,
        max_stack = 1
    },

    ---@type Spell
    paladin_aura               = {
        ---@type Spell
        alias = { "concentration_aura", "crusader_aura", "devotion_aura", "retribution_aura" },
        aliasMode = "first",
        aliasType = "buff",
        duration = 3600,
    },

    ---@type Spell
    empyreal_ward              = {
        id = 387792,
        duration = 60,
        max_stack = 1,
        copy = 287731
    },
    -- Power: 335069
    ---@type Spell
    negative_energy_token_proc = {
        id = 345693,
        duration = 5,
        max_stack = 1,
    },
    ---@type Spell
    reckoning_pvp              = {
        id = 247677,
        max_stack = 30,
        duration = 30
    },
    ---@type Spell
    templar_strikes            = {
        duration = 3,
        max_stack = 1
    },


}

---@type Spell
local S = {
    ---@type Spell
    avenging_wrath = {
        id = 31884,
        cooldown = 60,
        notalent = function()
            return T.radiant_glory:enabled() and "radiant_glory" or "crusade"
        end,
        toggle = "cooldowns",
        usable = function() return T.avenging_wrath:enabled() end,
    },

    -- Talent: Pierces an enemy with a blade of light, dealing $s1 Physical damage.    |cFFFFFFFFGenerates $s2 Holy Power.|r
    ---@type Spell
    blade_of_justice = {
        id = 184575,
        cooldown = function() return (T.light_of_justice:enabled() and 10 or 12) end,
        charges = function() if T.improved_blade_of_justice:enabled() then return 2 end end,
        recharge = function()
            if T.improved_blade_of_justice:enabled() then
                return (T.light_of_justice:enabled() and 10 or 12)
            end
        end,
        talent = "blade_of_justice",
    },

    -- Talent: Blesses a party or raid member, granting immunity to movement impairing effects $?s199325[and increasing movement speed by $199325m1% ][]for $d.
    ---@type Spell
    blessing_of_freedom = {
        id = 1044,
        cooldown = 25,
        talent = "blessing_of_freedom",
    },

    -- Talent: Blesses a party or raid member, granting immunity to Physical damage and harmful effects for $d.    Cannot be used on a target with Forbearance. Causes Forbearance for $25771d.$?c2[    Shares a cooldown with Blessing of Spellwarding.][]
    ---@type Spell
    blessing_of_protection = {
        id = 1022,
        cooldown = function() return T.improved_blessing_of_protection:enabled() and 240 or 300 end,
        talent = "blessing_of_protection",
    },

    -- Talent: Blesses a party or raid member, reducing their damage taken by $s1%, but you suffer ${100*$e1}% of damage prevented.    Last $d, or until transferred damage would cause you to fall below $s3% health.
    ---@type Spell
    blessing_of_sacrifice = {
        id = 6940,
        cooldown = function() return T.sacrifice_of_the_just:enabled() and 60 or 120 end,
        talent = "blessing_of_sacrifice",
    },

    ---@type Spell
    blessing_of_sanctuary = {
        id = 210256,
        cooldown = 0,
        pvptalent = "blessing_of_sanctuary",
    },

    -- Talent: Emits dazzling light in all directions, blinding enemies within $105421A1 yards, causing them to wander disoriented for $105421d. Non-Holy damage will break the disorient effect.
    ---@type Spell
    blinding_light = {
        id = 115750,
        cooldown = function() return T.lights_countenance:enabled() and 75 or 90 end,
        talent = "blinding_light",
    },

    -- Talent: Cleanses a friendly target, removing all Poison and Disease effects.
    ---@type Spell
    cleanse_toxins = {
        id = 213644,
        cooldown = 8,
    },

    -- Interrupt and Silence effects on party and raid members within $a1 yards are $s1% shorter. $?s339124[Fear effects are also reduced.][]
    ---@type Spell
    concentration_aura = {
        id = 317920,
        cooldown = 0,
        talent = "auras_of_the_resolute",
        nobuff = "paladin_aura",
    },

    -- Consecrates the land beneath you, causing $<dmg> Holy damage over $d to enemies who enter the area$?s204054[ and reducing their movement speed by $204054s2%.][.] Limit $s2.
    ---@type Spell
    consecration = {
        id = 26573,
        cooldown = 9,
    },

    -- Call upon the Light and begin a crusade, increasing your  $?s384376[and damage ][]by ${$s5/10}% for $d.; Each Holy Power spent during Crusade increases  $?s384376[and damage ][]by an additional ${$s5/10}%.; Maximum $u stacks.$?s53376[; While active, each Holy Power spent causes you to explode with Holy light for $326731s1 damage to nearby enemies.][]$?s384376[; Hammer of Wrath may be cast on any target.][];
    ---@type Spell
    crusade = {
        id = 231895,
        cooldown = 120,
        toggle = "cooldowns",
        talent = "crusade",
        notalent = "radiant_glory",
        nobuff = "crusade",
        usable = function()
            return T.crusade:is_learned() and not T.radiant_glory:is_learned() and FS.state.player:buff_down(A.crusade)
        end
    },

    -- Increases mounted speed by $s1% for all party and raid members within $a1 yards.
    ---@type Spell
    crusader_aura = {
        id = 32223,
        cooldown = 0,
        talent = "auras_of_the_resolute",
        nobuff = "paladin_aura",
    },

    -- Strike the target for $<damage> Physical damage.$?a196926[    Reduces the cooldown of Holy Shock by ${$196926m1/-1000}.1 sec.][]    |cFFFFFFFFGenerates $s2 Holy Power.
    ---@type Spell
    crusader_strike = {
        id = 35395,
        charges = 2,
        cooldown = function() return (T.swift_justice:enabled() and 4 or 6) end,
        recharge = function() return (T.swift_justice:enabled() and 4 or 6) end,
        notalent = "templar_strikes",
        usable = function() return not T.crusading_strikes:enabled() end,
    },

    -- Party and raid members within $a1 yards are bolstered by their devotion, reducing damage taken by $s1%.
    ---@type Spell
    devotion_aura = {
        id = 465,
        cooldown = 0,
        talent = "auras_of_the_resolute",
        nobuff = "paladin_aura",
    },

    -- Divine Hammers spin around you, consuming a Holy Power to strike enemies within $198137A1 yds for $?s405289[${$198137sw1*1.05} Radiant][$198137sw1 Holy] damage every $t sec. ; While active your Judgment, Blade of Justice$?a404542[][ and Crusader Strike] recharge $s2% faster, and increase the rate at which Divine Hammer strikes by $s1% when they are cast. Deals reduced damage beyond 8 targets.
    ---@type Spell
    divine_hammer = {
        id = 198034,
        cooldown = 120,
        talent = "divine_hammer",
    },

    -- Talent: Reduces all damage you take by $s1% for $d.
    ---@type Spell
    divine_protection = {
        id = function() return FS.is_retribution_paladin and 403876 or 498 end,
        cooldown = function() return 60 * (T.unbreakable_spirit:enabled() and 0.7 or 1) end,
        toggle = "defensives",
    },

    -- Grants immunity to all damage and harmful effects for $d. $?a204077[Taunts all targets within 15 yd.][]    Cannot be used if you have Forbearance. Causes Forbearance for $25771d.
    ---@type Spell
    divine_shield = {
        id = 642,
        cooldown = function() return 300 * (T.unbreakable_spirit:enabled() and 0.7 or 1) end,
        toggle = "cooldowns",
        nodebuff = function() if not T.lights_revocation:enabled() then return "forbearance" end end,
    },

    -- Talent: Leap atop your Charger for $221883d, increasing movement speed by $221883s4%. Usable while indoors or in combat.
    ---@type Spell
    divine_steed = {
        id = 190784,
        charges = function() if T.cavalier:enabled() then return 2 end end,
        cooldown = function() return 45 * (T.divine_spurs:enabled() and 0.8 or 1) end,
        recharge = function() if T.cavalier:enabled() then return 45 * (T.divine_spurs:enabled() and 0.8 or 1) end end,
        talent = "divine_steed",
    },

    -- Talent: Unleashes a whirl of divine energy, dealing $s1 Holy damage to all nearby enemies. Deals reduced damage beyond $s2 targets.
    ---@type Spell
    divine_storm = {
        id = 53385,
        cooldown = 0,
        talent = "divine_storm",
    },

    -- Talent: Instantly cast $?a137029[Holy Shock]?a137028[Avenger's Shield]?a137027[Judgment][Holy Shock, Avenger's Shield, or Judgment] on up to $s1 targets within $A2 yds.$?(a384027|a386738|a387893)[    After casting Divine Toll, you instantly cast ][]$?(a387893&c1)[Holy Shock]?(a386738&c2)[Avenger's Shield]?(a384027&c3)[Judgment][]$?a387893[ every $387895t1 sec. This effect lasts $387895d.][]$?a384027[ every $384029t1 sec. This effect lasts $384029d.][]$?a386738[ every $386730t1 sec. This effect lasts $386730d.][]$?c3[    Divine Toll's Judgment deals $326011s1% increased damage.][]$?c2[    Generates $s5 Holy Power per target hit.][]
    ---@type Spell
    divine_toll = {
        id = function() return T.divine_toll:enabled() and 375576 or 304971 end,
        cooldown = function() return T.quickened_invocation:enabled() and 45 or 60 end,
    },

    -- Heals an ally for $s2 and an additional $o1 over $d.; Healing increased by $s3% when cast on self.
    ---@type Spell
    eternal_flame = {
        id = 156322,
        cooldown = 0.0,
        talent = "eternal_flame",
    },

    -- Talent: A hammer slowly falls from the sky upon the target. After $d, they suffer ${$387113s1*$<mult>} Holy damage$?s387196[ and enemies within $387200a2 yards will suffer $387196s1% of the damage taken from your abilities in that time.][, plus $s2% of damage taken from your abilities in that time.]
    ---@type Spell
    execution_sentence = {
        id = 343527,
        cooldown = 60,
        talent = "execution_sentence",
    },

    -- Talent: Blasts the target with Holy Light, causing $383921s1 Holy damage and burns the target for an additional ${$383208s1*($383208d/$383208t)} Holy Damage over $383208d. Stuns Demon and Undead targets for $385149d.    Applies the damage over time effect to up to $s2 nearby enemies if the target is standing within your Consecration.
    ---@type Spell
    exorcism = {
        id = 383185,
        cooldown = 20,
        talent = "exorcism",
    },

    -- Talent: Surround yourself with a bladed bulwark, reducing Physical damage taken by $s2% and dealing $205202sw1 Physical damage to any melee attackers for $d.
    ---@type Spell
    eye_for_an_eye = {
        id = 205191,
        cooldown = 60,
        talent = "eye_for_an_eye",
    },

    -- Call down a blast of heavenly energy, dealing $s2 Holy damage to all targets in the area and causing them to take $s3% increased damage from your single target Holy Power abilities, and $s4% increased damage from other Holy Power abilities for $d.; $?s406158 [Generates $406158s1 Holy Power.][]
    ---@type Spell
    final_reckoning = {
        id = 343721,
        cooldown = 60,
        talent = "final_reckoning",
    },

    -- Expends a large amount of mana to quickly heal a friendly target for $?$c1&$?a134735[${$s1*1.15}][$s1].
    ---@type Spell
    flash_of_light = {
        id = 19750,
        cooldown = function() return T.lights_celerity:enabled() and 6 or 0 end,
    },

    -- Stuns the target for $d.
    ---@type Spell
    hammer_of_justice = {
        id = 853,
        cooldown = function() return 45 - (15 * (T.fist_of_justice:enabled() and 1 or 0)) end,
    },

    -- Hammer down your enemy with the power of the Light, dealing $429826s1 Holy damage and ${$429826s1/2} Holy damage up to 4 nearby enemies. ; Additionally, calls down Empyrean Hammers from the sky to strike $427445s2 nearby enemies for $431398s1 Holy damage each.;
    ---@type Spell
    hammer_of_light = {
        id = 427453,
        cooldown = 0.0,
        usable = function() return FS.state.player:buff_up(A.hammer_of_light_ready) end
    },

    ---@type Spell
    hammer_of_reckoning = {
        id = 247675,
        cooldown = 60,
        usable = function() return FS.state.player:buff_stack(A.reckoning) >= 50 end,
    },

    -- Talent: Hurls a divine hammer that strikes an enemy for $<damage> Holy damage. Only usable on enemies that have less than 20% health$?s326730[, or during Avenging Wrath][].    |cFFFFFFFFGenerates $s2 Holy Power.
    ---@type Spell
    hammer_of_wrath = {
        id = 24275,
        charges = function() if T.vanguards_momentum:enabled() then return 2 end end,
        cooldown = 7.5,
        recharge = function() if T.vanguards_momentum:enabled() then return 7.5 end end,
        talent = "hammer_of_wrath",
        usable = function()
            return
                FS.state.target:health_percentage() < 20 / 100 or FS.state.player:buff_up(A.avenging_wrath) or
                FS.state.player:buff_up(A.crusade) or
                FS.state.player:buff_up(A.final_verdict) or
                FS.state.player:buff_up(A.blessing_of_anshe) or
                FS.state.player:buff_up(A.negative_energy_token_proc)
        end,
    },

    -- Talent: Burdens an enemy target with the weight of their misdeeds, reducing movement speed by $s1% for $d.
    ---@type Spell
    hand_of_hindrance = {
        id = 183218,
        cooldown = 30,
        talent = "hand_of_hindrance",
    },

    -- Commands the attention of an enemy target, forcing them to attack you.
    ---@type Spell
    hand_of_reckoning = {
        id = 62124,
        cooldown = 8,
    },

    -- [114165] Fires a beam of light that scatters to strike a clump of targets. ; If the beam is aimed at an enemy target, it deals $114852s1 Holy damage and radiates ${$114852s2*$<healmod>} healing to 5 allies within $114852A2 yds.; If the beam is aimed at a friendly target, it heals for ${$114871s1*$<healmod>} and radiates $114871s2 Holy damage to 5 enemies within $114871A2 yds.
    ---@type Spell
    holy_prism = {
        id = 114852,
        cooldown = 20.0,
    },

    -- Judges the target, dealing $s1 Holy damage$?s231663[, and causing them to take $197277s1% increased damage from your next Holy Power ability.][]$?s315867[    |cFFFFFFFFGenerates $220637s1 Holy Power.][]
    ---@type Spell
    judgment = {
        id = 20271,
        charges = function() if T.improved_judgment:enabled() then return 2 end end,
        cooldown = function()
            return ((T.swift_justice:enabled() and 10 or 12))
        end,
        recharge = function()
            if T.improved_judgment:enabled() then
                return (T.swift_justice:enabled() and 10 or 12)
            end
        end,
    },

    -- Talent: Focuses Holy energy to deliver a powerful weapon strike that deals $s1 Holy damage, and restores health equal to the damage done.    Damage is increased by $s2% when used against a stunned target.
    ---@type Spell
    justicars_vengeance = {
        id = 215661,
        cooldown = 0,
        talent = "justicars_vengeance",
    },

    -- Talent: Heals a friendly target for an amount equal to $s2% your maximum health.$?a387791[    Grants the target $387792s1% increased armor for $387792d.][]    Cannot be used on a target with Forbearance. Causes Forbearance for $25771d.
    ---@type Spell
    lay_on_hands = {
        id = 633,
        cooldown = function() return 600 * (T.unbreakable_spirit:enabled() and 0.7 or 1) end,
        talent = "lay_on_hands",
        toggle = "cooldowns",
        nodebuff = "forbearance",
    },

    --[[ Talent: Lash out at your enemies, dealing $s1 Radiant damage to all enemies within $a1 yd in front of you and reducing their movement speed by $s2% for $d. Damage reduced on secondary targets.    Demon and Undead enemies are also stunned for $255941d.    |cFFFFFFFFGenerates $s3 Holy Power.
    ---@type Spell
    radiant_decree = {
        id = 383469,
        known = 255937,
        ---@type Spell
        flash = { 383469, 255937 },
        cast = 0,
        cooldown = 15,
        gcd = "spell",
        school = "holyfire",

        spend = function() return T.vanguard_of_justice:enabled() and 4 or 3 end,
        spendType = "holy_power",

        talent = "radiant_decree",
        startsCombat = true,

        handler = function ()
            removeDebuffStack( "target", "judgment" )
            removeDebuff( "target", "reckoning" )
            if target.is_undead or target.is_demon then applyDebuff( "target", "radiant_decree" ) end
            if T.divine_judgment:enabled() then addStack( "divine_judgment" ) end
            if T.truths_wake:enabled() or conduit.truths_wake.enabled then applyDebuff( "target", "truths_wake" ) end
        end,
    }, ]]

    -- Talent: Forces an enemy target to meditate, incapacitating them for $d.    Usable against Humanoids, Demons, Undead, Dragonkin, and Giants.
    ---@type Spell
    repentance = {
        id = 20066,
        cooldown = function() return T.lights_countenance:enabled() and 0 or 15 end,
        talent = "repentance",
    },

    -- When any party or raid member within $a1 yards dies, you gain Avenging Wrath for $s1 sec.    When any party or raid member within $a1 yards takes more than $s3% of their health in damage, you gain Seraphim for $s4 sec. This cannot occur more than once every 30 sec.
    ---@type Spell
    retribution_aura = {
        id = 183435,
        cooldown = 0,
        talent = "auras_of_swift_vengeance",
        nobuff = "paladin_aura",
    },

    -- Slams enemies in front of you with your shield, causing $s1 Holy damage, and increasing your Armor by $?c1[${$132403s1*$INT/100}][${$132403s1*$STR/100}] for $132403d.$?a386568[    $@spelldesc386568][]$?a280373[    $@spelldesc280373][]
    ---@type Spell
    shield_of_the_righteous = {
        id = 53600,
        cooldown = 1,
    },

    -- Talent: Creates a barrier of holy light that absorbs $<shield> damage for $d.    When the shield expires, it bursts to inflict Holy damage equal to the total amount absorbed, divided among all nearby enemies.
    ---@type Spell
    shield_of_vengeance = {
        id = 184662,
        cooldown = 90,
        talent = "shield_of_vengeance",
        toggle = "defensives",
    },

    -- Complete the Templar combo, slash the target for $<damage> $?s403664[Holystrike][Radiant] damage, and burn them over 4 sec for 50% of the damage dealt.; Generate $s2 Holy Power.
    ---@type Spell
    templar_slash = {
        id = 406647,
        cooldown = 0,
        talent = "templar_strikes",
        buff = "templar_strikes",
    },

    -- Begin the Templar combo, striking the target for 3,207 Radiant damage. Generates 1 Holy Power.
    ---@type Spell
    templar_strike = {
        id = 407480,
        cooldown = 6,
        recharge = 6,
        talent = "templar_strikes",
        nobuff = "templar_strikes",
    },

    -- Unleashes a powerful weapon strike that deals $s1 $?s403664[Holystrike][Holy] damage to an enemy target,; Final Verdict has a $s2% chance to reset the cooldown of Hammer of Wrath and make it usable on any target, regardless of their health.
    ---@type Spell
    templars_verdict = {
        id = function()
            return T.final_verdict:enabled() and 383328 or
                85256
        end,
        cast = 0,
        cooldown = 0,
        notalent = "justicars_vengeance",
    },

    -- Talent: The power of the Light compels an Undead, Aberration, or Demon target to flee for up to $d. Damage may break the effect. Lesser creatures have a chance to be destroyed. Only one target can be turned at a time.
    ---@type Spell
    turn_evil = {
        id = 10326,
        cooldown = 15,
        talent = "turn_evil",
    },

    --- Lash out at your enemies, dealing $s1 Radiant damage to all enemies within $a1 yds in front of you, and applying $@spellname403695, burning the targets for an additional ${$403695s2*($403695d/$403695t+1)} damage over $403695d.; Demon and Undead enemies are also stunned for $255941d.; Generates $s2 Holy Power.
    ---@type Spell
    wake_of_ashes = {
        id = 255937,
        cast = 0,
        cooldown = 15,
        usable = function()
            if FS.retribution.check_wake_range and not (FS.state.target_is_valid and FS.state.target_within_12) then
                return false
            end
            return true
        end,
    },

    -- Calls down the Light to heal a friendly target for $130551s1$?a378405[ and an additional $378412s1 over $378412d][].$?a379043[ Your block chance is increased by$379043s1% for $379041d.][]$?a315921&!a315924[    |cFFFFFFFFProtection:|r If cast on yourself, healing increased by up to $315921s1% based on your missing health.][]$?a315924[    |cFFFFFFFFProtection:|r Healing increased by up to $315921s1% based on the target's missing health.][]
    ---@type Spell
    word_of_glory = {
        id = 85673,
        cast = 0,
        cooldown = 0,
    },

    ---@type Spell
    lights_judgment = {
        id = 255647
    }
}

for k, v in pairs(A) do
    ---@type integer
    ---@diagnostic disable-next-line: missing-parameter, assign-type-mismatch
    local id = type(v.id) == "function" and v.id() or v.id
    A[k] = Spell(id)
    for meta_k, meta_v in pairs(v) do
        if meta_k ~= "id" then
            if type(meta_v) ~= "function" then
                A[k]["_" .. meta_k] = meta_v
            else
                A[k]["_" .. meta_k] = meta_v()
            end
        end
    end
end

for k, v in pairs(S) do
    ---@type integer
    ---@diagnostic disable-next-line: missing-parameter, assign-type-mismatch
    local id = type(v.id) == "function" and v.id() or v.id
    S[k] = Spell(id)
    for meta_k, meta_v in pairs(v) do
        if meta_k ~= "id" then
            if type(meta_v) ~= "function" or meta_k == "usable" then
                S[k]["_" .. meta_k] = meta_v
            elseif type(meta_v) == "function" then
                ---@diagnostic disable-next-line: assign-type-mismatch
                S[k]["_" .. meta_k] = meta_v()
            end
        end
    end
end

FS.retribution.spells = S
FS.retribution.auras = A
FS.retribution.talents = T
