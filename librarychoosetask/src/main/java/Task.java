import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import dao.AddCredit;
import dao.AddCreditMapper;
import dao.User;
import dao.UserMapper;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;
import org.springframework.transaction.annotation.Transactional;

import java.io.*;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.Map;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

@Transactional(rollbackFor = Exception.class)
public class Task {
    private static SqlSession sqlSession = null;
    private static UserMapper userMapper = null;
    private static AddCreditMapper addCreditMapper = null;
    public Task() {
        if (Task.sqlSession == null) {
            Reader reader = null;
            try {
                reader = new FileReader(System.getProperty("user.dir") + File.separator + "src" + File.separator + "main" + File.separator + "java" + File.separator + "mybatis-plus.xml");
                SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(reader);
                sqlSession = sqlSessionFactory.openSession();
                userMapper = sqlSession.getMapper(UserMapper.class);
                addCreditMapper = sqlSession.getMapper(AddCreditMapper.class);
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
        task.taskSchedule();
    }

    public boolean isAdd(){
        SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd");
        final String nowDay = simpleDateFormat.format(new Date());
        final boolean[] res = {false};
        List<Date> dates = addCreditMapper.allLog();
        dates.forEach(x->{
            String history = simpleDateFormat.format(x);
            if(nowDay.equals(history)){
                res[0] = true;
                return;
            }
        });
        return res[0];
    }

    public void addEveryDayCredit() {
        AddCredit addCredit = new AddCredit();
        addCredit.setAddtime(new Date());
        int res = addCreditMapper.add(addCredit);
        List<User> userList = userMapper.all();
        userList.forEach(user -> {
            String info = user.getInfo();
            Map<String, Object> infoMap = (Map<String, Object>) JSON.parse(info);
            int credit = (int) infoMap.get("credit");
            credit = credit >= 90 ? 100 : credit + 10;
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

    public void taskSchedule() {
        Runnable runnable = new Runnable() {
            public void run() {
                Task task = new Task();
                if(!task.isAdd()){
                    task.addEveryDayCredit();
                }
                System.out.println("end");
            }
        };
        long delay = 0;  //延迟执行时间（秒）
        long period = 1; //执行的时间间隔（秒）
        ScheduledExecutorService service = Executors.newSingleThreadScheduledExecutor();
        service.scheduleAtFixedRate(runnable, delay, period, TimeUnit.DAYS);
    }
}
