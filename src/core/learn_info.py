import requests
from bs4 import BeautifulSoup as bs

def init_session(mssv: str, password: str) -> requests.Session:
    """Initialize a session with the given MSSV and password.

    Args:
        mssv (str): MSSV of the student.
        password (str): Password of the student.

    Returns:
        requests.Session: A session with the given MSSV and password.
    """
    session = requests.Session()

    payload = f'chkSubmit=ok&txtLoginId={mssv}&txtPassword={password}&txtSel=1'

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://daotao.vnu.edu.vn',
        'Referer': 'https://daotao.vnu.edu.vn/dkmh/login.asp',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
        'sec-ch-ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    url = "https://daotao.vnu.edu.vn/dkmh/login.asp"

    # Get the session cookie
    session.request(
        method='POST',
        url=url,
        headers=headers,
        data=payload,
        verify=False
    )
    
    return session

def get_html(session: requests.Session) -> str:
    url = "https://daotao.vnu.edu.vn/ListPoint/listpoint_Brc1.asp"

    payload = {}
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'vi',
    'Connection': 'keep-alive',
    'Referer': 'https://daotao.vnu.edu.vn/ListPoint/listpoint.asp',
    'Sec-Fetch-Dest': 'iframe',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
    'sec-ch-ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
    }

    response = session.request("GET", url, headers=headers, data=payload)
    
    return response.content.decode('utf-8')

def __find_student_info(soup: bs) -> dict:
    student_info = {}
    print('Finding student info...')
    
    # Find student info 
    div_list_1 = soup.find('div', {'id': 'divList1'})
    table = div_list_1.find('table')
    tr_list = table.find_all('tr')
    tr_with_info = tr_list[1]
    cells = tr_with_info.find_all('td')
    name = cells[1].text.strip().replace('Sinh viên: ', '')
    mssv = cells[2].text.strip().replace('Mã số: ', '')
    lop = cells[3].text.strip().replace('Lớp quản lý: ', '')
    
    student_info['name'] = name
    student_info['mssv'] = mssv
    student_info['lop'] = lop
    
    return student_info

def __find_score_by_semester(soup: bs) -> dict:
    score_by_semester = {}
    current_semester = None
    print('Finding score by semester...')
    
    # Find score by semester
    div_list_3 = soup.find('div', {'id': 'divList3'})
    table = div_list_3.find('table')

    tr_list = table.find_all('tr')

    for tr in tr_list[:-3]:
        attr = tr.attrs # Get attributes of tr tag in type dict
        if attr.get('height') == '25': # This is a row of semester info
            b_tag = tr.find('b').text.strip()
            semester = b_tag.split(' ')[-1]
            score_by_semester[semester] = []
            current_semester = semester
            print(f'Current semester: {current_semester}')
        else:
            cells = tr.find_all('td')
            
            ma_hp = cells[1].text.strip()
            hp_name = cells[2].text.strip()
            so_tc = cells[3].text.strip()
            diem_he_10 = cells[4].text.strip()
            diem_chu = cells[5].text.strip()
            
            
            score_by_semester[current_semester].append({
                'ma_hp': ma_hp,
                'ten_hp': hp_name,
                'so_tc': so_tc,
                'diem_he_10': diem_he_10,
                'diem_chu': diem_chu
            })
    
    return score_by_semester

def __parse_credit_info(soup: bs) -> dict:
    credits_info = {}
    print('Finding credit info...')
    
    # Find credit info
    div_list_3 = soup.find('div', {'id': 'divList3'})
    table = div_list_3.find('table')

    tr_list = table.find_all('tr')
    
    for idx, tr in enumerate(tr_list[-3:]):
        b_tag = tr.find('b').text.strip()
        
        if idx == 0:
            credits_info['so_tc_tich_luy'] = b_tag.split(' ')[-1].replace('\xa0\xa0','')
        elif idx == 1:
            credits_info['so_tc_dat'] = b_tag.split(' ')[-1].replace('\xa0\xa0','')
        elif idx == 2:
            credits_info['diem_tb_tich_luy'] = b_tag.split(' ')[-1].replace('\xa0\xa0','')

    return credits_info

def run(mssv: str, password: str) -> dict:
    session = init_session(mssv, password)
    html = get_html(session)
    result = parse_html(html)
    
    return result


def parse_html(html: str) -> dict:
    soup = bs(html, 'html.parser')
    
    student_info = __find_student_info(soup)
    score_by_semester = __find_score_by_semester(soup)
    credits_info = __parse_credit_info(soup)
    
    return {
        'student_info': student_info,
        'score_by_semester': score_by_semester,
        'credits_info': credits_info
    }
    
if __name__ == '__main__':
    mssv = input('MSSV: ')
    password = input('Password: ')
    
    session = init_session(mssv, password)
    html = get_html(session)
    result = parse_html(html)
    print(result)
    

    
