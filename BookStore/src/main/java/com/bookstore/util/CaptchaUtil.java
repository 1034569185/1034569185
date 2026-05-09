package com.bookstore.util;

import javax.imageio.ImageIO;
import javax.servlet.http.HttpSession;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.io.OutputStream;
import java.util.Random;

/**
 * 验证码工具类：生成带干扰线的图片验证码
 */
public class CaptchaUtil {

    private static final int WIDTH = 120;
    private static final int HEIGHT = 40;
    private static final int CODE_COUNT = 4;
    private static final String SESSION_KEY      = "captchaCode";
    private static final String SESSION_EXPIRY   = "captchaExpiry";
    /** 验证码有效期：5 分钟 */
    private static final long   EXPIRY_MILLIS    = 5 * 60 * 1000L;

    private static final String CHARS = "ABCDEFGHJKMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789";

    private static final Color[] COLORS = {
        Color.RED, Color.BLUE, Color.BLACK, Color.DARK_GRAY, new Color(0, 128, 0)
    };

    /**
     * 生成验证码图片并将验证码存入Session
     */
    public static void generate(HttpSession session, OutputStream out) throws IOException {
        String code = generateCode();
        session.setAttribute(SESSION_KEY, code.toLowerCase());
        session.setAttribute(SESSION_EXPIRY, System.currentTimeMillis() + EXPIRY_MILLIS);

        BufferedImage image = new BufferedImage(WIDTH, HEIGHT, BufferedImage.TYPE_INT_RGB);
        Graphics2D g = image.createGraphics();

        // 背景
        g.setColor(new Color(248, 248, 255));
        g.fillRect(0, 0, WIDTH, HEIGHT);

        // 干扰线
        Random random = new Random();
        for (int i = 0; i < 5; i++) {
            g.setColor(new Color(200 + random.nextInt(55), 200 + random.nextInt(55), 200 + random.nextInt(55)));
            g.drawLine(random.nextInt(WIDTH), random.nextInt(HEIGHT),
                       random.nextInt(WIDTH), random.nextInt(HEIGHT));
        }

        // 验证码字符
        Font font = new Font("Arial", Font.BOLD, 24);
        g.setFont(font);
        for (int i = 0; i < code.length(); i++) {
            g.setColor(COLORS[random.nextInt(COLORS.length)]);
            // 随机旋转角度，增加识别难度
            int angle = -20 + random.nextInt(40);
            g.rotate(Math.toRadians(angle), 15 + i * 24, 28);
            g.drawString(String.valueOf(code.charAt(i)), 8 + i * 24, 30);
            g.rotate(-Math.toRadians(angle), 15 + i * 24, 28);
        }

        // 噪点
        for (int i = 0; i < 30; i++) {
            g.setColor(new Color(random.nextInt(180), random.nextInt(180), random.nextInt(180)));
            g.fillOval(random.nextInt(WIDTH), random.nextInt(HEIGHT), 2, 2);
        }

        g.dispose();
        ImageIO.write(image, "JPEG", out);
    }

    /**
     * 校验验证码（大小写不敏感，且检查是否已过期）
     */
    public static boolean verify(HttpSession session, String inputCode) {
        if (inputCode == null || inputCode.trim().isEmpty()) {
            return false;
        }
        Object sessionCode = session.getAttribute(SESSION_KEY);
        if (sessionCode == null) {
            return false;
        }
        // 检查是否过期
        Object expiry = session.getAttribute(SESSION_EXPIRY);
        if (expiry instanceof Long && System.currentTimeMillis() > (Long) expiry) {
            invalidate(session);
            return false;
        }
        return sessionCode.toString().equalsIgnoreCase(inputCode.trim());
    }

    /**
     * 使验证码失效（防止重复使用）
     */
    public static void invalidate(HttpSession session) {
        session.removeAttribute(SESSION_KEY);
        session.removeAttribute(SESSION_EXPIRY);
    }

    private static String generateCode() {
        Random random = new Random();
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < CODE_COUNT; i++) {
            sb.append(CHARS.charAt(random.nextInt(CHARS.length())));
        }
        return sb.toString();
    }
}
