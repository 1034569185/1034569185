<%-- menu_search.jsp – 搜索框 + 商品分类导航片段 --%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<div class="menu-search-bar">
    <!-- 搜索区域 -->
    <form class="search-form" action="${pageContext.request.contextPath}/MenuSearchServlet" method="get">
        <select name="category" class="search-category">
            <option value="">全部分类</option>
            <option value="computer">计算机</option>
            <option value="literature">文学小说</option>
            <option value="history">历史人文</option>
            <option value="science">科学技术</option>
            <option value="art">艺术设计</option>
            <option value="economics">经济管理</option>
            <option value="education">教育考试</option>
            <option value="children">少儿读物</option>
        </select>
        <input type="text" name="keyword" class="search-input" placeholder="搜索书名、作者、ISBN…">
        <button type="submit" class="search-btn">
            <img src="${pageContext.request.contextPath}/static/images/serchbutton.gif"
                 alt="搜索"
                 onerror="this.outerHTML='<span>搜索</span>'">
        </button>
    </form>

    <!-- 分类导航 -->
    <nav class="category-nav">
        <a href="${pageContext.request.contextPath}/" class="cat-link">首页</a>
        <a href="${pageContext.request.contextPath}/ProductList" class="cat-link">全部商品目录</a>
        <a href="${pageContext.request.contextPath}/book/list?category=computer" class="cat-link">计算机</a>
        <a href="${pageContext.request.contextPath}/book/list?category=literature" class="cat-link">文学小说</a>
        <a href="${pageContext.request.contextPath}/book/list?category=history" class="cat-link">历史人文</a>
        <a href="${pageContext.request.contextPath}/book/list?category=science" class="cat-link">科学技术</a>
        <a href="${pageContext.request.contextPath}/book/list?category=art" class="cat-link">艺术设计</a>
        <a href="${pageContext.request.contextPath}/book/list?category=economics" class="cat-link">经济管理</a>
        <a href="${pageContext.request.contextPath}/book/list?category=education" class="cat-link">教育考试</a>
        <a href="${pageContext.request.contextPath}/book/list?category=children" class="cat-link">少儿读物</a>
    </nav>
</div>
