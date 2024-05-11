function loadMoreProducts(url) {
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(products => {
            const productsContainer = document.getElementById('products');
            if (products.error === 'NoMoreProduct') {
                document.getElementById('loadMore').style.display = 'none';
            }
            else if (products.length == 0) {
                productsContainer.innerHTML = `
                <div id="khongCoSanPham">
                    <i class="fas fa-times-circle"></i>
                    Không có sản phẩm nào
                    <br/>
                    <a href="/">Quay lại trang chủ</a>
                </div>
            `;
            }
            else {
                products.forEach(product => {
                    const productElement = document.createElement('li');
                    productElement.className = 'sanPham';
                    productElement.innerHTML = `
                <a href="product-detail/${product.name}">
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
}
// kích hoạt owl carousel
$(document).ready(function () {
    var owl = $('.owl-carousel');
    owl.owlCarousel({
        items: 1.5,
        margin: 100,
        center: true,
        loop: true,
        smartSpeed: 450,
        autoplay: true,
        autoplayTimeout: 3500
    });
});