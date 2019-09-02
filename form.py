#-*-coding:utf-8-*-
import json
import func

home_menu = {
            "listCard": {
                "header": {
                    "title": "Home",
                },
                "items": [
                {
                    "title": "딩굴이의 혼잣말",
                    "description": "\"챗봇으로 전환하기\"를 해야 작동합니다!"
                }
                ],
                "buttons": [
                {
                    "label": "식단 보기",
                    "action": "message",
                    "messageText": "식단 보기"
                },
                {
                    "label": "생활 정보",
                    "action": "message",
                    "messageText": "생활 정보"
                }
                ]
            }
}

lifeinfo_menu = {
            "listCard": {
                "header": {
                    "title": "생활정보",
                },
                "items": [
                {
                    "title": "셔틀버스",
                    "description": "DGIST 셔틀버스 시간표를 확인하세요",
                    "link": {
                        "web": "https://www.dgist.ac.kr/kr/html/sub04/0406.html?sch_tab=tab3"
                    }
                },
                {
                    "title": "급행8 (대곡역)",
                    "description": "급행8의 대곡역 출발 시각을 확인하세요",
                    "link": {
                        "web": "http://m.businfo.go.kr/bp/m/realTime.do?act=arrInfo&bsId=7041033800&bsNm=%B4%EB%B0%EE%BF%AA(%C7%D1%B6%F3%C7%CF%BF%EC%C1%A8%C6%AE%B0%C7%B3%CA)"
                    }
                },
                {
                    "title": "급행8 (위치)",
                    "description": "급행8 위치를 확인하세요",
                    "link": {
                        "web": "http://m.businfo.go.kr/bp/m/realTime.do?act=posInfoMain&roNo=%B1%DE%C7%E08"
                    }
                },
                {
                    "title": "개설교과목조회",
                    "description": "개설교과목을 확인하세요",
                    "link": {
                        "web": "https://welcome.dgist.ac.kr/ucs/ucsqProfRespSbjtInq/index.do#"
# "web": "https://www.dgist.ac.kr/kr/html/sub04/040208.html"
                    }
                },
                {
                    "title": "조직도",
                    "description": "교직원 연락처를 확인하세요 (053-785-)",
                    "link": {
                        "web": "https://www.dgist.ac.kr/kr/html/sub01/010401.html"
                    }
                }
                ],
                "buttons": [
                {
                    "label": "오류 제보하기",
                    "action": "operator",
                    "messageText": "상담원과 연결합니다."
                },
                {
                    "label": "메인으로",
                    "action": "message",
                    "messageText": "홈"
                }
                ]
            }
}

lifeinfo = {
    "version": "2.0",
    "template": {
        "outputs": [
            lifeinfo_menu
         ]
    }
}


home = {
    "version": "2.0",
    "template": {
        "outputs": [
            home_menu
        ]        
    }
}

bob_menu = {
    "listCard": {
        "header": {
            "title": "오늘의 점심"
        },
        "items": [
        {
            "title": "학생식당 ",
            "description": "",
            "imageUrl": "",
            "link" : {
                "web" : ""
            }
        },
        {
            "title": "연구동   ",
            "description": "",
            "imageUrl": "",
            "link" : {
                "web" : ""
            }
        },
        {
            "title": "교직원   ",
            "description": "",
            "imageUrl": "",
            "link" : {
                "web" : ""
            }
        }
        ],
        "buttons": [
        {
            "label": "식단표",
            "action": "webLink",
            "webLinkUrl": "http://www.dgrang.com/menu.html"
        },
#        {
#            "label": "별점 주기",
#            "action": "message",
#            "messageText": "별점 주기"
#        } 
        {
            "label": "Be interactive",
            "action": "block",
            "messageText": "Be interactive",
            "blockId": "5d301014ffa748000122d182"
        }
        ]
    }
}

img_quick = [
    {
        "label": "학생식당",
        "action": "message",
        "messageText": "학생식당"
    },
    {
        "label": "연구동",
        "action": "message",
        "messageText": "연구동"
    },
    {
        "label": "교직원",
        "action": "message",
        "messageText": "교직원"
    },
    {
        "label": "홈",
        "action": "message",
        "messageText": "홈"
    }
]

card_quick = [
    {
        "label": "학생식당",
        "action": "block",
        "messageText": "학생식당",
        "blockId": "5d317a548192ac000132c371",
        "extra": {
            "rest": "student"
        }
    },
    {
        "label": "연구동",
        "action": "block",
        "messageText": "연구동",
        "blockId": "5d317a548192ac000132c371",
        "extra": {
            "rest": "r1"
        }
    },
    {
        "label": "교직원",
        "action": "block",
        "messageText": "교직원",
        "blockId": "5d317a548192ac000132c371",
        "extra": {
            "rest": "staff"
        }
    },
    {
        "label": "홈",
        "action": "message",
        "messageText": "홈"
    }
]

