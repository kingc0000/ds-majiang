package majiang.client.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

/**
 * 账号管理 Controller
 * @author SenseNova
 */
@RestController
@RequestMapping("/")
public class AccountController {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    /**
     * 测试接口
     * GET /account/test
     */
    @GetMapping("/account/test")
    public Map<String, Object> test() {
        Map<String, Object> result = new HashMap<>();
        result.put("status", 0);
        result.put("msg", "Manager 服务正常");
        return result;
    }

    /**
     * 登录接口
     * GET /account/login?name=xxx&password=***
     */
    @GetMapping("/account/login")
    public Map<String, Object> login(@RequestParam String name, @RequestParam String password) {
        Map<String, Object> result = new HashMap<>();
        
        try {
            // 查询用户（通过 name 字段）
            String sql = "SELECT * FROM user WHERE name = ?";
            Object[] user = jdbcTemplate.queryForObject(sql, new Object[]{name}, 
                (rs, rowNum) -> new Object[]{
                    rs.getInt("id"),
                    rs.getString("name"),
                    rs.getString("password"),
                    rs.getInt("gold"),
                    rs.getInt("level")
                });
            
            if (user == null) {
                result.put("status", 1);
                result.put("msg", "用户不存在");
                return result;
            }
            
            // 验证密码
            if (!password.equals(user[2])) {
                result.put("status", 1);
                result.put("msg", "密码错误");
                return result;
            }
            
            // 登录成功
            result.put("status", 0);
            result.put("msg", "登录成功");
            result.put("userId", user[0]);
            result.put("userName", user[1]);
            result.put("gold", user[3]);
            result.put("level", user[4]);
            
        } catch (Exception e) {
            result.put("status", 2);
            result.put("msg", "服务器错误: " + e.getMessage());
        }
        
        return result;
    }
}
