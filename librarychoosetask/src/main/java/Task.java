import com.baomidou.mybatisplus.extension.conditions.query.QueryChainWrapper;
import dao.User;
import dao.UserMapper;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;
import org.mybatis.spring.annotation.MapperScan;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.Reader;
import java.util.Arrays;
import java.util.List;


public class Task {
    public static void main(String[] args) throws FileNotFoundException {
        //通过配置文件获取数据库连接信息
        Reader reader = new FileReader(System.getProperty("user.dir") + File.separator + "src" + File.separator + "main" + File.separator + "java" + File.separator + "mybatis-plus.xml");
//通过配置信息构建SqlSessionFactory
        SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(reader);
//通过sqlSessionFactory打开数据库会话
        SqlSession sqlSession = sqlSessionFactory.openSession();
//        Connection connection = sqlSession.getConnection();
//        System.out.println(connection);
        UserMapper mapper = sqlSession.getMapper(UserMapper.class);
        List<User> list = mapper.all();
        System.out.println(list);
    }
}
