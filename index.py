#판다스 시각화 파일

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# 대용량 파일 처리를 위한 설정
pd.options.display.float_format = '{:.2f}'.format

# 1. 데이터 로드 (파일명은 이미지에 제공된 것과 일치시켰습니다)

baci_85 = pd.read_csv("./baci_85_only.csv")
countries = pd.read_csv('./country_codes_V202501.csv')

#1. i ==410(대한민국) 만 남기고 삭제
# 1. i == 410(대한민국) 만 남기고 필터링하여 새로운 변수에 할당
# 파이썬 규칙에 따라 숫자가 아닌 문자로 시작합니다.
# korea_2023 = df_2023[df_2023['i'] == 410].copy()

"""# 2. 인덱스 재정렬
korea_2023 = korea_2023.reset_index(drop=True)

# 3. 데이터 확인
print("--- 대한민국 2023년 수출 데이터 요약 ---")
print(korea_2023.head())
print(f"전체 행 개수: {len(korea_2023)}")"""

# print(len(df_2023))
# print(df_2023.head())

# df_2023.to_csv("./korea_2023.csv", index=False)

# HS코드 852352 -> 
# 1. k ==852352 만 남기고 삭제
# 1. k == 852352 만 남기고 필터링하여 새로운 변수에 할당
# 파이썬 규칙에 따라 숫자가 아닌 문자로 시작합니다.

# baci_85 = baci_85[baci_85['k'] == 852352].copy()
# print(baci_85.info)
# baci_85.to_csv("./baci_85_only.csv", index=False)

#데이터 가공후 새로 저장해서 변수에 저장함. 그래서 불러오는 과정은 주석처리 하였음.


# 1. 데이터 로드
baci_85 = pd.read_csv("./baci_85_only.csv")
countries = pd.read_csv('./country_codes_V202501.csv')

# 2. 'j'(수입국)를 기준으로 'country_code'와 병합
# left_on: 왼쪽(baci_85)에서 기준이 될 컬럼
# right_on: 오른쪽(countries)에서 기준이 될 컬럼
merged_df = pd.merge(
    baci_85, 
    countries[['country_code', 'country_name']], 
    left_on='j', 
    right_on='country_code', 
    how='left'
)

# 3. 중복되는 'country_code' 컬럼 제거 및 이름 정리
# 병합 후에는 'j'와 'country_code'가 같은 값을 가지므로 하나를 지워주는 것이 깔끔합니다.
merged_df = merged_df.drop(columns=['country_code']).rename(columns={'country_name': 'importer_name'})

# 4. 결과 확인
print("--- 병합 완료 데이터 요약 ---")
print(merged_df.head())

# 1. 데이터 로드
baci_85 = pd.read_csv("./baci_85_only.csv")
countries = pd.read_csv('./country_codes_V202501.csv')

# 2. j(수입국) 기준으로 국가 정보 병합
merged_df = pd.merge(
    baci_85, 
    countries[['country_code', 'country_name']], 
    left_on='j', 
    right_on='country_code', 
    how='left'
)

# 병합 후 불필요해진 country_code 컬럼 제거
merged_df.drop(columns=['country_code'], inplace=True)

# 3. t(연도) 컬럼의 값을 2021, 2022, 2023 중 랜덤하게 변경
# np.random.choice를 사용하면 지정된 리스트에서 무작위로 선택하여 채워줍니다.
years = [2021, 2022, 2023]
merged_df['t'] = np.random.choice(years, size=len(merged_df))

# 4. 결과 확인
print("--- 연도 무작위 변경 완료 (2021, 2022, 2023) ---")
print(merged_df[['t', 'j', 'country_name', 'v']].head(10))

# 5. 연습용 파일로 저장 (선택 사항)
# merged_df.to_csv("./practice_random_years.csv", index=False)

# 연도별 금액의 합을 내서 꺾은선으로 
#-----------------------------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

# --- 1. 한글 폰트 설정 ---
font_family = ''
system_fonts = [font.name for font in fm.fontManager.ttflist]

if 'NanumGothic' in system_fonts:
    font_family = 'NanumGothic'
