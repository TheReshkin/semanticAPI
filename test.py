from user_data import user
import asyncio


async def test():
    print("_testing")
    data = await user.sign_in("max")
    if data:
        print(data)
    else:
        raise StopAsyncIteration


if __name__ == "__main__":
    testing_uid = asyncio.get_event_loop().run_until_complete(test())
