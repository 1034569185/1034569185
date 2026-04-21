<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>后台管理首页 - 商品管理</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/static/css/admin.css">
</head>
<body>
<div class="admin-wrapper">
    <%@ include file="../top.jsp" %>
    <div class="admin-body">
        <%@ include file="left.jsp" %>
        <main class="admin-main">
            <%
                String item = request.getParameter("item");
                if ("product_list".equals(item)) {
            %>
            <%@ include file="../products/list.jsp" %>
            <%
                } else if ("product_add".equals(item)) {
            %>
            <%@ include file="../products/add.jsp" %>
            <%
                } else {
            %>
            <h2>商品管理模块</h2>
            <p>请选择左侧菜单进入商品列表或添加商品。</p>
            <%
                }
            %>
        </main>
    </div>
    <%@ include file="../bottom.jsp" %>
</div>
</body>
</html>
