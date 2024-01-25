# 자동화 테스트를 위해 셀리니움을 불러옵니다.
from selenium import webdriver # 동적 사이트 수집
from selenium.webdriver.common.by import By # find_element 함수 쉽게 쓰기 위함
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options  # 크롬 드라이버 옵션 추가
import time # 대기 시간 설정을 위함

# 브라우저 꺼짐 방지 옵션 추가
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
#driver = webdriver.Chrome()
driver = webdriver.Chrome(options=chrome_options)

# 접속할 URL 입력
url = input("접속할 URL: ")
#url = "https://manual.pentasecurity.com/!#/r/book/view/fa07b307a92b2bc0" # DCA_v5.0 테스트용
#url = "https://manual.pentasecurity.com/!#/r/book/update/cf261dfb57edc261" # SL3 테스트용
#url = "https://manual.pentasecurity.com/!#/r/book/update/6bdf44be8b2d6a26" # SL4 테스트용
#url = "https://manual.pentasecurity.com/!#/r/book/view/9a32974d1c72eb9f" # 책 변경 권한 없는 테스트용
#url = "https://manual.pentasecurity.com/!#/r/book/view/cf261dfb57edc261" # 책 변경 권한 체크하는 SL3 테스트용
#url = "https://manual.pentasecurity.com/!#/r/book/view/6bdf44be8b2d6a26" # 책 변경 권한 체크하는 SL4 테스트용

# 접속 시도
driver.get(url)

# 대기시간 설정
time.sleep(2)

# 대시보드 바로가기 클릭
#driver.find_element_by_xpath('//*[@id="menu"]/div/a[2]').click()

# 로그인 하기
# login = {
#     "id" : "", # <사용자의 ID를 입력해주세요.>
#     "pw" : ""  # <사용자의 PW를 입력해주세요.>
# }

# 로그인 하기
id = input("ID: ")
pw = input("Password: ")

login = {
    "id" : id,
    "pw" : pw
}

# 아이디와 비밀번호 받아와서 입력
driver.find_element(By.NAME, 'id').send_keys(login.get("id"))
time.sleep(0.5)
driver.find_element(By.NAME, 'pw').send_keys(login.get("pw"))
time.sleep(0.5)

# 로그인 버튼 클릭
driver.find_element(By.XPATH, '//*[@id="btn-login"]').click()
time.sleep(3)

# 매뉴얼 화면 진입
driver.get(url)
time.sleep(5)

# 책 변경 버튼 여부 확인
if driver.find_elements(By.CSS_SELECTOR, "#layout_inner_left_panel > fieldset:nth-child(1) > div > a"):
    print("'책 변경' 권한 확인 완료")

    button = driver.find_element(By.CSS_SELECTOR, "#layout_inner_left_panel > fieldset:nth-child(1) > div > a")
    button.click()
else:
    print("'책 변경'의 권한이 없습니다.")
    exit(0)

time.sleep(5)

# 선택된 웹 뷰어 레이아웃 확인
#checklayout = driver.find_element(By.XPATH, '//*[@id="book_web_viewer_layout"]/option[7]')
#checklayout = driver.find_element(By.XPATH, '//*[@id="book_web_viewer_layout"]')
#checklayout = Select(driver.find_element(By.XPATH, '//*[@id="book_web_viewer_layout"]'))
combobox_path = '//*[@id="book_web_viewer_layout"]'
checklayout = driver.find_element('xpath', combobox_path)

select = Select(checklayout) # Select 객체 생성
selected_option_text = select.first_selected_option.text # 선택된 옵션의 텍스트 가져오기
#print(f'Selected option text: {selected_option_text}') # 선택된 옵션 텍스트 확인
#print(selected_option_text)
#print(checklayout)

#string = checklayout.text
string = selected_option_text

# SL3/SL4 확인
print(string[-5:])

# TMM LEVEL 확인 / 'https://manual.pentasecurity.com/r/viewer/book/adb6f6d29fdfed1f/539340c4a0951d30'에서 참고했음
tmmlevel = string[-5:]

