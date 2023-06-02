// function deleteEmployee(empId) {
//   var confirmation = confirm("정말로 이 직원 정보를 삭제하시겠습니까?");
//
//   if (confirmation) {
//     // 서버로 삭제 요청 보내기
//     var xhr = new XMLHttpRequest();
//     xhr.onreadystatechange = function() {
//       if (xhr.readyState === 4 && xhr.status === 200) {
//         // 삭제 성공 메시지 표시
//         alert("Employee deleted successfully.");
//         // 새로고침 또는 다른 동작 수행
//       }
//     };
//
//     xhr.open('GET', '/delete-employee?empId=' + empId, true);  // 삭제를 처리하는 서버 엔드포인트 URL
//     xhr.send();
//   }
// }
function deleteEmployee(empId) {
  if (confirm('정말로 이 직원을 삭제하시겠습니까?')) {
    const form = document.getElementById('deleteForm');
    form.action = form.action.replace('emp_id', empId);
    form.submit();
  }
}