import base64
import json
import pyperclip

raw = pyperclip.paste()
save = raw.split("Fe12NAfA3R6z4k0z")[0]
save_json_base64 = ''.join([char for char in save[::2]])
save_json = base64.b64decode(save_json_base64).decode('UTF-8')
# print(json.dumps(json.loads(save_json), sort_keys=True, indent=4))
savegame = json.loads(save_json)

# print(savegame['rubies'])

"""
Usefull info :
    currentZoneHeight
    gold
    heroCollection {}
    highestFinishedZone
    readPatchNumber
    skillCooldowns {}

{
    "abaddonMultiplier": 1,
    "account": null,
    "accountId": 0,
    "achievements": {
        "1": true,
        "10": true,
        "11": true,
        "12": true,
        "13": true,
        "14": true,
        "15": true,
        "17": true,
        "18": true,
        "19": true,
        "2": true,
        "21": true,
        "25": true,
        "26": true,
        "27": true,
        "29": true,
        "3": true,
        "30": true,
        "31": true,
        "33": true,
        "34": true,
        "35": true,
        "36": true,
        "37": true,
        "38": true,
        "39": true,
        "4": true,
        "40": true,
        "41": true,
        "42": true,
        "47": true,
        "5": true,
        "50": true,
        "6": true,
        "61": true,
        "7": true,
        "8": true,
        "9": true
    },
    "actionBar": {},
    "activityCount": 262632,
    "activityRoller": null,
    "adCampaign": null,
    "adRetargetId": null,
    "adRetargetTime": 0,
    "allDpsMultiplier": 11.232423798750004,
    "ancientEntrySizes": {},
    "ancientSouls": 0,
    "ancientSoulsTotal": 0,
    "ancients": {
        "_currentUids": null,
        "ancients": {
            "29": {
                "id": 29,
                "level": "1",
                "locked": true,
                "purchaseTime": 1487019748361,
                "spentHeroSouls": "1",
                "uid": 29
            }
        },
        "ancientsRoller": {
            "numUses": 3,
            "seed": 1216404991
        },
        "artificiallyRaisedAncients": {},
        "numPurchased": 0,
        "numRerolls": 0,
        "rerollSoulsSpent": "0"
    },
    "appliedDLC": {},
    "autoclickerSkins": {
        "1": true
    },
    "autoclickers": 0,
    "baseClickDamage": 5,
    "baseCriticalClickChance": 9,
    "buyExactQuantity": false,
    "candyCanes": 0,
    "candyCanesEarned": 0,
    "clickDpsPercent": 3,
    "clickMultiplier": 210,
    "clickmasRoller": {
        "numUses": 0,
        "seed": 601390215
    },
    "clickmasRubiesEarned": 0,
    "collectedAchievements": {},
    "collectedRaidRewardDates": {},
    "creationTimestamp": 1484512256256,
    "criticalMultiplier": 18,
    "currentActivityOrderNumber": 0,
    "currentAutoclickerSkin": 1,
    "currentZoneHeight": 129,
    "damageFloatersDisabled": true,
    "darkRitualClicks": 4,
    "debug": false,
    "devGifts": {},
    "didClickOnAncientsTab": true,
    "didClickOnMercenaryTab": false,
    "didClickOnShopTab": false,
    "didClickOnTranscendenceTab": false,
    "dlcAutoclickers": 0,
    "dpsSacrificedInWorldResets": 0,
    "email": "",
    "epicHeroReceivedUpTo": 120,
    "epicHeroSeed": 609258674.015625,
    "epicRoller": {
        "numUses": 0,
        "seed": 601056882
    },
    "extraGildsAwarded": 0,
    "finishedPrimals": {
        "100": true,
        "110": true,
        "115": true,
        "120": true
    },
    "forgeCoals": 0,
    "freeRespecs": 0,
    "gold": "1.392234086999386e27",
    "goldFloatersDisabled": true,
    "goldMultiplier": 2.9296875,
    "goldQuestsCompleted": 0,
    "goldSacrificedInWorldResets": 0,
    "hasJoinedGuild": false,
    "hasSeenNewShopItems": true,
    "hasSeenZone100Tip": null,
    "heroCollection": {
        "_currentUids": {
            "heroes": 46
        },
        "heroes": {
            "1": {
                "damageMultiplier": "1",
                "epicLevel": 0,
                "id": 1,
                "level": 705,
                "locked": false,
                "uid": 1
            },
            "10": {
                "damageMultiplier": "8.4934656e7",
                "epicLevel": 0,
                "id": 10,
                "level": 495,
                "locked": false,
                "uid": 10
            },
            "11": {
                "damageMultiplier": "5.24288e6",
                "epicLevel": 0,
                "id": 11,
                "level": 421,
                "locked": false,
                "uid": 11
            },
            "12": {
                "damageMultiplier": "3.2768e5",
                "epicLevel": 0,
                "id": 12,
                "level": 370,
                "locked": false,
                "uid": 12
            },
            "13": {
                "damageMultiplier": "1.31072e6",
                "epicLevel": 0,
                "id": 13,
                "level": 397,
                "locked": false,
                "uid": 13
            },
            "14": {
                "damageMultiplier": "10240",
                "epicLevel": 1,
                "id": 14,
                "level": 315,
                "locked": false,
                "uid": 14
            },
            "15": {
                "damageMultiplier": "20480",
                "epicLevel": 0,
                "id": 15,
                "level": 302,
                "locked": false,
                "uid": 15
            },
            "16": {
                "damageMultiplier": "256",
                "epicLevel": 0,
                "id": 16,
                "level": 275,
                "locked": false,
                "uid": 16
            },
            "17": {
                "damageMultiplier": "1280",
                "epicLevel": 0,
                "id": 17,
                "level": 258,
                "locked": false,
                "uid": 17
            },
            "18": {
                "damageMultiplier": "45.5625",
                "epicLevel": 0,
                "id": 18,
                "level": 200,
                "locked": false,
                "uid": 18
            },
            "19": {
                "damageMultiplier": "80",
                "epicLevel": 0,
                "id": 19,
                "level": 221,
                "locked": false,
                "uid": 19
            },
            "2": {
                "damageMultiplier": "2.1990232555520004e13",
                "epicLevel": 0,
                "id": 2,
                "level": 699,
                "locked": false,
                "uid": 2
            },
            "20": {
                "damageMultiplier": "2",
                "epicLevel": 0,
                "id": 20,
                "level": 145,
                "locked": false,
                "uid": 20
            },
            "21": {
                "damageMultiplier": "8",
                "epicLevel": 0,
                "id": 21,
                "level": 107,
                "locked": false,
                "uid": 21
            },
            "22": {
                "damageMultiplier": "16",
                "epicLevel": 0,
                "id": 22,
                "level": 100,
                "locked": false,
                "uid": 22
            },
            "23": {
                "damageMultiplier": "8",
                "epicLevel": 0,
                "id": 23,
                "level": 100,
                "locked": false,
                "uid": 23
            },
            "24": {
                "damageMultiplier": "4",
                "epicLevel": 1,
                "id": 24,
                "level": 63,
                "locked": false,
                "uid": 24
            },
            "25": {
                "damageMultiplier": "1",
                "epicLevel": 0,
                "id": 25,
                "level": 14,
                "locked": false,
                "uid": 25
            },
            "26": {
                "damageMultiplier": "1",
                "epicLevel": 1,
                "id": 26,
                "level": 2,
                "locked": false,
                "uid": 26
            },
            "27": {
                "damageMultiplier": "1",
                "epicLevel": 0,
                "id": 27,
                "level": 0,
                "locked": true,
                "uid": 27
            },
            "28": {
                "damageMultiplier": "1",
                "epicLevel": 0,
                "id": 28,
                "level": 0,
                "locked": true,
                "uid": 28
            },
            "29": {
                "damageMultiplier": "1",
                "epicLevel": 0,
                "id": 29,
                "level": 0,
                "locked": true,
                "uid": 29
            },
            "3": {
                "damageMultiplier": "1.37438953472e12",
                "epicLevel": 0,
                "id": 3,
                "level": 649,
                "locked": false,
                "uid": 3
            },
            "30": {
                "damageMultiplier": "1",
                "epicLevel": 0,
                "id": 30,
                "level": 0,
                "locked": true,
                "uid": 30
            },
            "31": {
                "damageMultiplier": "1",
                "epicLevel": 0,
                "id": 31,
                "level": 0,
                "locked": true,
                "uid": 31
            },
            "32": {
                "damageMultiplier": "1",
                "epicLevel": 0,
                "id": 32,
                "level": 0,
                "locked": true,
                "uid": 32
            },
            "33": {
                "damageMultiplier": "1",
                "epicLevel": 0,
                "id": 33,
                "level": 0,
                "locked": true,
                "uid": 33
            },
            "34": {
                "damageMultiplier": "1",
                "epicLevel": 0,
                "id": 34,
                "level": 0,
                "locked": true,
                "uid": 34
            },
            "35": {
                "damageMultiplier": "1",
                "epicLevel": 0,
                "id": 35,
                "level": 0,
                "locked": true,
                "uid": 35
            },
            "36": {
                "damageMultiplier": "1",
                "epicLevel": 0,
                "id": 36,
                "level": 0,
                "locked": true,
                "uid": 36
            },
            "37": {
                "damageMultiplier": "1",
                "epicLevel": 0,
                "id": 37,
                "level": 0,
                "locked": true,
                "uid": 37
            },
            "38": {
                "damageMultiplier": "1",
                "epicLevel": 0,
                "id": 38,
                "level": 0,
                "locked": true,
                "uid": 38
            },
            "39": {
                "damageMultiplier": "1",
                "epicLevel": 0,
                "id": 39,
                "level": 0,
                "locked": true,
                "uid": 39
            },
            "4": {
                "damageMultiplier": "3.435973836800001e11",
                "epicLevel": 0,
                "id": 4,
                "level": 607,
                "locked": false,
                "uid": 4
            },
            "40": {
                "damageMultiplier": "1",
                "epicLevel": 0,
                "id": 40,
                "level": 0,
                "locked": true,
                "uid": 40
            },
            "41": {
                "damageMultiplier": "1",
                "epicLevel": 0,
                "id": 41,
                "level": 0,
                "locked": true,
                "uid": 41
            },
            "42": {
                "damageMultiplier": "1",
                "epicLevel": 0,
                "id": 42,
                "level": 0,
                "locked": true,
                "uid": 42
            },
            "43": {
                "damageMultiplier": "1",
                "epicLevel": 0,
                "id": 43,
                "level": 0,
                "locked": true,
                "uid": 43
            },
            "44": {
                "damageMultiplier": "1",
                "epicLevel": 0,
                "id": 44,
                "level": 0,
                "locked": true,
                "uid": 44
            },
            "45": {
                "damageMultiplier": "1",
                "epicLevel": 0,
                "id": 45,
                "level": 0,
                "locked": true,
                "uid": 45
            },
            "5": {
                "damageMultiplier": "5.497558138880001e11",
                "epicLevel": 0,
                "id": 5,
                "level": 627,
                "locked": false,
                "uid": 5
            },
            "6": {
                "damageMultiplier": "4.294967296000001e9",
                "epicLevel": 0,
                "id": 6,
                "level": 588,
                "locked": false,
                "uid": 6
            },
            "7": {
                "damageMultiplier": "8.589934592e10",
                "epicLevel": 0,
                "id": 7,
                "level": 595,
                "locked": false,
                "uid": 7
            },
            "8": {
                "damageMultiplier": "1.3421772800000005e8",
                "epicLevel": 0,
                "id": 8,
                "level": 496,
                "locked": false,
                "uid": 8
            },
            "9": {
                "damageMultiplier": "1.3421772800000005e9",
                "epicLevel": 0,
                "id": 9,
                "level": 512,
                "locked": false,
                "uid": 9
            }
        },
        "maxSize": 256
    },
    "heroEntrySizes": {},
    "heroSoulQuestsCompleted": 0,
    "heroSouls": "0",
    "heroSoulsSacrificed": "0",
    "hideRelicPopups": true,
    "highestFinishedZone": 129,
    "highestFinishedZonePersist": 129,
    "highestGold": "4.238354773374177e27",
    "highestHistoricAncients": 1,
    "highestMercenaryLevelEver": 0,
    "historicRubies": 26,
    "isBanned": false,
    "isCheater": false,
    "isTestUser": false,
    "items": {
        "_currentUids": null,
        "ascensionItemsRoller": {
            "numUses": 0,
            "seed": 601056882
        },
        "bonusZoneRoller": {
            "numUses": 0,
            "seed": 601056882
        },
        "equipmentSlots": 4,
        "gotAscensionItem": false,
        "guildItemsRoller": {
            "numUses": 0,
            "seed": 601056882
        },
        "items": {},
        "salvagePoints": 0,
        "slots": {}
    },
    "kongId": "",
    "language": null,
    "lastAdBonusTimestamp": 0,
    "lastGuildRankUpdatedTime": 0,
    "lastLoadTime": 0,
    "lastMiniGameStartTime": 0,
    "lastPageLoadTime": 0,
    "lastPrimalLevelChecked": 130,
    "lastPrimalLevelResult": true,
    "lastRaidTimestamp": 0,
    "lastSkillUsed": 1,
    "latestBuildLoaded": 107,
    "leeroyJenkinsBuried": 0,
    "lifetimeDarkRitualClicks": 4,
    "loginValidated": false,
    "maxDps": "2.553205996960652e24",
    "mercenaries": {
        "_currentUids": null,
        "hasGivenOneFreeRecruit": false,
        "mercRoller": {
            "numUses": 0,
            "seed": 601167993
        },
        "mercenaries": {},
        "questOptions": {},
        "questRoller": {
            "numUses": 0,
            "seed": 601279104
        },
        "startRecruitTime": 0
    },
    "mercenaryCount": 0,
    "mostClicksPerSecond": 58,
    "mostCritsPerSecond": 34,
    "musicEnabled": false,
    "numAscensionsThisTranscension": 0,
    "numPageLoads": 0,
    "numRaidsToday": 0,
    "numWorldResets": 0,
    "numberDisplayMode": false,
    "numberOfTranscensions": 0,
    "openedClickmasPresents": 0,
    "outsiderEntrySizes": {},
    "outsiders": {
        "_currentUids": null,
        "outsiders": {
            "1": {
                "id": 1,
                "level": 0,
                "spentAncientSouls": 0,
                "uid": 1
            },
            "2": {
                "id": 2,
                "level": 0,
                "spentAncientSouls": 0,
                "uid": 2
            },
            "3": {
                "id": 3,
                "level": 0,
                "spentAncientSouls": 0,
                "uid": 3
            },
            "4": {
                "id": 4,
                "level": 0,
                "spentAncientSouls": 0,
                "uid": 4
            },
            "5": {
                "id": 5,
                "level": 0,
                "spentAncientSouls": 0,
                "uid": 5
            }
        }
    },
    "paidForRubyMultiplier": false,
    "passwordHash": "06n58MaEqXmOSp6K",
    "persistentVars": {
        "allVisualEffects": true,
        "bloopCoinRequestDonationTimestamp": 0,
        "bloopCoins": 0,
        "bossDefeatHelpTimestamp": 0,
        "christmasSaleBuys": 0,
        "cooldownNotificationsEnabled": true,
        "didOpenAncientScreen": false,
        "didOpenOnlineSave": true,
        "didOpenShop": false,
        "didPurchaseSkill": true,
        "didShowTranscendenceNews": false,
        "didUseSkill": true,
        "fullScreen": false,
        "goldNotificationsEnabled": true,
        "halloweenSaleBuys": 0,
        "karma": 0,
        "mercenaryNotificationsEnabled": true,
        "nextRatePromptTime": 0,
        "preloadAds": true,
        "previousEventAdsTimestamp": 0,
        "previousMainScreenAdsTimestamp": 0,
        "previousPermaAdsTimestamp": 0,
        "pwbClosest": 0,
        "pwbHelp": false,
        "pwbPlayed": 0,
        "pwbWon": 0,
        "showBossDefeatHelp": true,
        "showGildedHeroHelp": true,
        "showItemHelp": true,
        "showLevel100Help": true,
        "showPrimalBossHelp": true
    },
    "personalSales": {
        "_largestPurchaseBundleId": 0,
        "_numHistoricSales": 0,
        "_saleEndTimestamp": 1484512255,
        "flashSalesEnabled": false,
        "seasonalSalesEnabled": true
    },
    "pretranscendentHighestFinishedZone": 129,
    "prevLoginTimestamp": 1487282526790,
    "primalNumberGenerator": {
        "numUses": 3,
        "seed": 339909894
    },
    "primalSouls": "4",
    "privateAdminMessages": {},
    "purchaseHashes": {},
    "purchaseRecord": {},
    "purchasedGilds": 0,
    "purchasedTitanFightExpTime": 0,
    "rarestMercenaryEver": 1,
    "readPatchNumber": "1.0e8",
    "relicQuestsCompleted": 0,
    "relicsReceivedThisTranscension": 0,
    "remoteQueue": null,
    "respondedToEmailSequelPrompt": false,
    "respondedToSurvey": false,
    "revision": 0,
    "rubies": 26,
    "rubyClickablesThisAscension": 25,
    "rubyQuestsCompleted": 0,
    "secondToLastSkillUsed": 2,
    "settings": null,
    "shouldAutoSetHeroDpsDisplay": false,
    "shouldShowHeroDps": true,
    "skillClickMultiplier": 2,
    "skillClickMultiplierEnd": 1487282265889,
    "skillCooldowns": {
        "1": 1487282238186,
        "2": 1487282237788,
        "3": 1487282237480,
        "4": 1487282237063,
        "5": 1487281600210,
        "6": 1487282236634,
        "7": 1487282235889,
        "8": 1487281601021
    },
    "skillCriticalClickChance": 50,
    "skillCriticalClickChanceEnd": 1487282267480,
    "skillDouble": false,
    "skillDpsMultiplier": 1,
    "skillDpsMultiplierEnd": 1487282267788,
    "skillFreeClicks": 10,
    "skillFreeClicksEnd": 1487282268186,
    "skillGoldBonus": 1,
    "skillGoldBonusEnd": 1487282267063,
    "skillQuestsCompleted": 0,
    "skillWildGold": 1,
    "skillWildGoldEnd": 1487282266634,
    "soulsSpent": "0",
    "soundsEnabled": false,
    "stageQuality": false,
    "startTimestamp": 1484512256255,
    "syncedGameServices": false,
    "ticketsUsed": "",
    "timelapses": 0,
    "tinyMonsters": true,
    "titanDamage": "4",
    "titanTypesDefeated": {},
    "total5MinuteQuests": 0,
    "totalBossKills": 29,
    "totalClicks": 237184,
    "totalCreditsPurchased": 0,
    "totalCrits": 16319,
    "totalGold": "5.898037299111212e27",
    "totalGoldThisGame": "5.898037299111212e27",
    "totalHeroLevels": 9263,
    "totalHeroSouls": "0",
    "totalHeroSoulsFromAscensions": "0",
    "totalKills": 87418.1618472896,
    "totalMercenariesBuried": 0,
    "totalMercenariesRevived": 0,
    "totalMoneySpent": 0,
    "totalPrimalsKilled": 4,
    "totalRelicsReceived": 0,
    "totalUpgrades": 112,
    "transcendent": false,
    "transcendentHighestFinishedZone": 0,
    "transcensionTimestamp": 0,
    "transparentAutoclickerMode": false,
    "treasureChestsKilled": 95,
    "tutorialArrow": 2,
    "uid": null,
    "uniqueId": "14845122619540003126564435660839",
    "unixTimestamp": 1487282526671,
    "unopenedClickmasPresents": 0,
    "upgrades": {
        "10": true,
        "100": true,
        "101": true,
        "102": true,
        "103": true,
        "104": true,
        "105": true,
        "106": false,
        "108": true,
        "109": true,
        "11": true,
        "110": true,
        "112": true,
        "113": true,
        "114": true,
        "116": true,
        "117": true,
        "119": true,
        "12": true,
        "120": true,
        "13": true,
        "132": false,
        "14": true,
        "15": true,
        "16": true,
        "17": true,
        "18": true,
        "19": true,
        "2": true,
        "20": true,
        "21": true,
        "22": true,
        "23": true,
        "24": true,
        "25": true,
        "26": true,
        "27": true,
        "28": true,
        "29": true,
        "3": true,
        "30": true,
        "31": true,
        "32": true,
        "33": true,
        "34": true,
        "35": true,
        "36": true,
        "37": true,
        "38": true,
        "39": true,
        "4": true,
        "40": true,
        "41": true,
        "42": true,
        "43": true,
        "44": true,
        "45": true,
        "46": true,
        "47": true,
        "48": true,
        "49": true,
        "5": true,
        "50": true,
        "51": true,
        "52": true,
        "53": true,
        "54": true,
        "55": true,
        "56": true,
        "57": true,
        "58": true,
        "59": true,
        "6": true,
        "60": true,
        "61": true,
        "62": true,
        "63": true,
        "64": true,
        "65": true,
        "66": true,
        "67": true,
        "68": true,
        "69": true,
        "7": true,
        "70": true,
        "71": true,
        "72": true,
        "73": true,
        "74": true,
        "75": true,
        "76": true,
        "77": true,
        "78": true,
        "79": true,
        "8": true,
        "80": true,
        "81": true,
        "82": true,
        "83": true,
        "84": true,
        "85": true,
        "86": true,
        "87": true,
        "88": true,
        "89": true,
        "9": true,
        "90": true,
        "91": true,
        "92": true,
        "93": true,
        "94": true,
        "96": true,
        "97": true,
        "98": true
    },
    "usedSkills": {
        "1": true,
        "2": true,
        "3": true,
        "4": true,
        "5": true,
        "6": true,
        "7": true,
        "8": true
    },
    "version": 7,
    "worldGoldBonus": 0
}

"""