# SL3인 경우
if tmmlevel == ("(SL3)"):
    # 1) 웹 뷰어에서 PDF 내려받기를 허용하지 않습니다.
    if driver.find_element(By.XPATH, '//*[@id="book_disable_pdf_download"]').get_attribute('checked'):
        print("웹 뷰어에서 PDF 내려받기를 허용하지 않습니다. (확인 완료)")
        #pass
    else:
        value1 = driver.find_element(By.XPATH, '//*[@id="book_disable_pdf_download"]')
        driver.find_element(By.ID, 'book_disable_pdf_download').click()
        #print(value1.text,"의 체크를 해제해주세요.")
        print("'웹 뷰어에서 PDF 내려받기를 허용하지 않습니다.'항목을 체크했습니다.")
        #exit(0)

    # 2) 웹 뷰어에서 EPUB 내려받기를 허용하지 않습니다.
    if driver.find_element(By.XPATH, '//*[@id="book_disable_epub_download"]').get_attribute('checked'):
        print("웹 뷰어에서 EPUB 내려받기를 허용하지 않습니다. (확인 완료)")
    else:
        value2 = driver.find_element(By.XPATH, '//*[@id="book_disable_epub_download"]')
        driver.find_element(By.ID, 'book_disable_epub_download').click()
        #print(value2.text, "항목을 체크해주세요.")
        print("'웹 뷰어에서 EPUB 내려받기를 허용하지 않습니다.'항목을 체크했습니다.")
        #exit(0)

    # 3) 웹 뷰어에서 HTML 내려받기를 허용하지 않습니다.
    if driver.find_element(By.XPATH, '//*[@id="book_disable_html_download"]').get_attribute('checked'):
        print("웹 뷰어에서 HTML 내려받기를 허용하지 않습니다. (확인 완료)")
    else:
        value3 = driver.find_element(By.XPATH, '//*[@id="book_disable_html_download"]')
        driver.find_element(By.ID, 'book_disable_html_download').click()
        #print(value3.text, "항목을 체크해주세요.")
        print("'웹 뷰어에서 HTML 내려받기를 허용하지 않습니다.'항목을 체크했습니다.")
        #exit(0)

    # 4) 웹 뷰어에서 MS 워드 내려받기를 허용하지 않습니다.
    if driver.find_element(By.XPATH, '//*[@id="book_disable_word_download"]').get_attribute('checked'):
        print("웹 뷰어에서 MS 워드 내려받기를 허용하지 않습니다. (확인 완료)")
    else:
        value4 = driver.find_element(By.XPATH, '//*[@id="book_disable_word_download"]')
        driver.find_element(By.ID, 'book_disable_word_download').click()
        # print(value4.text, "항목을 체크해주세요.")
        print("'웹 뷰어에서 MS 워드 내려받기를 허용하지 않습니다.'항목을 체크했습니다.")
        #exit(0)

    # 5) 권두 구성 페이지 번호로 아라비아 숫자를 사용합니다.
    if driver.find_element(By.XPATH, '//*[@id="book_use_arabic_for_front_matter"]').get_attribute('checked'):
        print("권두 구성 페이지 번호로 아라비아 숫자를 사용합니다. (확인 완료)")
    else:
        value5 = driver.find_element(By.XPATH, '//*[@id="book_use_arabic_for_front_matter"]')
        driver.find_element(By.ID, 'book_use_arabic_for_front_matter').click()
        #print(value5.text, "항목을 체크해주세요.")
        print("'권두 구성 페이지 번호로 아라비아 숫자를 사용합니다.'항목을 체크했습니다.")
        #exit(0)

    # 6) 홀수 페이지에서 장을 시작합니다.
    if driver.find_element(By.XPATH, '//*[@id="book_start_chapter_in_odd"]').get_attribute('checked'):
        print("홀수 페이지에서 장을 시작합니다.(확인 완료)")
    else:
        value6 = driver.find_element(By.XPATH, '//*[@id="book_start_chapter_in_odd"]')
        driver.find_element(By.ID, 'book_start_chapter_in_odd').click()
        # print(value6.text, "항목을 체크해주세요.")
        print("'홀수 페이지에서 장을 시작합니다.'항목을 체크했습니다.")
        #exit(0)

    # 7) 웹 뷰어에서 다음 단계 차례부터 보여주지 않습니다.
    if driver.find_element(By.XPATH, '//*[@id="book_hide_toc"]').get_attribute('checked'):
        value7 = driver.find_element(By.XPATH, '//*[@id="book_hide_toc"]')
        driver.find_element(By.ID, 'book_hide_toc').click()
        # print(value7.text, "항목의 체크를 해제해주세요.")
        print("'웹 뷰어에서 다음 단계 차례부터 보여주지 않습니다.'항목의 체크를 해제했습니다.")
        #exit(0)
    else:
        print("웹 뷰어에서 다음 단계 차례부터 보여주지 않습니다. (확인 완료)")
        #pass

    # 8) 웹 뷰어에서 차례를 펼칩니다.
    if driver.find_element(By.XPATH, '//*[@id="book_unfold_toc"]').get_attribute('checked'):
        print("웹 뷰어에서 차례를 펼칩니다.(확인 완료)")
    else:
        value8 = driver.find_element(By.XPATH, '//*[@id="book_unfold_toc"]')
        driver.find_element(By.ID, 'book_unfold_toc').click()
        #print(value8.text, "항목을 체크해주세요.")
        print("'웹 뷰어에서 차례를 펼칩니다.'항목을 체크했습니다.")
        #exit(0)

    # 9) 웹 뷰어 메인 페이지에서 다음 단계 차례까지 보여줍니다.
    if driver.find_element(By.XPATH, '//*[@id="book_show_toc_of_main"]').get_attribute('checked'):
        print("웹 뷰어 메인 페이지에서 다음 단계 차례까지 보여줍니다. (확인 완료)")
    else:
        value9 = driver.find_element(By.XPATH, '//*[@id="book_show_toc_of_main"]')
        driver.find_element(By.ID, 'book_show_toc_of_main').click()
        #print(value9.text, "항목을 체크해주세요.")
        print("'웹 뷰어 메인 페이지에서 다음 단계 차례까지 보여줍니다.'항목을 체크했습니다.")
        #exit(0)

    # 10) 제목 단락 다음에 들여쓰기를 합니다.
    if driver.find_element(By.XPATH, '//*[@id="book_indent_after_heading"]').get_attribute('checked'):
        value10 = driver.find_element(By.XPATH, '//*[@id="book_indent_after_heading"]')
        driver.find_element(By.ID, 'book_indent_after_heading').click()
        # print(value10.text, "항목의 체크를 해제해주세요.")
        print("'제목 단락 다음에 들여쓰기를 합니다.'항목의 체크를 해제했습니다.")
        #exit(0)
    else:
        print("제목 단락 다음에 들여쓰기를 합니다. (확인 완료)")
        #pass

    # 11) PDF에서 페이지가 바뀌어도 그림 크기를 줄이지 않습니다.
    if driver.find_element(By.XPATH, '//*[@id="book_prevent_image_resize"]').get_attribute('checked'):
        print("PDF에서 페이지가 바뀌어도 그림 크기를 줄이지 않습니다. (확인 완료)")
    else:
        value11 = driver.find_element(By.XPATH, '//*[@id="book_prevent_image_resize"]')
        driver.find_element(By.ID, 'book_prevent_image_resize').click()
        #print(value11.text, "항목을 체크해주세요.")
        print("'PDF에서 페이지가 바뀌어도 그림 크기를 줄이지 않습니다.'항목을 체크했습니다.")
        #exit(0)

    # 12) PDF에서 그림을 Float 하지 않습니다.
    if driver.find_element(By.XPATH, '//*[@id="book_prevent_image_float_in_pdf"]').get_attribute('checked'):
        print("PDF에서 그림을 Float 하지 않습니다. (확인 완료)")
    else:
        value12 = driver.find_element(By.XPATH, '//*[@id="book_prevent_image_float_in_pdf"]')
        driver.find_element(By.ID, 'book_prevent_image_float_in_pdf').click()
        #print(value12.text, "항목을 체크해주세요.")
        print("'PDF에서 그림을 Float 하지 않습니다.'항목을 체크했습니다.")
        #exit(0)

    # 13) 댓글을 지원합니다.
    if driver.find_element(By.XPATH, '//*[@id="book_support_comment"]').get_attribute('checked'):
        value13 = driver.find_element(By.XPATH, '//*[@id="book_support_comment"]')
        driver.find_element(By.ID, 'book_support_comment').click()
        #print(value13.text, "의 체크를 해제해주세요.")
        print("'댓글을 지원합니다.'항목의 체크를 해제했습니다.")
        #exit(0)
    else:
        print("댓글을 지원합니다. (확인 완료)")

    # 14) 피드백 받기를 지원합니다.
    if driver.find_element(By.XPATH, '//*[@id="book_support_feedback"]').get_attribute('checked'):
        print("피드백 받기를 지원합니다. (확인 완료)")
    else:
        value14 = driver.find_element(By.XPATH, '//*[@id="book_support_feedback"]')
        driver.find_element(By.ID, 'book_support_feedback').click()
        #print(value14.text, "항목을 체크해주세요.")
        print("'피드백 받기를 지원합니다.'항목을 체크했습니다.")
        #exit(0)

    # 15) 공유하기를 지원합니다.
    if driver.find_element(By.XPATH, '//*[@id="book_support_sharing"]').get_attribute('checked'):
        print("공유하기를 지원합니다. (확인 완료)")
    else:
        value15 = driver.find_element(By.XPATH, '//*[@id="book_support_sharing"]')
        driver.find_element(By.ID, 'book_support_sharing').click()
        #print(value15.text, "항목을 체크해주세요.")
        print("'공유하기를 지원합니다.'항목을 체크했습니다.")
        #exit(0)

    # 16) 외부 검색 엔진 접근을 막습니다.
    if driver.find_element(By.XPATH, '//*[@id="book_disable_access_of_crawler"]').get_attribute('checked'):
        print("외부 검색 엔진 접근을 막습니다. (확인 완료)")
    else:
        value16 = driver.find_element(By.XPATH, '//*[@id="book_disable_access_of_crawler"]')
        driver.find_element(By.ID, 'book_disable_access_of_crawler').click()
        #print(driver.find_element(By.XPATH, '//*[@id="book_form"]/fieldset[3]/dl/dd[16]/label/text()'))
        #print(value16.text, "항목을 체크해주세요.")
        print("'외부 검색 엔진 접근을 막습니다.'항목을 체크했습니다.")
        #exit(0)

    # 매뉴얼의 이름도 같이 불러오도록 업데이트 예정
    print("*** SL3의 옵션 체크 확인을 완료하였습니다. ***")

