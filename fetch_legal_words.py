#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import urllib.request
import urllib.parse
import json
import re
import time

# ==========================================
# [설정 정보]
# ==========================================
# 공공데이터포털 REST API 정보
SERVICE_KEY = os.environ.get("DATA_GO_KR_SERVICE_KEY")

if not SERVICE_KEY:
    raise RuntimeError(
        "DATA_GO_KR_SERVICE_KEY 환경변수가 설정되지 않았습니다."
    )
LIMIT = 50                 # 수집할 유효한 법률 용어 개수 (정의가 있는 항목 기준)
OUTPUT_FILE = "legal_words.json"

def fetch_legal_words():
    # 1. 인증키 디코딩 및 인코딩 처리 (공공데이터포털 특유의 double-encoding 문제 예방)
    decoded_key = urllib.parse.unquote(SERVICE_KEY)
    encoded_key = urllib.parse.quote(decoded_key)
    
    collected_data = []
    page = 1
    per_page = 100  # 페이지당 가져올 개수 (최대 100)
    
    print("==================================================")
    print("공공데이터포털 법률용어 REST API 수집 시작...")
    print(f"목표 수집 개수: {LIMIT}개 (정의가 존재하는 용어 대상)")
    print("==================================================")
    
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'accept': 'application/json'
    }
    
    max_empty_pages = 5  # 연속으로 빈 페이지가 나오면 종료할 임계값
    empty_pages_count = 0
    
    while len(collected_data) < LIMIT:
        # 공공데이터포털 REST API 엔드포인트 URL
        url = (
            f"https://api.odcloud.kr/api/15136793/v1/uddi:27e690da-670d-44eb-89bc-b38c0abdbe23"
            f"?page={page}"
            f"&perPage={per_page}"
            f"&serviceKey={encoded_key}"
        )
        
        print(f"🔄 API 페이지 {page} 호출 중... (현재 수집 완료: {len(collected_data)}/{LIMIT})")
        
        req = urllib.request.Request(url, headers=headers)
        
        response_success = False
        data = None
        
        # 에러 발생 시 최대 3번 재시도 (Backoff 가미)
        for attempt in range(1, 4):
            try:
                with urllib.request.urlopen(req) as response:
                    res_data = response.read().decode('utf-8')
                    data = json.loads(res_data)
                    response_success = True
                    break
            except Exception as e:
                print(f"  ⚠️ [시도 {attempt}/3] 호출 실패: {e}")
                if attempt < 3:
                    sleep_time = attempt * 1.5
                    print(f"  ⏳ {sleep_time}초 후 재시도합니다...")
                    time.sleep(sleep_time)
                else:
                    print(f"  ❌ 페이지 {page} 호출에 최종 실패했습니다. 다음 페이지로 넘어갑니다.")
        
        # 재시도 끝에 페이지 로딩에 실패한 경우 다음 페이지 진행
        if not response_success or data is None:
            page += 1
            time.sleep(0.5)
            continue
            
        records = data.get("data", [])
        if not records:
            empty_pages_count += 1
            print(f"⚠️ 페이지 {page}에 데이터가 없습니다.")
            if empty_pages_count >= max_empty_pages:
                print("⚠️ 연속으로 빈 페이지가 탐색되어 수집을 중단합니다.")
                break
            page += 1
            continue
        
        empty_pages_count = 0  # 데이터가 있으므로 리셋
        
        for record in records:
            word = record.get("법령용어")
            remark = record.get("비고내용")
            
            # 정의(비고내용)가 존재하고 비어있지 않은 항목만 수집
            if word and remark and str(remark).strip():
                remark_str = str(remark).strip()
                word_str = str(word).strip()
                
                # 한자 추출 정규식: 한자로만 이루어진 괄호 부분 매칭 (예: (外換))
                hanja = ""
                definition = remark_str
                hanja_match = re.search(r'\(([\u4e00-\u9fff]+)\)', remark_str)
                if hanja_match:
                    hanja = hanja_match.group(1)
                    # 정의 내용에서 괄호 한자 부분 제거 및 여분의 공백 정리
                    definition = remark_str.replace(hanja_match.group(0), "").strip()
                
                idx = len(collected_data) + 1
                word_obj = {
                    "id": f"legal_{idx:03d}",
                    "word": word_str,
                    "hanja": hanja,
                    "category": "법률기초",
                    "definition": definition,
                    "readingTip": "",
                    "frequency": 1
                }
                
                collected_data.append(word_obj)
                
                # 목표치 도달 시 루프 탈출
                if len(collected_data) >= LIMIT:
                    break
                    
        # API 서버 부하 방지를 위해 짧은 대기 시간 추가
        time.sleep(0.2)
        page += 1
            
    print("\n==================================================")
    print(f"수집 데이터 {len(collected_data)}건 JSON 파일로 저장 중...")
    print("==================================================")
    
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(collected_data, f, ensure_ascii=False, indent=2)
        print(f"🎉 성공적으로 '{OUTPUT_FILE}' 파일에 저장되었습니다!")
    except Exception as e:
        print(f"❌ 파일 저장 실패: {e}")

if __name__ == "__main__":
    fetch_legal_words()
