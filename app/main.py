# -*- coding: utf-8 -*-
from unittest import result
from flask import Flask, jsonify, request
import os,sys, json
import pandas as pd 
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import psycopg2
import start



app = Flask(__name__)

@app.route('/')
def hello_world():
    #start.db_create()
    return 'Hello World!!!!!!!'

# 카카오톡 텍스트형 응답
@app.route('/api/sayHello', methods=['POST'])
def sayHello():
    body = request.get_json() # 사용자가 입력한 데이터
    print(body)
    print(body['userRequest']['utterance'])

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "안녕 hello I'm Ryan"
                    }
                }
            ]
        }
    }

    return responseBody

  
# 장학금 추천
@app.route('/api/recommend', methods=['POST'])
def recommend():
    try:
        body = request.get_json()
        print(body)
        
        # 1차적으로 모든 발화를 한곳에 딕셔너리형태로 수집
        params_df=body['action']['params']
        # {'yes_no': '해당없음', 'job': '고등학생', 'loc': '서울', 'Benefits': '학비지원', 'sys_number': '{"amount": 10, "unit": null}'}

        # 본격적으로 발화별 분류
        job=params_df['job'] 
        # 직업(type = str)

        location=params_df['loc']
        # 지역(type = str)

        Benefits=params_df['Benefits']
        # 장학혜택(type = str)
        age=json.loads(params_df['sys_number'])['amount']
        # 나이(type = str) -> 숫자형을 원하면 int()를 해준다

        yes_no = params_df['yes_no']
        # 특수계층(type = str)

        # SQL에서의 해당글자가 포함된 행 출력 문법을 맞추기위해 앞뒤로 %를 붙혀준다.
        Benefits1="\'%%" + Benefits + "%%\'"
        job1="\'%%" + job + "%%\'"
        yes_no1 = "\'%%" + yes_no + "%%\'"
        location1 = "\'%%" + location + "%%\'"
        df=start.db_select(Benefits1,job1,age,location1,yes_no1)
        # name과 url의 컬럼을 가진 데이터프레임 만들기

        name=df['name']
        # 데이터프레임의 name컬럼을 시리즈형식으로 저장
        
        URL=df['url']
        # 데이터프레임의 url컬럼을 시리즈형식으로 저장
        Image=df['image']
    except:
    # 혹시 잘못입력했는데 끝까지 진행했을 경우 출력
        responseBody = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "basicCard": {
                            "title": '잘못입력하셨습니다',
                            "buttons": [
                                {
                                    "action": "block",
                                    "label": "처음으로",
                                    "blockId": "62fae42870055f434dcd241b"
                                },
                                {
                                    "action": "block",
                                    "label": "다시하기",
                                    "blockId": "63045f97bda32f3914d2fc41"
                                }
                            ]  
                        },
                    }
                ]
            }
        }
    
    else:
    # 오류가 안났을 경우 리스트 출력
    # df라는 데이터프레임의 인덱스 갯수에 맞는 리스트갯수를 출력해주기위해
    # 갯수를 새주는 len()사용
    # 인덱스가 1개일때 베이직카드 1개 출력, 인덱스가 2개일때 베이직카드 2개 출력...
    # 5개 이상이면 리스트출력
        if len(df) > 5:
            responseBody = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                
                                "text": "검색된 장학금은 총 : {}개 입니다".format(len(df))
                            }
                        },
                        {
                        "carousel": {
                        "type": "basicCard",
                        "items": [
                            {
                            "title": name[0],
                            "description": "장학금 추천",
                            "thumbnail": {
                                "imageUrl": Image[0]
                            },
                            "buttons": [
                                {
                                "action":"webLink",
                                "label": "구경하기",
                                "webLinkUrl": URL[0]
                                },
                                {
                                "action": "share",
                                "label": "공유하기"
                            
                                }
                            
                            ]
                        

                            },

                            {
                            "title": name[1],
                            "description": "장학금 추천",
                            "thumbnail": {
                                "imageUrl": Image[1]
                            },
                            "buttons": [
                                {
                                "action":  "webLink",
                                "label": "구경하기",
                                "webLinkUrl": URL[1]
                                },

                                {
                                "action": "share",
                                "label": "공유하기"                      
                                }
                            
                            ]
                            },
                            {
                            "title": name[2],
                            "description": "장학금 추천",
                            "thumbnail": {
                                "imageUrl": Image[2]
                            },
                            "buttons": [
                                {
                                "action": "webLink",
                                "label": "구경하기",
                                "webLinkUrl": URL[2]
                                },
                                {
                                "action": "share",
                                "label": "공유하기"
                                }
                        
                            ]
                            },
                            {
                            "title": name[3],
                            "description": "장학금 추천",
                            "thumbnail": {
                                "imageUrl": Image[3]
                            },
                            "buttons": [
                                {
                                "action":  "webLink",
                                "label": "구경하기",
                                "webLinkUrl": URL[3]
                                },

                                {
                                "action": "share",
                                "label": "공유하기"                      
                                }
                            
                            ]
                            },
                            {
                            "title": name[4],
                            "description": "장학금 추천",
                            "thumbnail": {
                                "imageUrl": Image[4]
                            },
                            "buttons": [
                                {
                                "action":  "webLink",
                                "label": "구경하기",
                                "webLinkUrl": URL[4]
                                },

                                {
                                "action": "share",
                                "label": "공유하기"                      
                                }
                            
                            ]
                            }
                        ]
                        }
                    }
                    ],
                    "quickReplies": [
                    {
                    "messageText": "추가 장학금",
                    "action": "message",
                    "label": "장학금 더보기"
                    }
                
                    ]
                }
            }
        if len(df) == 5:
            responseBody = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                
                                "text": "검색된 장학금은 총 : {}개 입니다".format(len(df))
                            }
                        },
                        {
                        "carousel": {
                        "type": "basicCard",
                        "items": [
                            {
                            "title": name[0],
                            "description": "장학금 추천",
                            "thumbnail": {
                                "imageUrl": Image[0]
                            },
                            "buttons": [
                                {
                                "action":"webLink",
                                "label": "구경하기",
                                "webLinkUrl": URL[0]
                                },
                                {
                                "action": "share",
                                "label": "공유하기"
                            
                                }
                            
                            ]
                        

                            },

                            {
                            "title": name[1],
                            "description": "장학금 추천",
                            "thumbnail": {
                                "imageUrl": Image[1]
                            },
                            "buttons": [
                                {
                                "action":  "webLink",
                                "label": "구경하기",
                                "webLinkUrl": URL[1]
                                },

                                {
                                "action": "share",
                                "label": "공유하기"                      
                                }
                            
                            ]
                            },
                            {
                            "title": name[2],
                            "description": "장학금 추천",
                            "thumbnail": {
                                "imageUrl": Image[2]
                            },
                            "buttons": [
                                {
                                "action": "webLink",
                                "label": "구경하기",
                                "webLinkUrl": URL[2]
                                },
                                {
                                "action": "share",
                                "label": "공유하기"
                                }
                        
                            ]
                            },
                            {
                            "title": name[3],
                            "description": "장학금 추천",
                            "thumbnail": {
                                "imageUrl": Image[3]
                            },
                            "buttons": [
                                {
                                "action":  "webLink",
                                "label": "구경하기",
                                "webLinkUrl": URL[3]
                                },

                                {
                                "action": "share",
                                "label": "공유하기"                      
                                }
                            
                            ]
                            },
                            {
                            "title": name[4],
                            "description": "장학금 추천",
                            "thumbnail": {
                                "imageUrl": Image[4]
                            },
                            "buttons": [
                                {
                                "action":  "webLink",
                                "label": "구경하기",
                                "webLinkUrl": URL[4]
                                },

                                {
                                "action": "share",
                                "label": "공유하기"                      
                                }
                            
                            ]
                            }
                        ]
                        }
                    }
                    ],
                }
            }
        elif(len(df)) == 1 :
            responseBody = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                
                                "text": "검색된 장학금은 총 : {}개 입니다".format(len(df))
                            }
                        },
                        
                        {
                        "carousel": {
                        "type": "basicCard",
                        "items": [
                            {
                            "title": name[0],
                            "description": "장학금 추천",
                            "thumbnail": {
                                "imageUrl": Image[0]
                            },
                            "buttons": [
                                {
                                "action":"webLink",
                                "label": "구경하기",
                                "webLinkUrl": URL[0]
                                },
                                {
                                "action": "share",
                                "label": "공유하기"
                            
                                }
                            
                            ]                       
                            }
                            
                        ]
                        }
                    }
                    ]
                }
            }
        elif(len(df)) == 0 :
            responseBody = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "basicCard": {
                                "title": '죄송합니다. 해당되는 장학금이 없습니다.',
                                "buttons": [
                                    
                                    {
                                        "action": "block",
                                        "label": "다시하기",
                                        "blockId": "63045f97bda32f3914d2fc41"
                                    }
                                ]  
                            },
                        }
                            
                        ]
                    }
            }
                
            

        elif(len(df)) == 2 :
            responseBody = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                
                                "text": "검색된 장학금은 총 : {}개 입니다".format(len(df))
                            }
                        },
                        
                        {
                        "carousel": {
                        "type": "basicCard",
                        "items": [
                            {
                            "title": name[0],
                            "description": "장학금 추천",
                            "thumbnail": {
                                "imageUrl": Image[0]
                            },
                            "buttons": [
                                {
                                "action":"webLink",
                                "label": "구경하기",
                                "webLinkUrl": URL[0]
                                },
                                {
                                "action": "share",
                                "label": "공유하기"
                            
                                }
                            
                            ]                       
                            },
                            {
                            "title": name[1],
                            "description": "장학금 추천",
                            "thumbnail": {
                                "imageUrl": Image[1]
                            },
                            "buttons": [
                                {
                                "action":  "webLink",
                                "label": "구경하기",
                                "webLinkUrl": URL[1]
                                },

                                {
                                "action": "share",
                                "label": "공유하기"                      
                                }
                            
                            ]
                            }
                        ]
                        }
                    }
                    ]
                }
            }
        elif(len(df)) == 3 :
            responseBody = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                
                                "text": "검색된 장학금은 총 : {}개 입니다".format(len(df))
                            }
                        },
                        
                        {
                        "carousel": {
                        "type": "basicCard",
                        "items": [
                            {
                            "title": name[0],
                            "description": "장학금 추천",
                            "thumbnail": {
                                "imageUrl": Image[0]
                            },
                            "buttons": [
                                {
                                "action":"webLink",
                                "label": "구경하기",
                                "webLinkUrl": URL[0]
                                },
                                {
                                "action": "share",
                                "label": "공유하기"
                            
                                }
                            
                            ]                       
                            },
                            {
                            "title": name[1],
                            "description": "장학금 추천",
                            "thumbnail": {
                                "imageUrl": Image[1]
                            },
                            "buttons": [
                                {
                                "action":  "webLink",
                                "label": "구경하기",
                                "webLinkUrl": URL[1]
                                },

                                {
                                "action": "share",
                                "label": "공유하기"                      
                                }
                            
                            ]
                            },
                            {
                            "title": name[2],
                            "description": "장학금 추천",
                            "thumbnail": {
                                "imageUrl": Image[2]
                            },
                            "buttons": [
                                {
                                "action":  "webLink",
                                "label": "구경하기",
                                "webLinkUrl": URL[2]
                                },

                                {
                                "action": "share",
                                "label": "공유하기"                      
                                }
                            
                            ]
                            }
                        ]
                        }
                    }
                    ]
                }
            }
        elif (len(df)) == 4:
            responseBody = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                
                                "text": "검색된 장학금은 총 : {}개 입니다".format(len(df))
                            }
                        },
                        {
                        "carousel": {
                        "type": "basicCard",
                        "items": [
                            {
                            "title": name[0],
                            "description": "장학금 추천",
                            "thumbnail": {
                                "imageUrl": Image[0]
                            },
                            "buttons": [
                                {
                                "action":"webLink",
                                "label": "구경하기",
                                "webLinkUrl": URL[0]
                                },
                                {
                                "action": "share",
                                "label": "공유하기"
                            
                                }
                            ]                       
                            },
                            {
                            "title": name[1],
                            "description": "장학금 추천",
                            "thumbnail": {
                                "imageUrl": Image[1]
                            },
                            "buttons": [
                                {
                                "action":  "webLink",
                                "label": "구경하기",
                                "webLinkUrl": URL[1]
                                },

                                {
                                "action": "share",
                                "label": "공유하기"                      
                                }
                            
                            ]
                            },
                            {
                            "title": name[2],
                            "description": "장학금 추천",
                            "thumbnail": {
                                "imageUrl": Image[2]
                            },
                            "buttons": [
                                {
                                "action":  "webLink",
                                "label": "구경하기",
                                "webLinkUrl": URL[2]
                                },

                                {
                                "action": "share",
                                "label": "공유하기"                      
                                }
                            
                            ]
                            },
                            {
                            "title": name[3],
                            "description": "장학금 추천",
                            "thumbnail": {
                                "imageUrl": Image[3]
                            },
                            "buttons": [
                                {
                                "action":  "webLink",
                                "label": "구경하기",
                                "webLinkUrl": URL[3]
                                },

                                {
                                "action": "share",
                                "label": "공유하기"                      
                                }
                            ]
                            }
                        ]
                    }
                }
            ]
        
        }
    }
        
    return responseBody

