<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>注册成功 - BookStore</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/static/css/common.css">
</head>
<body>
<div class="page-wrapper">
    <%@ include file="head.jsp" %>
    <%@ include file="menu_search.jsp" %>
    <main style="max-width:900px;margin:24px auto;padding:20px;background:#fff;border-radius:8px;">
        <h2>注册成功</h2>
        <p>欢迎你，<strong>${param.username}</strong>。</p>
        <p>你的账号已创建完成，请继续登录。</p>
        <p>
            <a href="${pageContext.request.contextPath}/user/login">去登录</a>
            &nbsp;|&nbsp;
            <a href="${pageContext.request.contextPath}/">返回首页</a>
        </p>
    </main>
    <%@ include file="foot.jsp" %>
</div>
</body>
</html>
