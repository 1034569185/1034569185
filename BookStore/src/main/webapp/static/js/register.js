/**
 * BookStore - register.js
 * 用户注册页面 JavaScript
 * 功能：表单验证、验证码刷新、记住用户名/密码、密码强度检测、AJAX 实时校验
 */

'use strict';

/* ============================================================
   工具函数
   ============================================================ */

/**
 * 获取上下文路径（从当前 URL 中提取，兼容不同部署路径）
 */
function getContextPath() {
    var pathParts = window.location.pathname.split('/');
    // Spring Boot 默认部署在根路径，若有上下文路径则取第一段
    return '';
}

/**
 * 设置表单组的验证状态
 * @param {string} groupId - form-group 的 id
 * @param {'error'|'success'|''} state
 * @param {string} message - 提示文本
 */
function setFieldState(groupId, state, message) {
    var group = document.getElementById(groupId);
    var hint  = document.getElementById(groupId.replace('group-', '') + '-hint');

    if (!group) return;

    group.classList.remove('has-error', 'has-success');

    if (state === 'error') {
        group.classList.add('has-error');
        if (hint) {
            hint.className = 'field-hint hint-error';
            hint.textContent = message || '';
        }
    } else if (state === 'success') {
        group.classList.add('has-success');
        if (hint) {
            hint.className = 'field-hint hint-success';
            hint.textContent = message || '';
        }
    } else {
        if (hint) {
            hint.className = 'field-hint';
            hint.textContent = message || '';
        }
    }
}

/**
 * 为输入框设置样式类
 */
function setInputState(inputId, state) {
    var input = document.getElementById(inputId);
    if (!input) return;
    input.classList.remove('is-valid', 'is-invalid');
    if (state === 'valid')   input.classList.add('is-valid');
    if (state === 'invalid') input.classList.add('is-invalid');
}

/* ============================================================
   Cookie 操作（记住用户名/密码）
   ============================================================ */

function setCookie(name, value, days) {
    var expires = '';
    if (days) {
        var d = new Date();
        d.setTime(d.getTime() + days * 24 * 3600 * 1000);
        expires = '; expires=' + d.toUTCString();
    }
    document.cookie = encodeURIComponent(name) + '=' +
                      encodeURIComponent(value) + expires + '; path=/; SameSite=Lax';
}

function getCookie(name) {
    var prefix = encodeURIComponent(name) + '=';
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
        var c = cookies[i].trim();
        if (c.indexOf(prefix) === 0) {
            return decodeURIComponent(c.substring(prefix.length));
        }
    }
    return null;
}

function deleteCookie(name) {
    setCookie(name, '', -1);
}

/**
 * 页面加载时从 Cookie 恢复已记住的用户名
 * 注意：出于安全考虑，不在客户端存储密码
 */
function restoreRememberedCredentials() {
    var savedUsername = getCookie('bs_remember_username');

    if (savedUsername) {
        var usernameInput = document.getElementById('username');
        if (usernameInput && !usernameInput.value) {
            usernameInput.value = savedUsername;
        }

        var rememberCheck = document.getElementById('rememberMe');
        if (rememberCheck) {
            rememberCheck.checked = true;
        }
    }
}

/* ============================================================
   密码可见性切换
   ============================================================ */

function togglePassword(inputId) {
    var input = document.getElementById(inputId);
    if (!input) return;
    if (input.type === 'password') {
        input.type = 'text';
    } else {
        input.type = 'password';
    }
}

/* ============================================================
   验证码刷新
   ============================================================ */

function refreshCaptcha() {
    var img = document.getElementById('captchaImg');
    if (img) {
        // 添加时间戳参数，防止浏览器缓存
        img.src = '/captcha/image?t=' + Date.now();
    }
    // 清空验证码输入
    var input = document.getElementById('captchaInput');
    if (input) {
        input.value = '';
        input.classList.remove('is-valid', 'is-invalid');
        setFieldState('group-captcha', '', '');
        input.focus();
    }
}

/* ============================================================
   密码强度检测
   ============================================================ */

