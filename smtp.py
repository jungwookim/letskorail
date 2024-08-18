import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# 이메일 보내기 함수
def send_email(subject, body, to_email):
    # Gmail SMTP 서버 설정
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "kjw0323@gmail.com"
    password = ""

    # 이메일 메시지 작성
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject

    # 이메일 본문 추가
    msg.attach(MIMEText(body, "plain"))

    try:
        # SMTP 서버 연결
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # TLS(Transport Layer Security) 시작
        server.login(sender_email, password)  # 로그인

        # 이메일 전송
        server.send_message(msg)
        print("이메일이 성공적으로 보내졌습니다.")
    except Exception as e:
        print(f"이메일 전송에 실패했습니다: {e}")
    finally:
        server.quit()  # 서버 연결 종료
