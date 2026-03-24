package com.bookstore.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

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
}
