package domain;

import com.bookstore.util.JdbcUtil;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.ArrayList;
import java.util.List;

/**
 * 商品 JavaBean（实验十一）
 */
public class Product {
    private Integer id;
    private String name;
    private Double price;
    private String category;
    private Integer pnum;
    private String imgurl;
    private String description;

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Double getPrice() {
        return price;
    }

    public void setPrice(Double price) {
        this.price = price;
    }

    public String getCategory() {
        return category;
    }

    public void setCategory(String category) {
        this.category = category;
    }

    public Integer getPnum() {
        return pnum;
    }

    public void setPnum(Integer pnum) {
        this.pnum = pnum;
    }

    public String getImgurl() {
        return imgurl;
    }

    public void setImgurl(String imgurl) {
        this.imgurl = imgurl;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    /**
     * 查询全部商品
     */
    public List<Product> searchAll() {
        List<Product> ps = new ArrayList<>();
        String sql = "SELECT id, name, price, category, pnum, imgurl, description FROM products ORDER BY id DESC";
        try (Connection conn = JdbcUtil.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {
            while (rs.next()) {
                Product p = new Product();
                p.setId(rs.getInt("id"));
                p.setName(rs.getString("name"));
                p.setPrice(rs.getDouble("price"));
                p.setCategory(rs.getString("category"));
                p.setPnum(rs.getInt("pnum"));
                p.setImgurl(rs.getString("imgurl"));
                p.setDescription(rs.getString("description"));
                ps.add(p);
            }
        } catch (Exception e) {
            System.err.println("[domain.Product#searchAll] query products failed: " + e.getMessage());
            e.printStackTrace();
        }
        return ps;
    }

    /**
     * 添加商品
     */
    public boolean add(Product product) {
        String sql = "INSERT INTO products(name, price, category, pnum, imgurl, description) VALUES (?, ?, ?, ?, ?, ?)";
        try (Connection conn = JdbcUtil.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, product.getName());
            if (product.getPrice() == null) {
                stmt.setNull(2, java.sql.Types.DOUBLE);
            } else {
                stmt.setDouble(2, product.getPrice());
            }
            stmt.setString(3, product.getCategory());
            if (product.getPnum() == null) {
                stmt.setNull(4, java.sql.Types.INTEGER);
            } else {
                stmt.setInt(4, product.getPnum());
            }
            stmt.setString(5, product.getImgurl());
            stmt.setString(6, product.getDescription());
            return stmt.executeUpdate() > 0;
        } catch (Exception e) {
            System.err.println("[domain.Product#add] add product failed: name=" + product.getName() + ", error=" + e.getMessage());
            e.printStackTrace();
            return false;
        }
    }
}
