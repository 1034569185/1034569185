<%@ page import="java.util.List" %>
<%@ page import="java.util.Map" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%
    request.setCharacterEncoding("UTF-8");

    String id = request.getParameter("id");
    String clear = request.getParameter("clear");

    List<Map<String, Object>> cart = (List<Map<String, Object>>) session.getAttribute("cart");

    if (cart != null) {
        if ("true".equals(clear)) {
            session.removeAttribute("cart");
        } else if (id != null) {
            cart.removeIf(item -> id.equals(item.get("id")));
            if (cart.isEmpty()) {
                session.removeAttribute("cart");
            } else {
                session.setAttribute("cart", cart);
            }
        }
    }

    response.sendRedirect(request.getContextPath() + "/Cart");
%>
