//viết một hàm để gọi api api/check-login/ kiêm tra xem người dùng đã đăng nhập chưa
//nếu đã đăng nhập thì chuyển hướng về trang người dùng
//nếu chưa đăng nhập thì chuyển hướng về trang đăng nhập
//sử dụng hàm này ở tất cả các trang cần kiểm tra đăng nhập
//sử dụng hàm này ở tất cả các trang cần kiểm tra đăng nhập như trang người dùng, trang đặt hàng, trang giỏ hàng
//sử dụng fectch để gọi api
//sử dụng window.location.href để chuyển hướng trang
//sử dụng document.body.innerHTML để thay đổi nội dung của trang
function checkLogin() {
    fetch('/api/check-login/')
        .then(res => {
            if (!res.ok) {
                throw new Error(`HTTP error! status: ${res.status}`);
            }
            return res.json();
        })
        .then(data => {
            if (data.login) {
                var popup = document.getElementById('userOptionsPopup');
                popup.classList.remove('hide');
            } else {
                // Hiển thị popup
                var div = document.querySelector('.containTaikhoan');
                div.style.transform = 'scale(1)';
            }
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation: ', error);
        });
}

function closePopup() {
    var popup = document.querySelector('.containTaikhoan');
    if (popup) {
        popup.style.transform = 'scale(0)';
    }
}
function showPopup() {
    var popup = document.getElementById('userOptionsPopup');
    if (popup) {
        popup.classList.remove('hide');
    }
}

function hidePopup() {
    var popup = document.getElementById('userOptionsPopup');
    if (popup) {
        popup.classList.add('hide');
    }
}
//sử dụng để chuyển tab login và signup
document.addEventListener('DOMContentLoaded', function () {

    // Event chuyển tab login-signup
    const tabs = document.getElementsByClassName('tab');
    Array.from(tabs).forEach(tab => {
        const a = tab.getElementsByTagName('a')[0];
        a.addEventListener('click', function (e) {
            e.preventDefault(); // tắt event mặc định

            // Thêm active(màu xanh lá) cho li chứa tag a này => ấn login thì login xanh, signup thì signup sẽ xanh
            this.parentElement.classList.add('active');

            // Sau khi active login thì phải tắt active sigup và ngược lại
            // Trường hợp a này thuộc login => <li>Login</li> sẽ có nextElement là <li>SignUp</li>
            if (this.parentElement.nextElementSibling) {
                this.parentElement.nextElementSibling.classList.remove('active');
            }
            // Trường hợp a này thuộc signup => <li>SignUp</li> sẽ có .previousElement là <li>Login</li>
            if (this.parentElement.previousElementSibling) {
                this.parentElement.previousElementSibling.classList.remove('active');
            }

            // Ẩn phần nhập của login nếu ấn signup và ngược lại
            // href của 2 tab signup và login là #signup và #login -> tiện cho việc getElement dưới đây
            const target = this.href.split('#')[1];
            document.getElementById(target).style.display = 'block';

            const hide = (target == 'login' ? 'signup' : 'login');
            document.getElementById(hide).style.display = 'none';
        })
    });
});

//sử dụng để kiểm tra dữ liệu người dùng nhập vào form đăng ký

