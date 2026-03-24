<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>用户注册 - BookStore</title>
    <%-- 先引入公共样式，再引入注册页专属样式 --%>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/static/css/common.css">
    <link rel="stylesheet" href="${pageContext.request.contextPath}/static/css/register.css">
</head>
<body>

<div class="page-wrapper">
    <%-- 使用 include 指令包含公共头部 --%>
    <%@ include file="head.jsp" %>

    <%-- 使用 include 指令包含搜索/分类菜单 --%>
    <%@ include file="menu_search.jsp" %>

    <!-- 主要内容区 -->
    <main class="main-content">
        <div class="register-container">
            <div class="register-card">
                <h1 class="register-title">创建账号</h1>
                <p class="register-subtitle">加入 BookStore，开启你的阅读之旅</p>

                <!-- 成功提示 -->
                <c:if test="${not empty success}">
                    <div class="alert alert-success">
                        <span class="alert-icon">✅</span>
                        <span>${success}</span>
                    </div>
                </c:if>

                <!-- 错误提示 -->
                <c:if test="${not empty error}">
                    <div class="alert alert-error">
                        <span class="alert-icon">❌</span>
                        <span>${error}</span>
                    </div>
                </c:if>

                <form id="registerForm" action="${pageContext.request.contextPath}/user/register"
                      method="post" novalidate>
                    <input type="hidden" name="${_csrf.parameterName}" value="${_csrf.token}"/>

                    <!-- 用户名 -->
                    <div class="form-group" id="group-username">
                        <label for="username" class="form-label">
                            用户名 <span class="required">*</span>
                        </label>
                        <div class="input-wrapper">
                            <span class="input-icon">👤</span>
                            <input type="text" id="username" name="username"
                                   class="form-input"
                                   placeholder="4-20位字母、数字或下划线"
                                   value="${form.username}"
                                   autocomplete="username"
                                   maxlength="20">
                            <span class="check-indicator" id="username-check"></span>
                        </div>
                        <div class="field-hint" id="username-hint"></div>
                    </div>

                    <!-- 密码 -->
                    <div class="form-group" id="group-password">
                        <label for="password" class="form-label">
                            密码 <span class="required">*</span>
                        </label>
                        <div class="input-wrapper">
                            <span class="input-icon">🔒</span>
                            <input type="password" id="password" name="password"
                                   class="form-input"
                                   placeholder="6-20位，包含字母和数字"
                                   autocomplete="new-password"
                                   maxlength="20">
                            <button type="button" class="toggle-password" onclick="togglePassword('password')"
                                    title="显示/隐藏密码">👁</button>
                        </div>
                        <div class="password-strength" id="password-strength">
                            <div class="strength-bar">
                                <div class="strength-fill" id="strength-fill"></div>
                            </div>
                            <span class="strength-text" id="strength-text"></span>
                        </div>
                        <div class="field-hint" id="password-hint"></div>
                    </div>

                    <!-- 确认密码 -->
                    <div class="form-group" id="group-confirmPassword">
                        <label for="confirmPassword" class="form-label">
                            确认密码 <span class="required">*</span>
                        </label>
                        <div class="input-wrapper">
                            <span class="input-icon">🔒</span>
                            <input type="password" id="confirmPassword" name="confirmPassword"
                                   class="form-input"
                                   placeholder="再次输入密码"
                                   autocomplete="new-password"
                                   maxlength="20">
                            <button type="button" class="toggle-password" onclick="togglePassword('confirmPassword')"
                                    title="显示/隐藏密码">👁</button>
                        </div>
                        <div class="field-hint" id="confirmPassword-hint"></div>
                    </div>

                    <!-- 邮箱 -->
                    <div class="form-group" id="group-email">
                        <label for="email" class="form-label">
                            电子邮箱 <span class="required">*</span>
                        </label>
                        <div class="input-wrapper">
                            <span class="input-icon">📧</span>
                            <input type="email" id="email" name="email"
                                   class="form-input"
                                   placeholder="example@email.com"
                                   value="${form.email}"
                                   autocomplete="email"
                                   maxlength="100">
                            <span class="check-indicator" id="email-check"></span>
                        </div>
                        <div class="field-hint" id="email-hint"></div>
                    </div>

                    <!-- 手机号 -->
                    <div class="form-group" id="group-phone">
                        <label for="phone" class="form-label">手机号码</label>
                        <div class="input-wrapper">
                            <span class="input-icon">📱</span>
                            <input type="tel" id="phone" name="phone"
                                   class="form-input"
                                   placeholder="11位手机号（选填）"
                                   value="${form.phone}"
                                   autocomplete="tel"
                                   maxlength="11">
                        </div>
                        <div class="field-hint" id="phone-hint"></div>
                    </div>

                    <!-- 性别 -->
                    <div class="form-group" id="group-gender">
                        <label class="form-label">性别</label>
                        <div class="radio-group">
                            <label class="radio-label">
                                <input type="radio" name="gender" value="male"
                                       ${form.gender == 'male' ? 'checked' : ''}>
                                <span class="radio-custom"></span>
                                <span>男</span>
                            </label>
                            <label class="radio-label">
                                <input type="radio" name="gender" value="female"
                                       ${form.gender == 'female' ? 'checked' : ''}>
                                <span class="radio-custom"></span>
                                <span>女</span>
                            </label>
                            <label class="radio-label">
                                <input type="radio" name="gender" value="other"
                                       ${form.gender == 'other' ? 'checked' : ''}>
                                <span class="radio-custom"></span>
                                <span>保密</span>
                            </label>
                        </div>
                    </div>

                    <!-- 生日 -->
                    <div class="form-group" id="group-birthday">
                        <label for="birthday" class="form-label">出生日期</label>
                        <div class="input-wrapper">
                            <span class="input-icon">🎂</span>
                            <input type="date" id="birthday" name="birthday"
                                   class="form-input"
                                   value="${form.birthday}"
                                   max="">
                        </div>
                        <div class="field-hint" id="birthday-hint"></div>
                    </div>

                    <!-- 验证码 -->
                    <div class="form-group" id="group-captcha">
                        <label for="captchaInput" class="form-label">
                            验证码 <span class="required">*</span>
                        </label>
                        <div class="captcha-wrapper">
                            <div class="input-wrapper captcha-input-wrapper">
                                <span class="input-icon">🔑</span>
                                <input type="text" id="captchaInput" name="captcha"
                                       class="form-input"
                                       placeholder="请输入验证码"
                                       maxlength="4"
                                       autocomplete="off">
                            </div>
                            <div class="captcha-image-wrapper">
                                <img id="captchaImg"
                                     src="${pageContext.request.contextPath}/captcha/image"
                                     alt="验证码"
                                     class="captcha-img"
                                     title="点击刷新">
                                <button type="button" class="captcha-refresh" onclick="refreshCaptcha()"
                                        title="刷新验证码">↺</button>
                            </div>
                        </div>
                        <div class="field-hint" id="captcha-hint"></div>
                    </div>

                    <!-- 记住用户名/密码 -->
                    <div class="form-group">
                        <label class="checkbox-label">
                            <input type="checkbox" id="rememberMe" name="rememberMe">
                            <span class="checkbox-custom"></span>
                            <span>记住用户名（下次自动填入）</span>
                        </label>
                    </div>

                    <!-- 用户协议 -->
                    <div class="form-group">
                        <label class="checkbox-label" id="agreement-label">
                            <input type="checkbox" id="agreeTerms">
                            <span class="checkbox-custom"></span>
                            <span>我已阅读并同意 <a href="#" class="link">《用户服务协议》</a> 和 <a href="#" class="link">《隐私政策》</a></span>
                        </label>
                        <div class="field-hint" id="agree-hint"></div>
                    </div>

                    <!-- 提交按钮 -->
                    <button type="submit" class="btn-register" id="submitBtn">立即注册</button>

                    <div class="login-link">
                        已有账号？<a href="#" class="link">立即登录</a>
                    </div>
                </form>
            </div>
        </div>
    </main>

    <%-- 使用 include 指令包含公共页脚 --%>
    <%@ include file="foot.jsp" %>
</div>

<script src="${pageContext.request.contextPath}/static/js/register.js"></script>
</body>
</html>