tempcard = {
    "version": "2.0",
    "template": {
        "outputs": [
        {
            "simpleText": {
                "text": "카드를 볼 식당을 골라주세요."
            }
        }
        ],
        "quickReplies": card_quick
    }
}


seebobs = {
    "version": "2.0",
    "template": {
        "outputs": [
#        {
#            "simpleText": {
#                "text": "www.dgrang.com/menu.html"
#            }
#        }
#        {
#            "simpleImage": {
#                "imageUrl": "http://www.dgrang.com/menu.png",
#                "altText": "식단표가 로드되지 않았어요"
#            }
#        },
#        bob_menu
        ],
# "quickReplies": img_quick
        "quickReplies": card_quick
    }
}

starchoose = {
    "version": "2.0",
    "template": {
        "outputs": [
        {
            "simpleText": {
                "text": "오늘 별점을 줄 식당을 선택하세요"
            }
        }
        ],
        "quickReplies": [
        {
            "label": "학생식당",
            "action": "block",
            "messageText": "학생식당",
            "blockId": "5d14c345ffa7480001185051",
            "extra": {
                "rest": "student"
            }
        },
        {
            "label": "연구동",
            "action": "block",
            "messageText": "연구동",
            "blockId": "5d14c345ffa7480001185051",
            "extra": {
                "rest": "r1"
            }
        },
        {
            "label": "교직원",
            "action": "block",
            "messageText": "교직원",
            "blockId": "5d14c345ffa7480001185051",
            "extra": {
                "rest": "staff"
            }
        }
        ]
    } 
}

stargive = {
    "version": "2.0",
    "template": {
        "outputs": [
        {
            "simpleText": {
                "text": "[0,5] 정수의 별점을 입력해주세요"
            }
        }
        ],
    },
    "context": {
        "values": [
        {
            "name": "choosenrest",
            "lifeSpan": 1,
            "params": {
                "rest": ""
            }
        }
        ]
    }
}

stardone = {
    "version": "2.0",
    "template": {
        "outputs": [
        {
            "simpleText": {
                "text": "별점주기가 완료되었습니다"
            }
        }
        ],
        "quickReplies": img_quick
    }
}

simpleImage = {
    "simpleImage": {
        "imageUrl": "http://www.dgrang.com/kakao_files/",
        "altText": "식단 이미지 로드에 실패하였습니다"
    }
}

img = {
    "version": "2.0",
    "template": {
        "outputs": [
        
        ],
        "quickReplies": img_quick
    }
} 

uploadchoose = {
    "version": "2.0",
    "template": {
        "outputs": [
        {
            "simpleText": {
                "text": "이미지를 업로드 할  식당을 선택하세요"
            }
        }
        ],
        "quickReplies": [
        {
            "label": "별점주기",
            "action": "message",
            "messageText": "별점주기",
           
        },
        {
            "label": "학생식당",
            "action": "block",
            "messageText": "학생식당",
            "blockId": "5d2ffc0492690d00011f39a2",
            "extra": {
                "rest": "student"
            }
        },
        {
            "label": "연구동",
            "action": "block",
            "messageText": "연구동",
            "blockId": "5d2ffc0492690d00011f39a2",
            "extra": {
                "rest": "r1"
            }
        },
        {
            "label": "교직원",
            "action": "block",
            "messageText": "교직원",
            "blockId": "5d2ffc0492690d00011f39a2",
            "extra": {
                "rest": "staff"
            }
        },
        {
            "label": "뒤로가기",
            "action": "message",
            "messageText": "식단보기",
        }
        ]
    },
   
}

uploadtextgive = {
    "version": "2.0",
    "template": {
        "outputs": [
        {
            "simpleText": {
                "text": "설명을 입력해주세요"
            }
        }
        ]
    },
    "context": {
        "values": [
        {
            "name": "resturls",
            "lifeSpan": 1,
            "params": {
                "rest": "",
                "urls": ""
            }
        }
        ]
    }
}


card = {
    "title": "",
    "description": "",
    "thumbnail": {
        "imageUrl": ""
    },
    "buttons": [
    {
        "action": "webLink",
        "label": "자세히 보기",
        "webLinkUrl": "http://www.dgrang.com/kakao_files/show.php?num="
    },
    {
        "action": "block",
        "label": "추천 취소",
        "messageText": "추천 취소",
        "blockId": "5d345223b617ea0001da32b5",
        "extra": {
            "cardId": ""
        }
    }
    ]
}

cardDelBtn = {
    "action": "block",
    "label": "삭제하기",
    "messageText": "삭제하기",
    "blockId": "5d3441628192ac000132c77c",
    "extra": {
        "cardId": ""
    }
}