function checkPasswordStrength(password) {
    var score = 0;
    var desc  = '';
    var color = '';

    if (!password || password.length === 0) {
        return { score: 0, desc: '', color: '' };
    }

    if (password.length >= 6)  score++;
    if (password.length >= 10) score++;
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) score++;
    if (/\d/.test(password))   score++;
    if (/[^a-zA-Z0-9]/.test(password)) score++;

    if (score <= 1) {
        desc = '弱'; color = '#ef4444';
    } else if (score <= 3) {
        desc = '中'; color = '#f59e0b';
    } else if (score === 4) {
        desc = '强'; color = '#22c55e';
    } else {
        desc = '极强'; color = '#059669';
    }

    return { score: score, desc: desc, color: color };
}

function updateStrengthBar(password) {
    var fill   = document.getElementById('strength-fill');
    var text   = document.getElementById('strength-text');
    var result = checkPasswordStrength(password);

    if (!fill || !text) return;

    if (!password) {
        fill.style.width = '0';
        text.textContent = '';
        return;
    }

    var pct = Math.min(100, result.score * 20);
    fill.style.width = pct + '%';
    fill.style.backgroundColor = result.color;
    text.style.color = result.color;
    text.textContent = result.desc;
}

/* ============================================================
   表单验证规则
   ============================================================ */

var RULES = {
    username: {
        required: true,
        minLen: 4,
        maxLen: 20,
        pattern: /^[a-zA-Z0-9_]+$/,
        messages: {
            required: '请输入用户名',
            minLen:   '用户名至少 4 个字符',
            maxLen:   '用户名最多 20 个字符',
            pattern:  '用户名只能包含字母、数字和下划线'
        }
    },
    password: {
        required: true,
        minLen: 6,
        maxLen: 20,
        messages: {
            required: '请输入密码',
            minLen:   '密码至少 6 个字符',
            maxLen:   '密码最多 20 个字符'
        }
    },
    confirmPassword: {
        required: true,
        messages: {
            required: '请再次输入密码',
            mismatch: '两次输入的密码不一致'
        }
    },
    email: {
        required: true,
        pattern: /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/,
        messages: {
            required: '请输入电子邮箱',
            pattern:  '请输入有效的邮箱地址'
        }
    },
    phone: {
        required: false,
        pattern: /^1[3-9]\d{9}$/,
        messages: {
            pattern: '请输入正确的 11 位手机号'
        }
    },
    birthday: {
        required: false,
        messages: {
            future: '出生日期不能是将来的日期',
            tooOld: '请输入合理的出生日期（不超过 120 年前）'
        }
    },
    captcha: {
        required: true,
        minLen: 4,
        maxLen: 4,
        messages: {
            required: '请输入验证码',
            length:   '验证码为 4 位字符'
        }
    }
};

/**
 * 校验单个字段，返回 { valid, message }
 */
function validateField(fieldName, value) {
    var rule = RULES[fieldName];
    if (!rule) return { valid: true, message: '' };

    var v = (value || '').trim();

    // 必填检查
    if (rule.required && !v) {
        return { valid: false, message: rule.messages.required };
    }

    // 如果非必填且为空，直接通过
    if (!rule.required && !v) {
        return { valid: true, message: '' };
    }

    // 最小长度
    if (rule.minLen && v.length < rule.minLen) {
        return { valid: false, message: rule.messages.minLen };
    }

    // 最大长度
    if (rule.maxLen && v.length > rule.maxLen) {
        return { valid: false, message: rule.messages.maxLen };
    }

    // 格式校验
    if (rule.pattern && !rule.pattern.test(v)) {
        return { valid: false, message: rule.messages.pattern };
    }

    // 确认密码特殊处理
    if (fieldName === 'confirmPassword') {
        var pw = document.getElementById('password');
        if (pw && v !== pw.value) {
            return { valid: false, message: rule.messages.mismatch };
        }
    }

    // 生日特殊处理
    if (fieldName === 'birthday' && v) {
        var bDate = new Date(v);
        var today = new Date();
        today.setHours(0, 0, 0, 0);
        if (bDate > today) {
            return { valid: false, message: rule.messages.future };
        }
        var minDate = new Date();
        minDate.setFullYear(minDate.getFullYear() - 120);
        if (bDate < minDate) {
            return { valid: false, message: rule.messages.tooOld };
        }
    }

    return { valid: true, message: '✓' };
}

/* ============================================================
   实时字段验证（blur 事件）
   ============================================================ */

