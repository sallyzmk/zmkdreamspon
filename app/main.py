from cgi import parse_multipart
from flask import Flask, request
import json
import start


app = Flask(__name__)

@app.route('/')
def hello_world():
    return '11'

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

  
# 장학금 추가로 받아오기 
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
        if len(df) >= 5:
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
                                "imageUrl": "https://github.com/seungukkim/flower75982/blob/main/image/%EC%9E%A5%ED%95%99%EA%B8%881.jpg?raw=true"
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
                                "imageUrl": "https://github.com/seungukkim/flower75982/blob/main/image/%EC%9E%A5%ED%95%99%EA%B8%882.jpg?raw=true"
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
                                "imageUrl": "https://github.com/seungukkim/flower75982/blob/main/image/%EC%9E%A5%ED%95%99%EA%B8%883.jpg?raw=true"
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
                                "imageUrl": "https://github.com/seungukkim/flower75982/blob/main/image/%EC%9E%A5%ED%95%99%EA%B8%884.jpg?raw=true"
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
                                "imageUrl": "https://github.com/seungukkim/flower75982/blob/main/image/%EC%9E%A5%ED%95%99%EA%B8%885.jpg?raw=true"
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
                                "imageUrl": "https://github.com/seungukkim/flower75982/blob/main/image/%EC%9E%A5%ED%95%99%EA%B8%881.jpg?raw=true"
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
                                "imageUrl": "https://github.com/seungukkim/flower75982/blob/main/image/%EC%9E%A5%ED%95%99%EA%B8%881.jpg?raw=true"
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
                                "imageUrl": "https://github.com/seungukkim/flower75982/blob/main/image/%EC%9E%A5%ED%95%99%EA%B8%882.jpg?raw=true"
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
                                "imageUrl": "https://github.com/seungukkim/flower75982/blob/main/image/%EC%9E%A5%ED%95%99%EA%B8%881.jpg?raw=true"
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
                                "imageUrl": "https://github.com/seungukkim/flower75982/blob/main/image/%EC%9E%A5%ED%95%99%EA%B8%882.jpg?raw=true"
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
                                "imageUrl": "https://github.com/seungukkim/flower75982/blob/main/image/%EC%9E%A5%ED%95%99%EA%B8%882.jpg?raw=true"
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
                                "imageUrl": "https://github.com/seungukkim/flower75982/blob/main/image/%EC%9E%A5%ED%95%99%EA%B8%881.jpg?raw=true"
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
                                "imageUrl": "https://github.com/seungukkim/flower75982/blob/main/image/%EC%9E%A5%ED%95%99%EA%B8%882.jpg?raw=true"
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
                                "imageUrl": "https://github.com/seungukkim/flower75982/blob/main/image/%EC%9E%A5%ED%95%99%EA%B8%882.jpg?raw=true"
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
                                "imageUrl": "https://github.com/seungukkim/flower75982/blob/main/image/%EC%9E%A5%ED%95%99%EA%B8%882.jpg?raw=true"
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
    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                "carousel": {
                "type": "basicCard",
                "items": [
                    {
                    "title": name[5],
                    "description": "장학금 추천",
                    "thumbnail": {
                        "imageUrl": "https://github.com/seungukkim/flower75982/blob/main/image/%EC%9E%A5%ED%95%99%EA%B8%881.jpg?raw=true"
                    },
                    "buttons": [
                        {
                        "action":"webLink",
                        "label": "구경하기",
                        "webLinkUrl": URL[5]
                        },
                        {
                        "action": "share",
                         "label": "공유하기"
                        
                        }
                        
                    ]
                    

                    },

                    {
                    "title": name[6],
                    "description": "장학금 추천",
                    "thumbnail": {
                        "imageUrl": "https://github.com/seungukkim/flower75982/blob/main/image/%EC%9E%A5%ED%95%99%EA%B8%882.jpg?raw=true"
                    },
                    "buttons": [
                        {
                        "action":  "webLink",
                        "label": "구경하기",
                        "webLinkUrl": URL[6]
                        },

                        {
                        "action": "share",
                        "label": "공유하기"                      
                        }
                        
                    ]
                    },
                    {
                    "title": name[7],
                    "description": "장학금 추천",
                    "thumbnail": {
                        "imageUrl": "https://github.com/seungukkim/flower75982/blob/main/image/%EC%9E%A5%ED%95%99%EA%B8%883.jpg?raw=true"
                    },
                    "buttons": [
                         {
                        "action": "webLink",
                        "label": "구경하기",
                        "webLinkUrl": URL[7]
                        },
                        {
                        "action": "share",
                        "label": "공유하기"
                        }
                       
                    ]
                    },
                    {
                    "title": name[8],
                    "description": "장학금 추천",
                    "thumbnail": {
                        "imageUrl": "https://github.com/seungukkim/flower75982/blob/main/image/%EC%9E%A5%ED%95%99%EA%B8%884.jpg?raw=true"
                    },
                    "buttons": [
                        {
                        "action":  "webLink",
                        "label": "구경하기",
                        "webLinkUrl": URL[8]
                        },

                        {
                        "action": "share",
                        "label": "공유하기"                      
                        }
                        
                    ]
                    },
                    {
                    "title": name[9],
                    "description": "장학금 추천",
                    "thumbnail": {
                        "imageUrl": "https://github.com/seungukkim/flower75982/blob/main/image/%EC%9E%A5%ED%95%99%EA%B8%885.jpg?raw=true"
                    },
                    "buttons": [
                        {
                        "action":  "webLink",
                        "label": "구경하기",
                        "webLinkUrl": URL[9]
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
                "messageText": "추가 장학금1",
                "action": "message",
                "label": "장학금 더보기"
            }
            
            ]
        }
    }

    return responseBody
