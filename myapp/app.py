from app import create_app

# Flask 앱 인스턴스 생성
app = create_app()

# 로컬에서 테스트할 때만 실행
if __name__ == "__main__":
    # host와 port는 필요에 맞게 수정 가능
    app.run(host="0.0.0.0", port=5000, debug=True)
