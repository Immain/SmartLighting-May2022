import asyncio

from pywizlight import wizlight, PilotBuilder, discovery


async def main():
    bulbs = await discovery.discover_lights(broadcast_space="x.x.x.x")

    print(f"Bulb IP address: {bulbs[0].ip}")

    for bulb in bulbs:
        print(bulb.__dict__)

    light = wizlight("x.x.x.x")

    await light.turn_on(PilotBuilder(rgb=(239, 0, 255)))


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
