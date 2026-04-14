<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>用户登录 - BookStore</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/static/css/common.css">
</head>
<body>
<div class="page-wrapper">
    <%@ include file="head.jsp" %>
    <%@ include file="menu_search.jsp" %>
    <main style="max-width:900px;margin:24px auto;padding:20px;background:#fff;border-radius:8px;">
        <h2>用户登录</h2>
        <form action="${pageContext.request.contextPath}/Handle-login" method="post">
            <input type="hidden" name="${_csrf.parameterName}" value="${_csrf.token}"/>
            <p>
                <label>用户名：</label>
                <input type="text" name="username" required maxlength="20">
            </p>
            <p>
                <label>密码：</label>
                <input type="password" name="password" required maxlength="50">
            </p>
            <p>
                <button type="submit">登录</button>
                <a href="${pageContext.request.contextPath}/user/register" style="margin-left:12px;">去注册</a>
            </p>
        </form>
    </main>
    <%@ include file="foot.jsp" %>
</div>
</body>
</html>
