import os
from datetime import date, timedelta
import requests
from bs4 import BeautifulSoup
from time import sleep
import subprocess
from zipfile import ZipFile, BadZipFile
from dotenv import load_dotenv


def baixar_arquivo():
    response1 = requests.get(
        'http://www.bmf.com.br/arquivos1/lum-arquivos_ipn.asp?idioma=pt-BR&status=ativo')

    load_dotenv()
    código = os.getenv('CODIGO')

    cookies = {
        'ASPSESSIONIDCSQRBDDA': 'GJKFCEFBPJNIODHDGPLAENFC',
        'dtCookie': 'v_4_srv_28_sn_03DF81497399B5D4A87262E31B3B24D3_perc_100000_ol_0_mul_1_app-3Ae44446475f923f8e_1_rcs-3Acss_0',
        'TS01ccf8f5': '011d592ce181ab51bfd94aeb807281d8bca13ea80484204b008bfb770e77e933b0030852619ba6a61e59899f358e04bbe3bd58fdcd',
        'rxVisitor': '1669075435999I59K5BHMNDLHEJGOBO6O480FIGJ4B2KM',
        '_ga': 'GA1.3.1634761639.1669075437',
        'ASPSESSIONIDSASSTRSQ': 'PBCNNMPBDPDHCEFNMMNHGDCD',
        'ASPSESSIONIDCSTSDBDA': 'PPMHPPBCCFDBNLGDAECADBPH',
        'ASPSESSIONIDCSRCSCQB': 'CHCBAIOCBDAPOPGPAGOKALKI',
        'ASPSESSIONIDASSATDQA': 'JLPJIMJDOJBNKMLJADPEFGON',
        '_gid': 'GA1.3.2083412774.1669326881',
        'ASPSESSIONIDASSSADDA': 'PPAGMHLDCOBJNKKFCLAHHACC',
        'TS01871345': '011d592ce159bb58b61c387c11f5c58090cdf97baa7f35d0333853281295fc2542de965becf163802b29d59d68d3395a725135015a',
        '_dc_gtm_UA-43178799-13': '1',
        'dtPC': f'28{código}',
        'dtLatC': '1',
        'rxvt': '1669329641506|1669326880335',
        'dtSa': 'true%7CC%7C-1%7CDownload%7C-%7C1669327841482%7C127834278_752%7Chttp%3A%2F%2Fwww.bmf.com.br%2Farquivos1%2Flum-arquivos_5Fipn.asp%3Fidioma%3Dpt-BR%26status%3Dativo%7C%7C%7C%7C',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Origin': 'http://www.bmf.com.br',
        'Referer': 'http://www.bmf.com.br/arquivos1/lum-arquivos_ipn.asp?idioma=pt-BR&status=ativo',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    }

    hoje = date.today()
    contador_dias = 0
    error = False
    while not error:
        um_dia_antes = timedelta(contador_dias)
        dias_anteriores = (hoje - um_dia_antes)
        data1 = dias_anteriores.strftime('%d-%m-%Y')
        data2 = dias_anteriores.strftime('%y%m%d')

        data = {
            'hdnStatus': 'ativo',
            'chkArquivoDownload_ativo': '15',
            'txtDataDownload_ativo': f'{data1}',
            'imgSubmeter': 'Download',
            'txtDataDownload_externo_ativo': [
                '25/08/2017',
                '25/08/2017',
                '25/08/2017',
            ],
        }

        response2 = requests.post('http://www.bmf.com.br/arquivos1/lum-download_ipn.asp',
                                  cookies=cookies, headers=headers, data=data, verify=False)
        data_ultimo_arquivo = BeautifulSoup(response1.content, 'html.parser')
        data_ultimo_arquivo = data_ultimo_arquivo.find_all(
            'input', id='txtDataDownload14_ativo')[0]['value']
        response3 = requests.get(response2.url)
        if response3.status_code == requests.codes.OK:
            print(f'Sua requisição \033[32mdeu certo\033[m e seu arquivo está sendo salvo. {
                  data1}')
            with open('Download.zip', 'wb') as arquivo_zip:
                for parte in response3.iter_content(chunk_size=256):
                    arquivo_zip.write(parte)
            try:
                ZipFile('Download.zip').testzip()
            except BadZipFile:
                print(f'Sua requisição \033[31mnão foi bem sucedida\033[m, tentando novamente. {
                      data1}')
                sleep(600)
            else:
                if not os.path.exists(rf'C: \Users\vfrei\Documents\arquivosBMF\VE{data2}.txt'):
                    subprocess.run(
                        [r"C:\Program Files\7-Zip\7z.exe", "e", 'Download.zip'])
                    os.rename(
                        f'VE{data2}.txt', rf'C: \Users\vfrei\Documents\arquivosBMF\VE{data2}.txt')
                contador_dias += 1
            os.remove('Download.zip')
        elif not response3.status_code == requests.codes.OK:
            print(
                f'Sua requisição \033[31mnão foi bem sucedida\033[m. {data1}')
            contador_dias += 1
        sleep(5)


baixar_arquivo()
# Se quiser testar ele, comente o código abaixo e descomente o de cima
# cron = BackgroundScheduler(daemon=True, timezone='America/Sao_Paulo')
# cron.start()
# cron.add_job(baixar_arquivo, 'cron', day_of_week='0-4', hour='19', minute='*/1')
# while True:
#     sleep(1)
#     if os.path.exists(rf'C:\Users\vfrei\Documents\arquivosBMF\PE{date.today().strftime("%y%m%d")}.txt'):
#         print('Esse arquivo \033[33mjá foi baixado\033[m')
#         break
