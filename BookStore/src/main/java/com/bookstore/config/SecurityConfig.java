package com.bookstore.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;

/**
 * Spring Security 配置
 * 当前开放所有接口，后续可在此添加认证/授权规则
 */
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeRequests()
                // 允许访问注册、验证码、静态资源、H2控制台
                .antMatchers("/user/register", "/captcha/**", "/static/**",
                             "/css/**", "/js/**", "/images/**",
                             "/h2-console/**", "/user/checkUsername", "/user/checkEmail")
                .permitAll()
                .anyRequest().authenticated()
            .and()
            .formLogin()
                .loginPage("/user/login")
                .defaultSuccessUrl("/")
                .permitAll()
            .and()
            .logout()
                .permitAll()
            .and()
            .csrf()
                // H2 console 需要关闭 CSRF
                .ignoringAntMatchers("/h2-console/**")
            .and()
            // 允许 H2 console 的 iframe
            .headers().frameOptions().sameOrigin();

        return http.build();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}
