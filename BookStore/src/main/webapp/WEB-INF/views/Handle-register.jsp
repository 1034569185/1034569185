<%@ page import="com.bookstore.util.JdbcUtil" %>
<%@ page import="java.net.URLEncoder" %>
<%@ page import="java.nio.charset.StandardCharsets" %>
<%@ page import="java.sql.Connection" %>
<%@ page import="java.sql.PreparedStatement" %>
<%@ page import="java.sql.ResultSet" %>
<%@ page import="java.time.LocalDateTime" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%
    request.setCharacterEncoding("UTF-8");

    String username = request.getParameter("username");
    String password = request.getParameter("password");
    String confirmPassword = request.getParameter("confirmPassword");
    String email = request.getParameter("email");
    String phone = request.getParameter("phone");
    String gender = request.getParameter("gender");
    String birthday = request.getParameter("birthday");

    if (username == null || username.trim().isEmpty()
            || password == null || password.trim().isEmpty()
            || email == null || email.trim().isEmpty()) {
        response.sendRedirect(request.getContextPath() + "/loginfail?message="
                + URLEncoder.encode("注册失败：用户名、密码、邮箱不能为空", StandardCharsets.UTF_8.name()));
        return;
    }

    if (confirmPassword != null && !confirmPassword.isEmpty() && !password.equals(confirmPassword)) {
        response.sendRedirect(request.getContextPath() + "/loginfail?message="
                + URLEncoder.encode("注册失败：两次密码不一致", StandardCharsets.UTF_8.name()));
        return;
    }

    Connection conn = null;
    PreparedStatement checkStmt = null;
    PreparedStatement insertStmt = null;
    ResultSet rs = null;
    try {
        conn = JdbcUtil.getConnection();

        checkStmt = conn.prepareStatement("SELECT COUNT(*) FROM `user` WHERE username = ?");
        checkStmt.setString(1, username.trim());
        rs = checkStmt.executeQuery();
        if (rs.next() && rs.getInt(1) > 0) {
            response.sendRedirect(request.getContextPath() + "/loginfail?message="
                    + URLEncoder.encode("注册失败：用户名已存在", StandardCharsets.UTF_8.name()));
            return;
        }

        insertStmt = conn.prepareStatement(
                "INSERT INTO `user` (username, password, email, telephone, gender, role) VALUES (?, ?, ?, ?, ?, ?)");
        insertStmt.setString(1, username.trim());
        insertStmt.setString(2, password);
        insertStmt.setString(3, email.trim());
        insertStmt.setString(4, phone == null || phone.trim().isEmpty() ? null : phone.trim());
        insertStmt.setString(5, gender == null || gender.trim().isEmpty() ? null : gender.trim());
        insertStmt.setString(6, "普通用户");

        int rows = insertStmt.executeUpdate();
        if (rows > 0) {
            response.sendRedirect(request.getContextPath() + "/registersuccess?username="
                    + URLEncoder.encode(username.trim(), StandardCharsets.UTF_8.name()));
        } else {
            response.sendRedirect(request.getContextPath() + "/loginfail?message="
                    + URLEncoder.encode("注册失败：写入数据库失败", StandardCharsets.UTF_8.name()));
        }
    } catch (Exception e) {
        System.err.println("[Handle-register.jsp] Registration DB error at " + LocalDateTime.now()
                + ", username=" + username + ", email=" + email + ", message=" + e.getMessage());
        e.printStackTrace();
        response.sendRedirect(request.getContextPath() + "/loginfail?message="
                + URLEncoder.encode("注册失败：" + e.getMessage(), StandardCharsets.UTF_8.name()));
    } finally {
        if (rs != null) try { rs.close(); } catch (Exception ignored) {}
        if (checkStmt != null) try { checkStmt.close(); } catch (Exception ignored) {}
        if (insertStmt != null) try { insertStmt.close(); } catch (Exception ignored) {}
        if (conn != null) try { conn.close(); } catch (Exception ignored) {}
    }
%>
