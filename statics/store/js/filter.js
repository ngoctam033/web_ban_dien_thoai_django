window.history.pushState({}, document.title, window.location.pathname);
// Hàm xử lý sự kiện click trên một thẻ <a>
function handleLinkClick(link) {
    link.addEventListener('click', function(event) {
        event.preventDefault(); // Ngăn chặn hành vi mặc định của thẻ <a>
        var content = this.textContent; // Lấy nội dung văn bản của thẻ <a>
        var buttonId = this.parentNode.id; // Lấy id của phần tử cha
        var container = document.querySelector('.choosedFilter.flexContain'); // Lấy phần tử container
        var existingLink = container.querySelector('a[data-button-id="' + buttonId + '"]'); // Tìm thẻ <a> hiện có
        var newLink = createOrUpdateLink(existingLink, content, buttonId, container); // Tạo hoặc cập nhật thẻ <a>
        handleCloseIconClick(newLink, container); // Xử lý sự kiện click trên biểu tượng đóng
        updateQueryParams(this, newLink); // Cập nhật tham số truy vấn
    });
}

// Hàm tạo hoặc cập nhật thẻ <a>
function createOrUpdateLink(existingLink, content, buttonId, container) {
    var newLink;
    if (existingLink) { // Nếu thẻ <a> hiện có tồn tại
        existingLink.innerHTML = '<h3>' + content + ' <i class="fas fa-times"></i></h3>'; // Cập nhật nội dung HTML
        newLink = existingLink; // Gán newLink bằng thẻ <a> hiện có
    } else { // Nếu thẻ <a> hiện có không tồn tại
        newLink = document.createElement('a'); // Tạo một thẻ <a> mới
        newLink.innerHTML = '<h3>' + content + ' <i class="fas fa-times"></i></h3>'; // Cập nhật nội dung HTML
        newLink.setAttribute('data-button-id', buttonId); // Thêm thuộc tính data-button-id
        container.appendChild(newLink); // Thêm thẻ <a> mới vào container
    }
    return newLink; // Trả về thẻ <a> mới hoặc đã được cập nhật
}

// Hàm xử lý sự kiện click trên biểu tượng đóng
function handleCloseIconClick(newLink, container) {
    newLink.querySelector('i.fas.fa-times').addEventListener('click', function(event) {
        event.stopPropagation(); // Ngăn chặn sự kiện lan truyền
        container.removeChild(newLink); // Xóa thẻ <a> khỏi container
        var url = new URL(window.location.href); // Lấy URL hiện tại
        var params = new URLSearchParams(url.search); // Lấy các tham số truy vấn từ URL
        var attributes = newLink.attributes; // Lấy các thuộc tính của thẻ <a>
        for (var i = 0; i < attributes.length; i++) { // Duyệt qua tất cả các thuộc tính
            var attr = attributes[i];
            if (attr.name.startsWith('data-') || attr.name.endsWith('-filter')) { // Nếu tên thuộc tính bắt đầu bằng 'data-' hoặc kết thúc bằng '-filter'
                params.delete(attr.name); // Xóa tham số truy vấn tương ứng
            }
        }
        url.search = params.toString(); // Cập nhật tham số truy vấn trong URL
        window.history.pushState({}, '', url.toString()); // Cập nhật URL trong lịch sử duyệt web
    });
}

// Hàm cập nhật tham số truy vấn
function updateQueryParams(clickedLink, newLink) {
    var attributes = clickedLink.attributes; // Lấy các thuộc tính của thẻ <a> đã được click
    for (var i = 0; i < attributes.length; i++) { // Duyệt qua tất cả các thuộc tính
        var attr = attributes[i];
        newLink.setAttribute(attr.name, attr.value); // Thêm hoặc cập nhật thuộc tính trong thẻ <a> mới
    }
    var url = new URL(window.location.href); // Lấy URL hiện tại
    var params = new URLSearchParams(url.search); // Lấy các tham số truy vấn từ URL
    for (var i = 0; i < attributes.length; i++) { // Duyệt qua tất cả các thuộc tính
        var attr = attributes[i];
        if (attr.name.startsWith('data-') || attr.name.endsWith('-filter')) { // Nếu tên thuộc tính bắt đầu bằng 'data-' hoặc kết thúc bằng '-filter'
            params.set(attr.name, attr.value); // Thêm hoặc cập nhật tham số truy vấn tương ứng
        }
    }
    url.search = params.toString(); // Cập nhật tham số truy vấn trong URL
    window.history.pushState({}, '', url.toString()); // Cập nhật URL trong lịch sử duyệt web
}

/// Duyệt qua tất cả các thẻ <a> trong .flexContain .dropdown-content và thêm sự kiện click
document.querySelectorAll('.flexContain .dropdown-content a').forEach(handleLinkClick);