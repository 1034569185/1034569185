package com.bookstore.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

/**
 * 根路径控制器，统一跳转逻辑
 */
@Controller
public class HomeController {

    @GetMapping("/")
    public String home() {
        return "redirect:/user/register";
    }
}
