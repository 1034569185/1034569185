<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>后台管理 - BookStore</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/static/css/admin.css">
</head>
<body>

<div class="admin-wrapper">

    <%-- 使用 include 指令包含顶部 --%>
    <%@ include file="top.jsp" %>

    <div class="admin-body">

        <%-- 使用 include 指令包含左侧菜单 --%>
        <%@ include file="left.jsp" %>

        <!-- 主内容区 -->
        <main class="admin-main">
            <div class="admin-breadcrumb">
                <a href="${pageContext.request.contextPath}/admin/welcome">首页</a>
                <span> &gt; </span>
                <span>控制面板</span>
            </div>

            <!-- 欢迎横幅 -->
            <div class="welcome-banner">
                <img src="${pageContext.request.contextPath}/static/images--admin/images/mis_05c.jpg"
                     alt="欢迎" class="welcome-img"
                     onerror="this.style.display='none'">
                <div class="welcome-text">
                    <h2>欢迎使用 BookStore 后台管理系统</h2>
                    <p>
                        <c:choose>
                            <c:when test="${not empty sessionScope.loginUser}">
                                ${sessionScope.loginUser.username}，您好！今天是
                            </c:when>
                            <c:otherwise>
                                管理员，您好！今天是
                            </c:otherwise>
                        </c:choose>
                        <strong id="todayDate"></strong>
                    </p>
                </div>
            </div>

            <!-- 数据概览卡片 -->
            <div class="stat-cards">
                <div class="stat-card">
                    <div class="stat-icon">📚</div>
                    <div class="stat-info">
                        <p class="stat-num" id="bookCount">--</p>
                        <p class="stat-label">图书总数</p>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">👥</div>
                    <div class="stat-info">
                        <p class="stat-num" id="userCount">--</p>
                        <p class="stat-label">注册用户</p>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">📦</div>
                    <div class="stat-info">
                        <p class="stat-num" id="orderCount">--</p>
                        <p class="stat-label">累计订单</p>
                    </div>
                </div>
                <div class="stat-card stat-card-warn">
                    <div class="stat-icon">⏳</div>
                    <div class="stat-info">
                        <p class="stat-num" id="pendingCount">--</p>
                        <p class="stat-label">待处理订单</p>
                    </div>
                </div>
            </div>

            <!-- 快捷操作 -->
            <div class="quick-actions">
                <h3 class="qa-title">快捷操作</h3>
                <div class="qa-grid">
                    <a href="${pageContext.request.contextPath}/admin/book/add" class="qa-btn">
                        <span class="qa-icon">➕</span>添加图书
                    </a>
                    <a href="${pageContext.request.contextPath}/admin/book/list" class="qa-btn">
                        <span class="qa-icon">📋</span>图书列表
                    </a>
                    <a href="${pageContext.request.contextPath}/admin/order/list" class="qa-btn">
                        <span class="qa-icon">📦</span>查看订单
                    </a>
                    <a href="${pageContext.request.contextPath}/admin/user/list" class="qa-btn">
                        <span class="qa-icon">👤</span>用户管理
                    </a>
                    <a href="${pageContext.request.contextPath}/admin/notice" class="qa-btn">
                        <span class="qa-icon">📢</span>发布公告
                    </a>
                    <a href="${pageContext.request.contextPath}/" class="qa-btn">
                        <span class="qa-icon">🏠</span>前台首页
                    </a>
                </div>
            </div>

        </main>
    </div><!-- end .admin-body -->

    <%-- 使用 include 指令包含底部 --%>
    <%@ include file="bottom.jsp" %>

</div><!-- end .admin-wrapper -->

<script>
// 显示今日日期
document.getElementById('todayDate').textContent = new Date().toLocaleDateString('zh-CN', {
    year: 'numeric', month: 'long', day: 'numeric', weekday: 'long'
});

// 后续可通过 AJAX 从 /admin/api/stats 获取真实数据
// 此处暂用占位数值
document.getElementById('bookCount').textContent   = '0';
document.getElementById('userCount').textContent   = '0';
document.getElementById('orderCount').textContent  = '0';
document.getElementById('pendingCount').textContent = '0';
</script>
</body>
</html>