elif 'Noto Sans CJK JP' in system_fonts:
    font_family = 'Noto Sans CJK JP'
elif 'Malgun Gothic' in system_fonts:
    font_family = 'Malgun Gothic'
elif 'AppleGothic' in system_fonts:
    font_family = 'AppleGothic'
else:
    font_family = plt.rcParams['font.family'][0]

plt.rcParams['font.family'] = font_family
plt.rcParams['axes.unicode_minus'] = False
print(f"설정된 폰트: {plt.rcParams['font.family']}")


# --- 2. 데이터 생성 (실제 데이터 사용 시 이 부분은 생략 가능) ---
np.random.seed(42)
years = [2021, 2022, 2023]
countries_list = ['USA', 'China', 'Vietnam', 'Germany', 'India', 'Japan', 'UK', 'France', 'Italy', 'Brazil', 'Canada', 'Russia', 'Singapore', 'Australia']
data = {
    't': np.random.choice(years, 500),
    'country_name': np.random.choice(countries_list, 500),
    'v': np.random.uniform(100, 5000, 500)
}
merged_df = pd.DataFrame(data)


# --- 3. 데이터 가공 ---
# 3-1. 연도별 합계 (꺾은선 그래프용)
yearly_total = merged_df.groupby('t')['v'].sum().reset_index()

# 3-2. 국가별/연도별 피벗 및 성장률 (기타 그래프용)
pivot_df = merged_df.pivot_table(index='country_name', columns='t', values='v', aggfunc='sum').fillna(0)
pivot_df['growth_rate'] = ((pivot_df[2023] - pivot_df[2021]) / pivot_df[2021] * 100).replace([np.inf, -np.inf], 0)
pivot_df['total_v'] = pivot_df[2021] + pivot_df[2022] + pivot_df[2023]


# --- 4. 시각화 시작 ---

# [추가] 시각화 1: 연도별 총 수출액 추이 (꺾은선 그래프)
plt.figure(figsize=(10, 6))
sns.lineplot(data=yearly_total, x='t', y='v', marker='o', markersize=12, linewidth=3, color='#E74C3C')

# 그래프에 금액 수치 직접 표시
for i in range(len(yearly_total)):
    plt.text(yearly_total.iloc[i]['t'], yearly_total.iloc[i]['v'], 
             f"{yearly_total.iloc[i]['v']:,.0f}", 
             va='bottom', ha='center', fontsize=11, fontweight='bold')

plt.title('보고서 1: 스마트카드 연도별 총 수출액 추이', fontsize=16, pad=20)
plt.xlabel('연도', fontsize=12)
plt.ylabel('총 수출액 (Value)', fontsize=12)
plt.xticks(years)
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.show()


# 시각화 2: 글로벌 시장 수출 집중도 (파이 차트)
top_5_value = pivot_df.nlargest(5, 'total_v')
others_value = pivot_df['total_v'].sum() - top_5_value['total_v'].sum()
pie_data = pd.concat([top_5_value['total_v'], pd.Series({'기타 국가': others_value})])

plt.figure(figsize=(8, 8))
plt.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=140,
        colors=sns.color_palette("Pastel1"), explode=[0.05] * len(pie_data))
plt.title('보고서 2: 글로벌 시장 수출 집중도 (Top 5 vs 기타)', fontsize=16)
plt.show()


# 시각화 3: 수출 성장률 상위 7개국 (막대 그래프)
top_growth = pivot_df.nlargest(7, 'growth_rate')

plt.figure(figsize=(12, 6))
colors = sns.color_palette("rocket", len(top_growth))
sns.barplot(x=top_growth['growth_rate'], y=top_growth.index, palette=colors)

plt.title('보고서 3: 21년 대비 23년 수출 성장률 상위 7개국', fontsize=16, pad=20)
plt.xlabel('성장률 (%)', fontsize=12)
plt.ylabel('국가명', fontsize=12)

for i, v in enumerate(top_growth['growth_rate']):
    plt.text(v, i, f" {v:.1f}%", va='center', fontweight='bold')

plt.tight_layout()
plt.show()

