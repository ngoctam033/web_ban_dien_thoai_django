//bạn hãy tạo một hàm themVaoGioHang() nhận vào 1 tham số là name
//hàm này sẽ thêm sản phẩm có tên name vào giỏ hàng
//hàm này sẽ hiển thị thông báo "Đã thêm sản phẩm vào giỏ hàng" bằng alert
function themVaoGioHang(tenSanPham) {
    fetch('/api/add-to-cart/', {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            ten_san_pham: tenSanPham,
        }),
    })
    .then(response => {
        if (!response.ok) {
            if(response.status === 401) {
                // Người dùng chưa đăng nhập
                alert('Bạn chưa đăng nhập.');
            } else {
                // Lỗi khi tạo đơn hàng
                alert(`Không thể tạo đơn hàng. Lỗi: ${response.status}`);
            }
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(json => {
        // Đơn hàng được tạo thành công
        alert('Đã thêm sản phẩm vào giỏ hàng.');
        console.log(json);
        // Cập nhật số lượng sản phẩm trong giỏ hàng trên giao diện
        updateCartCount();

    })
    .catch(e => {
        console.log('Có vấn đề với thao tác fetch: ' + e.message);
    });
}

function updateCartCount() {
    fetch('/api/cart-count/')
    .then(response => response.json())
    .then(data => {
        document.querySelector('.cart-number').textContent = data.count;
    });
}

function tinhTongTien() {
    // Lấy tất cả các checkbox
    var checkboxes = document.getElementsByName('orderProduct');
    
    var total = 0;

    // Lặp qua tất cả các checkbox
    for (var i = 0; i < checkboxes.length; i++) {
        // Nếu checkbox này đã được đánh dấu, thêm giá của sản phẩm tương ứng vào tổng số tiền
        if (checkboxes[i].checked) {
            total += parseFloat(checkboxes[i].dataset.price);
        }
    }

    // Hiển thị tổng số tiền
    document.getElementById('total').textContent = 'Tổng số tiền: ' + total + ' VND';
}

function datHang() {
    // Lấy tất cả các checkbox
    var checkboxes = document.getElementsByName('orderProduct');
    
    // Lưu trữ tên của tất cả các sản phẩm đã chọn
    var selectedProducts = [];

    // Lặp qua tất cả các checkbox
    for (var i = 0; i < checkboxes.length; i++) {
        // Nếu checkbox này đã được đánh dấu, thêm tên của sản phẩm tương ứng vào danh sách
        if (checkboxes[i].checked) {
            selectedProducts.push(checkboxes[i].value);
        }
    }
    // Kiểm tra xem người dùng có chọn sản phẩm nào không
    if (selectedProducts.length === 0) {
        alert('Bạn chưa chọn sản phẩm nào.');
        return;
    }
    //in ra danh sách sản phẩm đã chọn
    console.log(selectedProducts);
    // Gửi danh sách sản phẩm đã chọn tới server
    // Bạn cần thay thế '/path/to/your/api' bằng đường dẫn thực tế tới API của bạn
    fetch('/api/create-order/', {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({'selectedProducts': selectedProducts}),
    })
    .then(response => response.json())
    .then(data => {
        // In ra thông báo alert
        alert(data.message);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function deleteProduct(button, productname) {
    const params = new URLSearchParams({ productName: productname });
    fetch(`/api/delete_product/?${params.toString()}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ 'productName': productname })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Xóa sản phẩm khỏi bảng
            // Lấy hàng chứa nút xóa
            let row = button.parentElement.parentElement;

            // Xóa hàng
            row.remove();
        } else {
            // Hiển thị thông báo lỗi
            alert(data.error);
        }
    });
}