<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="domain.Product" %>
<%@ page import="java.util.*" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%
    if (request.getAttribute("products") == null) {
        Product productBean = new Product();
        List<Product> products = productBean.searchAll();
        request.setAttribute("products", products);
    }
%>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>全部商品目录 - BookStore</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/static/css/common.css">
    <style>
        .product-page { max-width: 1100px; margin: 18px auto 24px; padding: 0 16px; }
        .product-title { font-size: 24px; margin-bottom: 12px; color: #1e293b; }
        .product-table { width: 100%; border-collapse: collapse; background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 16px rgba(0,0,0,.08); }
        .product-table th, .product-table td { padding: 12px 10px; border-bottom: 1px solid #e2e8f0; text-align: center; font-size: 14px; }
        .product-table th { background: #2563eb; color: #fff; font-weight: 600; }
        .product-table img { width: 74px; height: 96px; object-fit: cover; border-radius: 4px; border: 1px solid #e2e8f0; }
        .book-name { text-align: left; font-weight: 600; color: #334155; }
        .book-price { color: #dc2626; font-weight: 700; }
        .buy-btn { border: 0; background: #2563eb; color: #fff; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-size: 14px; }
        .buy-btn:hover { background: #1d4ed8; }
    </style>
</head>
<body>
<div class="page-wrapper">
    <%@ include file="head.jsp" %>
    <%@ include file="menu_search.jsp" %>

    <main class="product-page">
        <c:set var="keyword" value="${requestScope.keyword}" />
        <c:set var="category" value="${requestScope.category}" />
        <h1 class="product-title">
            <c:choose>
                <c:when test="${not empty keyword || not empty category}">搜索结果</c:when>
                <c:otherwise>全部商品目录</c:otherwise>
            </c:choose>
        </h1>
        <table class="product-table">
            <thead>
            <tr>
                <th>封面</th>
                <th>书名</th>
                <th>分类</th>
                <th>单价</th>
                <th>购买</th>
            </tr>
            </thead>
            <tbody>
            <c:choose>
                <c:when test="${empty products}">
                    <tr>
                        <td colspan="5" style="text-align:center;padding:24px;color:#64748b;">暂无匹配商品</td>
                    </tr>
                </c:when>
                <c:otherwise>
                    <c:forEach var="p" items="${products}">
                        <c:set var="imgUrl" value="${empty p.imgurl ? '/static/images/logo.jpg' : p.imgurl}" />
                        <tr>
                            <td><img src="${pageContext.request.contextPath}${imgUrl}" alt="${p.name}"></td>
                            <td class="book-name">${p.name}</td>
                            <td>${p.category}</td>
                            <td class="book-price">￥${p.price}</td>
                            <td>
                                <form action="${pageContext.request.contextPath}/Handle-AddCart" method="get">
                                    <input type="hidden" name="id" value="${p.id}">
                                    <input type="hidden" name="name" value="${p.name}">
                                    <input type="hidden" name="author" value="${p.category}">
                                    <input type="hidden" name="price" value="${p.price}">
                                    <input type="hidden" name="image" value="${imgUrl}">
                                    <button type="submit" class="buy-btn">加入购物车</button>
                                </form>
                            </td>
                        </tr>
                    </c:forEach>
                </c:otherwise>
            </c:choose>
            </tbody>
        </table>
    </main>

    <%@ include file="foot.jsp" %>
</div>
</body>
</html>
