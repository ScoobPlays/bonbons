from motor import motor_asyncio
import os

cluster = motor_asyncio.AsyncIOMotorClient(os.environ.get('mongo_token'))

db = cluster["discord"]
starboard = db["starboard"]
config = db["config"]
thank = db["thank"]
nft = db["nft"]
levels = db["levels"]


headers = {
    "x-rapidapi-host": os.environ.get('x_host'),
    "x-rapidapi-key": os.environ.get('x_key'),
}
