package com.bookstore.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

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
    @GetMapping({"/ProductList.jsp", "/ProductList"})
    public String productList() {
        return "ProductList";
    }

    /**
     * 购物车展示页（实验七）
     */
    @GetMapping({"/Cart.jsp", "/Cart"})
    public String cart() {
        return "Cart";
    }

    /**
     * 购物车添加处理页（实验七）
     */
    @RequestMapping({"/Handle-AddCart.jsp", "/Handle-AddCart"})
    public String handleAddCart() {
        return "Handle-AddCart";
    }

    /**
     * 购物车删除处理页（实验七）
     */
    @RequestMapping({"/DeleteCart.jsp", "/DeleteCart"})
    public String deleteCart() {
        return "DeleteCart";
    }
}
