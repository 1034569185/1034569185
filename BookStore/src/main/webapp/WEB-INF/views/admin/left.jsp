<%-- admin/left.jsp – 后台管理左侧菜单片段 --%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<div class="admin-left">
    <div class="admin-menu-header">
        <img src="${pageContext.request.contextPath}/static/images--admin/images/mis_05a.jpg"
             alt="" class="menu-header-img"
             onerror="this.style.display='none'">
        <span>管理菜单</span>
    </div>

    <nav class="admin-nav">

        <!-- 欢迎 / 首页 -->
        <div class="admin-nav-group">
            <div class="admin-nav-title">🏠 系统首页</div>
            <ul class="admin-nav-list">
                <li><a href="${pageContext.request.contextPath}/admin/welcome" class="admin-nav-link">控制面板</a></li>
            </ul>
        </div>

        <!-- 图书管理 -->
        <div class="admin-nav-group">
            <div class="admin-nav-title">📚 图书管理</div>
            <ul class="admin-nav-list">
                <li><a href="${pageContext.request.contextPath}/admin/book/list"   class="admin-nav-link">图书列表</a></li>
                <li><a href="${pageContext.request.contextPath}/admin/book/add"    class="admin-nav-link">添加图书</a></li>
                <li><a href="${pageContext.request.contextPath}/admin/book/category" class="admin-nav-link">分类管理</a></li>
                <li><a href="${pageContext.request.contextPath}/admin/login/home.jsp?item=product_list" class="admin-nav-link">商品管理(实验11)</a></li>
            </ul>
        </div>

        <!-- 用户管理 -->
        <div class="admin-nav-group">
            <div class="admin-nav-title">👥 用户管理</div>
            <ul class="admin-nav-list">
                <li><a href="${pageContext.request.contextPath}/admin/user/list"   class="admin-nav-link">用户列表</a></li>
            </ul>
        </div>

        <!-- 订单管理 -->
        <div class="admin-nav-group">
            <div class="admin-nav-title">📦 订单管理</div>
            <ul class="admin-nav-list">
                <li><a href="${pageContext.request.contextPath}/admin/order/list"   class="admin-nav-link">订单列表</a></li>
                <li><a href="${pageContext.request.contextPath}/admin/order/pending" class="admin-nav-link">待处理订单</a></li>
            </ul>
        </div>

        <!-- 系统设置 -->
        <div class="admin-nav-group">
            <div class="admin-nav-title">⚙️ 系统设置</div>
            <ul class="admin-nav-list">
                <li><a href="${pageContext.request.contextPath}/admin/settings" class="admin-nav-link">基本设置</a></li>
                <li><a href="${pageContext.request.contextPath}/admin/notice"   class="admin-nav-link">公告管理</a></li>
            </ul>
        </div>

    </nav>

    <div class="admin-menu-footer">
        <img src="${pageContext.request.contextPath}/static/images--admin/images/mis_05b.jpg"
             alt="" onerror="this.style.display='none'">
    </div>
</div>
