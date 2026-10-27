"""
SecretBlox Channel Configuration
Multi-language settings, voices, and metadata for:
- English (SecretBlox)
- German (SecretBlox Deutsch)
- Spanish (SecretBlox Español)
- French (SecretBlox Français)
"""

LANGUAGES = {
    "en": {
        "channel_name": "SecretBlox",
        "locale": "en-US",
        "voice": "en-US-AndrewMultilingualNeural",
        "voice_rate": "+8%",
        "title_prefix": "SecretBlox",
        "cpm_tier": "Tier 1 ($4 - $8+)",
        "target_regions": ["United States", "United Kingdom", "Canada", "Australia"],
        "default_tags": ["#roblox", "#robloxshorts", "#robloxsecrets", "#robloxstories", "#secretblox", "#gaming"],
        "cta_template": "Comment '{keyword}' if you want to play this! Subscribe to SecretBlox for more mysteries."
    },
    "de": {
        "channel_name": "SecretBlox Deutsch",
        "locale": "de-DE",
        "voice": "de-DE-FlorianMultilingualNeural",
        "voice_rate": "+6%",
        "title_prefix": "SecretBlox DE",
        "cpm_tier": "Tier 1 Highest ($5 - $10+)",
        "target_regions": ["Germany", "Austria", "Switzerland"],
        "default_tags": ["#robloxdeutsch", "#robloxshorts", "#robloxgermany", "#secretblox", "#robloxmythen", "#gamingdeutsch"],
        "cta_template": "Schreib '{keyword}' in die Kommentare, wenn du das spielen willst! Abonniere SecretBlox für mehr Geheimnisse."
    },
    "es": {
        "channel_name": "SecretBlox Español",
        "locale": "es-MX",
        "voice": "es-MX-JorgeNeural",
        "voice_rate": "+8%",
        "title_prefix": "SecretBlox ES",
        "cpm_tier": "Hybrid (Massive Viral Volume + Tier 1 Spain)",
        "target_regions": ["Mexico", "Spain", "Argentina", "Colombia", "United States Hispanic"],
        "default_tags": ["#robloxespañol", "#robloxshorts", "#secretosroblox", "#secretblox", "#historiasroblox", "#gaming"],
        "cta_template": "¡Comenta '{keyword}' si quieres jugar esto! Suscríbete a SecretBlox para más misterios."
    },
    "fr": {
        "channel_name": "SecretBlox Français",
        "locale": "fr-FR",
        "voice": "fr-FR-RemyMultilingualNeural",
        "voice_rate": "+6%",
        "title_prefix": "SecretBlox FR",
        "cpm_tier": "Tier 1 ($4 - $8+)",
        "target_regions": ["France", "Belgium", "Canada (Quebec)", "Switzerland"],
        "default_tags": ["#robloxfr", "#robloxshorts", "#robloxsecrets", "#secretblox", "#gamingfr", "#robloxfrance"],
        "cta_template": "Écris '{keyword}' en commentaire si tu veux y jouer ! Abonne-toi à SecretBlox pour plus de secrets."
    }
}