# 장학금 추천 더보기
@app.route('/api/recommen2d', methods=['POST'])
def recommen2d():
    body = request.get_json()
    print(body)
    
    params_df=body['action']['params']
    print(params_df)
    
    job=params_df['job']
    print(job)
    print(type(job))
    location=params_df['loc']
    print(location)
    Benefits=params_df['Benefits']
    age=json.loads(params_df['sys_number'])['amount']
    yes_no = params_df['yes_no']

    Benefits1="\'%%" + Benefits + "%%\'"
    job1="\'%%" + job + "%%\'"
    yes_no1 = "\'%%" + yes_no + "%%\'"
    location1 = "\'%%" + location + "%%\'"
    df=start.db_select(Benefits1,job1,age,location1,yes_no1)
    print(df)
    name=df['name']
    URL=df['url']
    image=df['image']
    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                "listCard": {
          "header": {
            "title": "장학금 추가 출력"
          },
          "items": [
            {
              "title": name[5],
              "imageUrl": image[5],
              "link": {
                "web": URL[5]
              }
            },
            {
              "title": name[6],
              "imageUrl": image[6],
              "link": {
                "web": URL[6]
              }
            },
            {
              "title": name[7],
              "imageUrl": image[7],
              "link": {
                "web": URL[7]
              }
            },
            {
              "title": name[8],
              "imageUrl": image[8],
              "link": {
                "web": URL[8]
              }
            },
            {
              "title": name[9],
              "imageUrl": image[9],
              "link": {
                "web": URL[9]
              }
            }
          ],
          "buttons": [
            {
              "label": "더보기",
              "action": "block",
              "blockId": "62654c249ac8ed78441532de",
              "extra": {
                "key1": "value1",
                "key2": "value2"
              }
            }
          ]
        }
      }
    ]
  }
}
    return responseBody


