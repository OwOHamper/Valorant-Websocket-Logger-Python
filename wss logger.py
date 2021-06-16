import asyncio
import ssl
import websockets
import base64
import os

lockfile = {}


try:
    with open(os.path.join(os.getenv('LOCALAPPDATA'), R'Riot Games\Riot Client\Config\lockfile')) as lockfile:
        data = lockfile.read().split(':')
        keys = ['name', 'PID', 'port', 'password', 'protocol']
        lockfile = dict(zip(keys, data))
except:
    raise Exception("Lockfile not found")




ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

local_headers = {}
local_headers['Authorization'] = 'Basic ' + base64.b64encode(('riot:' + lockfile['password']).encode()).decode()

async def ws():
    async with websockets.connect(f"wss://127.0.0.1:{lockfile['port']}", ssl=ssl_context, extra_headers=local_headers) as websocket:
        await websocket.send("[5, \"OnJsonApiEvent\"]")

        while True:
            response = await websocket.recv()
            print(response)


asyncio.get_event_loop().run_until_complete(ws())
asyncio.get_event_loop().run_forever()