cardDelChk = {
    "version": "2.0",
    "template": {
        "outputs": [
        {
            "simpleText": {
                "text": "정말 삭제하시겠습니까?"
            }
        }
        ],
        "quickReplies": [
        {
            "label": "예",
            "action": "block",
            "messageText": "예",
            "blockId": "5d34161a92690d00011f47c0"
        },
        {
            "label": "아니오",
            "action": "block",
            "messageText": "아니오",
            "blockId": "5d317a548192ac000132c371",
            "extra": {
                "page": "stay"
            }
        }
        ]
    },
    "context": {
        "values": [
        {
            "name": "showcontext",
            "lifeSpan": 1,
            "params": {
                "rest": "",
                "sort_type": "",
                "page": "",
                "cardId": ""
            }
        }
        ]
    }
}



cards = {
    "version": "2.0",
    "template": {
        "outputs": [
        {
            "carousel": {
                "type": "basicCard",
                "items": [

                ]
            }
        }
        ],
        "quickReplies": [ 
        {
            "label": "홈",
            "action": "message",
            "messageText": "홈",
        },
        {
            "label": "이전",
            "action": "block",
            "messageText": "이전",
            "blockId": "5d317a548192ac000132c371",
            "extra": {
                "page": "before"
            }
        },
        {
            "label": "다음",
            "action": "block",
            "messageText": "다음",
            "blockId": "5d317a548192ac000132c371",
            "extra": {
                "page": "next"
            }
        },
        {
            "label": "추천순(today)",
            "action": "block",
            "messageText": "좋아요순",
            "blockId": "5d317a548192ac000132c371",
            "extra": {
                "page": "mostlike_today"
            }
        },
        {
            "label": "최신순",
            "action": "block",
            "messageText": "최신순",
            "blockId": "5d317a548192ac000132c371",
            "extra": {
                "page": "latest"
            }
        },
        {
            "label": "추천순",
            "action": "block",
            "messageText": "좋아요순",
            "blockId": "5d317a548192ac000132c371",
            "extra": {
                "page": "mostlike"
            }
        },
        {
            "label": "내 포스트",
            "action": "block",
            "messageText": "내 포스트",
            "blockId": "5d317a548192ac000132c371",
            "extra": {
                "page": "mycard"
            }
        }
        ]
    },
    "context": {
        "values": [
        {
            "name": "showcontext",
            "lifeSpan": 1,
            "params": {
                "rest": "",
                "sort_type": "",
                "page": ""
            }
        }
        ]
    }
}

mailYN = {
    "version": "2.0",
    "template": {
        "outputs": [
        {
            "simpleText": {
                "text": "메일 인증이 필요합니다. \n 인증을 하려고 하신다면 메일 인증을 위한 개인정보 제공 동의가 필요합니다. \n수집되어 이용되는 개인정보 항목 : 이메일 주소 정보\n이용 목적 : 식단 이미지 업로드 서비스 사용에 있어서 개인을 식별하기 위함.\n개인정보의 보유 및 이용기간 : 사용자가 디지스트봇 딩굴이 서비스를 이용하지 않은 채로 6개월 경과시까지"
            }
        }
        ],
        "quickReplies": [ 
        {
            "label": "동의합니다.",
            "action": "block",
            "messageText": "메일인증",
            "blockId": "5d35206cb617ea0001da354d"
        },
        {
            "label": "동의하지 않습니다.",
            "action": "message",
            "messageText": "식단보기"
        }
        ]
    }
}
 

mailgive = {
    "version": "2.0",
    "template": {
        "outputs": [
        {
            "simpleText": {
                "text": "DGIST 메일 주소를 입력해주세요. 입력시 개인정보 제공에 동의하는 것으로 간주되며, 1년간 보관됩니다."
            }
        }
        ]
    },
    "context": {
        "values": [
        {
            "name": "mailflag",
            "lifeSpan": 2,
            "params": {
                "stage": "0",
            }
        }
        ]
    }
}

mailkey = {
    "version": "2.0",
    "template": {
        "outputs": [
        {
            "simpleText": {
                "text": "인증메일이 발송되었습니다. 5분 이내에 메일로 받은 인증번호 5자리를 입력해주세요."
            }
        }
        ]
    },
    "context": {
        "values": [
        {
            "name": "mailflag",
            "lifeSpan": 1,
            "params": {
                "stage": "1",
            }
        }
        ]
    }
}



home_json = json.dumps(home)
bob_menu_json = json.dumps(bob_menu)
seebobs_json = json.dumps(seebobs)
starchoose_json = json.dumps(starchoose)
stargive_json = json.dumps(stargive)
stardone_json = json.dumps(stardone)
img_json = json.dumps(img)
simpleImage_json = json.dumps(simpleImage)
lifeinfo_json = json.dumps(lifeinfo)
uploadchoose_json = json.dumps(uploadchoose)
uploadtextgive_json = json.dumps(uploadtextgive)
tempcard_json = json.dumps(tempcard)
cards_json = json.dumps(cards)
card_json = json.dumps(card)
cardDelBtn_json = json.dumps(cardDelBtn)
cardDelChk_json = json.dumps(cardDelChk)
mailgive_json = json.dumps(mailgive)
mailkey_json = json.dumps(mailkey)
mailYN_json = json.dumps(mailYN)
