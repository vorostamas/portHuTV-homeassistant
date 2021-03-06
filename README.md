# Port.hu TV Schedule for Home Assistant
This component gets the schedule of a (Hungarian) TV channel from Port.hu for that day.

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

**This component will set up the following sensor:**

Name | Description
-- | --
`entity_id` | `sensor.name_of_the_channel`
`state` | The show that is live at the moment.

**The sensor has the following attributes:**

Attribute | Description
-- | --
`next_show` | The upcoming show.
`previous_show` | The show before the ongoing one.
`schedule` | The guide for the day.
`friendly_name` | The name of the channel
`icon` | `mdi:television-guide`


## Installation

<details>
<summary>Installation with HACS</summary>

1. Go to any of the sections in HACS(integrations, frontend, automation).
1. Click on the 3 dots in the top right corner.
1. Select "Custom repositories"
1. Add this URL to the repository:
 `https://github.com/vorostamas/portHuTV-homeassistant`
1. Select the Integration category.
1. Click the "ADD" button.
1. Click on "Install" button.
</details>

<details>
<summary>Manual installation</summary>

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `porthutv`.
4. Download _all_ the files from the `custom_components/porthutv/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
</details>

## Configuration in the UI
In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Port.hu TV".

You need to add the channel ID of the TV channel. You can check the channel ID in the [`channel_mapping.json`](https://github.com/vorostamas/portHuTV-homeassistant/blob/master/custom_components/porthutv/channel_mapping.json) file.

You can repeat this method to add multiple channels.

***

## Support
If you like this component, help me out with a couple of 🍻 or a ☕!

[![coffee](https://www.buymeacoffee.com/assets/img/custom_images/black_img.png)](https://www.buymeacoffee.com/tamasvoros)

***

## Lovelace
One possible way to show the schedules on the UI is using [List Card](https://github.com/iantrich/list-card). See examples below.

## Examples

<details>
<summary>Example entity</summary>

![entity-example]
</details>

<details>
<summary>List-card example</summary>

![list-card-example]
</details>

## Notes
- Some channels provide schedules for only daytime. For example, `tvchannel-2` schedule ends at 19:50, and there is a corresponding evening channel `tvchannel-361` starts after 19:50.
- You may want to exclude the sensor from [`recorder`](https://www.home-assistant.io/integrations/recorder/), because Home Assistant will store the states in the database.

<details>
<summary>Example list-card configuration</summary>

```yaml
type: 'custom:list-card'
entity: sensor.comedy_central
title: Comedy Central
feed_attribute: schedule
row_limit: 100
columns:
  - title: Start
    field: start_time
  - title: End
    field: end_time
  - title: Title
    field: title
    add_link: film_url
  - title: Description
    field: short_description
```
</details>

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

## Legal
This project is in no way affiliated with, authorized, maintained, sponsored or endorsed by Port.hu or any of its affiliates or subsidiaries. This is an independent and unofficial application.

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
[entity-example]: entity-example.png
[list-card-example]: list-card-example.png
