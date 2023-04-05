from motor.motor_tornado import MotorClient





cluster = MotorClient("mongodb+srv://mircus:0x14lzl04t39igh@botcluster.omo2cfl.mongodb.net/?retryWrites=true&w=majority")
db = cluster['botdb']
collection = db['users']
collection_shop = db['shop']
collection_marrys = db['marrys']
