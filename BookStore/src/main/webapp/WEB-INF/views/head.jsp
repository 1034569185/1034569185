<%-- head.jsp – 公共头部片段（通过 <%@ include %> 静态包含） --%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<header class="site-header">
    <div class="header-inner">
        <!-- Logo -->
        <a href="${pageContext.request.contextPath}/" class="logo">
            <img src="${pageContext.request.contextPath}/static/images/logo.jpg"
                 alt="BookStore Logo" class="logo-img"
                 onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
            <span class="logo-fallback">
                <span class="logo-icon">📚</span>
                <span class="logo-text">BookStore</span>
            </span>
        </a>

        <!-- 右侧用户信息 & 购物车 -->
        <div class="header-right">
            <c:choose>
                <c:when test="${not empty sessionScope.loginUser}">
                    <span class="header-user">你好，${sessionScope.loginUser.username}</span>
                    <a href="${pageContext.request.contextPath}/user/logout" class="header-btn">退出</a>
                </c:when>
                <c:otherwise>
                    <a href="${pageContext.request.contextPath}/user/login" class="header-btn">登录</a>
                    <a href="${pageContext.request.contextPath}/user/register" class="header-btn header-btn-primary">注册</a>
                </c:otherwise>
            </c:choose>
            <a href="${pageContext.request.contextPath}/cart" class="header-cart" title="购物车">
                🛒 <span class="cart-count">0</span>
            </a>
        </div>
    </div>
</header>
