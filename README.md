# BookStore 📚

一个基于 **Spring Boot + JSP** 的书城 Web 应用，作为 Dynamic Web Project 作业的起点，后续可轻松扩展功能。

## 项目结构

```
BookStore/
├── src/main/java/com/bookstore/
│   ├── BookStoreApplication.java      # 主入口
│   ├── config/
│   │   └── SecurityConfig.java        # Spring Security 配置
│   ├── controller/
│   │   ├── HomeController.java        # 根路径跳转
│   │   ├── UserController.java        # 注册/登录控制器
│   │   └── CaptchaController.java     # 验证码生成
│   ├── model/
│   │   ├── User.java                  # 用户实体
│   │   └── RegisterForm.java          # 注册表单 DTO
│   ├── repository/
│   │   └── UserRepository.java        # JPA 数据访问层
│   ├── service/
│   │   └── UserService.java           # 业务逻辑层
│   └── util/
│       └── CaptchaUtil.java           # 验证码工具
├── src/main/java/filter/
│   └── EncodingFilter.java            # 全站统一编码过滤器（实验十一）
├── src/main/java/listener/
│   └── MyListener.java                # 在线人数监听器（实验十一）
├── src/main/resources/
│   └── application.properties
├── src/main/webapp/
│   ├── WEB-INF/views/
│   │   └── register.jsp               # 注册页面 (JSP)
│   └── static/
│       ├── css/register.css           # 样式
│       └── js/register.js             # 前端验证逻辑
└── pom.xml
```

## 已实现功能

| 功能 | 说明 |
|------|------|
| **注册表单** | 用户名、密码、确认密码、邮箱、手机号、性别、生日 |
| **CSS 样式** | 响应式布局、现代 UI 设计、移动端适配 |
| **JS 前端验证** | 实时校验所有字段，提交前完整验证 |
| **密码强度** | 可视化密码强度指示条 |
| **记住密码** | Cookie 保存用户名/密码，下次自动填入 |
| **图片验证码** | 服务端生成带干扰线的随机字母验证码，支持刷新 |
| **AJAX 实时检查** | 失焦时异步检查用户名/邮箱是否已被注册 |
| **密码加密** | BCrypt 加密后存储 |
| **H2 内存数据库** | 开发阶段无需配置数据库，开箱即用 |
| **全站统一编码** | Filter 统一设置请求/响应 UTF-8（实验十一） |
| **在线人数统计** | Listener 统计登录在线人数，页面头部展示（实验十一） |

## 快速启动

```bash
cd BookStore
mvn spring-boot:run
```

默认访问基地址：`http://localhost:8080`

H2 数据库控制台：[http://localhost:8080/h2-console](http://localhost:8080/h2-console)  
（JDBC URL: `jdbc:h2:mem:bookstoredb`，用户名: `sa`，密码: 空）

## 页面访问指南（可直接复制到浏览器）

> 说明：项目里很多 JSP 在 `WEB-INF` 下，不能直接按文件路径访问，需要通过下面这些 URL 进入。

### 1) 前台页面

| 页面 | 访问地址 |
|------|----------|
| 首页 | `http://localhost:8080/` |
| 注册页 | `http://localhost:8080/user/register` |
| 登录页 | `http://localhost:8080/user/login`（或 `/login`） |
| 商品列表（实验七） | `http://localhost:8080/ProductList` |
| 购物车（实验七） | `http://localhost:8080/Cart` |
| 注册成功页 | `http://localhost:8080/registersuccess` |
| 登录成功页 | `http://localhost:8080/loginsuccess` |
| 登录失败页 | `http://localhost:8080/loginfail` |

### 2) 后台页面（重点：可直接打开）

| 页面 | 访问地址 |
|------|----------|
| 后台欢迎页 | `http://localhost:8080/admin/welcome` |
| 商品管理容器页（实验十一） | `http://localhost:8080/admin/login/home` |
| 商品列表页（实验十一） | `http://localhost:8080/admin/login/home?item=product_list` |
| 添加商品页（实验十一） | `http://localhost:8080/admin/login/home?item=product_add` |

### 3) 表单处理与接口地址（调试时使用）

| 功能 | 地址 |
|------|------|
| 注册提交 | `POST http://localhost:8080/Handle-register` |
| 登录提交 | `POST http://localhost:8080/Handle-login` |
| 添加购物车 | `http://localhost:8080/Handle-AddCart` |
| 删除购物车 | `http://localhost:8080/DeleteCart` |
| 添加商品提交（实验十一） | `POST http://localhost:8080/admin/products/add-handle` |
| 验证码图片 | `http://localhost:8080/captcha/image` |
| 用户名可用性检查 | `http://localhost:8080/user/checkUsername?username=test` |
| 邮箱可用性检查 | `http://localhost:8080/user/checkEmail?email=test@example.com` |

## 建议的使用顺序（新用户）

1. 打开 `http://localhost:8080/` 查看首页  
2. 访问 `http://localhost:8080/user/register` 注册账号  
3. 访问 `http://localhost:8080/user/login` 登录  
4. 访问 `http://localhost:8080/admin/login/home?item=product_list` 进入商品管理  
5. 访问 `http://localhost:8080/admin/login/home?item=product_add` 添加商品  

## 后续扩展建议

- **登录页面** (`login.jsp` + `UserController.login()`)
- **书籍列表/详情/购物车**（新增 Book、Cart 实体及对应 Controller）
- **订单管理**（Order 实体）
- **MySQL / PostgreSQL**（修改 `application.properties` 中数据源即可）
- **邮件验证**（引入 `spring-boot-starter-mail`）
- **前后端分离升级**（保留 Service/Repository，替换 JSP 为 Vue 3 + Axios）

## 技术栈

- Java 11 + Spring Boot 2.7
- Spring Security（密码加密 + 未来登录认证）
- Spring Data JPA + H2（可换 MySQL）
- JSP + JSTL（视图层）
- 原生 HTML5 / CSS3 / JavaScript（无框架，符合作业要求）