# SL4인 경우
elif tmmlevel == ("(SL4)"):
    # 1) 웹 뷰어에서 PDF 내려받기를 허용하지 않습니다.
    if driver.find_element(By.XPATH, '//*[@id="book_disable_pdf_download"]').get_attribute('checked'):
        value1 = driver.find_element(By.XPATH, '//*[@id="book_disable_pdf_download"]')
        driver.find_element(By.ID, 'book_disable_pdf_download').click()
        #print(value1.text,"의 체크를 해제해주세요.")
        print("'웹 뷰어에서 PDF 내려받기를 허용하지 않습니다.'항목의 체크를 해제했습니다.")
        #exit(0)
    else:
        print("웹 뷰어에서 PDF 내려받기를 허용하지 않습니다. (확인 완료)")
        #pass

    # 2) 웹 뷰어에서 EPUB 내려받기를 허용하지 않습니다.
    if driver.find_element(By.XPATH, '//*[@id="book_disable_epub_download"]').get_attribute('checked'):
        print("웹 뷰어에서 EPUB 내려받기를 허용하지 않습니다. (확인 완료)")
    else:
        value2 = driver.find_element(By.XPATH, '//*[@id="book_disable_epub_download"]')
        driver.find_element(By.ID, 'book_disable_epub_download').click()
        #print(value2.text, "항목을 체크해주세요.")
        print("'웹 뷰어에서 EPUB 내려받기를 허용하지 않습니다.'항목을 체크했습니다.")
        #exit(0)

    # 3) 웹 뷰어에서 HTML 내려받기를 허용하지 않습니다.
    if driver.find_element(By.XPATH, '//*[@id="book_disable_html_download"]').get_attribute('checked'):
        print("웹 뷰어에서 HTML 내려받기를 허용하지 않습니다. (확인 완료)")
    else:
        value3 = driver.find_element(By.XPATH, '//*[@id="book_disable_html_download"]')
        driver.find_element(By.ID, 'book_disable_html_download').click()
        #print(value3.text, "항목을 체크해주세요.")
        print("'웹 뷰어에서 HTML 내려받기를 허용하지 않습니다.'항목을 체크했습니다.")
        #exit(0)

    # 4) 웹 뷰어에서 MS 워드 내려받기를 허용하지 않습니다.
    if driver.find_element(By.XPATH, '//*[@id="book_disable_word_download"]').get_attribute('checked'):
        print("웹 뷰어에서 MS 워드 내려받기를 허용하지 않습니다. (확인 완료)")
    else:
        value4 = driver.find_element(By.XPATH, '//*[@id="book_disable_word_download"]')
        driver.find_element(By.ID, 'book_disable_word_download').click()
        #print(value4.text, "항목을 체크해주세요.")
        print("'웹 뷰어에서 MS 워드 내려받기를 허용하지 않습니다.'항목을 체크했습니다.")
        #exit(0)

    # 5) 권두 구성 페이지 번호로 아라비아 숫자를 사용합니다.
    if driver.find_element(By.XPATH, '//*[@id="book_use_arabic_for_front_matter"]').get_attribute('checked'):
        print("권두 구성 페이지 번호로 아라비아 숫자를 사용합니다. (확인 완료)")
    else:
        value5 = driver.find_element(By.XPATH, '//*[@id="book_use_arabic_for_front_matter"]')
        driver.find_element(By.ID, 'book_use_arabic_for_front_matter').click()
        #print(value5.text, "항목을 체크해주세요.")
        print("'권두 구성 페이지 번호로 아라비아 숫자를 사용합니다.'항목을 체크했습니다.")
        #exit(0)

    # 6) 홀수 페이지에서 장을 시작합니다.
    if driver.find_element(By.XPATH, '//*[@id="book_start_chapter_in_odd"]').get_attribute('checked'):
        print("홀수 페이지에서 장을 시작합니다.(확인 완료)")
    else:
        value6 = driver.find_element(By.XPATH, '//*[@id="book_start_chapter_in_odd"]')
        driver.find_element(By.ID, 'book_start_chapter_in_odd').click()
        #print(value6.text, "항목을 체크해주세요.")
        print("'홀수 페이지에서 장을 시작합니다.'항목을 체크했습니다.")
        #exit(0)

    # 7) 웹 뷰어에서 다음 단계 차례부터 보여주지 않습니다.
    if driver.find_element(By.XPATH, '//*[@id="book_hide_toc"]').get_attribute('checked'):
        value7 = driver.find_element(By.XPATH, '//*[@id="book_hide_toc"]')
        driver.find_element(By.ID, 'book_hide_toc').click()
        #print(value7.text, "항목의 체크를 해제해주세요.")
        print("'웹 뷰어에서 다음 단계 차례부터 보여주지 않습니다.'항목의 체크를 해제했습니다.")
        #exit(0)
    else:
        print("웹 뷰어에서 다음 단계 차례부터 보여주지 않습니다. (확인 완료)")
        #pass

    # 8) 웹 뷰어에서 차례를 펼칩니다.
    if driver.find_element(By.XPATH, '//*[@id="book_unfold_toc"]').get_attribute('checked'):
        print("웹 뷰어에서 차례를 펼칩니다.(확인 완료)")
    else:
        value8 = driver.find_element(By.XPATH, '//*[@id="book_unfold_toc"]')
        driver.find_element(By.ID, 'book_unfold_toc').click()
        #print(value8.text, "항목을 체크해주세요.")
        print("'웹 뷰어에서 차례를 펼칩니다.'항목을 체크했습니다.")
        #exit(0)

    # 9) 웹 뷰어 메인 페이지에서 다음 단계 차례까지 보여줍니다.
    if driver.find_element(By.XPATH, '//*[@id="book_show_toc_of_main"]').get_attribute('checked'):
        print("웹 뷰어 메인 페이지에서 다음 단계 차례까지 보여줍니다. (확인 완료)")
    else:
        value9 = driver.find_element(By.XPATH, '//*[@id="book_show_toc_of_main"]')
        driver.find_element(By.ID, 'book_show_toc_of_main').click()
        #print(value9.text, "항목을 체크해주세요.")
        print("'웹 뷰어 메인 페이지에서 다음 단계 차례까지 보여줍니다.'항목을 체크했습니다.")
        #exit(0)

    # 10) 제목 단락 다음에 들여쓰기를 합니다.
    if driver.find_element(By.XPATH, '//*[@id="book_indent_after_heading"]').get_attribute('checked'):
        value10 = driver.find_element(By.XPATH, '//*[@id="book_indent_after_heading"]')
        driver.find_element(By.ID, 'book_indent_after_heading').click()
        #print(value10.text, "항목의 체크를 해제해주세요.")
        print("'제목 단락 다음에 들여쓰기를 합니다.'항목의 체크를 해제했습니다.")
        #exit(0)
    else:
        print("제목 단락 다음에 들여쓰기를 합니다. (확인 완료)")
        #pass

    # 11) PDF에서 페이지가 바뀌어도 그림 크기를 줄이지 않습니다.
    if driver.find_element(By.XPATH, '//*[@id="book_prevent_image_resize"]').get_attribute('checked'):
        print("PDF에서 페이지가 바뀌어도 그림 크기를 줄이지 않습니다. (확인 완료)")
    else:
        value11 = driver.find_element(By.XPATH, '//*[@id="book_prevent_image_resize"]')
        driver.find_element(By.ID, 'book_prevent_image_resize').click()
        #print(value11.text, "항목을 체크해주세요.")
        print("'PDF에서 페이지가 바뀌어도 그림 크기를 줄이지 않습니다.'항목을 체크했습니다.")
        #exit(0)

    # 12) PDF에서 그림을 Float 하지 않습니다.
    if driver.find_element(By.XPATH, '//*[@id="book_prevent_image_float_in_pdf"]').get_attribute('checked'):
        print("PDF에서 그림을 Float 하지 않습니다. (확인 완료)")
    else:
        value12 = driver.find_element(By.XPATH, '//*[@id="book_prevent_image_float_in_pdf"]')
        driver.find_element(By.ID, 'book_prevent_image_float_in_pdf').click()
        #print(value12.text, "항목을 체크해주세요.")
        print("'PDF에서 그림을 Float 하지 않습니다.'항목을 체크했습니다.")
        #exit(0)

    # 13) 댓글을 지원합니다.
    if driver.find_element(By.XPATH, '//*[@id="book_support_comment"]').get_attribute('checked'):
        value13 = driver.find_element(By.XPATH, '//*[@id="book_support_comment"]')
        driver.find_element(By.ID, 'book_support_comment').click()
        #print(value13.text, "의 체크를 해제해주세요.")
        print("'댓글을 지원합니다.'항목의 체크를 해제했습니다.")
        #exit(0)
    else:
        print("댓글을 지원합니다. (확인 완료)")

    # 14) 피드백 받기를 지원합니다.
    if driver.find_element(By.XPATH, '//*[@id="book_support_feedback"]').get_attribute('checked'):
        print("피드백 받기를 지원합니다. (확인 완료)")
    else:
        value14 = driver.find_element(By.XPATH, '//*[@id="book_support_feedback"]')
        driver.find_element(By.ID, 'book_support_feedback').click()
        #print(value14.text, "항목을 체크해주세요.")
        print("'피드백 받기를 지원합니다.'항목을 체크했습니다.")
        #exit(0)

    # 15) 공유하기를 지원합니다.
    if driver.find_element(By.XPATH, '//*[@id="book_support_sharing"]').get_attribute('checked'):
        print("공유하기를 지원합니다. (확인 완료)")
    else:
        value15 = driver.find_element(By.XPATH, '//*[@id="book_support_sharing"]')
        driver.find_element(By.ID, 'book_support_sharing').click()
        #print(value15.text, "항목을 체크해주세요.")
        print("'공유하기를 지원합니다.'항목을 체크했습니다.")
        #exit(0)

    # 16) 외부 검색 엔진 접근을 막습니다.
    if driver.find_element(By.XPATH, '//*[@id="book_disable_access_of_crawler"]').get_attribute('checked'):
        print("외부 검색 엔진 접근을 막습니다. (확인 완료)")
    else:
        value16 = driver.find_element(By.XPATH, '//*[@id="book_disable_access_of_crawler"]')
        driver.find_element(By.ID, 'book_disable_access_of_crawler').click()
        #print(driver.find_element(By.XPATH, '//*[@id="book_form"]/fieldset[3]/dl/dd[16]/label/text()'))
        #print(value16.text, "항목을 체크해주세요.")
        print("'외부 검색 엔진 접근을 막습니다.'항목을 체크했습니다.")
        #exit(0)

    # 매뉴얼의 이름도 같이 불러오도록 업데이트 예정
    print("*** SL4의 옵션 체크 확인을 완료하였습니다. ***")

