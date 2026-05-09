<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>操作失败 - BookStore</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/static/css/common.css">
</head>
<body>
<div class="page-wrapper">
    <%@ include file="head.jsp" %>
    <%@ include file="menu_search.jsp" %>
    <main style="max-width:900px;margin:24px auto;padding:20px;background:#fff;border-radius:8px;">
        <h2>操作失败</h2>
        <p style="color:#dc2626;">${empty param.message ? "用户名或密码错误，请重试。" : param.message}</p>
        <p>
            <a href="${pageContext.request.contextPath}/user/login">返回登录</a>
            &nbsp;|&nbsp;
            <a href="${pageContext.request.contextPath}/user/register">返回注册</a>
        </p>
    </main>
    <%@ include file="foot.jsp" %>
</div>
</body>
</html>
