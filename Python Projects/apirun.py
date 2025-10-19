import requests
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from urllib.parse import quote
from dataclasses import dataclass
from IPython.display import display
"""=====================================================================
API 호출 코드 
서울시 열린데이터광장 데이터 활용
Link : https://data.seoul.go.kr/dataList/OA-15361/S/1/datasetView.do
과제 스텝 
    1. API 호출
    2. json parsing, DataFrame 변환
    3. Visualization
    4. Report 별도
====================================================================="""

#바닐라 파이썬은 정적으로 타입 할당이 불가능하여 dataclass모듈 사용함. 
@dataclass
class URLStruct:
    DOMAIN: str
    KEY: str
    TYPE: str                             
    SERVICE: str       
    START_INDEX: int
    END_INDEX: int
    YEAR: str
    MON: str
    def buildUrl(self) -> str:
        return (
            f"{self.DOMAIN}/"
            f"{self.KEY}/{self.TYPE}/{self.SERVICE}/"
            f"{self.START_INDEX}/{self.END_INDEX}/{self.YEAR}/{self.MON}" )

    def addMonth(self) :
        year_int = int(self.YEAR)
        mon_int = int(self.MON)
        if mon_int >= 12:
            year_int += 1
            mon_int = 1
        else:
            mon_int += 1 
            
        self.YEAR = str(year_int)
        self.MON = f"{mon_int:02d}"

        return self

def getAPI(url: str):
    try:
        resp = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"오류코드 : HTTP_REQ_ERROR\n메시지 : {e.__class__.__name__}: {e}")
        return None

    if resp.status_code < 200 or resp.status_code >= 300:
        print(f"오류코드 : HTTP_STATUS_ERROR\n메시지 : {resp.status_code}")
        return None

    try:
        data = resp.json()
    except ValueError:
        print("오류코드 : JSON_DECODE_ERROR\n메시지 : 응답 본문을 JSON으로 해석할 수 없음")
        return None

    root_key = next((k for k in data.keys() if k.endswith("Info")), None)
    if not root_key:
        print("오류코드 : SCHEMA_ERROR\n메시지 : '*Info' 루트 키 없음")
        return None

    payload = data.get(root_key)
    if not isinstance(payload, dict):
        print("오류코드 : SCHEMA_ERROR\n메시지 : payload가 dict 형식이 아님")
        return None

    result = payload.get("RESULT", {})
    code = result.get("CODE", "")
    msg = result.get("MESSAGE", "")
    if code != "INFO-000":
        print(f"오류코드 : {code or 'API_ERROR'}\n메시지 : {msg or 'API 내부 오류'}")
        return None

    rows = payload.get("row")
    if not rows:
        print("오류코드 : NO_DATA\n메시지 : row 데이터 없음")
        return None

    return rows

def getJsonFromAPI(url: str) -> list:
    rows = getAPI(url)
    if rows is None:
        return []
    return rows

def getDframe(json):
    if not json:
        print("데이터 없음")
        return None
    else:
        df = pd.DataFrame(json)
        #계절 계산
        conditions = [
            (df["MON"].astype(int) >= 3) & (df["MON"].astype(int) <= 5),
            (df["MON"].astype(int) >= 6) & (df["MON"].astype(int) <= 8),
            (df["MON"].astype(int) >= 9) & (df["MON"].astype(int) <= 11),
            (df["MON"].astype(int) <= 2) | (df["MON"].astype(int) == 12)
        ]
        vals = [ "봄", "여름", "가을", "겨울"]
        df["SEASON"] = np.select(conditions, vals, default="계절 미상")
        return df

def calcbetween(sDt, eDt) -> int:
    sYear_int = int(sDt[0:4])
    sMon_int = int(sDt[5:7])
    eYear_int = int(eDt[0:4])
    eMon_int = int(eDt[4:7])

    year_calc = (eYear_int - sYear_int)*12
    mon_calc = eMon_int - sMon_int  

    return year_calc + mon_calc + 1

