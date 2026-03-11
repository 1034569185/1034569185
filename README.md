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

## 快速启动

```bash
cd BookStore
mvn spring-boot:run
```

浏览器访问：[http://localhost:8080/user/register](http://localhost:8080/user/register)

H2 数据库控制台：[http://localhost:8080/h2-console](http://localhost:8080/h2-console)  
（JDBC URL: `jdbc:h2:mem:bookstoredb`，用户名: `sa`，密码: 空）

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
