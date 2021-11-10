# -*- coding: utf-8 -*-
"""추천시스템_사용자 평점 반영(가수 반영).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15I4zm1rqoBZcQ4hSTxigTB52pwfGag0Y

4) **user의 피드백을 반영하고 싶다면?**

- user가 추천한 노래들을 바탕으로 평가를 매김
- ex) 1번 노래 5점, 2번 노래 3점, 3번 노래 1점
- 1번 노래의 정보들(위에서 뽑아낸 tag와 가중치)을 활용
- 높게 점수 매긴 노래와 관련된 애들을 더 추천하고, 낮게 매긴 노래와 관련된 애들은 추천항목에서 배제
"""

import pandas as pd

data= pd.read_excel('/content/drive/Shareddrives/BOAZ_Adv/recommender_data.xlsx')
data

song = pd.read_json('/content/drive/Shareddrives/BOAZ_Adv/melon_data/song_meta.json')
song.head()

song.rename(columns={"song_gn_dtl_gnr_basket":"곡 세부 장르 리스트", "issue_date":"발매일", "album_name": "앨범 명", "album_id":"앨범 ID", "artist_id_basket":"아티스트 ID 리스트", "song_name":"곡 제목", "song_gn_gnr_basket":"곡 장르 리스트", "artist_name_basket":"아티스트 리스트","id":"곡 ID"},inplace= True )
song.head()

song= song[['곡 ID','곡 제목','아티스트 리스트']]
song

song_data = pd.merge(data,song,how='left',left_on='song id',right_on ='곡 ID')
song_data = song_data.drop('song id',axis = 1)
song_data

user_tag = song_data[song_data['tag max'].str.contains('휴식')]
user_tag

user_emotion = song_data[song_data['emotion max'].str.contains('편안한')]
user_emotion

tag_id = set(user_tag['곡 ID'].unique())
emotion_id = set(user_emotion['곡 ID'].unique())

intersection = tag_id & emotion_id
intersection = list(intersection)

len(intersection)

intersection

res  =[]
for i in intersection:
  ls = song_data[song_data['곡 ID'] == i].index[0]
  res.append(ls)

print(len(res))

selected = song_data.iloc[res]
selected.tail()

selected_sample  = selected.sample(n=15,random_state=42)
selected_sample

selected_sample['점수']=0
selected_sample

name = list(selected_sample['곡 제목'])



score=[]
for i in name:
  s = input(f'\'{i}\' 의 점수를 입력해주세요   ',)
  score.append(int(s))

mn = min(score)
mx = max(score)

# score_list=[10,9,3,4,3,2,3,4,5,2,10,10,6,6,6]
selected_sample['점수'] = score

selected_sample

"""## 노래 추천시 가수 고려"""

fav_artist = list(selected_sample[selected_sample['점수']==mx]['아티스트 리스트'])
fav_artist

hate_artist = list(selected_sample[selected_sample['점수']==mn]['아티스트 리스트'])
hate_artist

# selected['fav_artist'] = selected['아티스트 리스트'].apply(lambda x: True if x in fav_artist else False)
# fav_artist_song = selected[selected['fav_artist']==True]
# fav_artist_song
song_data['가중치']=0  # 가중치 열 생성
song_data['fav_artist'] = song_data['아티스트 리스트'].apply(lambda x: True if x in fav_artist else False)
fav_artist_index = song_data[song_data['fav_artist']==True].index.values.tolist()

for i in fav_artist_index:
  song_data['가중치'].iloc[i]  = song_data['가중치'].iloc[i] + 0.3


song_data.iloc[fav_artist_index].tail(30)

song_data['hate_artist'] = song_data['아티스트 리스트'].apply(lambda x: True if x in hate_artist else False)
hate_artist_index = song_data[song_data['hate_artist']==True].index.values.tolist()

for i in hate_artist_index:
  song_data['가중치'].iloc[i]  = song_data['가중치'].iloc[i] - 0.2


song_data.iloc[hate_artist_index].tail(30)

fav_tag = list(selected_sample[selected_sample['점수']==mx]['tag max'])
fav_tag

song_data['fav_tag'] = song_data['tag max'].apply(lambda x: True if x in fav_tag else False)
fav_tag_index = song_data[song_data['fav_tag']==True].index.values.tolist()

for i in fav_tag_index:
  song_data['가중치'].iloc[i]  = song_data['가중치'].iloc[i] + 0.3


song_data.iloc[fav_tag_index].tail(30)






# selected['fav_tag'] = selected['max_key'].apply(lambda x: True if x in fav_tag else False)
# fav_tag_song = selected[selected['fav_tag']==True]
# fav_tag_song

hate_tag = list(selected_sample[selected_sample['점수']==mn]['tag max'])

song_data['hate_tag'] = song_data['tag max'].apply(lambda x: True if x in hate_tag else False)
hate_tag_index = song_data[song_data['hate_tag']==True].index.values.tolist()

for i in hate_tag_index:
  song_data['가중치'].iloc[i]  = song_data['가중치'].iloc[i] - 0.2


song_data.iloc[hate_tag_index].tail(30)

fav_emotion = list(selected_sample[selected_sample['점수']==mx]['emotion max'])
print(fav_emotion)

hate_emotion = list(selected_sample[selected_sample['점수']==mn]['emotion max'])
print(hate_emotion)

song_data['fav_emotion'] = song_data['emotion max'].apply(lambda x: True if x in fav_emotion else False)
fav_emotion_index = song_data[song_data['fav_emotion']==True].index.values.tolist()

for i in fav_emotion_index:
  song_data['가중치'].iloc[i]  = song_data['가중치'].iloc[i] + 0.3


song_data.iloc[fav_emotion_index].tail(30)

song_data['hate_emotion'] = song_data['emotion max'].apply(lambda x: True if x in hate_emotion else False)
hate_emotion_index = song_data[song_data['hate_emotion']==True].index.values.tolist()

for i in hate_emotion_index:
  song_data['가중치'].iloc[i]  = song_data['가중치'].iloc[i] - 0.2


song_data.iloc[hate_emotion_index].tail(30)

song_data[song_data['가중치']>0.3]

"""## 사용자가 재추천을 원했다고 가정"""

selected = song_data.iloc[res]

wgt_rec = selected.sort_values('가중치',ascending=False).iloc[:5]   #가중치를 고려하여 5개 추천
wgt_rec

rand_rec  = selected.sample(n=10,random_state=1110)
rand_rec

selected_sample = pd.concat([wgt_rec,rand_rec])
selected_sample['점수']=0
selected_sample

name = list(selected_sample['곡 제목'])
score=[]
for i in name:
  s = input(f'\'{i}\' 의 점수를 입력해주세요   ',)
  score.append(int(s))


selected_sample['점수'] = score

selected_sample

# 재추천을 원할 시 위에서와 동일하게 높은 점수를 받은 태그, 가수, 감정 가중치 +, 낮은 점수를 받은 태그, 가수, 감정 가중치 -