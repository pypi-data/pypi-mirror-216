import requests
from datetime import datetime
import pandas as pd
from tabulate import tabulate

class OpenAIPricing:

    __models = {'gpt-4-32k': 'GPT-4 32k',
                'gpt-4': 'GPT-4',
                'gpt-3.5-turbo-16k': 'GPT-3.5 16k',
                'gpt-3.5-turbo': 'GPT-3.5',
                'text-davinci-003': 'Davinci',
                'text-curie-001': 'Curie',
                'text-babbage-001': 'Babbage',
                'text-ada-001': 'Ada'}
                
    def __init__(self):
        try:
            self.__frame = self.__parse__(self.__load__())
            
        except:
            raise Exception('An error ocourred while trying to access the data in "https://gptforwork.com/tools/openai-chatgpt-api-pricing-calculator". Check the internet connection and the availability of that page.')


    def __load__(self):
        headers = {
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
            'purpose': 'prefetch',
            'x-nextjs-data': '1',
            'Referer': 'https://gptforwork.com/tools/openai-chatgpt-api-pricing-calculator',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58',
            'sec-ch-ua-platform': '"Windows"',
        }

        params = {
            'slug': [
                'guides',
                'openai-gpt3-tokens',
            ],
        }

        response = requests.get(
            'https://gptforwork.com/_next/data/USgHDRbEE25LhVVtESD0C/guides/openai-gpt3-tokens.json',
            params=params,
            headers=headers,
        )
        return response
    
    @staticmethod
    def model_name(technical_name):

        if technical_name in OpenAIPricing.__models:
            return OpenAIPricing.__models[technical_name]

        return 'Unknown'
    def __parse__(self, response):
        blocos = response.json()['pageProps']['notionRecordMap']['block']

        dados = []

        for k in blocos:
            if  blocos[k]['value']['type'] == 'table_row':
                # print(blocos[k]['value']['properties']["VCBi"])
                dados.append(blocos[k]['value']['properties'])

        frame = pd.DataFrame(dados)

        for col in frame:
            frame[col] = frame[col].apply(lambda x: x[0][0] if x == x else None)


        frame['VCBi'] = frame['yp{s'].apply(OpenAIPricing.model_name)

        def __guess_measure(x):
            if type(x.value) != str:
                return None

            value = x.value.strip()
            if value.startswith('USD'):
                if x.variable == 'OYF;':
                    return 'Price for 1000 tokens (prompt)'
                if x.variable == 'dIE|':
                    return 'Price for 1000 tokens (completion)'
                
            if value.isdigit():
                return 'Max tokens'


        frame = frame.melt(['VCBi', 'yp{s'], ['OYF;', 'dIE|'])

        frame['Measure'] = frame[['variable','value']].apply(__guess_measure, axis=1)

        frame = frame[frame['Measure'] == frame['Measure']].pivot(index=['yp{s'],columns='Measure', values='value')

        def __convert_price_to_float__(x):
            if type(x) != str:
                return x
                
            value = x.strip()

            if value.startswith('USD'):
                return float(value[3:].strip())
            
            return 'fail'

        def __convert_tokens_to_int__(x):
            if type(x) != str:
                return x
                
            value = x.strip()

            if value.isdigit():
                return int(value.strip())
            
            return 'fail'


        frame['Max tokens'] = frame['Max tokens'].apply(__convert_tokens_to_int__)
        frame['Price for 1000 tokens (prompt)'] = frame['Price for 1000 tokens (prompt)'].apply(__convert_price_to_float__)
        frame['Price for 1000 tokens (completion)'] = frame['Price for 1000 tokens (completion)'].apply(__convert_price_to_float__)

        return frame

    def refresh(self):
        try:
            self.__frame = self.__parse__(self.__load__())
            print(f'All prices were refreshed in {datetime.now().strftime("%d %b %Y at %H:%M:%S")} according to published in "https://gptforwork.com/tools/openai-chatgpt-api-pricing-calculator".')
        except:
            raise Exception('An error ocourred while trying to access the data in "https://gptforwork.com/tools/openai-chatgpt-api-pricing-calculator". Check the internet connection and the availability of that page.')


    # --------------------------------------------------------
    @staticmethod
    def list_available_models():
        __models = OpenAIPricing.__models
        print(tabulate(pd.DataFrame([{'Model name':__models[k],'Technical name':k} for k in __models]), headers='keys', tablefmt='psql', showindex=False))


    def get_price(self, model, type='both', tokens=1000 ):
        # global __models
        if model in self.__models:
            completion = self.__frame.loc[model]['Price for 1000 tokens (completion)']
            prompt = self.__frame.loc[model]['Price for 1000 tokens (prompt)']

            if type == 'both':
                return tokens*(completion+prompt)/2000
            
            if type == 'completion':
                return tokens*completion/1000

            if type == 'prompt':
                return tokens*prompt/1000

            raise Exception('Argument "type" should be equal to "prompt", "completion" or "both".')
        else:
            raise Exception(f'Price is unavailable or model "{model}" is nonexistent. Check the available models by calling "list_available_models()".')


    def get_max_tokens(self, model):
        # global __models
        if model in self.__models:
            return int(self.__frame.loc[model]['Max tokens'])
        else:
            raise Exception(f'Max tokens is unavailable or model "{model}" is nonexistent. Check the available models by calling "list_available_models()".')

