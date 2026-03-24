<%-- admin/top.jsp – 后台管理顶部导航片段 --%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<div class="admin-top">
    <!-- Logo / 系统名称 -->
    <div class="admin-top-logo">
        <img src="${pageContext.request.contextPath}/static/images--admin/images/mis_01.jpg"
             alt="后台管理系统"
             onerror="this.style.display='none'">
        <span class="admin-sys-title">BookStore 后台管理系统</span>
    </div>

    <!-- 右侧用户信息 -->
    <div class="admin-top-user">
        <c:choose>
            <c:when test="${not empty sessionScope.loginUser}">
                <span class="admin-username">管理员：${sessionScope.loginUser.username}</span>
            </c:when>
            <c:otherwise>
                <span class="admin-username">管理员</span>
            </c:otherwise>
        </c:choose>
        <span class="admin-sep">|</span>
        <a href="${pageContext.request.contextPath}/" class="admin-top-link">前台首页</a>
        <span class="admin-sep">|</span>
        <a href="${pageContext.request.contextPath}/user/logout" class="admin-top-link">安全退出</a>
    </div>
</div>
