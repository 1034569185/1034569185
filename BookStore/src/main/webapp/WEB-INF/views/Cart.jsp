<%@ page import="java.util.ArrayList" %>
<%@ page import="java.util.List" %>
<%@ page import="java.util.Map" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%
    List<Map<String, Object>> cart = (List<Map<String, Object>>) session.getAttribute("cart");
    if (cart == null) {
        cart = new ArrayList<>();
        session.setAttribute("cart", cart);
    }
%>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>我的购物车 - BookStore</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/static/css/common.css">
    <style>
        .cart-page { max-width: 1100px; margin: 18px auto 24px; padding: 0 16px; }
        .cart-title { font-size: 24px; margin-bottom: 12px; color: #1e293b; }
        .cart-actions { display: flex; justify-content: space-between; margin-bottom: 10px; }
        .text-link { color: #1d4ed8; font-size: 14px; }
        .danger-link { color: #dc2626; font-size: 14px; }
        .cart-table { width: 100%; border-collapse: collapse; background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 16px rgba(0,0,0,.08); }
        .cart-table th, .cart-table td { padding: 12px 10px; border-bottom: 1px solid #e2e8f0; text-align: center; font-size: 14px; }
        .cart-table th { background: #0f766e; color: #fff; font-weight: 600; }
        .cart-table img { width: 60px; height: 80px; object-fit: cover; border-radius: 4px; border: 1px solid #e2e8f0; }
        .book-name { text-align: left; font-weight: 600; color: #334155; }
        .price { color: #dc2626; font-weight: 700; }
        .empty { background: #fff; border: 1px dashed #cbd5e1; border-radius: 8px; padding: 40px 16px; text-align: center; color: #64748b; }
        .checkout-box { margin-top: 12px; display: flex; justify-content: flex-end; gap: 16px; align-items: center; }
        .total { font-size: 18px; color: #1e293b; }
        .total span { color: #dc2626; font-weight: 700; }
        .pay-btn { border: 0; background: #2563eb; color: #fff; padding: 10px 20px; border-radius: 6px; cursor: pointer; }
    </style>
</head>
<body>
<div class="page-wrapper">
    <%@ include file="head.jsp" %>
    <%@ include file="menu_search.jsp" %>

    <main class="cart-page">
        <h1 class="cart-title">我的购物车</h1>
        <div class="cart-actions">
            <a class="text-link" href="${pageContext.request.contextPath}/ProductList.jsp">继续购物</a>
            <a class="danger-link" href="${pageContext.request.contextPath}/DeleteCart.jsp?clear=true"
               onclick="return confirm('确定清空购物车吗？');">清空购物车</a>
        </div>

        <%
            if (cart.isEmpty()) {
        %>
        <div class="empty">购物车为空，快去 <a class="text-link" href="${pageContext.request.contextPath}/ProductList.jsp">商品目录</a> 选购吧。</div>
        <%
            } else {
                double total = 0.0;
        %>
        <table class="cart-table">
            <thead>
            <tr>
                <th>封面</th>
                <th>书名</th>
                <th>作者</th>
                <th>单价</th>
                <th>数量</th>
                <th>小计</th>
                <th>操作</th>
            </tr>
            </thead>
            <tbody>
            <%
                for (Map<String, Object> item : cart) {
                    String id = String.valueOf(item.get("id"));
                    String name = String.valueOf(item.get("name"));
                    String author = String.valueOf(item.get("author"));
                    String image = String.valueOf(item.get("image"));
                    Double price = (Double) item.get("price");
                    Integer quantity = (Integer) item.get("quantity");
                    double subTotal = price * quantity;
                    total += subTotal;
            %>
            <tr>
                <td><img src="${pageContext.request.contextPath}<%= image %>" alt="<%= name %>"></td>
                <td class="book-name"><%= name %></td>
                <td><%= author %></td>
                <td class="price">￥<%= String.format("%.2f", price) %></td>
                <td><%= quantity %></td>
                <td class="price">￥<%= String.format("%.2f", subTotal) %></td>
                <td>
                    <a class="danger-link" href="${pageContext.request.contextPath}/DeleteCart.jsp?id=<%= id %>"
                       onclick="return confirm('确定删除该商品吗？');">删除</a>
                </td>
            </tr>
            <%
                }
            %>
            </tbody>
        </table>
        <div class="checkout-box">
            <div class="total">总计：<span>￥<%= String.format("%.2f", total) %></span></div>
            <button class="pay-btn" type="button">去结算</button>
        </div>
        <%
            }
        %>
    </main>

    <%@ include file="foot.jsp" %>
</div>
</body>
</html>
