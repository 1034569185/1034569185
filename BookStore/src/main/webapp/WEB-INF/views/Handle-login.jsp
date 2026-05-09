<%@ page import="com.bookstore.util.JdbcUtil" %>
<%@ page import="java.net.URLEncoder" %>
<%@ page import="java.nio.charset.StandardCharsets" %>
<%@ page import="java.sql.Connection" %>
<%@ page import="java.sql.PreparedStatement" %>
<%@ page import="java.sql.ResultSet" %>
<%@ page import="java.util.HashMap" %>
<%@ page import="java.util.Map" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%
    request.setCharacterEncoding("UTF-8");

    String username = request.getParameter("username");
    String password = request.getParameter("password");

    if (username == null || username.trim().isEmpty() || password == null || password.trim().isEmpty()) {
        response.sendRedirect(request.getContextPath() + "/loginfail?message="
                + URLEncoder.encode("登录失败：用户名或密码不能为空", StandardCharsets.UTF_8.name()));
        return;
    }

    Connection conn = null;
    PreparedStatement stmt = null;
    ResultSet rs = null;
    try {
        conn = JdbcUtil.getConnection();
        stmt = conn.prepareStatement("SELECT id, username, role FROM `user` WHERE username = ? AND password = ?");
        stmt.setString(1, username.trim());
        stmt.setString(2, password);
        rs = stmt.executeQuery();

        if (rs.next()) {
            Map<String, Object> loginUser = new HashMap<>();
            loginUser.put("id", rs.getLong("id"));
            loginUser.put("username", rs.getString("username"));
            loginUser.put("role", rs.getString("role"));
            session.setAttribute("loginUser", loginUser);
            session.setAttribute("username", rs.getString("username"));
            response.sendRedirect(request.getContextPath() + "/loginsuccess");
        } else {
            response.sendRedirect(request.getContextPath() + "/loginfail?message="
                    + URLEncoder.encode("登录失败：用户名或密码错误", StandardCharsets.UTF_8.name()));
        }
    } catch (Exception e) {
        response.sendRedirect(request.getContextPath() + "/loginfail?message="
                + URLEncoder.encode("登录失败：" + e.getMessage(), StandardCharsets.UTF_8.name()));
    } finally {
        if (rs != null) try { rs.close(); } catch (Exception ignored) {}
        if (stmt != null) try { stmt.close(); } catch (Exception ignored) {}
        if (conn != null) try { conn.close(); } catch (Exception ignored) {}
    }
%>
