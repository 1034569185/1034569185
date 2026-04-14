<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>登录成功 - BookStore</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/static/css/common.css">
</head>
<body>
<div class="page-wrapper">
    <%@ include file="head.jsp" %>
    <%@ include file="menu_search.jsp" %>
    <main style="max-width:900px;margin:24px auto;padding:20px;background:#fff;border-radius:8px;">
        <h2>登录成功</h2>
        <p>欢迎回来，<strong>${sessionScope.loginUser.username}</strong>。</p>
        <p>
            <a href="${pageContext.request.contextPath}/">进入首页</a>
            &nbsp;|&nbsp;
            <a href="${pageContext.request.contextPath}/Cart">查看购物车</a>
        </p>
    </main>
    <%@ include file="foot.jsp" %>
</div>
</body>
</html>
