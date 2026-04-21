<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="domain.Product" %>
<%@ page import="java.util.*" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

<%
    Product productBean = new Product();
    List<Product> products = productBean.searchAll();
    request.setAttribute("products", products);
%>

<div class="admin-breadcrumb">
    <a href="${pageContext.request.contextPath}/admin/login/home.jsp?item=product_list">商品管理</a>
    <span> &gt; </span>
    <span>商品列表</span>
</div>

<div class="quick-actions" style="margin-top:12px;">
    <h3 class="qa-title">商品列表</h3>
    <div style="margin-bottom: 12px;">
        <a class="qa-btn" href="${pageContext.request.contextPath}/admin/login/home.jsp?item=product_add">➕ 添加商品</a>
    </div>

    <table border="1" cellspacing="0" cellpadding="8" width="100%" style="background:#fff;border-collapse:collapse;">
        <thead>
        <tr>
            <th>ID</th>
            <th>名称</th>
            <th>价格</th>
            <th>分类</th>
            <th>库存</th>
            <th>图片地址</th>
            <th>描述</th>
        </tr>
        </thead>
        <tbody>
        <c:choose>
            <c:when test="${empty products}">
                <tr><td colspan="7" style="text-align:center;">暂无商品数据</td></tr>
            </c:when>
            <c:otherwise>
                <c:forEach var="p" items="${products}">
                    <tr>
                        <td>${p.id}</td>
                        <td>${p.name}</td>
                        <td>${p.price}</td>
                        <td>${p.category}</td>
                        <td>${p.pnum}</td>
                        <td>${p.imgurl}</td>
                        <td>${p.description}</td>
                    </tr>
                </c:forEach>
            </c:otherwise>
        </c:choose>
        </tbody>
    </table>
</div>
