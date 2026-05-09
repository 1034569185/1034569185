package listener;

import javax.servlet.ServletContext;
import javax.servlet.ServletContextEvent;
import javax.servlet.ServletContextListener;
import javax.servlet.annotation.WebListener;
import javax.servlet.http.HttpSession;
import javax.servlet.http.HttpSessionAttributeListener;
import javax.servlet.http.HttpSessionBindingEvent;
import javax.servlet.http.HttpSessionEvent;
import javax.servlet.http.HttpSessionListener;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * 在线人数统计监听器
 */
@WebListener
public class MyListener implements ServletContextListener, HttpSessionListener, HttpSessionAttributeListener {

    private static final String COUNTER_KEY = "onlineCounter";
    private static final String COUNT_KEY = "onlineCount";
    private static final String USERNAME_KEY = "username";

    @Override
    public void contextInitialized(ServletContextEvent sce) {
        ServletContext context = sce.getServletContext();
        context.setAttribute(COUNTER_KEY, new AtomicInteger(0));
        context.setAttribute(COUNT_KEY, 0);
    }

    @Override
    public void attributeAdded(HttpSessionBindingEvent event) {
        if (USERNAME_KEY.equals(event.getName())) {
            updateCount(event.getSession().getServletContext(), 1);
        }
    }

    @Override
    public void attributeRemoved(HttpSessionBindingEvent event) {
        if (USERNAME_KEY.equals(event.getName())) {
            updateCount(event.getSession().getServletContext(), -1);
        }
    }

    @Override
    public void attributeReplaced(HttpSessionBindingEvent event) {
        if (USERNAME_KEY.equals(event.getName())) {
            // 保持计数稳定，避免重复加减
            ServletContext context = event.getSession().getServletContext();
            syncCount(context);
        }
    }

    @Override
    public void sessionDestroyed(HttpSessionEvent se) {
        HttpSession session = se.getSession();
        if (session.getAttribute(USERNAME_KEY) != null) {
            updateCount(session.getServletContext(), -1);
        }
    }

    private void updateCount(ServletContext context, int delta) {
        AtomicInteger counter = getCounter(context);
        int value = delta > 0 ? counter.incrementAndGet() : counter.decrementAndGet();
        context.setAttribute(COUNT_KEY, Math.max(value, 0));
    }

    private void syncCount(ServletContext context) {
        AtomicInteger counter = getCounter(context);
        context.setAttribute(COUNT_KEY, Math.max(counter.get(), 0));
    }

    private AtomicInteger getCounter(ServletContext context) {
        Object existing = context.getAttribute(COUNTER_KEY);
        if (existing instanceof AtomicInteger) {
            return (AtomicInteger) existing;
        }
        AtomicInteger counter = new AtomicInteger(0);
        context.setAttribute(COUNTER_KEY, counter);
        context.setAttribute(COUNT_KEY, 0);
        return counter;
    }
}
