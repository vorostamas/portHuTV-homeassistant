[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

**This component will set up the following platform.**

Platform | Description
-- | --
`sensor` | Show info of a TV channel.

***

{% if not installed %}
## Installation

1. Click install.
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Port.hu TV".

{% endif %}


## Configuration is done in the UI

You need to add the channel ID of the TV channel. You can check the channel ID in the [`channel_mapping.json`](https://github.com/vorostamas/portHuTV-homeassistant/blob/master/custom_components/porthutv/channel_mapping.json) file.

***

[porthutv]: https://github.com/vorostamas/portHuTV-homeassistant
[buymecoffee]: https://www.buymeacoffee.com/tamasvoros
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/vorostamas/portHuTV-homeassistant?style=for-the-badge
[commits]: https://github.com/vorostamas/portHuTV-homeassistant/commits/master
[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/custom-components/blueprint.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Tamas%20Voros%20%40vorostamas-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/vorostamas/portHuTV-homeassistant.svg?style=for-the-badge
[releases]: https://github.com/vorostamas/portHuTV-homeassistant/releases
