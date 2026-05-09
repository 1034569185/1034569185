package servlet;

import domain.Product;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.List;

@WebServlet(name = "MenuSearchServlet", urlPatterns = "/MenuSearchServlet")
public class MenuSearchServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        request.setCharacterEncoding("UTF-8");
        String keyword = request.getParameter("keyword");
        String category = request.getParameter("category");

        Product productBean = new Product();
        List<Product> products = productBean.searchByKeyword(keyword, category);
        request.setAttribute("products", products);
        request.setAttribute("keyword", keyword);
        request.setAttribute("category", category);

        RequestDispatcher dispatcher = request.getRequestDispatcher("/WEB-INF/views/ProductList.jsp");
        dispatcher.forward(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        doGet(request, response);
    }
}
