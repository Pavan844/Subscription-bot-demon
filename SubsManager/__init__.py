from logging import ERROR, INFO, FileHandler, StreamHandler, basicConfig, getLogger
from os import getenv
from time import time

from dotenv import load_dotenv
from pyrogram import Client
from pyrogram.enums import ParseMode
from uvloop import install

install()
basicConfig(
    format="[%(asctime)s] [%(levelname)s] - %(message)s",  #  [%(filename)s:%(lineno)d]
    datefmt="%d-%b-%y %I:%M:%S %p",
    handlers=[FileHandler("log.txt"), StreamHandler()],
    level=INFO,
)

getLogger("pyrogram").setLevel(ERROR)
getLogger("pymongo").setLevel(ERROR)
LOGGER = getLogger(__name__)

load_dotenv("config.env", override=True)
BOT_START = time()
bot_cache = {}

bot_chats = {    
      -1002094932065: {
        "prices": {"1d": 10, "30d": 299, "90d": 600},
        "sshots": [
            "https://telegra.ph/file/c1caf4659e5e495355a0a.jpg",
            "https://telegra.ph/file/949cba8c7936a0aef636e.jpg",
            "https://telegra.ph/file/7d9ae2da8f2fc35492597.jpg",
        ],
        "args": {
            "Type": "All type of videos", 
            "Desp": "Nothing to Say, Highly Recommended all type videos include fre user refer and paid"},
    },    
      -1002093797403: {
        "prices": {"365d": 99,  "730d": 199},
        "sshots": [
            "https://telegra.ph/file/408c464aa15decb52d9eb.jpg",
            "https://telegra.ph/file/dbae82f39b64c55668e42.jpg",
            "https://telegra.ph/file/20de33383da6a864395aa.jpg",
        ],
        "args": {
            "Type": "Kannada videos",
            "Desp": "Nothing to Say, Highly Recommended kannada videos",},
      },
   -1002062783095: {
        "prices": {"365d": 99,  "730d": 199},
        "sshots": [
            "https://telegra.ph/file/140319b9aee613f929291.jpg",
        ],
      "args": {      
            "Type": "Ćhìld porn videos",
            "Desp": "Nothing to Say, Highly Recommended childporn",},
     },
      -1002054920818: {
        "prices": {"365d": 99,  "730d": 199},
        "sshots": [
            "https://telegra.ph/file/ae96db554b43c6d6b33a9.jpg",
            "https://telegra.ph/file/8cb81c8c284bd472324b8.jpg",
        ],
          "args": {
            "Type": "R@pe videos",
            "Desp": "Nothing to Say, Highly Recommended rape videos",},
      },
       -1002232203998: { 
         "prices": {"365d": 199,  "180d": 199},       
         "sshots": [ 
            "https://telegra.ph/file/408c464aa15decb52d9eb.jpg",            
            "https://telegra.ph/file/532a4becebb26e6e9faef.jpg", 
            "https://telegra.ph/file/ba9833e773731d8fcd792.jpg", ], 
         "args": {
             "Type": "Over Forced videos", 
             "Desp": "Nothing to Say, Highly Recommended Overforced r@p videos", },
 },

        -1002216476093: {
                 "prices": {"365d": 99,  "730d": 199},       
           "sshots": [
            "https://telegra.ph/file/1999fdbfe4f901a4a1687.jpg",          
            "https://telegra.ph/file/5da582aff1c6e12e39f19.jpg", 
            "https://telegra.ph/file/529c5bd1d6bc29395ccde.jpg",
   ],
        "args": {            
            "Type": "TORCHER",
            "Desp": "Nothing to Say, Highly NOT Recommended TORCHER ",},
     },
     -1002012075373: {
        "prices": {"365d": 99,  "730d": 199},
        "sshots": [
            "https://telegra.ph/file/b061bd85ee8a41565616e.jpg",
        ],
        "args": {
            "Type": "MILFY BOOBS",
            "Desp": "Nothing to Say, Highly Recommended rape videos",},
     },
      -1002187836707: {
        "prices": {"365d": 99,  "730d": 199},        
        "sshots": [
            "https://telegra.ph/file/05719461901faee0b80eb.jpg",          
            "https://telegra.ph/file/1c39a200c1e0e31abc585.jpg", 
            "https://telegra.ph/file/fa83b6ee83dbf9e5bbeb2.jpg",
   ],
        "args": {            
            "Type": "DESI FORIGNERS",
            "Desp": "Nothing to Say, Highly Recommended DESI FORIGNERS PREMIUM 40000 fucking videos",        },       
    },
    -1002057152413: {
        "prices": {"365d": 99,  "730d": 199},
        "sshots": [
            "https://telegra.ph/file/df24b7f1c82a4c02d9cc5.jpg",
            "https://telegra.ph/file/605e243f060edd164f8e8.jpg",
        ],
        "args": {
            "Type": "prajwal revanna",
            "Desp": "Nothing to Say,Highly Recommended prajwal revanna videos",},
    },
     -1002025167901: {
         "prices": {"365d": 99,  "730d": 199},
         "sshots": [
             "https://telegra.ph/file/79fb5774c5cb3a8c44853.jpg",
             "https://telegra.ph/file/e1e1198bdba65e775d2ee.jpg",
         ],
         "args": {
            "Type": "bra panty ",
            "Desp": "Nothing to Say, Highly Recommended bra panty weared videos photos",},
     },
     -1002132453287: {
         "prices": {"365d": 99,  "730d": 199},
         "sshots": [
             "https://telegra.ph/file/2bab102cee5fb4ee33140.jpg",
             "https://telegra.ph/file/2c099023aec4aec9b7608.jpg",
        ],
         "args": {
            "Type": "lebsian ",
            "Desp":"Nothing to Say, Highly Recommended lebsian fucking video videos videos",},
     },
     -1002043373889: {
             "prices": {"365d": 99,  "730d": 199},
             "sshots": [
            "https://telegra.ph/file/03b68799c1e90b0533f50.jpg",
            "https://telegra.ph/file/92f33db2e55a382a74829.jpg",
        ],
        "args": {
            "Type": "Amrature",
            "Desp":"Nothing to Say, Highly Recommended amrature fucking video videos videos",},
      },    
      -1002210339171: {
        "prices": {"365d": 99,  "730d": 199},        
        "sshots": [
            "https://telegra.ph/file/589754769cab455d9894d.jpg",          
            "https://telegra.ph/file/d95bb1bf6a946bd9f332b.jpg", 
            "https://telegra.ph/file/0c269c6c66e85bcfc2fad.jpg",
   ],
        "args": {            
            "Type": "COMBODIAN XXX",
            "Desp": "Nothing to Say, Highly Recommended COMBODIAN fucking videos",},
 },
     -1002143506351: {
        "prices": {"365d": 99,  "730d": 199},
        "sshots": [
            "https://telegra.ph/file/e80391cf199781e178d0c.jpg",
            "https://telegra.ph/file/12ffdffc9522095306f9e.jpg",
        ],
 "args": {
            "Type": "Arkestra",
 "Desp": "Nothing to Say, Highly Recommended Arkestra fucking video videos videos",},
 },
     -1001990894943: {
        "prices": {"365d": 99, "730d": 199},
        "sshots": [
            "https://telegra.ph/file/cebf410aab51a86d89d4a.jpg",
            "https://telegra.ph/file/6aa05ab2113a6873b73e4.jpg",
        ],
         "args": {
            "Type": "Auntys and girls ",
            "Desp": "Nothing to Say, Highly Recommended Auntys and girls fucking video videos videos",},
 },
     -1002014215972: {
        "prices": {"365d": 99,  "730d": 199},
        "sshots": [
            "https://telegra.ph/file/7c20f2a912ff467b74a8c.jpg",
        ],
         "args": {
            "Type": "Fingering girl ",
            "Desp": "Nothing to Say, Highly Recommended Fingering girl  videos videos",},
 },
      -1002035263833: {
        "prices": {"365d": 99,  "730d": 199},
        "sshots": [
           "https://telegra.ph/file/bec5e9ba05e9a8fb384e8.jpg", 
           "https://telegra.ph/file/d92635036084702b8c1cf.jpg",
          ],
 "args": { 
            "Type": "shemale videos",
            "Desp": "Nothing to Say, Highly Recommended shemale videos",},
 },
     -1002115785604: {
        "prices": {"365d": 99,  "730d": 199},
        "sshots": [
            "https://telegra.ph/file/df9b00a2e86cff722ca1b.jpg",
            "https://telegra.ph/file/fffa68c3cfe6823d3f7ec.jpg",
            "https://telegra.ph/file/4227c068cc7c0465b43ea.jpg", 
        ], 
         "args": {
            "Type": "BLOW JOB",
 "Desp": "Nothing to Say, Highly Recommended Ony blow job videos",},
 },
     -1002021845785: {
        "prices": {"365d": 99,  "730d": 199},
        "sshots": [
            "https://telegra.ph/file/c8c891a6869341c9c03b9.jpg", 
            "https://telegra.ph/file/839fe37996b3847b79355.jpg", 
        ],
         "args": {
            "Type": "Real Mom son ",
            "Desp": "Nothing to Say, Highly Recommended Real Mom son adult fucking video videos videos",},
},    
   -1002097246586: {
        "prices": {"365d": 99,  "730d": 199},
        "sshots": [
            "https://telegra.ph/file/cecfc6dedfed35c28287a.png",
            "https://telegra.ph/file/5ddaaab9d18f7148a6b9c.png",
        ],
        "args": {
            "Type": "pedro mom videos",
            "Desp": "Nothing to Say, Highly Recommended pedro mom videos ",},
 },
    -1002052874333: {
        "prices": {"365d": 99,  "730d": 199},
        "sshots": [
            "https://telegra.ph/file/1d516853b93e511e3199e.jpg",
        ],
        "args": {
            "Type": "Real muslim mom videos",
            "Desp": "Nothing to Say, Highly Recommended Real muslim mom videos",},
 },
         -1002054957272: {
        "prices": {"365d": 99,  "730d": 199}, 
        "sshots": [
            "https://telegra.ph/file/23f666e437392b5139cbb.jpg", 
        ],
 "args": {
            "Type": "Spy dressing mom",
            "Desp": "Nothing to Say, Highly Recommended Spy dressing mom videos", }, 
 },
     -1002059225110: {
        "prices": {"365d": 99,  "730d": 199}, 
        "sshots": [
        "https://telegra.ph/file/047a27315bd1db94239a0.jpg", 
        ],
"args": {
            "Type": "Mom vc cough",
            "Desp": "Nothing to Say, Highly Recommended Mom vc cough while calling to boy freind .videos",}, 
 },
    -1002014191919: {
        "prices": {"365d": 99,  "730d": 199}, 
        "sshots": [
            "https://telegra.ph/file/84a2d1b8f46ebfc225947.jpg", 
        ],
          "args": {
            "Type": "Mom spy",
            "Desp": "Nothing to Say, Highly Recommended Son Spys his mom in full mood and jerk videos",},
 },
      -1002013265570: { 
        "prices": {"365d": 99,  "730d": 199}, 
        "sshots": [
            "https://telegra.ph/file/19fe32bd5da075d8a92b0.jpg",
            "https://telegra.ph/file/f3ab30b519e105f028158.jpg",
        ], "args": {
            "Type": "Mom son Indian",
            "Desp": "Nothing to Say, Highly Recommended MOM SON FUCKS TO GETHER WHEN FATHER NOT THERE fucking  videos",},
},
      -1002176904721: {
        "prices": {"365d": 99,  "730d": 199},        
        "sshots": [
            "https://telegra.ph/file/b9d65d7f7c32d8c7d505b.jpg",          
            "https://telegra.ph/file/94b3b342dd1615ddda1bb.jpg", 
            "https://telegra.ph/file/35f449cb8a300e2b848f0.jpg",
   ],
        "args": {           
            "Type": "FANTASY PICS ",
            "Desp": "Nothing to Say, Highly Recommended FANTASY PICS PHOTOS 40000 fucking videos",        },
     },
      -1002170912336: {
        "prices": {"365d": 99,  "730d": 199},
        "sshots": [
            "https://telegra.ph/file/5ae3eb6c580f999caa764.jpg",          
            "https://telegra.ph/file/de9fdf9de0ca1456a2332.jpg", 
            "https://telegra.ph/file/03bf3e7c088420818117f.jpg",
   ],
        "args": {
            "Type": "naughty america",
            "Desp": "Nothing to Say, Highly Recommended NAUGHTY AMERICA  fucking videos",        },
     },
     -1002161538113: {
        "prices": {"365d": 99,  "730d": 199},
        "sshots": [
            "https://telegra.ph/file/99626b28cf3415d60a4e4.jpg",          
            "https://telegra.ph/file/3da95da0e8fefb87538c7.jpg", 
            "https://telegra.ph/file/062f5c9881844ab7f7388.jpg", 
   
   ],
        "args": {    "Type": "BRAZZERS PREMIUM",
                     "Desp": "Nothing to Say, Highly Recommended BRAZZERS PREMIUM 40000 fucking videos",        },
     },
       -1002234327122: {
        "prices": {"365d": 99,  "730d": 199},        "sshots": [
            "https://telegra.ph/file/e8edf671cc53a36366a7d.jpg",          
            "https://telegra.ph/file/0496f1154295110f9809a.jpg",
 ],
            "args": {
            "Type": "RED PORN PREMIUM",
            "Desp": "Nothing to Say, Highly Recommended REDPORN PREMIUM fucking videos",  },
     },
     -1002220464336: {
        "prices": {"1d": 10, "30d": 28, "90d": 70},
        "sshots": [
            "https://te.legra.ph/file/e3aaee8624be55289c771.jpg",
            "https://te.legra.ph/file/949cba8c7936a0aef636e.jpg",
            "https://te.legra.ph/file/949cba8c7936a0aef636e.jpg",
        ],
        "args": {
            "Type": "test1",
            "Desp": "Nothing to Say, Highly Recommended with wide varieties",
        },
    },
}



class Config:
    BOT_TOKEN = getenv("BOT_TOKEN", "7080709991:AAFXSt9i4k6OypBcPSd8KllkiucXR4_sMho")
    API_HASH = getenv("API_HASH", "7b93fc0adc30039f74a7faeba4a3875d")
    API_ID = getenv("API_ID", "20508620")
    if BOT_TOKEN == "" or API_HASH == "" or API_ID == "":
        LOGGER.critical("ENV Missing. Exiting Now...")
        exit(1)
    LOG_CHAT = int(getenv("LOG_CHAT", "-1002061267081"))
    ADMINS = list(map(int, getenv("ADMINS", "6059507751 6822467996 6971938312").split()))
    MONGODB_URL = getenv("MONGODB_URL", "mongodb+srv://kp9731818219:A6j4uZkfAhymgclV@cluster0.zanohyt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    AUTO_APPROVE = getenv("AUTO_APPROVE", "false").lower() == "true"
    REF_NEEDED = int(getenv("REF_NEEDED", "40"))

bot = Client(
    "Subs-Bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="SubsManager/plugins"),
    parse_mode=ParseMode.HTML,
    workers=1000,
    in_memory=True,
)