function bindFieldValidation(inputId, fieldName) {
    var input = document.getElementById(inputId);
    if (!input) return;

    input.addEventListener('blur', function () {
        var result = validateField(fieldName, this.value);
        setFieldState('group-' + fieldName, result.valid ? 'success' : 'error', result.message);
        setInputState(inputId, result.valid ? 'valid' : 'invalid');
    });

    // 输入时清除错误状态（即时反馈）
    input.addEventListener('input', function () {
        var group = document.getElementById('group-' + fieldName);
        if (group && group.classList.contains('has-error')) {
            var result = validateField(fieldName, this.value);
            if (result.valid) {
                setFieldState('group-' + fieldName, 'success', result.message);
                setInputState(inputId, 'valid');
            }
        }
    });
}

/* ============================================================
   AJAX 实时检查用户名/邮箱是否已存在
   ============================================================ */

var ajaxTimer = {};

function checkFieldAvailability(type, value) {
    clearTimeout(ajaxTimer[type]);
    if (!value || value.trim().length < 1) return;

    ajaxTimer[type] = setTimeout(function () {
        var url = '/user/check' + (type === 'username' ? 'Username' : 'Email') +
                  '?' + type + '=' + encodeURIComponent(value.trim());

        var xhr = new XMLHttpRequest();
        xhr.open('GET', url, true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                try {
                    var data = JSON.parse(xhr.responseText);
                    var indicator = document.getElementById(type + '-check');
                    if (data.available) {
                        setFieldState('group-' + type, 'success', data.message);
                        setInputState(type, 'valid');
                        if (indicator) {
                            indicator.className = 'check-indicator ok';
                            indicator.textContent = '✓';
                        }
                    } else {
                        setFieldState('group-' + type, 'error', data.message);
                        setInputState(type, 'invalid');
                        if (indicator) {
                            indicator.className = 'check-indicator fail';
                            indicator.textContent = '✗';
                        }
                    }
                } catch (e) {
                    // JSON 解析错误，忽略
                }
            }
        };
        xhr.send();
    }, 500);
}

/* ============================================================
   表单提交验证
   ============================================================ */

function validateForm() {
    var valid = true;

    // 验证用户名
    var usernameVal = (document.getElementById('username') || {}).value || '';
    var r = validateField('username', usernameVal);
    setFieldState('group-username', r.valid ? 'success' : 'error', r.message);
    setInputState('username', r.valid ? 'valid' : 'invalid');
    if (!r.valid) valid = false;

    // 验证密码
    var pwVal = (document.getElementById('password') || {}).value || '';
    r = validateField('password', pwVal);
    setFieldState('group-password', r.valid ? 'success' : 'error', r.message);
    setInputState('password', r.valid ? 'valid' : 'invalid');
    if (!r.valid) valid = false;

    // 验证确认密码
    var cpwVal = (document.getElementById('confirmPassword') || {}).value || '';
    r = validateField('confirmPassword', cpwVal);
    setFieldState('group-confirmPassword', r.valid ? 'success' : 'error', r.message);
    setInputState('confirmPassword', r.valid ? 'valid' : 'invalid');
    if (!r.valid) valid = false;

    // 验证邮箱
    var emailVal = (document.getElementById('email') || {}).value || '';
    r = validateField('email', emailVal);
    setFieldState('group-email', r.valid ? 'success' : 'error', r.message);
    setInputState('email', r.valid ? 'valid' : 'invalid');
    if (!r.valid) valid = false;

    // 验证手机号（选填）
    var phoneVal = (document.getElementById('phone') || {}).value || '';
    if (phoneVal.trim()) {
        r = validateField('phone', phoneVal);
        setFieldState('group-phone', r.valid ? 'success' : 'error', r.message);
        setInputState('phone', r.valid ? 'valid' : 'invalid');
        if (!r.valid) valid = false;
    }

    // 验证生日（选填）
    var bVal = (document.getElementById('birthday') || {}).value || '';
    if (bVal) {
        r = validateField('birthday', bVal);
        setFieldState('group-birthday', r.valid ? 'success' : 'error', r.message);
        if (!r.valid) valid = false;
    }

    // 验证验证码
    var captchaVal = (document.getElementById('captchaInput') || {}).value || '';
    if (!captchaVal.trim()) {
        setFieldState('group-captcha', 'error', RULES.captcha.messages.required);
        setInputState('captchaInput', 'invalid');
        valid = false;
    } else if (captchaVal.trim().length !== 4) {
        setFieldState('group-captcha', 'error', RULES.captcha.messages.length);
        setInputState('captchaInput', 'invalid');
        valid = false;
    } else {
        setFieldState('group-captcha', 'success', '');
        setInputState('captchaInput', 'valid');
    }

    // 验证用户协议
    var agree    = document.getElementById('agreeTerms');
    var agreeHint = document.getElementById('agree-hint');
    if (agree && !agree.checked) {
        if (agreeHint) {
            agreeHint.className = 'field-hint hint-error';
            agreeHint.textContent = '请阅读并同意用户协议';
        }
        valid = false;
    } else {
        if (agreeHint) {
            agreeHint.className = 'field-hint';
            agreeHint.textContent = '';
        }
    }

    return valid;
}

