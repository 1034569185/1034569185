<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="domain.Product" %>
<%@ page import="java.util.List" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%
    Product productBean = new Product();
    List<Product> products = productBean.searchAll();
    request.setAttribute("products", products);
%>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BookStore 网上书城</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/static/css/common.css">
    <link rel="stylesheet" href="${pageContext.request.contextPath}/static/css/index.css">
</head>
<body>

<div class="page-wrapper">

    <%-- 使用 include 指令包含公共头部 --%>
    <%@ include file="head.jsp" %>

    <%-- 使用 include 指令包含搜索菜单 --%>
    <%@ include file="menu_search.jsp" %>

    <!-- ===== 广告轮播区 ===== -->
    <div class="carousel-section">
        <div class="carousel" id="carousel">
            <div class="carousel-track" id="carouselTrack">
                <div class="carousel-slide active">
                    <img src="${pageContext.request.contextPath}/static/images/ad/index_ad0.jpg" alt="广告0">
                </div>
                <div class="carousel-slide">
                    <img src="${pageContext.request.contextPath}/static/images/ad/index_ad1.jpg" alt="广告1">
                </div>
                <div class="carousel-slide">
                    <img src="${pageContext.request.contextPath}/static/images/ad/index_ad2.jpg" alt="广告2">
                </div>
                <div class="carousel-slide">
                    <img src="${pageContext.request.contextPath}/static/images/ad/index_ad3.jpg" alt="广告3">
                </div>
                <div class="carousel-slide">
                    <img src="${pageContext.request.contextPath}/static/images/ad/index_ad4.jpg" alt="广告4">
                </div>
                <div class="carousel-slide">
                    <img src="${pageContext.request.contextPath}/static/images/ad/index_ad5.jpg" alt="广告5">
                </div>
            </div>

            <!-- 左右箭头 -->
            <button class="carousel-btn carousel-prev" id="prevBtn" onclick="carouselPrev()">&#10094;</button>
            <button class="carousel-btn carousel-next" id="nextBtn" onclick="carouselNext()">&#10095;</button>

            <!-- 指示点 -->
            <div class="carousel-dots" id="carouselDots">
                <span class="dot active" onclick="goToSlide(0)"></span>
                <span class="dot" onclick="goToSlide(1)"></span>
                <span class="dot" onclick="goToSlide(2)"></span>
                <span class="dot" onclick="goToSlide(3)"></span>
                <span class="dot" onclick="goToSlide(4)"></span>
                <span class="dot" onclick="goToSlide(5)"></span>
            </div>
        </div>

        <!-- 右侧小广告 -->
        <div class="side-ads">
            <div class="side-ad">
                <img src="${pageContext.request.contextPath}/static/images/ad/myad.jpg" alt="促销活动">
            </div>
            <div class="side-ad">
                <img src="${pageContext.request.contextPath}/static/images/billboard.gif" alt="公告"
                     onerror="this.parentElement.style.background='#f0f4ff'">
            </div>
        </div>
    </div>

    <!-- ===== 主内容区 ===== -->
    <div class="main-section">

        <!-- 热门新书 -->
        <section class="book-section">
            <div class="section-title">
                <img src="${pageContext.request.contextPath}/static/images/hottitle.gif" alt="热门新书"
                     onerror="this.outerHTML='<h2>🔥 热门新书</h2>'">
            </div>
            <div class="book-grid">
                <c:choose>
                    <c:when test="${empty products}">
                        <!-- 占位书目（无数据时展示） -->
                        <c:forEach var="i" begin="1" end="6">
                            <div class="book-card">
                                <div class="book-cover">
                                    <img src="${pageContext.request.contextPath}/static/images/icon${i <= 3 ? i : (i-3)}.png"
                                         alt="书籍封面"
                                         onerror="this.src='${pageContext.request.contextPath}/static/images/logo.jpg'">
                                </div>
                                <div class="book-info">
                                    <p class="book-title">示例书目 ${i}</p>
                                    <p class="book-author">作者：示例作者</p>
                                    <p class="book-price">¥<span>39.00</span></p>
                                </div>
                                <div class="book-actions">
                                    <a href="#" class="btn-buy">
                                        <img src="${pageContext.request.contextPath}/static/images/buy.gif"
                                             alt="购买"
                                             onerror="this.outerHTML='<span>立即购买</span>'">
                                    </a>
                                    <a href="#" class="btn-cart">
                                        <img src="${pageContext.request.contextPath}/static/images/gwc_buy.gif"
                                             alt="加入购物车"
                                             onerror="this.outerHTML='<span>加入购物车</span>'">
                                    </a>
                                </div>
                            </div>
                        </c:forEach>
                    </c:when>
                    <c:otherwise>
                        <c:forEach var="p" items="${products}" varStatus="status">
                            <c:if test="${status.index < 6}">
                                <c:set var="imgUrl" value="${empty p.imgurl ? '/static/images/logo.jpg' : p.imgurl}" />
                                <div class="book-card">
                                    <div class="book-cover">
                                        <img src="${pageContext.request.contextPath}${imgUrl}"
                                             alt="${p.name}"
                                             onerror="this.src='${pageContext.request.contextPath}/static/images/logo.jpg'">
                                    </div>
                                    <div class="book-info">
                                        <p class="book-title">${p.name}</p>
                                        <p class="book-author">分类：${p.category}</p>
                                        <p class="book-price">¥<span>${p.price}</span></p>
                                    </div>
                                    <div class="book-actions">
                                        <a href="${pageContext.request.contextPath}/ProductList" class="btn-buy">
                                            <img src="${pageContext.request.contextPath}/static/images/buy.gif"
                                                 alt="购买"
                                                 onerror="this.outerHTML='<span>查看详情</span>'">
                                        </a>
                                        <a href="${pageContext.request.contextPath}/ProductList" class="btn-cart">
                                            <img src="${pageContext.request.contextPath}/static/images/gwc_buy.gif"
                                                 alt="加入购物车"
                                                 onerror="this.outerHTML='<span>加入购物车</span>'">
                                        </a>
                                    </div>
                                </div>
                            </c:if>
                        </c:forEach>
                    </c:otherwise>
                </c:choose>
            </div>
        </section>

        <!-- 侧边栏 -->
        <aside class="sidebar">
            <div class="sidebar-block">
                <div class="sidebar-title">公告栏</div>
                <ul class="notice-list">
                    <li><a href="#">📢 双十一优惠活动开始啦！</a></li>
                    <li><a href="#">📦 配送时效说明</a></li>
                    <li><a href="#">🎁 新用户注册即享优惠</a></li>
                    <li><a href="#">📚 新书上架：计算机专区</a></li>
                </ul>
            </div>
            <div class="sidebar-block">
                <div class="sidebar-title">快速入口</div>
                <div class="quick-links">
                    <a href="${pageContext.request.contextPath}/user/register" class="quick-link">
                        <img src="${pageContext.request.contextPath}/static/images/signup.gif"
                             alt="注册"
                             onerror="this.outerHTML='📝 注册'">
                    </a>
                    <a href="${pageContext.request.contextPath}/user/login" class="quick-link">
                        <img src="${pageContext.request.contextPath}/static/images/loginbutton.gif"
                             alt="登录"
                             onerror="this.outerHTML='🔑 登录'">
                    </a>
                    <a href="${pageContext.request.contextPath}/Cart" class="quick-link">
                        <img src="${pageContext.request.contextPath}/static/images/cart.gif"
                             alt="购物车"
                             onerror="this.outerHTML='🛒 购物车'">
                    </a>
                </div>
            </div>
        </aside>
    </div>

    <%-- 使用 include 指令包含公共页脚 --%>
    <%@ include file="foot.jsp" %>