# 장학금 조회
@app.route('/api/Lookup', methods=['POST'])
def Lookup():
    
    body = request.get_json()
    print(body)
    # 카카오 챗봇에서 보낸 요청값을 body에 저장
    name=body['action']['detailParams']['name']['value']
    print(name)
    # 사용자 발화값 중 입력값을 받기 위함
    df1=start.area_db(name)
    # db_select함수에 name값 입력
    name=df1['name']
    print(name)
    print(type(name))
    # df1이라는 데이터프레임의 'name'컬럼값을 series형식으로 저장
    URL=df1['url']
    # df1이라는 데이터프레임의 'url'컬럼값을 series형식으로 저장
    image=df1['image']
    # df1이라는 데이터프레임의 'image'컬럼값을 series형식으로 저장

    if len(df1) > 0:
        responseBody = {
            "version": "2.0",
            "template": {
                "outputs": [
                     {
                        "simpleText": {
                            
                            "text": "조회하신 장학금입니다"
                            },
                    },

                    {
                    "carousel": {
                    "type": "basicCard",        
                    "items": [
                        {
                        "title": name[0],
                        "description": "장학금 조회",
                        "thumbnail": {
                            "imageUrl": image[0]
                        },
                        "buttons": [
                            {
                            "action":"webLink",
                            "label": "장학금 정보 보기",
                            "webLinkUrl": URL[0]
                            },
                            {
                            "action": "share",
                            "label": "공유하기"

                            }
                        ]
                        }
                    ]      
                    }    
                }
                ]
            }  
        }


    return responseBody