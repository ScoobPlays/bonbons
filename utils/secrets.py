from motor import motor_asyncio


cluster = motor_asyncio.AsyncIOMotorClient("mongodb+srv://kayle:kaylebetter@cluster0.s0wqa.mongodb.net/discord?retryWrites=true&w=majority")
database = cluster["discord"]
starboard = database["starboard"]
config = database["config"]

headers = {
    'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
    'x-rapidapi-key': "c8b299ee91msha4c1921cebbedabp1f70a0jsnc4c1cc4b9c5c"
    }