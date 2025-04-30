import json
import urllib.request

def lambda_handler(event, context):
        try:
            # リクエストボディを解析
             body = json.loads(event['body'])
             message = body['message']
             conversation_history = body.get('conversationHistory', [])
             # 独自APIへのリクエスト用データ（最小構成）
             payload = {
                     "prompt": message,
                     "max_new_tokens": 512,
                     "do_sample": True,
                     "temperature": 0.7,
                     "top_p": 0.9
             }
             # 独自に立てたFastAPIのエンドポイントURL                                                                            
             api_url = "https://705e-34-142-241-202.ngrok-free.app/generate"
             req = urllib.request.Request(
                     api_url,
                     data=json.dumps(payload).encode('utf-8'),
                     headers={"Content-Type": "application/json"},
                     method="POST"
                     )
             with urllib.request.urlopen(req) as res:
                 response_body = json.loads(res.read().decode("utf-8"))
                 assistant_response = response_body.get("generated_text", "応答が取得できませんでした．")
                 # 会話履歴にアシスタントの応答を追加
                 conversation_history.append({
                     "role": "user",
                     "content": message
                     })
                 conversation_history.append({
                     "role": "assistant",
                     "content": assistant_response
                     })
                 
                 
             return {
                     "statusCode": 200,
                     "headers": {
                         "Content-Type": "application/json",
                         "Access-Control-Allow-Origin": "*",
                         "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                         "Access-Control-Allow-Methods": "OPTIONS,POST"
                         },
                     "body": json.dumps({
                         "success": True,
                         "response": assistant_response,
                         "conversationHistory": conversation_history
                         })
                     }
                 
        except Exception as error:
            print("Error:", str(error))
            return {
                    "statusCode": 500,

                    "headers": {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                        "Access-Control-Allow-Methods": "OPTIONS,POST" 
                    },
                    "body": json.dumps({
                            "success": False,
                            "error": str(error)
                    })
            }
                    

