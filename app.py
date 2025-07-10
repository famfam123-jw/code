import streamlit as st
import feedparser
from datetime import datetime, timezone, timedelta
import pytz

# 📰 뉴스 수집 키워드 & RSS 소스
keywords = ['고용노동부', '노동부', '고용부']
rss_sources = {
    "경향신문": "https://www.khan.co.kr/rss/rssdata/total_news.xml",
    "국민일보": "https://www.kmib.co.kr/rss/data/kmibRssAll.xml",
    "동아일보": "https://rss.donga.com/total.xml",
    "서울신문": "https://www.seoul.co.kr/xml/rss/rss_society.xml",
    "세계일보": "http://rss.segye.com/segye_recent.xml",
    "아시아투데이": "http://www.asiatoday.co.kr/rss/01.xml",
    "조선일보": "https://www.chosun.com/arc/outboundfeeds/rss/?outputType=xml",
    "한겨레": "https://www.hani.co.kr/rss/",
    "이투데이": "https://rss.etoday.co.kr/eto/etoday_news_all.xml",
    "한국일보": "http://rss.hankooki.com/news/hk00_list.xml",
    "뉴스토마토": "https://www.newstomato.com/rss/",
    "머니투데이": "http://rss.mt.co.kr/mt_news.xml",
    "매일경제": "https://www.mk.co.kr/rss/40300001/",
    "메트로경제": "http://www.metroseoul.co.kr/rss/rss.xml",
    "브릿지경제": "http://www.viva100.com/rss/rss.xml",
    "서울경제": "https://www.sedaily.com/rss/Feed.xml",
    "아주경제": "http://www.ajunews.com/rss/news_all.xml",
    "이데일리": "http://rss.edaily.co.kr/edaily_news.xml",
    "매일노동뉴스": "https://www.labortoday.co.kr/rss/allArticle.xml",
    "파이낸셜뉴스": "http://www.efnews.co.kr/rss/allArticle.xml",
    "한국경제": "https://www.hankyung.com/feed/all-news",
    "대한경제": "http://www.dnews.co.kr/rss/rss.xml",
    "전자신문": "http://rss.etnews.com/Section901.xml",
    "연합뉴스": "https://www.yna.co.kr/rss/news.xml",
    "뉴시스(속보)": "https://www.newsis.com/RSS/sokbo.xml",
    "뉴시스(사회)": "https://www.newsis.com/RSS/society.xml",
    "뉴시스(정치)": "https://www.newsis.com/RSS/politics.xml",
    "뉴스1": "https://www.news1.kr/rss/news.xml"
}

# 🌐 서울 기준 시간대 설정
kst = timezone(timedelta(hours=9))

# 📌 Streamlit UI
st.title("🗞 고용노동 뉴스 수집기 (RSS 기반)")
st.markdown("지정한 시간대의 RSS 뉴스를 수집하여 키워드에 맞는 기사만 추출합니다.")

col1, col2 = st.columns(2)
with col1:
    start_time_input = st.time_input("⏱ 시작 시간", value=datetime.now().time())
with col2:
    end_time_input = st.time_input("⏱ 종료 시간", value=datetime.now().time())

if st.button("🔍 뉴스 수집 시작"):
    today = datetime.now(tz=kst).date()
    start_time = datetime.combine(today, start_time_input).replace(tzinfo=kst)
    end_time = datetime.combine(today, end_time_input).replace(tzinfo=kst)

    filename = f"고용노동뉴스_{start_time.strftime('%Y%m%d_%H%M')}_to_{end_time.strftime('%H%M')}.txt"
    content_lines = []
    match_count = 0

    with st.spinner("뉴스 수집 중입니다..."):
        for press, url in rss_sources.items():
            feed = feedparser.parse(url)
            for entry in feed.entries:
                title = entry.get("title", "")
                summary = entry.get("summary", "")
                published = entry.get("published_parsed")

                if published:
                    pub_time = datetime(*published[:6], tzinfo=timezone.utc).astimezone(kst)
                    if not (start_time <= pub_time <= end_time):
                        continue
                else:
                    pub_time = None

                if any(k in title for k in keywords) or any(k in summary for k in keywords):
                    line = f"[{press}] {title}\n{entry.link}\n"
                    line += f"🕒 {pub_time.strftime('%Y-%m-%d %H:%M:%S') if pub_time else '발행시간 정보 없음'}\n\n"
                    content_lines.append(line)
                    match_count += 1

    if match_count > 0:
        result = "".join(content_lines)
        st.success(f"✅ 총 {match_count}건의 뉴스가 수집되었습니다.")
        st.download_button(label="📥 결과 다운로드", data=result, file_name=filename, mime="text/plain")
        st.text_area("📝 미리보기", result, height=300)
    else:
        st.warning("⚠️ 해당 시간대에 조건에 맞는 뉴스가 없습니다.")
