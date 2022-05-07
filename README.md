<img src=https://assets.ifttt.com/images/channels/851621020/icons/large.png>
# SmartLighting-May2022
Python Script for changing Phillips Wiz A19 Lights.

- This script controls both Wiz and Lifx Branded smart home lights

# How To Use (Wiz)
To use this script, install Pywizlight using 
```
pip3 install pywizlight
```
# Fedora/CentOS
```
sudo dnf -y install python3-pywizlight
```

# How To Use (Lifx)
```
pip3 install lifxlan
```

# Discover bulbs via CLI (Wiz)
To find bulbs via cli you can use the following:
```
python3 -m pywizlight.cli discover
```
# Example
```
import asyncio

from pywizlight import wizlight, PilotBuilder, discovery

async def main():
    """Sample code to work with bulbs."""
    # Discover all bulbs in the network via broadcast datagram (UDP)
    # function takes the discovery object and returns a list of wizlight objects.
    bulbs = await discovery.discover_lights(broadcast_space="192.168.1.255")
    # Print the IP address of the bulb on index 0
    print(f"Bulb IP address: {bulbs[0].ip}")

    # Iterate over all returned bulbs
    for bulb in bulbs:
        print(bulb.__dict__)
        # Turn off all available bulbs
        # await bulb.turn_off()

    # Set up a standard light
    light = wizlight("192.168.1.27")
    # Set up the light with a custom port
    #light = wizlight("your bulb's IP address", port=12345)

    # The following calls need to be done inside an asyncio coroutine
    # to run them from normal synchronous code, you can wrap them with
    # asyncio.run(..).

    # Turn the light on into "rhythm mode"
    await light.turn_on(PilotBuilder())
    # Set bulb brightness
    await light.turn_on(PilotBuilder(brightness = 255))

    # Set bulb brightness (with async timeout)
    timeout = 10
    await asyncio.wait_for(light.turn_on(PilotBuilder(brightness = 255)), timeout)

    # Set bulb to warm white
    await light.turn_on(PilotBuilder(warm_white = 255))

    # Set RGB values
    # red to 0 = 0%, green to 128 = 50%, blue to 255 = 100%
    await light.turn_on(PilotBuilder(rgb = (0, 128, 255)))

    # Get the current color temperature, RGB values
    state = await light.updateState()
    print(state.get_colortemp())
    red, green, blue = state.get_rgb()
    print(f"red {red}, green {green}, blue {blue}")

    # Start a scene
    await light.turn_on(PilotBuilder(scene = 4)) # party

    # Get the name of the current scene
    state = await light.updateState()
    print(state.get_scene())

    # Get the features of the bulb
    bulb_type = await bulbs[0].get_bulbtype()
    print(bulb_type.features.brightness) # returns True if brightness is supported
    print(bulb_type.features.color) # returns True if color is supported
    print(bulb_type.features.color_tmp) # returns True if color temperatures are supported
    print(bulb_type.features.effect) # returns True if effects are supported
    print(bulb_type.kelvin_range.max) # returns max kelvin in INT
    print(bulb_type.kelvin_range.min) # returns min kelvin in INT
    print(bulb_type.name) # returns the module name of the bulb

    # Turn the light off
    await light.turn_off()

    # Do operations on multiple lights in parallel
    #bulb1 = wizlight("<your bulb1 ip>")
    #bulb2 = wizlight("<your bulb2 ip>")
    # --- DEPRECATED in 3.10 see [#140](https://github.com/sbidy/pywizlight/issues/140)
    # await asyncio.gather(bulb1.turn_on(PilotBuilder(brightness = 255)),
    #    bulb2.turn_on(PilotBuilder(warm_white = 255)))
    # --- For >3.10 await asyncio.gather() from another coroutine
    # async def turn_bulbs_on(bulb1, bulb2):
    #    await asyncio.gather(bulb1.turn_on(PilotBuilder(warm_white=255)), bulb2.turn_on(PilotBuilder(warm_white=255)))
    #  def main:
    #    asyncio.run(async turn_bulbs_on(bulb1, bulb2))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

# CLI (Wiz)
```
$ wizlight
Usage: wizlight [OPTIONS] COMMAND [ARGS]...

  Simple command-line tool to interact with Wizlight bulbs.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  discover  Discover bulb in the local network.
  off       Turn the bulb off.
  on        Turn the bulb on.
  state     Get the current state from the given bulb.
  ```
  
# Run (Lifxlan)
See the examples folder for example scripts that use lifxlan.

To be as generic as possible, the examples use automatic device discovery to find individual bulbs, which causes a short but noticeable delay. To avoid device discovery, you can either instantiate Light objects directly using their MAC address and IP address (which you can learn by running examples/hello_world.py), or you can use the broadcast methods provided in the LifxLAN API. In the examples folder, broadcast_on.py, broadcast_off.py, and broadcast_color.py will allow you to send commands to all lights quickly from the command line without doing device discovery.
