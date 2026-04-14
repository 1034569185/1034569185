package com.bookstore.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import javax.servlet.http.HttpSession;

/**
 * 根路径控制器，统一跳转逻辑
 */
@Controller
public class HomeController {

    /**
     * 根路径 → 首页
     */
    @GetMapping("/")
    public String home() {
        return "index";
    }

    /**
     * 后台管理欢迎页
     */
    @GetMapping("/admin/welcome")
    public String adminWelcome() {
        return "admin/welcome";
    }

    /**
     * 商品目录页（实验七）
     */
    @GetMapping({"/ProductList", "/ProductList.*"})
    public String productList() {
        return "ProductList";
    }

    /**
     * 购物车展示页（实验七）
     */
    @GetMapping({"/Cart", "/Cart.*"})
    public String cart() {
        return "Cart";
    }

    /**
     * 购物车添加处理页（实验七）
     */
    @RequestMapping({"/Handle-AddCart", "/Handle-AddCart.*"})
    public String handleAddCart() {
        return "Handle-AddCart";
    }

    /**
     * 购物车删除处理页（实验七）
     */
    @RequestMapping({"/DeleteCart", "/DeleteCart.*"})
    public String deleteCart() {
        return "DeleteCart";
    }

    /**
     * 实验八：登录页
     */
    @GetMapping({"/login", "/login.*", "/user/login"})
    public String loginPage() {
        return "login";
    }

    /**
     * 实验八：注册处理页
     */
    @RequestMapping({"/Handle-register", "/Handle-register.*"})
    public String handleRegister() {
        return "Handle-register";
    }

    /**
     * 实验八：登录处理页
     */
    @RequestMapping({"/Handle-login", "/Handle-login.*"})
    public String handleLogin() {
        return "Handle-login";
    }

    /**
     * 实验八：注册成功页
     */
    @GetMapping({"/registersuccess", "/registersuccess.*"})
    public String registerSuccess() {
        return "registersuccess";
    }

    /**
     * 实验八：登录成功页
     */
    @GetMapping({"/loginsuccess", "/loginsuccess.*"})
    public String loginSuccess() {
        return "loginsuccess";
    }

    /**
     * 实验八：登录失败页
     */
    @GetMapping({"/loginfail", "/loginfail.*"})
    public String loginFail() {
        return "loginfail";
    }

    /**
     * 自定义退出：清除 session 登录信息
     */
    @GetMapping("/user/logout")
    public String userLogout(HttpSession session) {
        session.removeAttribute("loginUser");
        return "redirect:/";
    }
}
