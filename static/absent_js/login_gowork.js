function gowork() {
    const empId = document.getElementById('empid').value;
    const empPhone = document.getElementById('empphone').value;

    // ID와 전화번호 일치 여부 확인
    if (empId === empPhone) {
        // 현재 시각 정보 가져오기
        const currentTime = new Date();
        var options = {
            year: 'numeric',
            month: 'numeric',
            day: 'numeric',
            hour: 'numeric',
            minute: 'numeric',
            second: 'numeric'
        };
        var dateTimeString = new Intl.DateTimeFormat('ko-kr', options).format(currentTime);

        // 시간 DB에 저장하는 로직 추가
        saveTimeToDB(currentTime, empId);

        // 알림 메시지 표시
        var message = +empId + '번 직원, 출근 처리되었습니다. 좋은 하루 되세요! \n출근시간: ' + dateTimeString;
        alert(message);

    } else {
        alert('ID와 전화번호가 일치하지 않습니다.');
    }
}

function saveTimeToDB(time, id, wag_id) {
    // DB에 시간 저장하는 로직 구현
    // 예: Ajax 요청을 사용하여 서버로 시간 데이터 전송
    // AJAX 요청 생성
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/save_time_to_db', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    // 요청 본문에 시간 데이터 전송
    var time_data = JSON.stringify({time: time});
    var id_data = id;
    var wag_id =
        xhr.send(time_data, id_data,);
}

function gohome() {
    var currentTime = new Date();
    var message = '퇴근하시겠습니까? 퇴근시간: ' + currentTime.toLocaleTimeString();
    var confirmresult = confirm(message);

    if (confirmresult) {
        alert('퇴근시간: ' + currentTime.toLocaleTimeString() + '\n퇴근처리 되었습니다. 오늘도 수고하셨습니다!')
    } else {
        alert('퇴근이 취소되었습니다.')
    }
}