def selectRawDataByPeriod(sDt, eDt):
    obj = URLStruct(
        DOMAIN = "http://openapi.seoul.go.kr:8088",
        KEY = "777244707363686137346e52484347",
        TYPE = "json",
        SERVICE = "energyUseDataSummaryInfo",
        START_INDEX = 1,
        END_INDEX = 10,
        YEAR = sDt[0:4],
        MON = f"{int(sDt[4:7]):02}"
    )

    Months = calcbetween(sDt,eDt)

    df = pd.DataFrame()

    for i in range(Months):
        url = obj.buildUrl()
        df = pd.concat([df, getDframe(getJsonFromAPI(url))], ignore_index = True)
        obj.addMonth()

    return df

def selectData(df, cols = []): 
    result = (
        df[df["MM_TYPE"] == "개인"]      
            #EUS = 전기(kWh), GUS = 가스(m^3), WUS=수도(m^3), HUS=난방(미상)      
            [["YEAR", "SEASON", "EUS", "GUS", "WUS", "HUS"]]  
            .sort_values("YEAR", ascending=True) 
    )
    display(result)

    #1000000으로 나눠서 백만분의 일 단위로 환산, 소수점 반올림     
    for col in cols:
        result[col] = pd.to_numeric(result[col], errors="coerce").fillna(0) 
        result[col] = (result[col] / 1_000_000).round(0).astype(int)
    return result

def showDframeOnWeb(df):
    fig = go.Figure(data=[go.Table(
    header=dict(values=list(df.columns), fill_color='paleturquoise', align='left'),
    cells=dict(values=[df[col] for col in df.columns], fill_color='lavender', align='left')
    )])
    fig.show()

def groupBySUM(df, agg, cols):
    #행 집계
    df = df.groupby(agg, as_index=False)[cols].sum()
    #열 집계
    df["SUM"] = df[cols].sum(axis=1)
    df =  df[[agg] + ["SUM"]]
    return df

def groupByAVG(df, agg, cols):
    #행 집계
    df = df.groupby(agg, as_index=False)[cols].mean()
    #열 집계
    df["AVG"] = df[cols].mean(axis=1)
    df =  df[[agg] + ["AVG"]]
    return df

raw = selectRawDataByPeriod("201501","202412")
display(raw)

cols = ["EUS", "GUS", "WUS", "HUS"]

df = selectData(raw, cols)

gb1 = groupBySUM(df, "YEAR", cols)
gb2 = groupByAVG(df, "SEASON",["GUS"] )

display(gb1)
display(gb2)

# 연도별 변화
graphEnergyRate = px.line(
    gb1, 
    x="YEAR", 
    y="SUM",
    text= "SUM", 
    title="연도별 에너지 사용량 변화 - 6401 (백만분의 1 스케일링) ",
    labels = {
        "YEAR": "연도",
        "SUM": "에너지 총 사용량"
    }

)
graphEnergyRate.show()

#계절별 가스 사용량 
chartGasUseAmount = px.bar(
    gb2,
    x = "SEASON",
    y = "AVG",
    text ="AVG",
    title = "계절별 가스 사용량 평균 (백만분의 1 스케일링) ",
    labels = {
        "SEASON": "계절",
        "AVG": "가스 사용량 평균"
    },
    color="SEASON",
    color_discrete_map={
        "봄":"yellow", 
        "여름":"red", 
        "가을":"green",
        "겨울":"blue"
    }
)
chartGasUseAmount.show()


'''
1-2. Python을 사용하여 API를 호출하는 코드를 작성하고, 
2015년 1월부터 2024년 12월까지의 개인 유형의 현년 전기, 가스, 수도, 
지역난방 에너지 사용량 데이터를 수집하는 프로그램을 작성하시오. 
API 호출 성공을 확인할 수 있는 실행 결과를 캡처하여 첨부하시오. (7점)
 연도별 에너지 사용 총 사용량(전기+가스+수도+지역난방) 변화량을

3-1. 연도별 에너지 사용 총 사용량(전기+가스+수도+지역난방) 변화량을 선 그래프로 시각화하고, 그래프에 자신의 학번 뒤 4자리를 제목에 포함하여 저장하시오. (예: "연도별 에너지 사용 총액 변화 - 1234") 시각화 코드와 생성된 그래프를 첨부하시오. (4점)
3-2. 계절별 가스 사용량 평균을 막대 그래프로 시각화하고, 각 막대에 구체적인 수치를 표시하시오. 시각화 코드와 생성된 그래프를 첨부하시오. (4점)

 

from .net to asp.net core 
마이그레이션이라 흠. 

 '''
