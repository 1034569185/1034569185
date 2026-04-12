<%@ page import="java.util.ArrayList" %>
<%@ page import="java.util.HashMap" %>
<%@ page import="java.util.List" %>
<%@ page import="java.util.Map" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%
    // 1) 设置请求编码，支持中文
    request.setCharacterEncoding("UTF-8");

    String id = request.getParameter("id");
    String name = request.getParameter("name");
    String author = request.getParameter("author");
    String priceStr = request.getParameter("price");
    String image = request.getParameter("image");

    // 2) 从 session 获取购物车（作用域：当前会话）
    List<Map<String, Object>> cart = (List<Map<String, Object>>) session.getAttribute("cart");
    if (cart == null) {
        cart = new ArrayList<>();
    }

    if (id != null && !id.trim().isEmpty()) {
        boolean exists = false;
        for (Map<String, Object> item : cart) {
            if (id.equals(item.get("id"))) {
                Integer quantity = (Integer) item.get("quantity");
                item.put("quantity", quantity == null ? 1 : quantity + 1);
                exists = true;
                break;
            }
        }

        if (!exists) {
            Map<String, Object> newItem = new HashMap<>();
            newItem.put("id", id);
            newItem.put("name", name);
            newItem.put("author", author);
            newItem.put("price", priceStr == null ? 0.0 : Double.parseDouble(priceStr));
            newItem.put("image", image);
            newItem.put("quantity", 1);
            cart.add(newItem);
        }
    }

    // 3) 将购物车重新放入 session
    session.setAttribute("cart", cart);

    // 4) 跳转到购物车页面
    response.sendRedirect(request.getContextPath() + "/Cart");
%>
