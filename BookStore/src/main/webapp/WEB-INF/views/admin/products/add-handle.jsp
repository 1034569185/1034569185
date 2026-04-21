<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="domain.Product" %>
<jsp:useBean id="product" class="domain.Product" scope="page"/>
<jsp:setProperty name="product" property="*"/>
<%
    Product helper = new Product();
    boolean ok = helper.add(product);
    if (!ok) {
        System.err.println("[admin/products/add-handle.jsp] add product failed, name=" + product.getName());
    }
    response.sendRedirect(request.getContextPath() + "/admin/login/home.jsp?item=product_list");
%>