/* ============================================================
   页面初始化
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {

    // 设置生日最大值为今天
    var birthdayInput = document.getElementById('birthday');
    if (birthdayInput) {
        birthdayInput.max = new Date().toISOString().split('T')[0];
    }

    // 恢复记住的用户名/密码
    restoreRememberedCredentials();

    // 绑定实时字段校验
    bindFieldValidation('username',        'username');
    bindFieldValidation('password',        'password');
    bindFieldValidation('confirmPassword', 'confirmPassword');
    bindFieldValidation('email',           'email');
    bindFieldValidation('phone',           'phone');
    bindFieldValidation('birthday',        'birthday');
    bindFieldValidation('captchaInput',    'captcha');

    // 密码输入时更新强度条
    var passwordInput = document.getElementById('password');
    if (passwordInput) {
        passwordInput.addEventListener('input', function () {
            updateStrengthBar(this.value);
        });
    }

    // 密码变化时重新校验确认密码
    if (passwordInput) {
        passwordInput.addEventListener('input', function () {
            var cpwInput = document.getElementById('confirmPassword');
            if (cpwInput && cpwInput.value) {
                var r = validateField('confirmPassword', cpwInput.value);
                setFieldState('group-confirmPassword', r.valid ? 'success' : 'error', r.message);
                setInputState('confirmPassword', r.valid ? 'valid' : 'invalid');
            }
        });
    }

    // AJAX 检查用户名是否已存在
    var usernameInput = document.getElementById('username');
    if (usernameInput) {
        usernameInput.addEventListener('blur', function () {
            var localResult = validateField('username', this.value);
            if (localResult.valid) {
                checkFieldAvailability('username', this.value);
            }
        });
    }

    // AJAX 检查邮箱是否已存在
    var emailInput = document.getElementById('email');
    if (emailInput) {
        emailInput.addEventListener('blur', function () {
            var localResult = validateField('email', this.value);
            if (localResult.valid) {
                checkFieldAvailability('email', this.value);
            }
        });
    }

    // 点击验证码图片也可刷新
    var captchaImg = document.getElementById('captchaImg');
    if (captchaImg) {
        captchaImg.addEventListener('click', refreshCaptcha);
    }

    // 表单提交
    var form = document.getElementById('registerForm');
    if (form) {
        form.addEventListener('submit', function (e) {
            if (!validateForm()) {
                e.preventDefault();
                // 定位到第一个错误字段
                var firstError = document.querySelector('.has-error .form-input');
                if (firstError) {
                    firstError.focus();
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
                return;
            }

            // 处理记住用户名（出于安全考虑，不在客户端 Cookie 中存储密码）
            var rememberMe  = document.getElementById('rememberMe');
            var usernameVal = (document.getElementById('username') || {}).value || '';

            if (rememberMe && rememberMe.checked) {
                setCookie('bs_remember_username', usernameVal, 30);
            } else {
                deleteCookie('bs_remember_username');
            }
        });
    }

    // 协议复选框点击时清除提示
    var agreeTerms = document.getElementById('agreeTerms');
    if (agreeTerms) {
        agreeTerms.addEventListener('change', function () {
            if (this.checked) {
                var agreeHint = document.getElementById('agree-hint');
                if (agreeHint) {
                    agreeHint.className = 'field-hint';
                    agreeHint.textContent = '';
                }
            }
        });
    }
});
