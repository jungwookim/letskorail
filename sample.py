# coding=utf-8

import json
import letskorail
from letskorail import Korail
from letskorail.options import AdultPsg, ChildPsg
from letskorail.options import TrainType
from letskorail.options import SeatOption
from letskorail.options import YouthDisc
from smtp import send_email
info = {
    "id": "",
    "pw": ""
}

korail = Korail()

###########################
# 디바이스의 uuid를 알고 있을 떄
###########################
# korail.set_uuid(info["uuid"])

###########################
# 로그인
###########################
profile = korail.login(info["id"], info["pw"])

###########################
# 승객 설정
###########################
psgrs = [AdultPsg(1)]

###########################
# 열차 조회
###########################

# ###########################
# # 할인 상품 열차 조회
# ###########################
# trains = korail.search_train(
#     "청량리",
#     "안동",
#     discnt_type=YouthDisc(),  # 힘내라 청춘 상품
#     passengers=[AdultPsg()]
#     # 힘내라 청춘은 성인 1명 대상임
#     # 인원을 초과하면 DiscountError exception 발생
#     # 자세한 조건은 코레일 app이나 discount.py 참고
# )
# print(trains[0])

###########################
# 열차 예약
###########################
import time
cnt = 1
while True:
    try:
        data = {
            "dpt": "창원중앙",
            "arv": "서울",
            "date": "20240714",
            "time": "180000",
            "train_no": "4024",
            
        }
        trains = korail.search_train(
            "창원중앙",
            "서울",
            date="20240714",
            time="180000",
            passengers=psgrs,
            train_type=TrainType.KTX_ALL,
        )
        for train in trains:   
            # print("기차 정보", train.train_no)
            if "4024" in train.train_no:
                print("열차를 찾았습니다", train)
                rsv = korail.reserve(trains[0], seat_opt=SeatOption.SPECIAL_FIRST)
                print("구매내역", rsv.info)

                # 이메일 보내기
                subject = "[코레일] 예약이 완료되었습니다."
                to_email = "kjw0323@gmail.com"
                send_email(subject, rsv.info, to_email)
                break
        else:
            print(f"시도횟수: {cnt} 기차를 찾고 있습니다.")
            cnt += 1
            time.sleep(0.5)
            continue
    except letskorail.exceptions.NoResultsError as e:
        print(f"재시도 {cnt} 번째")
        cnt += 1
        time.sleep(1)
        continue
    print("종료")
    break
        

###########################
# 선호 좌석 예약
###########################
# seats = (
#     trains[0].cars[3].select_seats(location="출입문", position="내측"),
# )  # 3호차 좌석 예약

# rsv = korail.reserve(trains[0], seat_opt=seats)  # Iterable 형태로 넘겨줘야 함
# print(rsv.info)

###########################
# 예약 취소
###########################
# korail.cancel(rsv)
# print(">>> 취소 완료 <<<")

# ###########################
# # 정기권 조회 및 예약
# ###########################
# ticket = korail.pass_ticket("내일로")
# trains = korail.pass_search(ticket, "서울", "부산", "20220207", "000000")
# rsv = korail.pass_reserve(ticket, trains[0])
# print(rsv.info)