</div><!-- end .page-wrapper -->

<script>
/* ====================================================
   广告轮播 JavaScript
   ==================================================== */
var currentSlide = 0;
var totalSlides  = 6;
var autoTimer    = null;

function goToSlide(index) {
    var slides = document.querySelectorAll('.carousel-slide');
    var dots   = document.querySelectorAll('.dot');

    slides[currentSlide].classList.remove('active');
    dots[currentSlide].classList.remove('active');

    currentSlide = (index + totalSlides) % totalSlides;

    slides[currentSlide].classList.add('active');
    dots[currentSlide].classList.add('active');
}

function carouselNext() {
    goToSlide(currentSlide + 1);
    resetAutoPlay();
}

function carouselPrev() {
    goToSlide(currentSlide - 1);
    resetAutoPlay();
}

function startAutoPlay() {
    autoTimer = setInterval(function () {
        goToSlide(currentSlide + 1);
    }, 4000);
}

function resetAutoPlay() {
    clearInterval(autoTimer);
    startAutoPlay();
}

// 页面加载后自动播放
window.addEventListener('DOMContentLoaded', function () {
    startAutoPlay();

    // 鼠标悬停暂停，离开继续
    var carousel = document.getElementById('carousel');
    if (carousel) {
        carousel.addEventListener('mouseenter', function () { clearInterval(autoTimer); });
        carousel.addEventListener('mouseleave', startAutoPlay);
    }
});
</script>
</body>
</html>
