import asyncio

from aiovantage import Vantage

load_id = 1436

async def test_rgbw_loads() -> None:
    async with Vantage("10.2.0.103", "administrator", "ZZuUw76CnL") as vantage:
        await vantage.rgb_loads.initialize()
        await vantage.rgb_loads.set_rgbw(load_id, 128, 0, 0, 255)
        rgbw = await vantage.rgb_loads.get_rgbw(load_id)
        assert rgbw == (128, 0, 0, 255)

        print(await vantage.rgb_loads.get_level(load_id))

        await vantage.rgb_loads.set_level(load_id, 100)
        rgbw = await vantage.rgb_loads.get_rgbw(load_id)
        print(rgbw)
        await vantage.rgb_loads.set_rgb_component(load_id, 3, 255)
        rgbw = await vantage.rgb_loads.get_rgbw(load_id)
        print(rgbw)


asyncio.run(test_rgbw_loads())
