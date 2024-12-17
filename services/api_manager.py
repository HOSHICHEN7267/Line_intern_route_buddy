import json
import openai_receive_unit
import map_unit
import tdx_unit
import openai_send_unit


class ApiManager:
    def __init__(self):
        self.tdx_unit = tdx_unit.TdxUnit()

    def get_result(self, input_string: str) -> str:
        """
        Manages the workflow of extracting user inputs, validating them, and returning final results
        by integrating OpenAI, Map API, and TDX API.

        :param input_string: The user's input string.
        :return: A JSON-formatted string containing the result.
        """

        # Validate input string length
        if len(input_string) > 200:
            return json.dumps({
                'result': False,
                'data': '''抱歉，你的訊息有點太長了，我小小的腦袋裝不下QQ\n\n
可以麻煩你用簡短的文字告訴我，你的起點、目的地，以及希望省錢還是省時間嗎？'''
            })

        # Call OpenAI to extract origin, destination, and preference
        AI_to_MAP = openai_receive_unit.get_result(input_string)

        # print("AI_to_MAP: ", json.loads(AI_to_MAP))

        if not json.loads(AI_to_MAP)['result']:
            message = json.loads(AI_to_MAP)['message']
            if message == 'origin or destination is not correct':
                return json.dumps({
                    'result': False,
                    'data': '''抱歉，我沒有聽懂你的起點及目的地，分別在哪裡QQ\n\n
可以再告訴我一次：你的起點、目的地，以及希望省錢還是省時間嗎？'''
                })
            else:
                return json.dumps({
                    'result': False,
                    'data': f'''抱歉，連接 open ai 時出現問題。錯誤訊息：{message}'''
                })

        # Call Map API to validate the input
        MAP_to_TDX = map_unit.get_result(AI_to_MAP)

        # print("MAP_to_TDX: ", json.loads(MAP_to_TDX))

        if not json.loads(MAP_to_TDX)['result']:
            return json.dumps({
                'result': False,
                'data': '''抱歉，你的起點及目的地，似乎有無法在地圖上搜尋到的地方QQ\n\n
可以再告訴我一次：你的起點、目的地，以及希望省錢還是省時間嗎？'''
            })

        # Call TDX API to get the route
        TDX_to_AI = self.tdx_unit.get_result(MAP_to_TDX)

        # print("TDX_to_AI: ", json.loads(TDX_to_AI))

        if not json.loads(TDX_to_AI)['result']:
            message = json.loads(TDX_to_AI)['message']
            if message == 'Route not found':
                return json.dumps({
                    'result': False,
                    'data': '''抱歉，看起來這超出了我的能力範圍，無法給你幫助QQ\n\n
你可以試試這些方法，幫助我更好地找到正確的路線：\n\n
1. 對地點更詳細的描述：比起**市政府**，**臺南市政府**會是更好的選擇！\n
2. 避免輸入國外地點：我只能協助規劃臺灣境內的路線\n
3. 起終點附近的大眾運輸：有些地方大眾運輸到不了，我就沒辦法規劃了\n\n
確認過上面幾點後，可以再告訴我一次：你的起點、目的地，以及希望省錢還是省時間嗎？'''
                })
            else:
                return json.dumps({
                    'result': False,
                    'data': f'''抱歉，連接 TDX 時出現問題。錯誤訊息：{message}'''
                })

        # Combine OpenAI and TDX results for final response
        TDX_to_AI = f"{json.loads(AI_to_MAP)['data']}{TDX_to_AI}"

        # Call OpenAI to generate the final user-friendly response
        AI_to_USER = openai_send_unit.get_result(TDX_to_AI)

        if not json.loads(AI_to_USER)['result']:
            return json.dumps({
                'result': False,
                'data': '''抱歉，小幫手在產生交通路線時，出了一點問題QQ\n\n
可以再告訴我一次：你的起點、目的地，以及希望省錢還是省時間嗎？'''
            })

        return AI_to_USER


# For debugging and testing
if __name__ == '__main__':
    """
    Debugging function to test the API workflow.
    """
    api_manager = ApiManager()

    # input_message = "從台北市政府到政治大學，甚麼方式最快？"

    input_message = input("請輸入你的起點、目的地，以及希望省錢還是省時間：")

    output_message = api_manager.get_result(input_message)
    response = json.loads(output_message)

    # Handle success or failure
    if response['result']:
        output_message = response['data']
    else:
        output_message = response['data']

    print("output_message: ", output_message)

