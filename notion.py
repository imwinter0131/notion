from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import date
import calendar

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI()

# Jinja2Templates를 사용하여 'templates' 폴더 지정
templates = Jinja2Templates(directory="templates")

# 동적으로 연도와 월을 받아 캘린더를 렌더링하는 경로
@app.get("/calendar/{year}/{month}", response_class=HTMLResponse)
def get_calendar(request: Request, year: int, month: int):
    # 월이 유효한 범위(1~12)인지 확인
    if not 1 <= month <= 12:
        # 유효하지 않은 월이면 오류 메시지 반환
        return HTMLResponse("<h1>오류: 유효하지 않은 월입니다.</h1>", status_code=400)

    # 해당 월의 첫 번째 요일(월요일=0, 일요일=6)과 총 일수 계산
    first_weekday, num_days = calendar.monthrange(year, month)
    
    # 캘린더 그리드를 위한 날짜 리스트 생성
    # 첫째 날의 요일까지 빈 칸(None)을 추가
    days_list = [None] * (first_weekday + 1)
    # 1일부터 마지막 날까지 날짜를 추가
    for day in range(1, num_days + 1):
        days_list.append(day)

    # 이전 달과 다음 달의 연도, 월을 계산 (탐색용)
    prev_month_year, prev_month = (year, month - 1) if month > 1 else (year - 1, 12)
    next_month_year, next_month = (year, month + 1) if month < 12 else (year + 1, 1)

    # 템플릿에 전달할 컨텍스트(데이터) 준비
    context = {
        "request": request,
        "year": year,
        "month": month,
        "days": days_list,
        "prev_month_year": prev_month_year,
        "prev_month": prev_month,
        "next_month_year": next_month_year,
        "next_month": next_month,
    }
    
    # "calendar.html" 템플릿을 렌더링하고 동적 데이터 전달
    return templates.TemplateResponse("calendar.html", context=context)

# 기본 URL로 접속하면 현재 날짜의 캘린더로 자동 리다이렉션
@app.get("/", response_class=HTMLResponse)
def get_current_calendar():
    today = date.today()
    return HTMLResponse(f"""
        <script>
            window.location.href = "/calendar/{today.year}/{today.month}";
        </script>
    """)
