package com.bookstore.controller;

import com.bookstore.model.RegisterForm;
import com.bookstore.model.User;
import com.bookstore.service.UserService;
import com.bookstore.util.CaptchaUtil;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import javax.servlet.http.HttpSession;
import java.time.LocalDate;
import java.time.format.DateTimeParseException;
import java.util.HashMap;
import java.util.Map;

/**
 * 用户注册控制器
 */
@Controller
@RequestMapping("/user")
public class UserController {

    private static final Logger logger = LoggerFactory.getLogger(UserController.class);

    @Autowired
    private UserService userService;

    /**
     * 显示注册页面
     */
    @GetMapping("/register")
    public String registerPage(Model model) {
        model.addAttribute("form", new RegisterForm());
        return "register";
    }

    /**
     * 处理注册表单提交
     */
    @PostMapping("/register")
    public String register(RegisterForm form, Model model, HttpSession session) {
        // 1. 验证码校验
        if (!CaptchaUtil.verify(session, form.getCaptcha())) {
            model.addAttribute("error", "验证码错误，请重新输入");
            model.addAttribute("form", form);
            return "register";
        }
        CaptchaUtil.invalidate(session); // 使验证码失效，防止重复使用

        // 2. 密码一致性校验
        if (!form.getPassword().equals(form.getConfirmPassword())) {
            model.addAttribute("error", "两次输入的密码不一致");
            model.addAttribute("form", form);
            return "register";
        }

        // 3. 用户名唯一性校验
        if (userService.isUsernameExists(form.getUsername())) {
            model.addAttribute("error", "用户名 [" + form.getUsername() + "] 已被注册，请换一个");
            model.addAttribute("form", form);
            return "register";
        }

        // 4. 邮箱唯一性校验
        if (userService.isEmailExists(form.getEmail())) {
            model.addAttribute("error", "邮箱 [" + form.getEmail() + "] 已被注册，请换一个");
            model.addAttribute("form", form);
            return "register";
        }

        // 5. 构建用户对象并保存
        try {
            User user = new User();
            user.setUsername(form.getUsername().trim());
            user.setPassword(form.getPassword());
            user.setEmail(form.getEmail().trim());
            String phone = form.getPhone();
            user.setPhone(phone != null && !phone.trim().isEmpty() ? phone.trim() : null);
            user.setGender(form.getGender());

            if (form.getBirthday() != null && !form.getBirthday().isEmpty()) {
                try {
                    user.setBirthday(LocalDate.parse(form.getBirthday()));
                } catch (DateTimeParseException e) {
                    logger.warn("Invalid birthday format: {}", form.getBirthday());
                }
            }

            userService.register(user);
            logger.info("New user registered: {}", user.getUsername());
            model.addAttribute("success", "注册成功！欢迎加入 BookStore，" + user.getUsername() + "！");
            return "register";
        } catch (Exception e) {
            logger.error("Registration failed", e);
            model.addAttribute("error", "注册失败，请稍后重试。");
            model.addAttribute("form", form);
            return "register";
        }
    }

    /**
     * AJAX：检查用户名是否已存在
     */
    @GetMapping("/checkUsername")
    @ResponseBody
    public Map<String, Object> checkUsername(String username) {
        Map<String, Object> result = new HashMap<>();
        if (username == null || username.trim().isEmpty()) {
            result.put("available", false);
            result.put("message", "用户名不能为空");
        } else if (userService.isUsernameExists(username.trim())) {
            result.put("available", false);
            result.put("message", "用户名已被使用");
        } else {
            result.put("available", true);
            result.put("message", "用户名可用");
        }
        return result;
    }

    /**
     * AJAX：检查邮箱是否已存在
     */
    @GetMapping("/checkEmail")
    @ResponseBody
    public Map<String, Object> checkEmail(String email) {
        Map<String, Object> result = new HashMap<>();
        if (email == null || email.trim().isEmpty()) {
            result.put("available", false);
            result.put("message", "邮箱不能为空");
        } else if (userService.isEmailExists(email.trim())) {
            result.put("available", false);
            result.put("message", "邮箱已被使用");
        } else {
            result.put("available", true);
            result.put("message", "邮箱可用");
        }
        return result;
    }

    /**
     * 首页跳转到注册页
     */
    @GetMapping("/")
    public String index() {
        return "redirect:/user/register";
    }
}