else:
    print("현재 구현되지 않았습니다.")



# 엔터
#element.submit()
#keyword = "DP-ORA_v5.0_메인_사용자_설명서(SL4)"

# 사용자에게 검색어 입력
#driver.find_element(By.XPATH, '//*[@id="layout_inner_main"]/ui-page/ui-tab/ui-switch-panel/ui-flex-panel/ui-search-box/div/input').click()
# 검색 창에 keyword 입력
#driver.find_element(By.XPATH, '//*[@id="layout_inner_main"]/ui-page/ui-tab/ui-switch-panel/ui-flex-panel/ui-search-box/div/input').send_keys(Keyword)
# 검색 버튼 클릭하기
#driver.find_element(By.XPATH, '//*[@id="layout_inner_main"]/ui-page/ui-tab/ui-switch-panel/ui-flex-panel/ui-search-box/div/ui-icon[2]').click()

#element.send_keys(query_txt)  #검색어입력하게 하는 부분
#element.send_keys("\n")
#driver.find_element(By.CLASS_NAME, "clear").click()
#Search = {
#    "search" : "DP-ORA_v5.0_메인_사용자_설명서(SL4)", # <이곳에 ID를 입력하세요>
#}
#driver.find_element(By.CLASS_NAME, 'clear').send_keys(Search.get("search"))

#driver.find_element(By.XPATH, '//*[@id="layout_inner_main"]').click()
#query_txt = input('DP-ORA_v5.0_메인_사용자_설명서(SL4)')

# 사용자에게 검색어 입력
#element = driver.find_element_by_id("검색")
#element.send_keys(query_txt)  #검색어입력하게 하는 부분
#element.send_keys("\n")  #엔터효과
#//*[@id="layout_inner_main"]/ui-page/ui-tab/ui-switch-panel/ui-flex-panel/ui-search-box/div/input

#[NEW] D'Amo_DP-ORA_v5.0_메인_사용자_설명서(SL4)

#//*[@id="layout_inner_main"]/ui-page/ui-tab/ui-switch-panel/ui-flex-panel/ui-search-box/div/ui-icon[2]
