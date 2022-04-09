package dao;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.Date;
import java.util.List;

@Mapper
public interface AddCreditMapper extends BaseMapper<AddCredit> {

    @Select("select add_time from add_user_credit_log")
    public List<Date> allLog();

    @Insert("insert into add_user_credit_log values(#{addtime})")
    public int add(AddCredit addCredit);

}
