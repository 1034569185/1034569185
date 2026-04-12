<%@ page contentType="text/html;charset=UTF-8" language="java" %>
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
        <h1 class="product-title">全部商品目录</h1>
        <table class="product-table">
            <thead>
            <tr>
                <th>封面</th>
                <th>书名</th>
                <th>作者</th>
                <th>单价</th>
                <th>购买</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td><img src="${pageContext.request.contextPath}/static/images/productImg/0270eba2-2b48-48df-956b-0341204384d9.jpg" alt="书籍1"></td>
                <td class="book-name">Java Web 开发实战</td>
                <td>张三</td>
                <td class="book-price">￥59.00</td>
                <td>
                    <form action="${pageContext.request.contextPath}/Handle-AddCart.jsp" method="post">
                        <input type="hidden" name="id" value="book-001">
                        <input type="hidden" name="name" value="Java Web 开发实战">
                        <input type="hidden" name="author" value="张三">
                        <input type="hidden" name="price" value="59.00">
                        <input type="hidden" name="image" value="/static/images/productImg/0270eba2-2b48-48df-956b-0341204384d9.jpg">
                        <button type="submit" class="buy-btn">加入购物车</button>
                    </form>
                </td>
            </tr>
            <tr>
                <td><img src="${pageContext.request.contextPath}/static/images/productImg/697a23d6-225a-41a3-8c20-7ab624265ecc.png" alt="书籍2"></td>
                <td class="book-name">Spring Boot 企业应用</td>
                <td>李四</td>
                <td class="book-price">￥66.00</td>
                <td>
                    <form action="${pageContext.request.contextPath}/Handle-AddCart.jsp" method="post">
                        <input type="hidden" name="id" value="book-002">
                        <input type="hidden" name="name" value="Spring Boot 企业应用">
                        <input type="hidden" name="author" value="李四">
                        <input type="hidden" name="price" value="66.00">
                        <input type="hidden" name="image" value="/static/images/productImg/697a23d6-225a-41a3-8c20-7ab624265ecc.png">
                        <button type="submit" class="buy-btn">加入购物车</button>
                    </form>
                </td>
            </tr>
            <tr>
                <td><img src="${pageContext.request.contextPath}/static/images/productImg/a2da626c-c72d-4972-83de-cf48405c5563.jpg" alt="书籍3"></td>
                <td class="book-name">数据库系统原理</td>
                <td>王五</td>
                <td class="book-price">￥72.00</td>
                <td>
                    <form action="${pageContext.request.contextPath}/Handle-AddCart.jsp" method="post">
                        <input type="hidden" name="id" value="book-003">
                        <input type="hidden" name="name" value="数据库系统原理">
                        <input type="hidden" name="author" value="王五">
                        <input type="hidden" name="price" value="72.00">
                        <input type="hidden" name="image" value="/static/images/productImg/a2da626c-c72d-4972-83de-cf48405c5563.jpg">
                        <button type="submit" class="buy-btn">加入购物车</button>
                    </form>
                </td>
            </tr>
            <tr>
                <td><img src="${pageContext.request.contextPath}/static/images/productImg/c4ab442f-95c7-4d6f-a57e-3eb7dc6b83c4.jpg" alt="书籍4"></td>
                <td class="book-name">数据结构与算法</td>
                <td>赵六</td>
                <td class="book-price">￥68.00</td>
                <td>
                    <form action="${pageContext.request.contextPath}/Handle-AddCart.jsp" method="post">
                        <input type="hidden" name="id" value="book-004">
                        <input type="hidden" name="name" value="数据结构与算法">
                        <input type="hidden" name="author" value="赵六">
                        <input type="hidden" name="price" value="68.00">
                        <input type="hidden" name="image" value="/static/images/productImg/c4ab442f-95c7-4d6f-a57e-3eb7dc6b83c4.jpg">
                        <button type="submit" class="buy-btn">加入购物车</button>
                    </form>
                </td>
            </tr>
            </tbody>
        </table>
    </main>

    <%@ include file="foot.jsp" %>
</div>
</body>
</html>
