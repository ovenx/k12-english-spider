# k12-english-spider
import requests
import re
import json
import sys
import time
from bs4 import BeautifulSoup, Comment, NavigableString
from openpyxl import Workbook
from city import city_datas

avaiable_site = {
    1: '乂学教育',
    2: '瑞思学科英语',
    3: '励步英语',
    4: '番茄田儿童国际艺术',
    5: '芝麻街英语',
    6: '爱贝国际少儿英语',
    7: '山姆大叔少儿英语',
    8: '新东方'
}

input_str = ''
for k, v in avaiable_site.items():
    input_str += str(k)+'：'+v+'\n'
input_str += '请选择要抓取的站点：'
site = int(input(input_str))
while site not in avaiable_site.keys():
  site = int(input('站点id错误，重新输入：'))

wb = Workbook()
ws = wb.active
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/25.2'}
cookies = 'Qs_lvt_204038=1567310822; looyu_id=afd7ef2551c94e0d9d49525d9f1c7589_10038875%3A1; looyu_10038875=v%3Aafd7ef2551c94e0d9d49525d9f1c7589%2Cref%3A%2Cr%3A%2Cmon%3Ahttp%3A//m9109.talk99.cn/monitor%2Cp0%3Ahttp%253A//www.sesamestreetenglishchina.com/school/; Hm_lvt_7ea2f631b040ae3187b2173a0e1c6fc4=1567310841; _99_mon=%5B0%2C0%2C0%5D; Qs_pv_204038=3191893150279417000%2C2686434662950092000%2C4371466837669108700%2C4542674249871678500%2C4602570193011525000; Hm_lpvt_7ea2f631b040ae3187b2173a0e1c6fc4=1567310998'


# 乂学教育
if site == 1:
  base_url = 'https://www.songshuai.com/api/school/search'
  city = input('请输入城市：')
  res = requests.post(base_url, {'search':city})
  jsonData = json.loads(res.content)
  print(jsonData)
  if jsonData['data']:
    for data in jsonData['data']['rows']:
      ws.append(['乂学教育', data['SchoolName'], data['AddressName']])
  print('ok')
  wb.save("./k12英语-乂学教育.xlsx")


# 瑞思学科英语
if site == 2:
  base_url = 'http://www.risecenter.com/plus/school.php?a=formcampuses'
  res = requests.get(base_url)
  soup = BeautifulSoup(res.content, "lxml")
  for child in soup.select('.hidelist3'):
    for item in child.find_all('li'):
      textParent = item.find('a')
      textName = textParent.select('.ttt')[0].string
      textAddr = textParent.select('.tips')[0].string
      ws.append(['瑞思学科英语', textName, textAddr])
  wb.save("./k12英语-瑞思学科英语.xlsx")

# 励步英语
if site == 3:
  for data in city_datas:
      for item in city_datas[data]['list']:
          mobile = re.findall('\<strong\>电话\<\/strong>\：(.*)', item['dianhua'])
          if (mobile) :
              mobile = mobile[0]
              mobile = mobile.replace("&nbsp;", "")
              mobile = mobile.replace("<br/>", "")
          else :
              mobile = ''
          ws_item = ['励步英语', item['title'], item['content'], mobile]
          print(ws_item)
          ws.append(ws_item)
  wb.save("./k12英语-励步英语.xlsx")

# 番茄田儿童国际艺术
if site == 4:
  base_url = 'http://www.tomatoart.com.cn/wap/tomato/schools?isReservation=false'
  res = requests.get(base_url)
  jsonData = json.loads(res.content)
  for prov_data in jsonData['datas']:
    base_url = 'http://www.tomatoart.com.cn/wap/tomato/schools?isReservation=true&prov='+prov_data['province']
    res = requests.get(base_url)
    jsonData = json.loads(res.content)
    for data in jsonData['datas']:
      phone = data['phone'] if 'phone' in data.keys() else ''
      ws_item = ['番茄田儿童国际艺术', data['centerName'], data['centerAddress'], phone]
      print(ws_item)
      ws.append(ws_item)
  wb.save("./k12英语-番茄田儿童国际艺术.xlsx")

