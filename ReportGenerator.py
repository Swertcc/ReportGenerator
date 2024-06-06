import os
import re
import requests
import pdfkit
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def fetch_page_content(url, headers, cookies):
    response = requests.get(url, headers=headers, cookies=cookies)
    response.raise_for_status()
    return response.content


def parse_judge_numbers(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    numbers = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        match = re.search(r'/judge/(\d{7})/course/116/', href) #116应该是课程号，此处自行更改
        if match:
            number = match.group(1)
            if number.startswith('55') or number.startswith('56'): #55和56是题号前两位，此处自行更改
                numbers.append(number)
    return numbers


def fetch_and_modify_content(url, headers, cookies):
    content = fetch_page_content(url, headers, cookies)
    soup = BeautifulSoup(content, 'html.parser')

    # Modify <td> tags
    location_td = soup.find('td', text='实验地点')
    if location_td and location_td.find_next_sibling('td'):
        location_td.find_next_sibling('td').string = 'xx-xxx'#实验地点

    teacher_td = soup.find('td', text='指导老师')
    if teacher_td and teacher_td.find_next_sibling('td'):
        teacher_td.find_next_sibling('td').string = 'xxx'#老师名字

    # Inline CSS and JS
    for link_tag in soup.find_all('link', rel='stylesheet'):
        css_url = link_tag['href']
        full_css_url = urljoin(url, css_url)
        css_response = requests.get(full_css_url)
        if css_response.status_code == 200:
            css_content = css_response.text
            new_style_tag = soup.new_tag('style')
            new_style_tag.string = css_content
            link_tag.replace_with(new_style_tag)

    for script_tag in soup.find_all('script', src=True):
        js_url = script_tag['src']
        full_js_url = urljoin(url, js_url)
        js_response = requests.get(full_js_url)
        if js_response.status_code == 200:
            js_content = js_response.text
            new_script_tag = soup.new_tag('script')
            new_script_tag.string = js_content
            script_tag.replace_with(new_script_tag)

    return soup


def save_html_to_pdf(soup, output_folder, options):
    title = soup.title.string if soup.title else 'untitled'
    title = title.replace(':', '_')

    local_html_path = os.path.join(output_folder, f'{title}.html')
    with open(local_html_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    output_pdf_path = os.path.join(output_folder, f'{title}.pdf')
    pdfkit.from_file(local_html_path, output_pdf_path, options=options)

def delete_html_files_in_pdfs():
    target_directory = os.path.join(os.getcwd(), 'pdfs')

    if os.path.exists(target_directory):
        for filename in os.listdir(target_directory):
            if filename.endswith('.html'):
                os.remove(os.path.join(target_directory, filename))
                print(f"已删除所有HTML文件")
    else:
        print(f"目录未创建")

def main():
    cookies = {
        'csrftoken': '',
        'sessionid': ''
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'acm.wzu.edu.cn',
        'Referer': 'http://acm.wzu.edu.cn/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Iron Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="115", "Chromium";v="115", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    base_url = "http://acm.wzu.edu.cn/judge/course/116/judgelist/?num=50&result=AC&userprofile=29211&page="#此处自行更改
    target_url_template = "http://acm.wzu.edu.cn/judge/{}/course/116/print_exp/"                           #此处自行更改
    urls = []
    pageNum = 5#此处自行更改

    for page in range(1, pageNum):
        page_content = fetch_page_content(base_url + str(page), headers, cookies)
        numbers = parse_judge_numbers(page_content)
        for number in numbers:
            urls.append(target_url_template.format(number))

    options = {
        'page-size': 'A4',
        'encoding': 'UTF-8',
        'margin-top': '0.1in',
        'margin-right': '0.1in',
        'margin-bottom': '0.1in',
        'margin-left': '0.1in',
    }

    output_folder = os.path.join(os.getcwd(), 'pdfs')
    os.makedirs(output_folder, exist_ok=True)

    for url in urls:
        try:
            soup = fetch_and_modify_content(url, headers, cookies)
            save_html_to_pdf(soup, output_folder, options)
        except Exception as e:
            print(f'有点问题但问题不大,请查看./pdfs')
    print(f'请查看./pdfs')

    delete_html_files_in_pdfs()

if __name__ == "__main__":
    main()
