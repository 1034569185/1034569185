<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<div class="admin-breadcrumb">
    <a href="${pageContext.request.contextPath}/admin/login/home?item=product_list">商品管理</a>
    <span> &gt; </span>
    <span>添加商品</span>
</div>

<div class="quick-actions" style="margin-top:12px;">
    <h3 class="qa-title">添加商品</h3>
    <form action="${pageContext.request.contextPath}/admin/products/add-handle" method="post" style="background:#fff;padding:16px;border-radius:6px;">
        <p>
            <label>商品名称：</label><br/>
            <input type="text" name="name" maxlength="40" required style="width: 360px;">
        </p>
        <p>
            <label>价格：</label><br/>
            <input type="number" step="0.01" name="price" required style="width: 360px;">
        </p>
        <p>
            <label>分类：</label><br/>
            <input type="text" name="category" maxlength="40" required style="width: 360px;">
        </p>
        <p>
            <label>库存：</label><br/>
            <input type="number" name="pnum" required style="width: 360px;">
        </p>
        <p>
            <label>图片URL：</label><br/>
            <input type="text" name="imgurl" maxlength="100" style="width: 360px;">
        </p>
        <p>
            <label>描述：</label><br/>
            <textarea name="description" maxlength="255" rows="4" style="width: 360px;"></textarea>
        </p>
        <p>
            <button type="submit">确定</button>
            <a href="${pageContext.request.contextPath}/admin/login/home?item=product_list">返回列表</a>
        </p>
    </form>
</div>
