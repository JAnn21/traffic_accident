import webbrowser
import pandas as pd
from matplotlib import font_manager, rc
import platform
import chardet
import folium
from scipy import spatial
import json
from urllib.request import urlopen

# 한글 폰트 깨지는 것을 막기위한 처리
if platform.system() == 'Windows':
    font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
    rc('font', family=font_name)

# 전국 교통사고 데이터
with open('C:/Users/dlwngus/Downloads/도로교통공단_교통사고다발지역_20191010.csv','rb')as f:  # csv파일을 불러올때 깨지는 한글을 위한 처리
    result = chardet.detect((f.read()))

accident_data=pd.read_csv("C:/Users/dlwngus/Downloads/도로교통공단_교통사고다발지역_20191010.csv",encoding=result['encoding']) # 전국 교통사고 다발지역 데이터 10365개

url = 'http://ip-api.com/json'
response = urlopen(url)
data = json.load(response)
IP=data['query']
lat=data['lat']
lon = data['lon']
current_position=[]
current_position.append(lat) # 위치 자동설정
current_position.append(lon)

accident_data1 = pd.DataFrame([accident_data["위도"],accident_data["경도"],accident_data["사고지역위치명"],accident_data["발생건수"]]) # 지도 표시를 위한 위도경도를 따로 추출
accident_data2 = accident_data1.T # 행,열을 교체
accident_data2['위도']=accident_data2['위도'].astype(float) # object인 위도,경도를 처리를 위해 float타입으로 변환
accident_data2['경도']=accident_data2['경도'].astype(float)
accident_data3 = pd.DataFrame([accident_data2["위도"],accident_data2["경도"]])
position = accident_data3.T
position2=position.as_matrix() # 데이터프레임을 행렬로 변환
print(position2)

list1 = accident_data2["위도"]
list2 = accident_data2["경도"]
list3 = accident_data2["사고지역위치명"]
list4 = accident_data2["발생건수"]

map = folium.Map(location=[current_position[0],current_position[1]], zoom_start = 17) # 맵 지도 설정
for i in range(len(list1)):  # 원하는 곳들에 마크 표시
    folium.Marker([list1[i],list2[i]], popup=list3[i]).add_to(map)

proximate_position=position2[spatial.KDTree(position2).query(current_position)[1]] # 제일 가까운 경로 표시
# KD Tree 알고리즘은 각 차수별로 비교한다

folium.Marker(location=[current_position[0],current_position[1]], popup="내 위치",icon=folium.Icon(color='green')).add_to(map)
folium.Marker(location=[proximate_position[0], proximate_position[1]], popup="가장 가까운 곳",icon=folium.Icon(icon='cloud',color='red')).add_to(map)
# 현재 위치와제일 가까운 위치표시

map.save('map.html') # 홈페이지를 통해 지도 추출

proximate_position1=pd.DataFrame([list1, list2, list3, list4]) # 위치에 따른 정보추출
proximate_position2=proximate_position1.T
proximate_position3=proximate_position2.loc[proximate_position2['위도']==proximate_position[0]] # 가까운 위치와 같으면 그에 맞는 정보추출
print("현재 나의 위치는 ", current_position)
print("제일 가까운 교통사고 다발지역은 \n" , proximate_position3)


webbrowser.open('C:/python/GPS/map.html')
