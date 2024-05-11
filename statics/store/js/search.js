//hàm này dùng để hiển thị sản phẩm tìm được
async function displayProducts(keyword) {
    if(keyword == 'Apple'){keyword = 'iphone';}
    const response = await fetch('/api/search/?keyword='+ keyword)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(products => {
        const productsContainer = document.getElementById('products');
        productsContainer.innerHTML = '';
        if(products.error === 'NoMoreProduct'){
            document.getElementById('loadMore').style.display = 'none';
        }
        else if(products.length == 0){
            productsContainer.innerHTML = `
            <p style="font-size: 20px; color: red; font-weight: bold; text-align: center;">
              Không có sản phẩm nào! <span style="color: blue;"><a href="/">Quay lại trang chủ</a></span>
            </p>
            `;
        }
        else{
        // Xóa nội dung hiện tại của productContainer
        
        products.forEach(product => {
            const productElement = document.createElement('li');
            productElement.className = 'sanPham';
            productElement.innerHTML = `
                    <a href="/product-detail/${product.name}">
                    <img src="${product.image}" alt="">
                    <h3>${product.name}</h3>
                    <div class="price">
                        <strong>${Math.floor(product.price).toLocaleString('vi-VN')}₫</strong>
                    </div>
                    <div class="ratingresult">
                        <i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="far fa-star"></i><span>đánh giá</span>
                    </div>
                    <label class="tragop">
                        Trả góp 0%
                    </label>
                    <div class="tooltip">
                        <button class="themvaogio" onclick="themVaoGioHang('${product.name}'); return false;">
                            <span class="tooltiptext" style="font-size: 15px;">Thêm vào giỏ</span>
                            +
                        </button>
                    </div>
                </a>
            `;
            productsContainer.appendChild(productElement);
        });
        
    }
    })
    .catch(error => console.error('Error:', error));
    document.getElementById('loadMore').style.display = 'none';
}

//hàm này dùng để tìm kiếm
async function search(keyword) {
    try {
        const response = await fetch('/api/search/?keyword='+ keyword);
        const products = await response.json();

        const searchBoxAutocompleteList = document.getElementById('search-boxautocomplete-list');
        searchBoxAutocompleteList.innerHTML = '';
        if(!keyword){
            searchBoxAutocompleteList.innerHTML = '';
            return;
        }
        products.forEach(product => {
            searchBoxAutocompleteList.innerHTML += `
                <div>
                    <a href="/product-detail/${product.name}">
                        ${product.name.replace(new RegExp(`(${keyword})`, 'gi'), '<strong>$1</strong>')}
                    </a>
                </div>
            `;
        });

        document.getElementById('loadMore').style.display = 'none';
    } catch (error) {
        console.error('Error:', error);
    }
}
//hàm này dùng để input
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('search-box').addEventListener('input', function() {
        const keyword = this.value;
        search(keyword);
    });
});

//tạo hàm để lọc sản phẩm
