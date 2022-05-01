import asyncio

from pywizlight import wizlight, PilotBuilder, discovery
from lifxlan import LifxLAN, Light


async def main():
    bulbs = await discovery.discover_lights(broadcast_space="x.x.x.x")

    print(f"Bulb IP address: {bulbs[0].ip}")

    for bulb in bulbs:
        print(bulb.__dict__)

    light2 = wizlight("x.x.x.x")
    light = wizlight("x.x.x.x")

    await light.turn_on(PilotBuilder(rgb=(239, 0, 255)))
    await light2.turn_on(PilotBuilder(rgb=(239, 0, 255)))

    await light.turn_off()
    await light2.turn_off()
loop = asyncio.get_event_loop()
loop.run_until_complete(main())

lifxlan = LifxLAN()

livingroom = Light("00:00:00:00:00:00", "x.x.x.x")
livingroom.set_power('on', rapid=True)
livingroom.set_brightness('13000', rapid=True)

livingroom.set_power('off', rapid=True)
