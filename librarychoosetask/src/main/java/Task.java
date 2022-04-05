import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import dao.User;
import dao.UserMapper;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;

import java.io.*;
import java.util.List;
import java.util.Map;


public class Task {
    private static SqlSession sqlSession = null;
    private static UserMapper userMapper = null;

    public Task() {
        if (Task.sqlSession == null) {
            Reader reader = null;
            try {
                reader = new FileReader(System.getProperty("user.dir") + File.separator + "src" + File.separator + "main" + File.separator + "java" + File.separator + "mybatis-plus.xml");
                SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(reader);
                sqlSession = sqlSessionFactory.openSession();
                userMapper = sqlSession.getMapper(UserMapper.class);
            } catch (FileNotFoundException e) {
                e.printStackTrace();
            } finally {
                if (reader != null) {
                    try {
                        reader.close();
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
            }
        }
    }

    public static void main(String[] args) {
        Task task = new Task();
        task.addEveryDayCredit();
    }

    public void addEveryDayCredit() {
        List<User> userList = userMapper.all();
        userList.forEach(user -> {
            String info = user.getInfo();
            Map<String, Object> infoMap = (Map<String, Object>) JSON.parse(info);
            int credit = (int) infoMap.get("credit");
            credit = credit >= 50 ? 100 : credit + 50;
            infoMap.put("credit", credit);
            user.setInfo(JSONObject.toJSONString(infoMap));
            System.out.println(user);
            userMapper.updateById(user);
            this.commit();
        });
    }

    protected void commit() {
        try {
            sqlSession.commit();
        } catch (RuntimeException runtimeException) {
            runtimeException.printStackTrace();
            sqlSession.rollback();
        }

    }
}
