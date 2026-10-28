# 도서관 대출 웹페이지 — 대출 규칙은 모두 solution.py의 LibraryLoan이 판단한다.
import streamlit as st

from solution import LibraryLoan

st.set_page_config(page_title="도서관 대출 시스템", page_icon="📚")

if "lib" not in st.session_state:
    st.session_state.lib = LibraryLoan()
    st.session_state.history = []
lib = st.session_state.lib


def parse_day(text):
    """입력 문자열을 숫자로 바꿔서 그대로 넘긴다. 유효성 판단은 solution.py가 한다."""
    text = text.strip()
    try:
        return int(text)
    except ValueError:
        pass
    try:
        return float(text)
    except ValueError:
        return text


def day_hint(day):
    if not isinstance(day, int):
        return "날짜는 정수로 입력하세요. (예: 1, 2, 3 …)"
    if day < 1:
        return "날짜는 1 이상이어야 합니다."
    return ""


def show_fail(title, detail=""):
    st.error(f"## ❌ 실패\n{title}" + (f"\n\n입력 확인: {detail}" if detail else ""))


st.title("📚 도서관 대출 시스템")
st.caption("책: B001 · B002 · B003 · B004 · B005  |  대출 기간 14일  |  날짜는 '며칠째'(1 이상 정수)")

tab_borrow, tab_return, tab_list = st.tabs(["대출", "반납", "대출 목록"])

with tab_borrow:
    with st.form("borrow"):
        book = st.text_input("책 번호", placeholder="B001")
        name = st.text_input("이름", placeholder="김민수")
        day_text = st.text_input("며칠째", placeholder="1")
        submitted = st.form_submit_button("대출하기")
    if submitted:
        day = parse_day(day_text)
        ok = lib.borrow(book.strip(), name.strip(), day)
        st.session_state.history.append(f"대출 {book} / {name} / {day_text} → {'성공' if ok else '실패'}")
        if ok:
            due = dict(lib.get_loans(name.strip()))[book.strip()]
            st.success(f"## ✅ 대출 성공\n{name}님이 {book}을(를) 빌렸습니다. 반납 기한: {due}일째")
        else:
            show_fail("대출이 거절되었습니다. (없는 책 · 잘못된 날짜 · 이미 대출 중 · 3권 초과 · 연체 중 · 대출 정지)",
                      day_hint(day))

with tab_return:
    with st.form("return"):
        book = st.text_input("책 번호", placeholder="B001")
        name = st.text_input("이름", placeholder="김민수")
        day_text = st.text_input("며칠째", placeholder="10")
        submitted = st.form_submit_button("반납하기")
    if submitted:
        day = parse_day(day_text)
        late = lib.return_book(book.strip(), name.strip(), day)
        st.session_state.history.append(f"반납 {book} / {name} / {day_text} → {'실패' if late == -1 else f'연체 {late}일'}")
        if late == -1:
            show_fail("반납이 거절되었습니다. (본인이 빌린 책이 아님 · 이미 반납함 · 잘못된 날짜 · 빌린 날보다 이른 날짜)",
                      day_hint(day))
        else:
            st.success(f"## ✅ 반납 성공\n연체 일수: **{late}일**")
            if late > 0:
                st.warning(f"{name}님은 {day}일째부터 {late}일 동안 대출 정지입니다.")

with tab_list:
    with st.form("list"):
        name = st.text_input("이름", placeholder="김민수")
        submitted = st.form_submit_button("대출 목록 보기")
    if submitted:
        loans = lib.get_loans(name.strip())
        if loans:
            st.table([{"책 번호": b, "반납 기한": f"{due}일째까지"} for b, due in loans])
        else:
            st.info(f"{name}님이 빌린 책이 없습니다.")

st.divider()
with st.expander("처리 기록"):
    for line in st.session_state.history:
        st.write(line)
if st.button("처음 상태로 초기화"):
    st.session_state.clear()
    st.rerun()
