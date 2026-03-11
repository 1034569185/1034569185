package com.bookstore;

import com.bookstore.model.RegisterForm;
import com.bookstore.service.UserService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;
import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
@AutoConfigureMockMvc
class BookStoreApplicationTests {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private UserService userService;

    @Test
    void contextLoads() {
        // Spring 上下文能够正常加载
    }

    @Test
    void registerPageLoads() throws Exception {
        mockMvc.perform(get("/user/register"))
               .andExpect(status().isOk())
               .andExpect(view().name("register"));
    }

    @Test
    void captchaImageEndpointWorks() throws Exception {
        mockMvc.perform(get("/captcha/image"))
               .andExpect(status().isOk())
               .andExpect(content().contentTypeCompatibleWith("image/jpeg"));
    }

    @Test
    void checkUsernameAvailable() throws Exception {
        mockMvc.perform(get("/user/checkUsername").param("username", "nonexistentuser999"))
               .andExpect(status().isOk())
               .andExpect(jsonPath("$.available").value(true));
    }

    @Test
    void checkEmailAvailable() throws Exception {
        mockMvc.perform(get("/user/checkEmail").param("email", "nonexistent@example.com"))
               .andExpect(status().isOk())
               .andExpect(jsonPath("$.available").value(true));
    }

    @Test
    void userServiceRegistersUserSuccessfully() {
        com.bookstore.model.User user = new com.bookstore.model.User();
        user.setUsername("testuser01");
        user.setPassword("Test123456");
        user.setEmail("testuser01@example.com");

        com.bookstore.model.User saved = userService.register(user);
        assertNotNull(saved.getId());
        assertTrue(userService.isUsernameExists("testuser01"));
        assertTrue(userService.isEmailExists("testuser01@example.com"));
    }

    @Test
    void userServiceDetectsDuplicateUsername() {
        com.bookstore.model.User user = new com.bookstore.model.User();
        user.setUsername("dupuser01");
        user.setPassword("Password1");
        user.setEmail("dupuser01@example.com");
        userService.register(user);

        assertTrue(userService.isUsernameExists("dupuser01"));
        assertFalse(userService.isUsernameExists("dupuser02"));
    }
}