# 芝麻街英语
if site == 5:
  base_url = 'http://m.sesamestreetenglishchina.com/school/cid1.html'
  res = requests.get(base_url)
  soup = BeautifulSoup(res.content, "lxml")
  for child in soup.select('.cityList a'):
      base_url = 'http://m.sesamestreetenglishchina.com/school/'+child['href']
      res = requests.get(base_url)
      soup = BeautifulSoup(res.content, "lxml")
      for item in soup.select('.school_list a'):
          base_url = 'http://m.sesamestreetenglishchina.com/school/'+item['href']
          res = requests.get(base_url)
          soup = BeautifulSoup(res.content, "lxml")
          idx = 0
          item = ['芝麻街英语', '', '', '']
          for strList in soup.select('.i_content li'):
              string = strList.string
              idx = idx + 1
              if idx == 3:
                  item[1] = string
              elif idx == 4:
                  string = string.replace("地址：", "")
                  item[2] = string
              elif idx == 5:
                  string = string.replace("电话：", "")
                  item[3] = string
          print(ws_item)
          ws.append(item)
  wb.save("./k12英语-芝麻街英语.xlsx")

# 爱贝国际少儿英语
if site == 6:
  base_url = 'http://www.abiechina.com/schoollist.aspx'
  res = requests.get(base_url)
  soup = BeautifulSoup(res.content, "lxml")
  for child in soup.select('.nation_dd'):
    item = ['爱贝国际少儿英语', '', '', '']
    for string in child.find('h2').stripped_strings:
      item[1] = string
      break
    idx = 0
    for string in child.find('p').stripped_strings:
      idx = idx + 1
      if (idx == 1) :
        item[3] = string
      elif (idx == 3):
        item[2] = string
      elif (idx > 3):
        break
    print(item)
    ws.append(item)
  wb.save("./k12英语-爱贝国际少儿英语.xlsx")

# 山姆大叔少儿英语
if site == 7:
  base_url = 'http://www.unclesamedu.com/index.php?c=article&m=country&column_id=28#huodong'
  res = requests.get(base_url)
  soup = BeautifulSoup(res.content, "lxml")
  for child in soup.select('.hd li'):
    page = 1
    while 1:
      base_url = 'http://www.unclesamedu.com/index.php?c=article&m=content&city_id='+child['city_id']+'&page='+str(page)
      page = page+1
      res = requests.get(base_url)
      soup = BeautifulSoup(res.content, "lxml")
      item_list = soup.select('.allson li')
      print(base_url)
      if item_list:
        for item in item_list:
          ws_item = ['山姆大叔少儿英语']
          ws_item.append(item.find('span').string)
          idx = 0
          for pString in item.find('div').find_all('p'):
            text = pString.string
            idx = idx + 1
            if idx == 3:
              text  = str(text).replace('咨询电话：', '')
            if idx > 1 and idx <=3 :
              ws_item.append(text)
          print(ws_item)
          ws.append(ws_item)
      else:
        break
  wb.save("./k12英语-山姆大叔少儿英语.xlsx")

# 新东方
if site == 8:
  base_url = 'http://souke.xdf.cn/Campus/1.html'
  res = requests.get(base_url)
  soup = BeautifulSoup(res.content, "lxml")
  for child in soup.select('.cityChange'):
    base_url = 'http://souke.xdf.cn/Campus/'+child['cid']+'.html'
    res = requests.get(base_url)
    soup = BeautifulSoup(res.content, "lxml")
    reText = re.findall('eval\(\'\((.*)\)\'\)\;', soup.get_text())
    jsonText = json.loads(reText[0])
    for data in jsonText:
      wx_item = ['新东方', data['Name'], data['Address'], data['Telephone']]
      print(wx_item)
      ws.append(wx_item)
    time.sleep(1)
  wb.save("./k12英语-新东方.xlsx")