document.addEventListener('DOMContentLoaded', function () {
    // Đoạn mã của bạn ở đây

    var taikhoan = document.getElementsByClassName('taikhoan')[0];
    // Nếu không tìm thấy phần tử có class 'taikhoan', không thực hiện gì cả
    if (!taikhoan) {
        return;
    }
    var list = taikhoan.getElementsByTagName('input');

    ['blur', 'focus'].forEach(function (evt) {
        for (var i = 0; i < list.length; i++) {
            list[i].addEventListener(evt, function (e) {
                var label = this.parentNode.querySelector('label'); // tìm nhãn trong cùng một div
                if (e.type === 'blur') {
                    if (this.value === '') {
                        label.classList.remove('active');
                        label.classList.remove('highlight');
                    } else {
                        label.classList.remove('highlight');
                    }
                } else if (e.type === 'focus') {
                    label.classList.add('active');
                    label.classList.add('highlight');
                }
            });
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    function signUp(event) {
        event.preventDefault(); // ngăn chặn hành vi mặc định của form

        // lấy giá trị từ các trường nhập liệu
        const ten = event.target.elements.ten.value;
        const ho = event.target.elements.ho.value;
        const email = event.target.elements.email.value;
        const newPass = event.target.elements.newPass.value;
        const phone = event.target.elements.soDienThoai.value; // thêm biến để lấy giá trị số điện thoại

        // kiểm tra xem các trường nhập liệu có đúng định dạng không
        const emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/; // định dạng email cơ bản
        const passwordPattern = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$/; // mật khẩu phải có ít nhất 8 ký tự, bao gồm cả chữ hoa, chữ thường và số
        // biểu thức chính quy kiểm tra số điện thoại bắt đầu bằng số 0 và có tổng cộng 10 chữ số
        const phonePattern = /^0\d{9}$/;
        //biểu thức chính quy kiểm tra tên người dùng không chứa ký tự đặc biệt, không chứa số
        const namePattern = /^[a-zA-ZÀ-ỹ ]+$/;

        if (!namePattern.test(ten)) {
            alert('Tên không được chứa ký tự đặc biệt hoặc số');
            return;
        }

        if (!namePattern.test(ho)) {
            alert('Họ không được chứa ký tự đặc biệt hoặc số');
            return;
        }

        if (!emailPattern.test(email)) {
            alert('Email không đúng định dạng');
            return;
        }

        if (!passwordPattern.test(newPass)) {
            alert('Mật khẩu phải có ít nhất 8 ký tự, bao gồm cả chữ hoa, chữ thường và số');
            return;
        }

        if (!phonePattern.test(phone)) {
            alert('Số điện thoại không đúng định dạng');
            return;
        }

        // Gửi dữ liệu lên server qua API
        fetch('/api/customer/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                ten: ten,
                ho: ho,
                email: email,
                newPass: newPass,
                soDienThoai: phone
            })
        })
            .then(response => {
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    alert('Đăng ký thành công');
                    window.location.href = '/'; // Chuyển hướng về trang chủ
                } else {
                    alert('Đăng ký thất bại: ' + data.message); // Hiển thị thông báo lỗi từ server
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });

    }

    var signupForm = document.querySelector('#signup form');
    if (signupForm) {
        signupForm.addEventListener('submit', signUp);
    }
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


async function logOut() {
    try {
        const response = await fetch('/logout/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
                // Include any other headers your API requires, such as CSRF or authentication tokens
            },
            // Include any other options your API requires, such as credentials for cookies
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (response.status === 200) {
            alert(data.message);
            // Handle successful logout, such as redirecting to the login page
            location.reload(); // Refresh the page
        } else {
            alert(data.message);
            // Handle unsuccessful logout
        }
    } catch (error) {
        console.error('Error:', error);
        // Handle network errors
    }
}

// Xử lý đăng nhập
document.addEventListener('DOMContentLoaded', function () {
    // Gắn sự kiện này vào form đăng nhập
    document.getElementById('loginForm').addEventListener('submit', function (e) {
        e.preventDefault();

        // Lấy giá trị email và password từ form
        var email = document.getElementById('email').value;
        var password = document.getElementById('password').value;

        // Tạo một đối tượng XMLHttpRequest mới
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/api/login/', true);
        xhr.setRequestHeader('Content-Type', 'application/json');

        // Xử lý kết quả trả về từ server
        xhr.onload = function () {
            if (xhr.status >= 200) {
                // Phân tích cú pháp dữ liệu JSON từ phản hồi
                var data = JSON.parse(xhr.responseText);

                // Kiểm tra trạng thái đăng nhập
                if (data.status === 'success') {
                    // Nếu đăng nhập thành công, tải lại trang
                    window.location.reload();
                } else {
                    // Nếu đăng nhập không thành công, hiển thị thông báo lỗi
                    alert(data.message);
                }
            } else {
                // Hiển thị thông báo lỗi nếu có vấn đề với yêu cầu
                alert('Có lỗi xảy ra trong quá trình đăng nhập.');
            }
        };

        // Gửi yêu cầu đăng nhập với dữ liệu JSON
        xhr.send(JSON.stringify({ email: email, password: password }));
    });
});

// Hàm mở pop-up đổi mật khẩu
function openPasswordChangePopup() {
    document.getElementById('passwordChangePopup').style.display = 'block';
}

// Hàm đóng pop-up đổi mật khẩu
function closePasswordChangePopup() {
    document.getElementById('passwordChangePopup').style.display = 'none';
}

// Hàm mở pop-up sửa số điện thoại
function openPhoneNumberEditPopup() {
    document.getElementById('phoneNumberChangePopup').style.display = 'block';
}

// Hàm đóng pop-up sửa số điện thoại
function closePhoneNumberChangePopup() {
    document.getElementById('phoneNumberChangePopup').style.display = 'none';
}

// Hàm mở pop-up sửa địa chỉ
function openAddressEditPopup() {
    document.getElementById('addressChangePopup').style.display = 'block';
}

// Hàm đóng pop-up sửa địa chỉ
function closeAddressChangePopup() {
    document.getElementById('addressChangePopup').style.display = 'none';
}


// Hàm xử lý sự kiện submit form sửa số điện thoại
function changePhoneNumber(event) {
    event.preventDefault();
    // Xử lý thay đổi số điện thoại ở đây
    //lấy giá trị số điện thoại mới
    const new_phone = document.getElementById('new_phone_number').value;
    //kiểm tra xem số điện thoại có đúng định dạng không
    const phonePattern = /^0\d{9}$/;
    if (!phonePattern.test(new_phone)) {
        alert('Số điện thoại không đúng định dạng');
        return;
    }
    // Gửi dữ liệu lên server qua API
    fetch('/api/change-tel/', {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            phone_number: new_phone
        })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json(); // Chuyển đổi response sang json và trả về để xử lý tiếp
        })
        .then(data => {
            alert(data.message); // Hiển thị thông báo từ server
            closePhoneNumberChangePopup(); // Đóng popup nếu thành công
            // load laij trang
            window.location.reload();
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}



// Hàm mở popup chỉnh sửa địa chỉ
function openAddressEditPopup() {
    loadCities();
    document.getElementById('addressChangePopup').style.display = 'block';
}

// Hàm đóng popup chỉnh sửa địa chỉ
function closeAddressChangePopup() {
    document.getElementById('addressChangePopup').style.display = 'none';
}
//hàm cập nhật tỉnh, thành phố
function loadCities() {
    fetch('http://127.0.0.1:8000/data.json')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            var citySelect = document.getElementById('city');
            citySelect.innerHTML = '<option value="">Vui lòng chọn...</option>' + data.map(city => '<option value="' + city.Id + '">' + city.Name + '</option>').join('');
    
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
}
// Hàm cập nhật quận/huyện dựa vào thành phố/tỉnh đã chọn
function updateDistricts() {
    const cityId = document.getElementById('city').value;
    console.log(cityId);
    fetch(`http://127.0.0.1:8000/data.json?province_id=${cityId}`) // Thay thế URL này bằng URL thực tế của bạn
        .then(response => response.json())
        .then(data => {
            const districtSelect = document.getElementById('district');
            districtSelect.innerHTML = ''; // Xóa các tùy chọn hiện tại
            districtSelect.innerHTML = '<option value="">Vui lòng chọn...</option>'; // Thêm tùy chọn "Vui lòng chọn..."
            
            data.forEach(district => {
                const option = document.createElement('option');
                option.value = district.Id;
                option.textContent = district.Name; // Sử dụng thuộc tính full_name
                districtSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error:', error));
}


// Hàm cập nhật xã/phường dựa vào quận/huyện đã chọn
function updateWards() {
    const districtId = document.getElementById('district').value;
    console.log(districtId);
    fetch(`http://127.0.0.1:8000/data.json?district_id=${districtId}`) // Thay thế `api/wards/${districtId}` bằng URL thực tế của bạn
        .then(response => response.json())
        .then(data => {
            //in ra data
            console.log(data);
            const wardSelect = document.getElementById('ward');
            wardSelect.innerHTML = ''; // Xóa các tùy chọn hiện tại
            wardSelect.innerHTML = '<option value="">Vui lòng chọn...</option>'; // Thêm tùy chọn "Vui lòng chọn..."
            data.forEach(ward => {
                const option = document.createElement('option');
                option.value = ward.Id;
                option.textContent = ward.Name; // Sử dụng thuộc tính name
                wardSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error:', error));
}

//hàm xử lý để xóa tùy chọn mặc định khi người dung dùng nhấp vào select:


// Hàm xử lý sự kiện submit form đổi mật khẩu
function changePassword(event) {
    event.preventDefault(); // Ngăn chặn hành vi submit mặc định của form

    var oldPassword = document.getElementById('old_password').value;
    var newPassword = document.getElementById('new_password').value;
    var confirmPassword = document.getElementById('confirm_password').value;

    // Kiểm tra mật khẩu mới có ít nhất 8 ký tự, bao gồm cả chữ hoa, chữ thường và số
    var passwordPattern = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$/;
    if (!passwordPattern.test(newPassword)) {
        alert('Mật khẩu mới phải có ít nhất 8 ký tự, bao gồm cả chữ hoa, chữ thường và số');
        return;
    }
    //kiểm tra mật khẩu mới và mật khẩu xác nhận có giống nhau không
    if (newPassword !== confirmPassword) {
        alert('Mật khẩu xác nhận không khớp');
        return;
    }

    // Gửi dữ liệu lên server qua API
    fetch('/api/change-password/', {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            old_password: oldPassword,
            new_password: newPassword,
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json(); // Chuyển đổi response sang json và trả về để xử lý tiếp
    })
    .then(data => {
        alert(data.message); // Hiển thị thông báo từ server
        closePasswordChangePopup(); // Đóng popup nếu thành công
        // load laij trang
        window.location.reload();
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

// Hàm xử lý sự kiện submit form sửa địa chỉ
function changeAddress(event) {
    event.preventDefault();
    //lấy phần nội dung được chọn trong các thẻ select
    const citySelect = document.getElementById('city');
    const districtSelect = document.getElementById('district');
    const wardSelect = document.getElementById('ward');
    const new_address = document.getElementById('new_address').value;

    // Kiểm tra xem người dùng có chọn tùy chọn "Vui lòng chọn..." không
    if (citySelect.value === '' || districtSelect.value === '' || wardSelect.value === '') {
        alert('Vui lòng chọn một tùy chọn.');
        return;
    }

    const city = citySelect.options[citySelect.selectedIndex].text;
    const district = districtSelect.options[districtSelect.selectedIndex].text;
    const ward = wardSelect.options[wardSelect.selectedIndex].text;

    //tạo một biến và cộng các giá trị thành một chuỗi
    const address = city + ', ' + district + ', ' + ward + ', ' + new_address;
    console.log(address);
    // Gửi dữ liệu lên server qua API
    fetch('/api/change-address/', {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            address: address
        })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json(); // Chuyển đổi response sang json và trả về để xử lý tiếp
        })
        .then(data => {
            alert(data.message); // Hiển thị thông báo từ server
            closeAddressChangePopup(); // Đóng popup nếu thành công
            // load lại trang
            window.location.reload();
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}
// thay đổi kiểu của trường mật khẩu khi người dùng nhấp vào biểu tượng.
function togglePasswordVisibility(inputId) {
    const passwordInput = document.getElementById(inputId);
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput.setAttribute('type', type);
}