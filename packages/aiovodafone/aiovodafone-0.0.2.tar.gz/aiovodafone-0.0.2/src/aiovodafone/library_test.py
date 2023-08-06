from aiovodafone import VodafoneStationApi
import asyncio

host = "192.168.1.1"
ssl = True
username = "vodafone"
password = "put-your-password-here"

async def main():
    api = VodafoneStationApi(host,ssl, username, "D8QLRCEGG4L2")
    logged = await api.login()
    print(logged)
    await api.logout()

if __name__ == "__main__":
    asyncio.run(main())
