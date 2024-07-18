from motor.motor_asyncio import AsyncIOMotorClient

from SubsManager import Config


class Database:
    def __init__(self, uri, database_name):
        self._client = AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.pusers = self.db.users
        self.grps = self.db.groups

    async def _defData(self, uid):
        return dict(_id=uid, prem_chats={}, my_cart={}, prev_trans=[], refers=dict(is_ref=False, uids=[]))

    async def _getUser(self, uid, val=None, _def=None):
        usr = await self.pusers.find_one({"_id": uid})
        if not usr:
            await self.pusers.insert_one(await self._defData(uid))
            usr = await self.pusers.find_one({"_id": uid})
        if val:
            return usr.get(val, _def)
        return usr
        
    async def _updateGroup(self, gid):
        grp = await self.grps.find_one({"_id": gid})
        if not grp:
            await self.grps.insert_one(dict(_id=gid))

    async def _setUserData(self, uid, data=None, key=None, value=None):
        await self._getUser(uid)
        if key:
            await self.pusers.update_one({"_id": uid}, {"$set": {key: value}})
        elif data:
            await self.pusers.update_one({"_id": uid}, {"$set": data})

    async def _rmUserData(self, uid):
        await self.pusers.delete_one({"_id": uid})
        
    async def _rmGroup(self, gid):
        await self.grps.delete_one(dict(_id=gid))

    async def _totalUsers(self):
        return await self.pusers.count_documents({})

    async def _getAllGrps(self):
        return self.grps.find({})
    
    async def _getAllUsers(self):
        return self.pusers.find({})


db = Database(Config.MONGODB_URL, "SubsManager")
