package com.bookstore.controller;

import com.bookstore.util.CaptchaUtil;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.IOException;

/**
 * 验证码控制器
 */
@RestController
@RequestMapping("/captcha")
public class CaptchaController {

    /**
     * 生成验证码图片
     * 请求示例：GET /captcha/image
     */
    @GetMapping("/image")
    public void captchaImage(HttpServletResponse response, HttpSession session) throws IOException {
        response.setContentType("image/jpeg");
        response.setHeader("Cache-Control", "no-cache, no-store, must-revalidate");
        response.setHeader("Pragma", "no-cache");
        response.setDateHeader("Expires", 0);
        CaptchaUtil.generate(session, response.getOutputStream());
    }
}
